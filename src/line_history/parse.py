import dataclasses
import datetime
import re
from typing import Iterator, TextIO
import typing


@dataclasses.dataclass
class HistoryEntry:
    timestamp: datetime.datetime
    speaker: str
    message: str


DATE_PATTERN = re.compile(r"^(\d{4})/(\d{2})/(\d{2})\(\w+\)$")
CHAT_PATTERN = re.compile(r"^\d{2}:\d{2}\t.*\t.+$")


def match_date(line: str) -> datetime.date | None:
    date_match = DATE_PATTERN.match(line)
    if date_match:
        year = int(date_match.group(1))
        month = int(date_match.group(2))
        day = int(date_match.group(3))
        return datetime.date(year, month, day)
    return None


def match_chat(line: str) -> typing.Tuple[datetime.time, str, str] | None:
    chat_match = CHAT_PATTERN.match(line)
    if not chat_match:
        return None

    time_str, speaker, message = line.split("\t", 2)

    hour, minute = map(int, time_str.split(":"))

    return datetime.time(hour, minute), speaker, message


class Parser:
    current_entry: HistoryEntry | None = None
    current_date: datetime.date | None = None
    current_multi_line = False

    def __init__(self):
        pass

    def finalize(self, entry: HistoryEntry) -> HistoryEntry:
        """
        メッセージ末尾の改行を削除し、
        両端のダブルクオートを除去（必要に応じて）してから返却する。
        """
        msg = entry.message.rstrip("\n")
        if self.current_multi_line:
            msg = msg[1:-1]
            self.current_multi_line = False
        entry.message = msg
        return entry

    def parse_history(self, io: TextIO) -> Iterator[HistoryEntry]:
        """
        LINEのチャット履歴をテキストファイルのようなオブジェクトからパースし、
        HistoryEntryインスタンスを順次yieldする。

        期待される入力フォーマット:
            YYYY/MM/DD(曜日)\n
            speaker\tHH:MM\tmessage\n
            speaker\tHH:MM\tmessage\n

            YYYY/MM/DD(曜日)\n
            ...

        カッコ内の曜日情報は無視される。
        """

        for line in io:
            date_match = match_date(line)

            # 日付の行
            if date_match and (
                not self.current_date
                or (self.current_date and date_match > self.current_date)
            ):
                self.current_date = date_match
                continue

            # 最初の日付までは無視する
            if self.current_date is None:
                continue

            chat_match = match_chat(line)

            if chat_match:
                if self.current_entry:
                    yield self.finalize(self.current_entry)

                time, speaker, message = typing.cast(
                    typing.Tuple[datetime.time, str, str], chat_match
                )

                self.current_entry = HistoryEntry(
                    timestamp=datetime.datetime.combine(self.current_date, time),
                    speaker=speaker,
                    message=message,
                )
            else:
                if self.current_entry:
                    self.current_entry.message += line
                    self.current_multi_line = True

        # ファイル末尾で最後のエントリがあればyield
        if self.current_entry:
            yield self.finalize(self.current_entry)
