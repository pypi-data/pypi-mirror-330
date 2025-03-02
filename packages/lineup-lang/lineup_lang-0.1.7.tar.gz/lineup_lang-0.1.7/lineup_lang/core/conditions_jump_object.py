from ..language_object import CoreObjectInterface
from ..error import LineupError
from typing import List, Tuple


class ConditionsJumpObject(CoreObjectInterface):
    last_result = None
    version = None

    def __init__(self):
        self.functions = {
            "IF": self._if,
            "NOTIF": self._notif,
            "ELSE": self._else,
            "EQUAL": self._equal,
        }

    def _get_two_command(self, jump_size: str, from_or_first_arg: str,
                         *args) -> Tuple[List[str], List[str]]:
        command = args
        jump_command = ["JUMP", jump_size]
        if from_or_first_arg == "FROM":
            jump_command.append("FROM")
        else:
            command.insert(0, from_or_first_arg)
        return [jump_command, command]

    def _if(self, jump_size: str, from_or_first_arg: str, *args):
        jump_command, command = self._get_two_command(jump_size,
                                                      from_or_first_arg,
                                                      *args)
        result = False
        try:
            result = self.executor.execute_line(command)
        except LineupError:
            pass
        if result:
            self.last_result = True
            self.executor.execute_line(jump_command)
        self.last_result = False

    def _notif(self, jump_size: str, from_or_first_arg: str, *args):
        jump_command, command = self._get_two_command(jump_size,
                                                      from_or_first_arg,
                                                      *args)
        result = False
        try:
            result = self.executor.execute_line(command)
        except LineupError:
            pass
        if not result:
            self.last_result = True
            self.executor.execute_line(jump_command)
        self.last_result = False

    def _else(self, *args):
        if self.last_result:
            raise LineupError("ELSE without IF")
        self.last_result = False
        self.executor.execute_line(["JUMP", *args])

    def _equal(self, *args):
        first = self.executor.execute_line(["VAR", args[0], "GET"])
        second = self.executor.execute_line(["VAR", args[1], "GET"])
        if first == second:
            self.last_result = True
        else:
            self.last_result = False
        return self.last_result
