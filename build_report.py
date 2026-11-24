# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

MEDIA = Path(r"C:\Users\user\AppData\Local\Cursor\AgentStores\cursor_agent_stores\bc-8b5ca42b-4d1c-4114-9c7f-ca34f8a7da2d\files\media\okfks3")
OUT = Path(r"C:\Users\user\AppData\Local\Cursor\AgentStores\cursor_agent_stores\bc-8b5ca42b-4d1c-4114-9c7f-ca34f8a7da2d\files\docs\OKFKS_Praktika_3.docx")

def set_run_font(run, size=12, bold=False, name="Times New Roman"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold

def add_p(doc, text, *, size=12, bold=False, center=False, first_line=True, space_after=6):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(0)
    pf.line_spacing = 1.15
    if first_line:
        pf.first_line_indent = Cm(1.25)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    return p

def add_heading_like(doc, text, size=14):
    return add_p(doc, text, size=size, bold=True, center=False, first_line=False, space_after=8)

def add_fig(doc, path, caption, width=15.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run()
    run.add_picture(str(path), width=Cm(width))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.first_line_indent = Cm(0)
    cap.paragraph_format.space_after = Pt(10)
    r = cap.add_run(caption)
    set_run_font(r, size=11, bold=False)

def fill_table(table, rows):
    for i, row in enumerate(rows):
        for j, cell_text in enumerate(row):
            cell = table.rows[i].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.first_line_indent = Cm(0)
            run = p.add_run(str(cell_text))
            set_run_font(run, size=11, bold=(i == 0))

def main():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(1.5)

    # Title page
    for line in [
        "МИНИСТЕРСТВО ОБРАЗОВАНИЯ МОСКОВСКОЙ ОБЛАСТИ",
        "ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ПРОФЕССИОНАЛЬНОЕ",
        "ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ МОСКОВСКОЙ ОБЛАСТИ",
        "«СЕРПУХОВСКИЙ КОЛЛЕДЖ»",
    ]:
        add_p(doc, line, size=12, bold=True, center=True, first_line=False, space_after=2)

    for _ in range(3):
        add_p(doc, "", first_line=False, space_after=6)

    add_p(doc, "Практическая работа №3", size=16, bold=True, center=True, first_line=False)
    add_p(doc, "по теме", size=12, center=True, first_line=False, space_after=2)
    add_p(doc, "«Выявление первичных и вторичных ошибок»", size=14, bold=True, center=True, first_line=False)
    add_p(doc, "Дисциплина: Основы компьютерных и функциональных систем (ОКФКС)", size=12, center=True, first_line=False)
    for _ in range(4):
        add_p(doc, "", first_line=False, space_after=6)
    add_p(doc, "студента 4 курса группы 1231", size=12, center=True, first_line=False, space_after=2)
    add_p(doc, "Гончаровский В.Г.", size=12, bold=True, center=True, first_line=False)
    add_p(doc, "", first_line=False)
    add_p(doc, "Преподаватель:", size=12, center=True, first_line=False, space_after=2)
    add_p(doc, "Шкуратова С.С.", size=12, center=True, first_line=False)
    for _ in range(6):
        add_p(doc, "", first_line=False, space_after=6)
    add_p(doc, "Серпухов, 2026", size=12, center=True, first_line=False)
    doc.add_page_break()

    add_heading_like(doc, "2. Цель и задачи")
    add_p(doc, "Цель работы: научиться находить причины дефектов в настольном приложении «Каталог книг» (BookDesk), отличать первичные ошибки от вторичных, править код на C# и проверять результат тестами.")
    add_p(doc, "Задачи: воспроизвести дефекты учебной версии; записать фактическое поведение; найти участок кода; отделить первичные причины от вторичных последствий; набросать причинно-следственную схему; написать Unit-тесты NUnit в проекте BookDesk.Tests; исправить первичные ошибки; повторно прогнать упавшие тесты; проверить связанные функции.")

    add_heading_like(doc, "3. Исходная версия программы")
    add_p(doc, "Объект тестирования - приложение BookDesk. Список книг держится в памяти. Добавление, правка, удаление и поиск лежат в BookCatalog, проверка полей - в BookValidator. Итоговая стоимость считается как Copies * Price и показывается в столбце «Итого». Окно собрано на WPF (.NET 9) в Visual Studio. Логику и тесты гонял через Test Explorer (NUnit).")

    t = doc.add_table(rows=6, cols=2)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    fill_table(t, [
        ("Компонент", "Назначение"),
        ("Book", "Название, жанр, число экземпляров, цена и итоговая стоимость"),
        ("BookValidator", "Проверка пустых полей, экземпляров и цены"),
        ("BookCatalog", "Сохранение, удаление и поиск"),
        ("MainWindow", "Таблица, кнопки и строка поиска"),
        ("BookDesk.Tests", "18 модульных тестов NUnit"),
    ])
    add_p(doc, "", first_line=False, space_after=4)
    add_p(doc, "В дефектной версии DefectMode включён. Так удобнее сравнивать «до» и «после» без двух копий решения.")
    add_fig(doc, MEDIA / "01_app_main.png", "Рисунок 1 - окно BookDesk, дефектная учебная версия", width=14)

    add_heading_like(doc, "4. Перечень дефектов")
    add_p(doc, "В учебной версии нашлось пять дефектов. Один из них вторичный: он вылезает только потому, что первичная ошибка пропускает плохие данные.")
    t = doc.add_table(rows=6, cols=4)
    t.style = "Table Grid"
    fill_table(t, [
        ("ID", "Описание", "Тип", "Фактический результат"),
        ("BUG-01", "Валидация пропускает отрицательное число экземпляров", "Первичная", "Книга с Copies = -1 сохраняется"),
        ("BUG-02", "При отрицательном числе экземпляров неверен итог", "Вторичная", "Итого = Copies * Price становится отрицательным"),
        ("BUG-03", "Удаление без выбранной строки", "Первичная", "Удаляется первая запись, сообщения нет"),
        ("BUG-04", "Поиск чувствителен к регистру", "Первичная", "Запрос «мышь» не находит «Мышь»"),
        ("BUG-05", "Пустая цена обрабатывается криво", "Первичная", "Пустое поле сохраняется как цена 0"),
    ])
    add_p(doc, "", first_line=False, space_after=4)
    add_fig(doc, MEDIA / "02_app_search_case.png", "Рисунок 2 - поиск «мышь» в дефектной версии: совпадений 0", width=14)
    add_fig(doc, MEDIA / "03_app_delete_bug.png", "Рисунок 3 - удаление без выбора: пропала первая книга", width=14)

    add_heading_like(doc, "5. Анализ первичных и вторичных ошибок")
    t = doc.add_table(rows=6, cols=4)
    t.style = "Table Grid"
    fill_table(t, [
        ("ID", "Причина", "Последствие", "Исправление"),
        ("BUG-01", "В BookValidator нет проверки Copies < 0", "В список попадает некорректная книга", "Добавлена проверка диапазона 0...5000"),
        ("BUG-02", "В расчёт итога попадает отрицательное число экземпляров", "Итоговая стоимость меньше нуля", "Отдельный патч не нужен: после BUG-01 такое значение не сохраняется"),
        ("BUG-03", "TryDelete при selected = null вызывает RemoveAt(0)", "Пропадает чужая книга", "Возвращается сообщение «Выберите книгу для удаления.»"),
        ("BUG-04", "Поиск сравнивает строки с учётом регистра", "Часть книг не находится", "Сравнение заменено на OrdinalIgnoreCase"),
        ("BUG-05", "Пустая строка цены подменяется нулём", "В каталог попадает книга с ценой 0", "Пустая цена отклоняется как нечисловое значение"),
    ])

    add_heading_like(doc, "6. Причинно-следственная схема")
    add_p(doc, "BUG-01 (нет нижней границы числа экземпляров) даёт сохранение отрицательного Copies. Это значение уходит в формулу итога, поэтому появляется BUG-02. После правки BUG-01 вторичный дефект пропадает сам. BUG-03, BUG-04 и BUG-05 независимы: у каждого своя причина, порождённого дефекта нет.")
    t = doc.add_table(rows=5, cols=3)
    t.style = "Table Grid"
    fill_table(t, [
        ("Первичная ошибка", "Что ломается дальше", "Вторичный дефект"),
        ("BUG-01. Copies < 0 принимается", "В список и в формулу итога попадает отрицательное число", "BUG-02. Итог становится отрицательным"),
        ("BUG-03. Удаление без выбора", "Удаляется первый элемент", "Вторичного дефекта нет"),
        ("BUG-04. Поиск с учётом регистра", "Совпадение «мышь» и «Мышь» не находится", "Вторичного дефекта нет"),
        ("BUG-05. Пустая цена становится 0", "Книга сохраняется с нулевой ценой", "Вторичного дефекта нет"),
    ])

    add_heading_like(doc, "7. Исправления")
    add_p(doc, "Первичные ошибки закрыты в BookValidator.Validate и BookCatalog. Для BUG-02 отдельную правку не делал: отрицательное число экземпляров больше не доходит до расчёта.")
    add_p(doc, "Ключевые места в коде (исправленная ветка): проверка Copies в диапазоне 0...5000; пустая цена не парсится как 0; при selected == null возвращается текст «Выберите книгу для удаления.»; поиск идёт через StringComparison.OrdinalIgnoreCase.")
    add_fig(doc, MEDIA / "06_code_validator.png", "Рисунок 4 - фрагмент BookValidator.cs с ветками DefectMode", width=15.5)
    add_fig(doc, MEDIA / "07_code_catalog.png", "Рисунок 5 - фрагмент BookCatalog.cs (удаление и поиск)", width=15.5)

    add_heading_like(doc, "8. Unit-тесты после исправлений")
    add_p(doc, "Написал 18 тестов NUnit в BookDesk.Tests. Ниже сводка. На дефектной версии часть из них падает. После правки первичных причин все проходят.")
    tests = [
        ("TC-01", "Корректная книга сохраняется, итог = 5000", "-", "Pass", "Pass"),
        ("TC-02", "Пустые название и жанр", "-", "Pass", "Pass"),
        ("TC-03", "Copies = -1 недопустимо", "BUG-01", "Fail", "Pass"),
        ("TC-04", "Copies = 0 допустимо", "регрессия", "Pass", "Pass"),
        ("TC-05", "Copies = 5000 допустимо", "регрессия", "Pass", "Pass"),
        ("TC-06", "Отрицательные экземпляры не попадают в итог", "BUG-01, BUG-02", "Fail", "Pass"),
        ("TC-07", "Удаление без выбора не меняет список", "BUG-03", "Fail", "Pass"),
        ("TC-08", "Поиск «мышь» находит «Мышь»", "BUG-04", "Fail", "Pass"),
        ("TC-09", "Пустая цена отклоняется", "BUG-05", "Fail", "Pass"),
        ("TC-10", "Правка с Copies = -5 не затирает старый итог", "BUG-01, BUG-02", "Fail", "Pass"),
        ("TC-11", "Copies = 5001 недопустимо", "регрессия", "Pass", "Pass"),
        ("TC-12", "Цена 0 недопустима", "регрессия", "Pass", "Pass"),
        ("TC-13", "Удаляется только выбранная книга", "регрессия", "Pass", "Pass"),
        ("TC-14", "Частичный поиск, пустой запрос, нет совпадений", "регрессия", "Pass", "Pass"),
        ("TC-15", "Текст вместо цены", "регрессия", "Pass", "Pass"),
        ("TC-16", "Корректное редактирование пересчитывает итог", "регрессия", "Pass", "Pass"),
        ("TC-17", "1 экземпляр и цена 0.01", "регрессия", "Pass", "Pass"),
        ("TC-18", "Итог 3 × 12000 = 36000", "регрессия", "Pass", "Pass"),
    ]
    t = doc.add_table(rows=1 + len(tests), cols=5)
    t.style = "Table Grid"
    fill_table(t, [("Тест", "Что проверяет", "Связанный дефект", "До", "После")] + tests)

    add_heading_like(doc, "9. Повторное тестирование")
    add_p(doc, "Сначала тесты запустил на дефектной версии в Test Explorer. Не прошли шесть проверок, которые ловят первичные ошибки и вторичный кривой итог: TC-03, TC-06, TC-07, TC-08, TC-09 и TC-10. Двенадцать остальных прошли. Значит соседние функции на этой сборке в целом живые.")
    add_fig(doc, MEDIA / "04_tests_defective.png", "Рисунок 6 - прогон NUnit на дефектной версии: 6 Fail / 12 Pass", width=14)
    add_p(doc, "После исправления эти шесть тестов запустил снова (режим DefectMode=OFF / флаг BOOKDESK_FIXED). Все прошли. BUG-02 отдельно не чинил: отрицательное число экземпляров больше не сохраняется, поэтому итог не уходит в минус.")
    t = doc.add_table(rows=7, cols=4)
    t.style = "Table Grid"
    fill_table(t, [
        ("Тест", "До", "После", "Что подтвердилось"),
        ("TC-03", "Fail", "Pass", "Отрицательные экземпляры отклоняются"),
        ("TC-06", "Fail", "Pass", "Отрицательные экземпляры не портят итог"),
        ("TC-07", "Fail", "Pass", "Без выбора список не меняется"),
        ("TC-08", "Fail", "Pass", "Поиск не зависит от регистра"),
        ("TC-09", "Fail", "Pass", "Пустая цена не сохраняется"),
        ("TC-10", "Fail", "Pass", "Неудачная правка не меняет старый итог"),
    ])
    add_p(doc, "", first_line=False, space_after=4)
    add_fig(doc, MEDIA / "05_tests_fixed.png", "Рисунок 7 - прогон NUnit после исправления: 18 из 18", width=14)

    add_heading_like(doc, "10. Регрессионное тестирование")
    add_p(doc, "После правок проверки экземпляров, удаления, поиска и разбора цены заново проверил связанные операции. Новых отказов нет.")
    t = doc.add_table(rows=9, cols=4)
    t.style = "Table Grid"
    fill_table(t, [
        ("Проверка", "До", "После", "Итог"),
        ("Добавление корректной книги, TC-01", "Pass", "Pass", "Сохранение работает"),
        ("Пустые строки, TC-02", "Pass", "Pass", "Проверка полей сохранена"),
        ("Границы 0, 5000 и 5001, TC-04, TC-05, TC-11", "Pass", "Pass", "Диапазон не сдвинулся"),
        ("Цена 0 и нечисловой ввод, TC-12, TC-15", "Pass", "Pass", "Разбор чисел сохранён"),
        ("Удаление выбранной книги, TC-13", "Pass", "Pass", "Удаление выбранной строки работает"),
        ("Поиск точный и частичный, TC-14", "Pass", "Pass", "Поиск не сломан"),
        ("Корректное редактирование, TC-16", "Pass", "Pass", "Пересчёт стоимости"),
        ("Мелкие цены и крупные итоги, TC-17, TC-18", "Pass", "Pass", "Арифметика на месте"),
    ])

    add_heading_like(doc, "11. Вывод")
    add_p(doc, "В работе разобраны дефекты приложения BookDesk («Каталог книг»). Первичными оказались пропуск отрицательного числа экземпляров, удаление без выбранной строки, поиск с учётом регистра и принятие пустой цены. Вторичным оказался неверный итог: он получается из уже ошибочного числа экземпляров и уходит вместе с BUG-01. Набор из 18 тестов NUnit на дефектной версии дал 6 ошибок и 12 успешных проверок. После правки первичных причин повторный прогон и регрессия прошли без ошибок: 18 из 18.")

    add_heading_like(doc, "Контрольные вопросы")
    add_p(doc, "Что такое первичная ошибка? Это дефект в коде, который сам по себе даёт неправильное поведение. В моей работе это пропущенная проверка экземпляров, кривая ветка удаления, сравнение строк с учётом регистра и подмена пустой цены нулём.")
    add_p(doc, "Что такое вторичная ошибка? Это следствие первичной ошибки в других данных или на экране. Отрицательный итог не отдельная ошибка формулы: формула просто умножает цену на то число экземпляров, которое уже сохранили неправильно.")
    add_p(doc, "Почему надо искать первичную причину? Если чинить только следствие, источник останется. Пока отрицательные экземпляры можно сохранить, итог снова станет кривым при следующем таком вводе.")
    add_p(doc, "Что такое регрессионное тестирование? Это повторная проверка функций, которые уже работали, после правки кода. Здесь заново проверил добавление, границы экземпляров, цену 0, удаление выбранной строки, поиск и редактирование.")
    add_p(doc, "Почему исправление может задеть другие функции? Сохранение, правка, поиск и удаление ходят через общие методы BookCatalog и BookValidator. Поменял одно условие - поменялось поведение всех экранов, которые это вызывают.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
