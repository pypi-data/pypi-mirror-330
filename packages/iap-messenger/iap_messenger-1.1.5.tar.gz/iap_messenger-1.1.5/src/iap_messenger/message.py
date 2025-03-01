from dataclasses import dataclass
from copy import copy, deepcopy
from typing import Any
from iap_messenger.data_decoder import decode

Error = ValueError | None

@dataclass(kw_only=True)
class Message:
    """Class for keeping track of messages."""
    Raw: bytes
    From: str
    To: str
    Parameters: dict | None = None
    Reply: bytes | Any
    error: str | None = None
    decoded: Any = None
    is_decoded: bool = False
    uid: str
    _link: str = ""
    _source: str = ""
    _content_type: str = "application/json"
    _inputs: dict

    def decode(self) -> tuple[Any, Error]:
        """Decode the Raw data."""
        return decode(self.Raw, self._content_type, self._inputs)
        
    def __copy__(self):
        """Return a copy of the message."""
        msg = type(self)(
            Raw = self.Raw,
            From = self.From,
            To = self.To,
            Parameters = None if self.Parameters is None else deepcopy(self.Parameters),
            Reply = None if self.Reply is None else deepcopy(self.Reply),
            error = self.error,
            decoded = None if self.decoded is None else deepcopy(self.decoded),
            is_decoded = self.is_decoded,
            uid = self.uid,
            _link = self._link,
            _source = self._source,
            _content_type = self._content_type,
            _inputs = self._inputs
        )
        return msg