from __future__ import annotations
from datetime import date, time
from typing import Dict, List, Optional, Tuple

class History:
    days: Dict[date, Day]

    def __init__(self, days: Dict[date, Day]) -> None: ...
    @classmethod
    def read_from_file(cls, file_path: str) -> History: ...
    @classmethod
    def from_text(cls, text: str) -> History: ...
    def days(self) -> Dict[date, Day]: ...
    def len(self) -> int: ...
    def is_empty(self) -> bool: ...
    def search_by_date(self, date: date) -> Optional[Day]: ...
    def search_by_keyword(self, keyword: str) -> List[Tuple[date, Chat]]: ...
    def search_by_random(self) -> Day: ...

class Day:
    def date(self) -> date: ...
    def chats(self) -> List[Chat]: ...
    def search_by_keyword(self, keyword: str) -> List[Tuple[date, Chat]]: ...

class Chat:
    def time(self) -> time: ...
    def speaker(self) -> Optional[str]: ...
    def message_lines(self) -> List[str]: ...
