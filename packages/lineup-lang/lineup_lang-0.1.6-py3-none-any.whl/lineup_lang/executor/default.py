from ..language_object import LanguageExecutorInterface, \
    CoreObjectInterface
from ..error import ExecutorFunctionAlreadyExistError, \
    ExecutorFunctionNotExistError
from typing import Any, List
import logging


class DefaultExecutor(LanguageExecutorInterface):
    stop = False
    logger = None
    # Executor version - it's set on the lineup version
    _version = None

    def __init__(self, core_object: List[CoreObjectInterface]):
        self.logger = logging.getLogger("lineup_lang")
        self._core_function = {}
        self._core = []
        for core in core_object:
            self._core.append(core)
            core.set_executor(self)
            for function_name in core.get_all_functions():
                if function_name in self._core_function:
                    fn = function_name
                    c1 = core
                    c2 = self._core_function[function_name]
                    raise ExecutorFunctionAlreadyExistError(
                        f"'{fn}' from '{c1}' in '{c2}'")
                self._core_function[function_name] = core

    def reset(self) -> None:
        self.stop = False
        super().reset()

    def execute_line(self, line: List[str]):
        if line[0] not in self._core_function:
            msg = f"'{line[0]}' not exist in '{self}'"
            self.logger.error(msg)
            raise ExecutorFunctionNotExistError(msg)
        self.logger.debug(f"Execute: {line}")
        return self._core_function[line[0]].execute(line[0], *line[1:])

    def execute(self, script: List[List[str]]) -> Any:
        self.stop = False
        result = None
        for line in script:
            result = self.execute_line(line)
            if self.stop:
                break
        return result
