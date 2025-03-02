from typing import List, Any, Dict
from .language_object import LanguageInterface, LanguageExecutorInterface, \
     LanguageObjectInterface, CoreObjectInterface
from .error import LineupError, UnexpectedError
from .logger import start_logging
from .line_decoder import LineDecoder
from .args_resolver import ArgsResolver
import lineup_lang.executor as luexec
import lineup_lang.core as lucore
import logging
import os

__all__ = ["Language", "LanguageObjectInterface", "CoreObjectInterface", "luexec", "lucore"]


class Language(LanguageInterface):
    """Language object"""

    _executor: LanguageExecutorInterface
    no_error: bool
    logger = logging.getLogger("lineup_lang")
    is_closed = False

    def __init__(self, executor: LanguageExecutorInterface,
                 no_error: bool = True, log_level: str = "WARN"):
        start_logging(log_level)
        self._executor = executor
        self.no_error = no_error
        self.logger.info(f"Start: {self} with executor: {executor}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if self.is_closed:
            return
        self.is_closed = True
        self.logger.info(f"Close: {self}")
        self._executor.close()

    def reset(self):
        super().reset()
        self._executor.reset()

    def get_all_functions(self) -> List[str]:
        return self._executor.get_all_functions()

    def get_versions(self) -> Dict[str, str]:
        file_version = os.path.join(os.path.dirname(__file__), "VERSION")
        lup_version = "0.0.0"
        with open(file_version, "r") as file:
            lup_version = file.read().strip()
        all_versions = self._executor.get_versions()
        all_versions["lineup_lang"] = lup_version
        for [name, version] in all_versions.items():
            if version is None:
                all_versions[name] = lup_version
        return all_versions

    def execute_script(self, script: str) -> Any:
        self.logger.info("Launch a script")
        self.logger.debug(f"Execute script:\n{script}")
        line_decoder = LineDecoder()
        script_lines = []
        for line in script.split("\n"):
            line = line_decoder.decode(line)
            if not line:
                continue
            script_lines.append(line)
        try:
            if self.is_closed:
                raise LineupError("Language is closed")
            result = self._executor.execute(script_lines)
        except Exception as e:
            if self.no_error:
                self.logger.error(f"Error: {e.__class__.__name__}: {e}")
                return None
            if isinstance(e, LineupError):
                raise e
            raise UnexpectedError(e)
        self._executor.reset()
        return result

    def execute_script_with_args(self, script: str, **kwargs) -> Any:
        args_resolver = ArgsResolver()
        script = args_resolver.resolve(script, **kwargs)
        return self.execute_script(script)

    def execute_file(self, file_path: str, **kwargs) -> Any:
        with open(file_path, "r") as file:
            script = file.read()
        return self.execute_script_with_args(script, **kwargs)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"
