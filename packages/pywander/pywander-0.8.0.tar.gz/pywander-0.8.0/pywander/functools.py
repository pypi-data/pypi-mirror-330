#!/usr/bin/env python
# -*-coding:utf-8-*-

from functools import reduce
from functools import wraps



def build_compose_function(*funcs):
    """
    combine a sequence functions to a compose function
    """
    return reduce(lambda f, g: lambda *args, **kwargs: g(f(*args, **kwargs)), funcs)


def build_stream_function(*funcs):
    """
    combine a sequence funtion to a compose function, and for the sake of simplicity, 
    limited the input parameter to a dict object.
    """

    return reduce(lambda f, g: lambda d: g(f(d)), funcs)


def flatten(inlst):
    """
    make multiple layer list or tuple to one dimension list

        >>> flatten((1,2,(3,4),((5,6))))
        [1, 2, 3, 4, 5, 6]
        >>> flatten([[1,2,3],[[4,5],[6]]])
        [1, 2, 3, 4, 5, 6]

    """
    lst = []
    for x in inlst:
        if not isinstance(x, (list, tuple)):
            lst.append(x)
        else:
            lst += flatten(x)
    return lst


def sumall(*args):
    """sum all numbers, support multiple layer structure.
    
    >>> sumall(1,1,2,3,[1,2,3])
    13
    >>> sumall(1,1,2,3,[1,2,3],(4,5,6),[[5,5],[6]])
    44
    >>>
    """
    args = flatten(args)
    return sum(args)


def _lazy_proxy_unpickle(func, args, kwargs, *resultclasses):
    return lazy(func, *resultclasses)(*args, **kwargs)


class Promise:
    """
    Base class for the proxy class created in the closure of the lazy function.
    It's used to recognize promises in code.
    """

    pass


def lazy(func, *resultclasses):
    """
    Turn any callable into a lazy evaluated callable. result classes or types
    is required -- at least one is needed so that the automatic forcing of
    the lazy evaluation code is triggered. Results are not memoized; the
    function is evaluated on every access.
    """

    class __proxy__(Promise):
        """
        Encapsulate a function call and act as a proxy for methods that are
        called on the result of that function. The function is not evaluated
        until one of the methods on the result is called.
        """

        def __init__(self, args, kw):
            self._args = args
            self._kw = kw

        def __reduce__(self):
            return (
                _lazy_proxy_unpickle,
                (func, self._args, self._kw) + resultclasses,
            )

        def __deepcopy__(self, memo):
            # Instances of this class are effectively immutable. It's just a
            # collection of functions. So we don't need to do anything
            # complicated for copying.
            memo[id(self)] = self
            return self

        def __cast(self):
            return func(*self._args, **self._kw)

        # Explicitly wrap methods which are defined on object and hence would
        # not have been overloaded by the loop over resultclasses below.

        def __repr__(self):
            return repr(self.__cast())

        def __str__(self):
            return str(self.__cast())

        def __eq__(self, other):
            if isinstance(other, Promise):
                other = other.__cast()
            return self.__cast() == other

        def __ne__(self, other):
            if isinstance(other, Promise):
                other = other.__cast()
            return self.__cast() != other

        def __lt__(self, other):
            if isinstance(other, Promise):
                other = other.__cast()
            return self.__cast() < other

        def __le__(self, other):
            if isinstance(other, Promise):
                other = other.__cast()
            return self.__cast() <= other

        def __gt__(self, other):
            if isinstance(other, Promise):
                other = other.__cast()
            return self.__cast() > other

        def __ge__(self, other):
            if isinstance(other, Promise):
                other = other.__cast()
            return self.__cast() >= other

        def __hash__(self):
            return hash(self.__cast())

        def __format__(self, format_spec):
            return format(self.__cast(), format_spec)

        # Explicitly wrap methods which are required for certain operations on
        # int/str objects to function correctly.

        def __add__(self, other):
            return self.__cast() + other

        def __radd__(self, other):
            return other + self.__cast()

        def __mod__(self, other):
            return self.__cast() % other

        def __mul__(self, other):
            return self.__cast() * other

    # Add wrappers for all methods from resultclasses which haven't been
    # wrapped explicitly above.
    for resultclass in resultclasses:
        for type_ in resultclass.mro():
            for method_name in type_.__dict__:
                # All __promise__ return the same wrapper method, they look up
                # the correct implementation when called.
                if hasattr(__proxy__, method_name):
                    continue

                # Builds a wrapper around some method. Pass method_name to
                # avoid issues due to late binding.
                def __wrapper__(self, *args, __method_name=method_name, **kw):
                    # Automatically triggers the evaluation of a lazy value and
                    # applies the given method of the result type.
                    result = func(*self._args, **self._kw)
                    return getattr(result, __method_name)(*args, **kw)

                setattr(__proxy__, method_name, __wrapper__)

    @wraps(func)
    def __wrapper__(*args, **kw):
        # Creates the proxy object, instead of the actual value.
        return __proxy__(args, kw)

    return __wrapper__
