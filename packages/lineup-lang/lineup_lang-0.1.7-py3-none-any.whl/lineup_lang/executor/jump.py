from .default import DefaultExecutor
from ..error import ExecutorFunctionNotExistError
from typing import Any, List


class JumperExecutor(DefaultExecutor):
    jump_functions = ["JUMP"]
    line = 0
    # Executor version - it's set on the lineup version
    _version = None

    def jump(self, line: int):
        self.line = line
        self.logger.debug(
            f"Jump to: {self.line} (execute index {self.line + 1} or line " +
            f"{self.line + 2})")

    def execute_jump(self, line: List[str]):
        if line[0] == "JUMP":
            if (len(line) > 2):
                if line[2] == "FROM":
                    self.jump(self.line + int(line[1]))
            else:
                self.jump(int(line[1]) - 2)
            return None
        raise ExecutorFunctionNotExistError(
            f"'{line[0]}' not exist in '{self}'")

    def execute_line(self, line: List[str]):
        if line[0] in self.jump_functions:
            return self.execute_jump(line)
        return super().execute_line(line)

    def execute(self, script: List[List[str]]) -> Any:
        self.stop = False
        result = None
        self.line = -1
        while self.line < len(script) - 1:
            if self.stop:
                break
            self.line += 1
            result = self.execute_line(script[self.line])
        return result
