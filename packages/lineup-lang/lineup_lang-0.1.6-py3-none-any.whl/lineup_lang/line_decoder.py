from .error import DecodeLineStringError
from typing import List
import regex as re


class LineDecoder:
    """
    Decode a line string to an instruction list
    """

    def decode(self, line: str) -> List[str] | None:
        """
        Decode a line string to an instruction list
        """
        line = line.strip()
        if line.startswith("#"):
            return None
        # delete comments on the line
        first_comment_block = re.search(r"[^\\]#", line)
        if first_comment_block:
            line = line[:first_comment_block.start()]
        line = line.replace("\\#", "#")  # replace escaped comments
        return self._split_line(line)

    def _split_line(self, line: str) -> List[str]:
        lines = self.format_quotes(line)
        result = []
        # odd is inside quotes, even is outside
        for i, line in enumerate(lines):
            if i % 2 == 1:
                # inside quotes, the line has to be kept as is
                result.append(line)
            elif line.strip() != "":
                # outside quotes, split by space for get the instructions
                result.extend(line.strip().split(" "))
        return result

    def format_quotes(self, line: str) -> List[str]:
        """
        Format the quotes in the line

        Split the line by quotes, keep the backslahed quotes
        Return a list of odd is inside quotes, even is outside the quotes
        """
        lines = line.split('"')
        result = []
        current_line = ""
        for i in lines:
            current_line += i
            if i.endswith("\\"):
                current_line += '"'
            else:
                result.append(current_line)
                current_line = ""
        if current_line:
            raise DecodeLineStringError(f"'{line}' is not valid line string")
        return result
