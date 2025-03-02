from typing import Type, TypeVar, Generic
from types import TracebackType, FunctionType
import inspect


T = TypeVar('T')
class NamespaceGroup(Generic[T]):
    def __init__(self) -> None:
        self.members: dict[str, Type[T]] = {}
        
    def __enter__(self):
        # Get the caller's frame and store its current local and global names
        caller_frame = inspect.stack()[1].frame
        self._entry_locals = dict(caller_frame.f_locals)
        return self

    def _add(self, elem: T, alias: str | None = None) -> None:
        if alias is None:
            alias: str = elem.__name__

        if isinstance(elem, FunctionType): # is a function
            self.members[alias] = FunctionType(elem.__code__, globals())

        else: # is a class
            method_dict = {name: method for name, method in elem.__dict__.items() if callable(method)}
            self.members[alias] = type(alias, (object,), method_dict)

        # add as attribute
        setattr(self, alias, self.members[alias])

    def __exit__(self,
                 exec_type: Type[BaseException] | None,
                 exec_value: BaseException | None,
                 traceback: TracebackType | None) -> bool | None:
        # Get the caller's frame and store its current local and global names
        caller_frame = inspect.stack()[1].frame
        self._exit_locals = dict(caller_frame.f_locals)

        # geta dded locals to the namespace
        self._new_locals = {k: self._exit_locals[k] for k in self._exit_locals.keys() - self._entry_locals.keys()}
        for key, val in self._new_locals.items():
            self._add(val, key)

        if exec_type is not None:
            print(f'Exception: {exec_type} with value {exec_value}\ntraceback: {traceback}')

if __name__ == '__main__':
    pass
