import csv
import argparse
from tabulate import tabulate


# функция обработки аргументов терминала
def parse_arguments(args=None):
    parser = argparse.ArgumentParser(description="Вывод таблицы из CSV файлов")
    parser.add_argument("--files", required=True, nargs='+', help="Выбор требуемых csv файлов")
    parser.add_argument("--report", nargs='+', help="Выбор требуемых для вывода столбцов")
    parser.add_argument("--count", help="Подсчет сотрудников с той или иной характеристикой")
    return parser.parse_args(args)


# функция чтения всех csv файлов и объединения в одну таблицу
def load_csv_files(file_paths):
    table = []
    for file in file_paths:
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                table.append(row)
    return table


# функция выбора указанных столбцов (формирование отчётной таблицы)
def build_report_table(table, columns=None):
    # если столбцы не указаны — возвращается копия исходной таблицы
    if not columns:
        return table.copy()

    header = table[0]
    indices = []

    # получение номеров требуемых столбцов
    for col in columns:
        if col not in header:
            raise ValueError(f"Column '{col}' not found")
        indices.append(header.index(col))

    new_table = []
    # формирование новой таблицы: имя + требуемые столбцы
    for row in table:
        filtered = [row[0]] + [row[i] for i in indices]
        new_table.append(filtered)

    return new_table


# функция удаления повторяющихся заголовков при объединении нескольких файлов
def remove_duplicate_headers(table, files_count):
    result = table.copy()
    header = result.pop(0)

    # если файлов больше одного — удалить повторяющиеся строки заголовков
    if files_count > 1:
        repeats_to_remove = files_count - 1
        for _ in range(repeats_to_remove):
            if header in result:
                result.remove(header)

    return header, result


# функция подсчёта строк (людей) с той или иной характеристикой
def count_rows(table_original, to_count):
    counter = 0
    for row in table_original:
        for item in row:
            if to_count in item:
                counter += 1
    return counter


def main(args=None):
    # получение аргументов терминала
    parsed = parse_arguments(args)

    # загрузка csv файлов
    table_original = load_csv_files(parsed.files)

    # формирование таблицы по требуемым столбцам
    #if parsed.report:
    table_for_output = build_report_table(table_original, parsed.report)

    # удаление дубликатов заголовков (если файлов несколько)
    header, body = remove_duplicate_headers(table_for_output, len(parsed.files))

    # вывод таблицы
    print(tabulate(body, headers=header))

    # если требуется подсчёт строк по характеристике
    if parsed.count:
        print("\nКоличество людей, у которых", parsed.count, ":", count_rows(table_original, parsed.count), "\n")


if __name__ == "__main__":
    main()
