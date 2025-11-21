# CSV_Report_Generator
Вывод данных из CSV файла в виде таблицы

`main.py` - основной файл программы.

`test_main.py` - файл, содержащий тесты pytest программы `main.py`.

Для `main.py` и `test_main.py` созданы текстовые файлы для удобства просмотра кода.

`image_examples` - папка, содержащая скрины примеров работы программы.

`employees1.csv` и `employees2.csv` - примеры CSV файлов для работы с программой.

## Возможности
- Загрузка одного или нескольких CSV-файлов (`--files`).
- Поддержка указания пути к требуемому файлу.
- Формирование отчёта по выбранным столбцам (`--report`).
- Подсчёт строк (людей), содержащих указанную подстроку, например, навык Python (`--count`).
- Вывод результата в табличном формате.

## Быстрый пример
```bash
python main.py --files C:\Users\admin\Desktop\employees1.csv employees2.csv --report performance skill --count Python
