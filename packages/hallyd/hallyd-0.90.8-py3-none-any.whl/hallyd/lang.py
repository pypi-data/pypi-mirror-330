#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
Various low-level features.
"""
import abc
import datetime
import functools
import json
import math
import os
import re
import string
import threading
import time
import typing as t
import weakref
import xml.etree.ElementTree

import hallyd.bindle as _bindle
import hallyd.fs as _fs
import hallyd.subprocess as _subprocess


_T = t.TypeVar("_T", bound=object)


def call_now_with_retry(*, tries: int = 8, interval: float = 30, interval_fact: float = 1,
                        retry_on: t.Optional[t.Iterable[type[Exception]]] = None) -> t.Callable:  # TODO use
    def decorator(fct, *args, **kwargs):
        return with_retry(tries=tries, interval=interval, interval_fact=interval_fact,
                          retry_on=retry_on)(fct)(*args, **kwargs)
    return decorator


def with_retry(*, tries: int = 8, interval: float = 30, interval_fact: float = 1,
               retry_on: t.Optional[t.Iterable[type[Exception]]] = None) -> t.Callable:
    if retry_on is None:
        retry_on = [Exception]
    def decorator(fct):
        @functools.wraps(fct)
        def func(*a, **b):
            nwi = interval
            for itr in reversed(range(tries)):
                try:
                    return fct(*a, **b)
                except Exception as e:
                    if (itr > 0) and any((issubclass(type(e), x) for x in retry_on)):
                    #    import krrezzeedtest.log
                     #   krrezzeedtest.log.debug(traceback.format_exc(), tag="grayerror")
                        time.sleep(nwi)
                        nwi *= interval_fact
                    else:
                        raise
        return func
    return decorator


def with_friendly_repr_implementation(*, skip: t.Iterable[str] = ()):
    #  TODO test (for all classes that use it);   more reliable (cycles?!)
    return functools.partial(_with_friendly_repr_implementation__decorator, tuple(skip))


def _with_friendly_repr_implementation__decorator(skip_, cls_):
    def friendly_repr(self):
        objdict = json.loads(_bindle.dumps(self))
        module_name, type_name = objdict.pop(_bindle._TYPE_KEY)
        objdict = _bindle._filter_unneeded_dict_entries(type(self), objdict)
        objdict = {key: value for key, value in objdict.items() if key not in skip_}
        params_pieces = []
        for key, value in objdict.items():
            params_pieces.append(f"{key}={repr(value)}")
        full_type_name = (f"{module_name}." if module_name else "") + type_name
        return f"{full_type_name}({', '.join(params_pieces)})"

    cls_.__repr__ = friendly_repr
    return cls_


class Counter:

    def __init__(self):
        self.__current = 0
        self.__lock = threading.Lock()

    def next(self):
        with self.__lock:
            self.__current += 1
            return self.__current


_unique_id_counter = Counter()

_unique_id_sources = [(time.time_ns, datetime.datetime(9999, 1, 1, 0, 0, 0).timestamp() * 1000**3),
                      (_unique_id_counter.next, 99999),
                      (threading.get_native_id, 2**32-1),
                      (functools.partial(os.getpgid, 0), 2**32-1)]


def unique_id(*, numeric_only: bool = False) -> str:
    alphabet = string.digits if numeric_only else f"{string.digits}{string.ascii_uppercase}{string.ascii_lowercase}"
    alphabet_len = len(alphabet)
    result = ""
    for source, range_max in _unique_id_sources:
        number = source()
        result_piece = ""
        while number > 0:
            result_piece = alphabet[number % alphabet_len] + result_piece
            number = number // alphabet_len
        length = math.floor(math.log(range_max, alphabet_len)) + 1
        result += result_piece[-length:].rjust(length, alphabet[0])
    return result


def execute_in_parallel(funcs: list[t.Callable[[], None]]) -> None:
    threads = [_ExecuteParallelThread(func) for func in funcs]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    errors = [thread.error for thread in threads if thread.error]
    if errors:
        errors_text = ", ".join([str(e) for e in errors])
        raise Exception(f"TODO Error(s) in parallel execution: {errors_text}")


class _ExecuteParallelThread(threading.Thread):

    def __init__(self, fct: t.Callable[[], None]):
        super().__init__(daemon=True)
        self.__fct = fct
        self.error = None

    def run(self):
#            with self.__logsection:
        try:
            self.__fct()
        except Exception as e:
            self.error = e


class _AllAbstractMethodsProvidedByTrickMeta(abc.ABCMeta, t.Generic[_T]):

    def __new__(mcs, name, bases, namespace):
        x = type.__new__(mcs, name, bases, namespace)
        for foo in [xx for xx in dir(_T) if not xx.startswith("_")]:
            setattr(x, foo, None)
        return x


class AllAbstractMethodsProvidedByTrick(t.Generic[_T], metaclass=_AllAbstractMethodsProvidedByTrickMeta[_T]):
    pass


_locks = {}
_locks_lock = threading.Lock()


def lock(lock_path: "_fs.TInputPath", *, is_reentrant: bool = True, peek_interval: float = 0.25) -> "Lock":
    def weakcheck(p):
        with _locks_lock:
            x = _locks.get(p)
            if x and not x():
                _locks.pop(p)
    lock_path = _fs.Path(lock_path).resolve()
    with _locks_lock:
        result_weakref = _locks.get(str(lock_path))
        result = result_weakref() if result_weakref else None
        if not result:
            result = lock = _Lock(lock_path, is_reentrant, peek_interval)
            _locks[str(lock_path)] = weakref.ref(lock)
            weakref.finalize(lock, lambda: weakcheck(str(lock_path)))
        return result


class Lock(abc.ABC):

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    @abc.abstractmethod
    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
        pass

    @abc.abstractmethod
    def release(self) -> None:
        pass

    @abc.abstractmethod
    def locked(self) -> bool:
        pass


class _Lock(Lock):

    def __init__(self, lock_path: "_fs.Path", is_reentrant: bool, peek_interval: float):
        self.__lock_path = lock_path
        self.__locked_count = 0
        self.__locked_by_thread = None
        self.__is_reentrant = is_reentrant
        self.__peek_interval = peek_interval

    def acquire(self, blocking=True, timeout=-1):
        if not (self.__is_reentrant and self.__locked_by_thread == threading.get_native_id()):
            timeout_at = None if (timeout < 0) else (time.monotonic() + timeout)
            next_lock_alive_check_at = 0
            while True:
                try:
                    self.__lock_path.make_file(exist_ok=False, readable_by_all=True)
                    self.__lock_path.write_text(json.dumps(_subprocess.process_permanent_id_for_pid(os.getpid())))
                    break
                except FileExistsError:
                    if next_lock_alive_check_at <= time.monotonic():
                        next_lock_alive_check_at = time.monotonic() + 10
                        try:
                            lock_process_permanent_id = json.loads(self.__lock_path.read_text())
                        except (FileNotFoundError, json.JSONDecodeError):
                            continue
                        if _subprocess.is_process_running(lock_process_permanent_id) is False:
                            self.__lock_path.unlink(missing_ok=True)
                            continue
                    if (not blocking) or (timeout_at and (timeout_at < time.monotonic())):
                        return False
                    time.sleep(self.__peek_interval)
        self.__locked_count += 1
        self.__locked_by_thread = threading.get_native_id()
        return True

    def release(self):
        if not self.locked():
            raise RuntimeError("release an unlocked Lock is forbidden")
        self.__locked_count -= 1
        if self.__locked_count == 0:
            self.__lock_path.unlink()
            self.__locked_count = False
            self.__locked_by_thread = None

    def locked(self):
        return self.__locked_count > 0


def match_format_string(pattern: str, string: str) -> dict[str, str]:
    def unescape_double_braces(s):
        return s.replace("{{", "{").replace("}}", "}")

    pattern_re = ""
    i = 0
    for expression_match in re.finditer(r"(?:[^{]|^)\{([^{}]+)\}(?:[^}]|$)", pattern):
        pattern_re += re.escape(unescape_double_braces(pattern[i:expression_match.start(1) - 1]))
        pattern_re += f"(?P<{expression_match.group(1)}>.*)"
        i = expression_match.end(1) + 1
    pattern_re += re.escape(unescape_double_braces(pattern[i:])) + "$"
    result_match = re.match(pattern_re, string)
    return result_match.groupdict() if result_match else None


def pretty_print_xml(input_xml: str) -> str:  # TODO broken
    xtree = xml.etree.ElementTree.fromstring(input_xml)
    ytree = xml.etree.ElementTree.ElementTree(xtree)
    xml.etree.ElementTree.indent(ytree, space=4*" ")
    result = ""
    for line in xml.etree.ElementTree.tostring(xtree, encoding="unicode").split("\n"):
        if line.strip():
            result += line + "\n"
    return result
