# cd examples
import line_history
from datetime import datetime

FILE_PATH = "./history.txt"

def main():
    history = line_history.History.read_from_file(FILE_PATH)

    print("2024-01-01の履歴")
    print(history.search_by_date(datetime(2024, 1, 1)), end="\n")

    keyword = "こん"
    print(f"テキスト検索「{keyword}」")
    print(list(map(lambda x: x.line, history.search_by_keyword(keyword)[:10])), end="\n")
    print()

    print("ランダム検索")
    print(history.search_by_random()[:100], end="\n")

    print("履歴の日数")
    print(history.len())

    print("履歴が空であるかどうか")
    print(history.is_empty())


if __name__ == '__main__':
    main()
