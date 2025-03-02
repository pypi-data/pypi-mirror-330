import inspect
from functools import wraps
import os
from types import UnionType
from kisa_utils.response import Response, Ok, Error
from kisa_utils.storage import Path

def private(func):
    '''
    function is used only in the same module as that in which its defined
    * if multiple decorators are used, this has to be the closest to the function being decorated
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        expectedModule = inspect.getfile(func)
        stack = inspect.stack()
        stackCallerModules = [(s.function,s.filename) for s in stack if ('<frozen' not in s.filename)]

        callingModule = stackCallerModules[1][1]
        # print(Path.getMyAbsolutePath())
        # from pprint import pprint; pprint(stackCallerModules)
        # print(expectedModule, callingModule, expectedModule == callingModule)
        if expectedModule != callingModule:
            raise Exception(f"can't call private function `{func.__name__}` from external module")

        return func(*args, **kwargs)
    return wrapper

def protected(func):
    '''
    function is only allowed to be used in;
    * the module in which its defined
    * submodules starting in the defining module's path

    NB:
    * if multiple decorators are used, this has to be the closest to the function being decorated
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        expectedModule = inspect.getfile(func)
        stack = inspect.stack()
        stackCallerModules = [(s.function,s.filename) for s in stack if ('<frozen' not in s.filename)]

        callingModule = stackCallerModules[1][1]
        # print(expectedModule, callingModule)
        if not callingModule.startswith(os.path.dirname(expectedModule)):
            raise Exception(f"can't call protected function `{func.__name__}` from path outside definition module path")

        return func(*args, **kwargs)
    return wrapper

def returnsKISAResponse(func):
    '''
    this decorator should be applied above `private` and/or `protected`
    '''
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response:
        if not isinstance(value := func(*args, **kwargs), Response):
            raise Exception(f'function `{func.__name__}` returned a non-KISA response')

        return value

    return wrapper

def returns(returnType):
    '''
    this decorator should be applied above `private` and/or `protected`
    '''
    if isinstance(returnType, UnionType):
        raise Exception(f'decorator `returns` does not accept union types as an argument')
    if type(returnType) != type(int):
        raise Exception(f'decorator `returns` only accepts a Type as an argument')
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not isinstance(value:=func(*args, **kwargs), returnType):
                raise Exception(f'function `{func.__name__}` expected to return `{returnType}`, got `{type(value)}` instead')
            return value
        return wrapper
    return decorator

def enforceReturnType(func):
    '''
    * this decorator should be applied above `private` and/or `protected`
    '''
    returnType = func.__annotations__.get('return',None)

    if returnType == None:
        raise Exception(f'`{func.__name__}` has no return type indicated')

    if isinstance(returnType, UnionType):
        raise Exception(f'decorator `returns` does not accept union types as an argument')

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not isinstance(value:=func(*args, **kwargs), returnType):
            raise Exception(f'function `{func.__name__}` expected to return `{returnType}`, got `{type(value)}` instead')
        return value
    return wrapper
