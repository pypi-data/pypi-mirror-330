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
        line_splitted = self._split_line(line)
        if not line_splitted:
            return None
        return line_splitted

    def _split_line(self, line: str) -> List[str]:
        lines = self.format_quotes(line)
        result = []
        if len(lines) % 2 == 0:
            raise DecodeLineStringError(f"'{line}' is not valid line string")
        # odd is inside quotes, even is outside
        for i, line in enumerate(lines):
            if i % 2 == 1:
                # inside quotes, the line has to be kept as is
                result.append(line)
            else:
                # outside quotes, split by space for get the instructions
                result.extend([
                    x for x in line.split(" ") if x.strip() != ""
                ])
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
                # delete the backslash and add the quote
                current_line = bytearray(current_line, "utf-8")
                current_line[-1] = ord('"')
                current_line = current_line.decode("utf-8")
            else:
                result.append(current_line)
                current_line = ""
        if current_line:
            raise DecodeLineStringError(f"'{line}' is not valid line string")
        return result
