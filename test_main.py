import sys
from pathlib import Path
import pytest

# импорт тестируемых функций
from main import (
    parse_arguments,
    load_csv_files,
    build_report_table,
    remove_duplicate_headers,
    count_rows,
    main)


# тестирование функции parse_arguments()
def test_parse_arguments_basic():
    # проверка корректного разбора аргументов
    args = parse_arguments(["--files", "a.csv", "b.csv", "--report", "position"])
    assert args.files == ["a.csv", "b.csv"]
    assert args.report == ["position"]


# должен корректно работать при отсутствии опции --report
def test_parse_arguments_without_report():
    args = parse_arguments(["--files", "a.csv"])
    assert args.report is None


# фикстура для временного csv файла
@pytest.fixture
def csv_file(tmp_path: Path):
    # создание тестового csv файла
    content = (
        "name,position,completed_tasks,performance\n"
        "Alice,Dev,10,4.5\n"
        "Bob,Manager,20,4.8\n"
    )
    file = tmp_path / "employees.csv"
    file.write_text(content, encoding="utf-8")
    return file


@pytest.fixture
def csv_file2(tmp_path: Path):
    # создание второго файла для тестов объединения
    content = (
        "name,position,completed_tasks,performance\n"
        "Chris,Engineer,15,4.6\n"
    )
    file = tmp_path / "employees2.csv"
    file.write_text(content, encoding="utf-8")
    return file


# тестирование загрузки файлов
def test_load_csv_files(csv_file):
    # проверка, что файл корректно загружается в таблицу
    table = load_csv_files([str(csv_file)])
    assert len(table) == 3  # 1 header + 2 строки
    assert table[1][0] == "Alice"


# тестирование функции создания таблицы с нужными столбцами
def test_build_report_table_all_columns(csv_file):
    # при отсутствии аргумента report таблица должна остаться полной
    table = load_csv_files([str(csv_file)])
    full = build_report_table(table)
    assert full == table


# выбор конкретных столбцов
def test_build_report_table_selected_columns(csv_file):
    table = load_csv_files([str(csv_file)])
    report = build_report_table(table, ["position", "performance"])
    assert report[0][1] == "position"
    assert report[0][2] == "performance"
    assert report[1][2] == "4.5"


# ошибка при указании несуществующего столбца
def test_build_report_table_wrong_column(csv_file):
    table = load_csv_files([str(csv_file)])
    with pytest.raises(ValueError):
        build_report_table(table, ["nonexistent"])


# тестирование обрезки повтора оглавления
def test_remove_duplicate_headers_single_file(csv_file):
    table = load_csv_files([str(csv_file)])
    header, body = remove_duplicate_headers(table, 1)
    assert header[0] == "name"
    assert len(body) == 2


# проверка удаления дублирующегося заголовка
def test_remove_duplicate_headers_multiple_files(csv_file, csv_file2):
    t1 = load_csv_files([str(csv_file)])
    t2 = load_csv_files([str(csv_file2)])
    merged = t1 + t2  # эмуляция объединения файлов

    header, body = remove_duplicate_headers(merged, 2)
    assert body.count(header) == 0  # заголовки удалены
    assert any("Chris" in row for row in body)


# тестирование функции подсчета строк
def test_count_rows_basic(csv_file):
    table = load_csv_files([str(csv_file)])
    # слово "Dev" встречается 1 раз
    assert count_rows(table, "Dev") == 1


# проверка, что при отсутствии совпадений пишется 0
def test_count_rows_no_matches(csv_file):
    table = load_csv_files([str(csv_file)])
    assert count_rows(table, "XYZ") == 0


# тестирование через monkeypatch
def run_main(monkeypatch, args):
    # подмена sys.argv для эмуляции вызова из терминала
    fake_argv = ["main.py"] + args
    monkeypatch.setattr(sys, "argv", fake_argv)
    main()


# проверка корректного вывода таблицы
def test_main_output(monkeypatch, capsys, csv_file):
    run_main(monkeypatch, ["--files", str(csv_file)])
    out = capsys.readouterr().out
    assert "Alice" in out
    assert "Manager" in out


# проверка выборочного вывода столбцов
def test_main_with_report(monkeypatch, capsys, csv_file):
    run_main(monkeypatch, ["--files", str(csv_file), "--report", "performance"])
    out = capsys.readouterr().out
    assert "performance" in out
    assert "4.5" in out
    assert "Dev" not in out  # не должно быть остальных столбцов


# проверка вывода подсчёта строк
def test_main_with_count(monkeypatch, capsys, csv_file):
    run_main(monkeypatch, ["--files", str(csv_file), "--count", "Dev"])
    out = capsys.readouterr().out.strip().split("\n")
    assert out[-1].endswith("1")  # последняя строка — результат подсчёта
