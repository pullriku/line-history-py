import datetime
from pathlib import Path

import polars

from line_history.history import MESSAGE_COL, SPEAKER_COL, History


def main():
    history = History.from_file(Path("./examples/history.txt"))

    result = (
        history.where_year(2024)
        .where_month_between(1, 3)
        .where_time_between(datetime.time(0, 0), datetime.time(10, 00))
        .get_lazy_df()
        .select(
            polars.format("{} 💬({})", polars.col(SPEAKER_COL), polars.col(MESSAGE_COL))
        )
        .collect()
    )

    print(result)
    # print("\n".join(map(str, result)))


if __name__ == "__main__":
    main()
