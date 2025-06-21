import dataclasses
import datetime
from io import StringIO
from pathlib import Path
from typing import Iterator, TextIO
import polars

from line_history import parse
from line_history.parse import HistoryEntry

__fields = dataclasses.fields(HistoryEntry)
TIMESTAMP_COL = __fields[0].name
SPEAKER_COL = __fields[1].name
MESSAGE_COL = __fields[2].name


@dataclasses.dataclass(frozen=True)
class Chat:
    timestamp: datetime.datetime
    speaker: str
    message: str

    @staticmethod
    def from_frame(frame: polars.DataFrame) -> Iterator["Chat"]:
        result = frame.iter_rows(named=True)
        return (Chat(**row) for row in result)


@dataclasses.dataclass(frozen=True)
class History:
    df: polars.DataFrame
    lazy_df: polars.LazyFrame

    @staticmethod
    def from_io(io: TextIO) -> "History":
        parser = parse.Parser()
        df = polars.DataFrame(parser.parse_history(io=io))
        lazy_df = df.lazy()
        return History(df=df, lazy_df=lazy_df)

    @staticmethod
    def from_file(path: Path) -> "History":
        with path.open() as f:
            history = History.from_io(f)
        return history

    @staticmethod
    def from_str(s: str) -> "History":
        return History.from_io(StringIO(s))

    def with_lazy_df(self, lazy_df: polars.LazyFrame) -> "History":
        return History(df=self.df, lazy_df=lazy_df)

    def timestamps(self) -> polars.Series:
        return self.df.get_column(TIMESTAMP_COL)

    def speakers(self) -> polars.Series:
        return self.df.get_column(SPEAKER_COL)

    def messages(self) -> polars.Series:
        return self.df.get_column(MESSAGE_COL)

    def where_year(self, year: int) -> "History":
        lazy_df = self.lazy_df.filter(polars.col(TIMESTAMP_COL).dt.year() == year)
        return self.with_lazy_df(lazy_df)

    def where_year_between(self, lower_bound: int, upper_bound: int) -> "History":
        lazy_df = self.lazy_df.filter(
            polars.col(TIMESTAMP_COL).dt.year().is_between(lower_bound, upper_bound)
        )
        return self.with_lazy_df(lazy_df)

    def where_month(self, month: int) -> "History":
        lazy_df = self.lazy_df.filter(polars.col(TIMESTAMP_COL).dt.month() == month)
        return self.with_lazy_df(lazy_df)

    def where_month_between(self, lower_bound: int, upper_bound: int) -> "History":
        lazy_df = self.lazy_df.filter(
            polars.col(TIMESTAMP_COL).dt.month().is_between(lower_bound, upper_bound)
        )
        return self.with_lazy_df(lazy_df)

    def where_day(self, day: int) -> "History":
        lazy_df = self.lazy_df.filter(polars.col(TIMESTAMP_COL).dt.day() == day)
        return self.with_lazy_df(lazy_df)

    def where_day_between(self, lower_bound: int, upper_bound: int) -> "History":
        lazy_df = self.lazy_df.filter(
            polars.col(TIMESTAMP_COL).dt.day().is_between(lower_bound, upper_bound)
        )
        return self.with_lazy_df(lazy_df)

    def where_date(self, date: datetime.date) -> "History":
        lazy_df = self.lazy_df.filter(polars.col(TIMESTAMP_COL).dt.date() == date)
        return self.with_lazy_df(lazy_df)

    def where_date_between(
        self, lower_bound: datetime.date, upper_bound: datetime.date
    ) -> "History":
        lazy_df = self.lazy_df.filter(
            polars.col(TIMESTAMP_COL).dt.date().is_between(lower_bound, upper_bound)
        )
        return self.with_lazy_df(lazy_df)

    def where_time_between(
        self, lower_bound: datetime.time, upper_bound: datetime.time
    ) -> "History":
        lazy_df = self.lazy_df.filter(
            polars.col(TIMESTAMP_COL).dt.time().is_between(lower_bound, upper_bound)
        )
        return self.with_lazy_df(lazy_df)

    def where_speaker(self, speaker: str) -> "History":
        lazy_df = self.lazy_df.filter(polars.col(SPEAKER_COL) == speaker)
        return self.with_lazy_df(lazy_df)

    def where_contains(self, message: str) -> "History":
        lazy_df = self.lazy_df.filter(polars.col(MESSAGE_COL).str.contains(message))
        return self.with_lazy_df(lazy_df)

    def where_message(self, message: str) -> "History":
        lazy_df = self.lazy_df.filter(polars.col(MESSAGE_COL) == message)
        return self.with_lazy_df(lazy_df)

    def collect(self) -> Iterator[Chat]:
        df = self.lazy_df.collect()
        result = df.iter_rows(named=True)

        return (Chat(**row) for row in result)

    def get_lazy_df(self):
        return self.lazy_df
