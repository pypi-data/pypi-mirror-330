from __future__ import annotations
from typing import Dict, Any, Callable, List
from .error import FunctionNotExistError, AlreadyClosedError
import logging


class LineupObjectInterface:
    """
    LineUp Object, who can be used by the language
    Can be close or reset
    """

    _is_closed = False
    """
    If the object is closed
    If it's closed, the object can't be used anymore
    """

    def close(self):
        """
        Destroy the object
        """
        self._is_closed = True

    def reset(self):
        """
        Reset the object for future new exectution
        """
        if self._is_closed:
            raise AlreadyClosedError(f"{self} is already closed")


class LanguageObjectInterface(LineupObjectInterface):
    """
    LineUp Object with functions who can be executed by the language
    """

    functions: Dict[str, Callable[..., Any]]
    """
    All functions the script can execute
    """

    logger = logging.getLogger("lineup_lang")

    def get_all_functions(self) -> List[str]:
        """
        Get all functions name in the object
        """
        if self._is_closed:
            raise AlreadyClosedError(f"{self} is already closed")
        return list(self.functions.keys())

    def execute(self, function_name: str, *args) -> Any:
        """
        Execute a function in the object
        """
        if self._is_closed:
            raise AlreadyClosedError(f"{self} is already closed")
        if function_name not in self.functions:
            msg = f"'{function_name}' not exist in '{self}'"
            self.logger.error(msg)
            raise FunctionNotExistError(msg)
        return self.functions[function_name](*args)

    def __str__(self) -> str:
        return f"<LUPO:{self.__class__.__name__}>"


class CoreObjectInterface(LanguageObjectInterface):
    """
    Object instancied before the creation of the language executor

    Function in this object is directly accessible by the language executor

    A core object is used for create the main function of the language executor
    """
    executor: Any
    version: str = "0.0.0"

    def set_executor(self, executor: LanguageExecutorInterface) -> None:
        if self._is_closed:
            raise AlreadyClosedError(f"{self} is already closed")
        self.executor = executor

    def get_version(self) -> str:
        return self.version

    def __str__(self) -> str:
        return f"<LUPC:{self.__class__.__name__}>"


class LanguageExecutorInterface(LineupObjectInterface):
    """
    Language executor interface

    This object is the main object who execute the script
    It execute line each by each
    """
    _core_function: Dict[str, LanguageObjectInterface]
    _core: List[LanguageObjectInterface]
    _version: str = "0.0.0"
    stopped: bool = False

    def execute_line(self, line: List[str]):
        """
        Execute one line of the script
        """
        if self._is_closed:
            raise AlreadyClosedError(f"{self} is already closed")

    def execute(self, script: List[List[str]]) -> Any:
        """
        Execute a list of line
        """
        if self._is_closed:
            raise AlreadyClosedError(f"{self} is already closed")

    def get_versions(self) -> Dict[str, str]:
        """
        Get all the versions who defined the language
        (executor and core object)
        """
        if self._is_closed:
            raise AlreadyClosedError(f"{self} is already closed")
        versions = {self.__str__(): self._version}
        for core in self._core:
            versions[core.__str__()] = core.get_version()
        return versions

    def close(self) -> None:
        """
        Close the executor

        This function is called when the executor is not used anymore
        """
        if self._is_closed:
            return
        super().close()
        for core in self._core:
            logging.getLogger("lineup_lang").info(f"Close: {core}")
            core.close()

    def reset(self) -> None:
        """
        Reset the executor for future new exectution

        This function is called when after a script execution
        """
        if self._is_closed:
            raise AlreadyClosedError(f"{self} is already closed")
        for core in self._core:
            logging.getLogger("lineup_lang").info(f"Reset: {core}")
            core.reset()

    def __str__(self) -> str:
        return f"<LUPE:{self.__class__.__name__}>"


class LanguageInterface(LineupObjectInterface):
    """"
    Language interface
    It read the script, cut it in line and
    send it to the executor for execute it
    """

    def get_all_functions(self) -> List[str]:
        """
        Get all functions name in the language
        """
        pass

    def get_versions(self) -> str:
        """
        Get all the versions who defined the language

        (executor, core object and lineup version)
        """
        pass

    def execute_script(self, script: str) -> Any:
        """
        Execute a script
        """
        pass

    def execute_script_with_args(self, script: str, **kwargs) -> Any:
        """
        Execute a script with arguments

        Arguments in the script is write like this:
        $LUP_ARG_NAME (in the script) -> kwargs["LUP_ARG_NAME"] (in the function)
        ${LUP_ARG_NAME} (in the script) -> kwargs["LUP_ARG_NAME"] (in the function)
        """
        pass

    def execute_file(self, file_path: str, **kwargs) -> Any:
        """
        Execute a file with arguments

        Arguments in the script is write like this:
        $LUP_ARG_NAME (in the script) -> kwargs["LUP_ARG_NAME"] (in the function)
        ${LUP_ARG_NAME} (in the script) -> kwargs["LUP_ARG_NAME"] (in the function)
        """
        pass

    def __str__(self) -> str:
        return f"<LUPL:{self.__class__.__name__}>"
