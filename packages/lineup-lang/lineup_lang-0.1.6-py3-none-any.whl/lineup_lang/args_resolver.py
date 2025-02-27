from typing import Tuple, Optional
import regex as re
from .error import ArgumentNotExistError
import logging


class ArgsResolver:
    """
    Resolve the arguments in the script
    """
    logging = logging.getLogger("lineup_lang")

    def resolve(self, script: str, **kwargs: str) -> str:
        regex: Tuple[str, int, int | None, Optional[str]] = [
            (r"\$\{([\w\-\_]+)(:(.+?))?\}", 1, 3),
            (r"\$([\w\-\_]+)", 1, None),
            (r"\$\((\w+):(.+?)\)", 1, 2, "{0} is deprecated")
        ]
        for i, r in enumerate(regex):
            matches = re.finditer(r[0], script)
            for match in matches:
                self.logging.debug(f"Match: {match.group(0)} with regex: {i} ({r[0]})")
                if len(r) == 4:
                    self.logging.warning(r[3].format(match.group(0)))
                script = self._modify_script(script, match, r, kwargs)
        return script

    def _modify_script(self, script: str, match: re.Match, regex: Tuple[str, int, int | None], kwargs: str) -> str:
        """
        Modify the script with the arguments
        """
        keyname = match.group(regex[1])
        default_value = None
        if regex[2]:
            default_value = match.group(regex[2])
        value = kwargs.get(keyname, default_value)
        if value is None:
            raise ArgumentNotExistError(f"'{keyname}' not exist in '{kwargs}'")
        value = value.replace("\"", "\\\"")
        value = value.replace("#", "\\#")
        return script.replace(match.group(0), "\"" + value + "\"")
