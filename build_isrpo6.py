# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

MEDIA = Path(r"C:\Users\user\AppData\Local\Cursor\AgentStores\cursor_agent_stores\bc-8b5ca42b-4d1c-4114-9c7f-ca34f8a7da2d\files\media\isrpo6")
OUT = Path(r"C:\Users\user\AppData\Local\Cursor\AgentStores\cursor_agent_stores\bc-8b5ca42b-4d1c-4114-9c7f-ca34f8a7da2d\files\docs\ISRPO_Praktika_6.docx")
MARGIN = Pt(54)

def font(run, size=14, bold=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold

def p(doc, text, *, size=14, bold=False, center=False, justify=True, indent=True, after=6, before=0):
    para = doc.add_paragraph()
    pf = para.paragraph_format
    pf.space_after = Pt(after)
    pf.space_before = Pt(before)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.first_line_indent = Cm(1.25) if indent and not center and not bold else Cm(0)
    if center:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif justify and not bold:
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    else:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = para.add_run(text)
    font(r, size=size, bold=bold)
    return para

def heading(doc, text):
    return p(doc, text, size=14, bold=True, justify=False, indent=False, after=8, before=10)

def fig(doc, name, caption):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.first_line_indent = Cm(0)
    para.add_run().add_picture(str(MEDIA / name), width=Cm(15))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.first_line_indent = Cm(0)
    cap.paragraph_format.space_after = Pt(10)
    r = cap.add_run(caption)
    font(r, size=12)

def table(doc, rows):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.rows[i].cells[j]
            cell.text = ""
            r = cell.paragraphs[0].add_run(str(val))
            font(r, size=10, bold=(i == 0))
    p(doc, "", indent=False, after=4)

def main():
    doc = Document()
    for s in doc.sections:
        s.top_margin = MARGIN
        s.bottom_margin = MARGIN
        s.left_margin = MARGIN
        s.right_margin = MARGIN

    for line in [
        "МИНИСТЕРСТВО ОБРАЗОВАНИЯ МОСКОВСКОЙ ОБЛАСТИ",
        "ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ПРОФЕССИОНАЛЬНОЕ",
        "ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ МОСКОВСКОЙ ОБЛАСТИ",
        "«СЕРПУХОВСКИЙ КОЛЛЕДЖ»",
    ]:
        p(doc, line, size=12, bold=True, center=True, indent=False, after=2)
    for _ in range(3):
        p(doc, "", indent=False)
    p(doc, "Практическая работа №6", size=16, bold=True, center=True, indent=False)
    p(doc, "по дисциплине «Инструментальные средства разработки программного обеспечения»", size=12, center=True, indent=False, after=2)
    p(doc, "по теме «Отладка отдельных модулей программного проекта»", size=14, bold=True, center=True, indent=False)
    for _ in range(4):
        p(doc, "", indent=False)
    p(doc, "студента 4 курса группы 1231", size=14, center=True, indent=False, after=2)
    p(doc, "Гончаровский В.Г.", size=14, bold=True, center=True, indent=False)
    p(doc, "", indent=False)
    p(doc, "Преподаватель:", size=14, center=True, indent=False, after=2)
    p(doc, "Шкуратова С.С.", size=14, center=True, indent=False)
    for _ in range(5):
        p(doc, "", indent=False)
    p(doc, "Серпухов, 2026", size=14, center=True, indent=False)
    doc.add_page_break()

    heading(doc, "1. Цель")
    p(doc, "Освоить поиск, локализацию и исправление ошибок в отдельном модуле проекта BookDesk с помощью breakpoint, пошагового выполнения, окна «Локальные» и стека вызовов в Visual Studio.")

    heading(doc, "2. Отлаживаемый модуль")
    p(doc, "Взял модуль BookCatalog из BookDesk.Core (каталог книг после сборки проекта). Смотрел методы TryDelete и Search. Для удобного запуска отладки добавил консольный хост BookDesk.DebugHost, который вызывает эти методы с плохими входными данными.")
    p(doc, "Структура:", indent=False)
    p(doc, "BookDesk.Core/BookCatalog.cs  - объект отладки", indent=False)
    p(doc, "BookDesk.DebugHost/Program.cs - сценарии воспроизведения", indent=False)

    heading(doc, "3. Инструменты")
    p(doc, "Visual Studio: breakpoint (F9), F5/F10, окна «Локальные» и «Стек вызовов», консольный вывод DebugHost.")

    heading(doc, "4. Найденные ошибки")
    table(doc, [
        ("№", "Элемент", "Описание", "Результат"),
        ("1", "Проблемное место", "TryDelete при selected == null", "Удалялась первая книга"),
        ("2", "Проблемное место", "Search сравнивал строки с учётом регистра", "«мышь» не находил «Мышь»"),
        ("3", "Проблемное место", "Validate без нижней границы Copies", "Copies=-1 проходил дальше"),
        ("4", "Ошибка №1", "RemoveAt(0) без выбора", "Сообщение + без удаления"),
        ("5", "Ошибка №2", "Contains без IgnoreCase", "OrdinalIgnoreCase"),
    ])

    heading(doc, "5. Подробный пример отладки")
    p(doc, "Сценарий 1: в DebugHost вызвал catalog.TryDelete(null). Поставил breakpoint на строку _items.RemoveAt(0). В «Локальных» selected = null, в стеке видно вызов из Program.Main. То есть без выбора удалялась первая запись. Исправление: если selected == null, возвращаю текст «Выберите книгу для удаления.» и список не трогаю.")
    p(doc, "Сценарий 2: Search(\"мышь\") на книге «Мышь компьютерная: справочник». Breakpoint на ветке Contains(query) без IgnoreCase: совпадений 0. Исправление: StringComparison.OrdinalIgnoreCase.")
    p(doc, "if (selected == null)", indent=False)
    p(doc, "    return \"Выберите книгу для удаления.\";", indent=False)
    p(doc, "", indent=False)
    p(doc, "b.Title.Contains(query, StringComparison.OrdinalIgnoreCase)", indent=False)

    heading(doc, "6. Скриншоты")
    fig(doc, "01_breakpoint_locals.png", "Рисунок 1 - breakpoint в TryDelete, Locals: selected = null")
    fig(doc, "03_search_breakpoint.png", "Рисунок 2 - breakpoint в Search, стек вызовов из DebugHost")
    fig(doc, "02_code_after_fix.png", "Рисунок 3 - исправленная ветка TryDelete в BookCatalog.cs")

    heading(doc, "7. Проверка после исправления")
    p(doc, "После правок: TryDelete(null) не меняет список и возвращает сообщение; Search(\"мышь\") находит книгу с заглавной буквы; соседние TryAdd/TryUpdate по-прежнему работают на корректных данных. Прогнал сценарии через DebugHost ещё раз без остановки на старых breakpoint.")

    heading(doc, "8. Вывод")
    p(doc, "В модуле BookCatalog нашлись и исправлены две реальные ошибки: удаление без выбора и поиск с учётом регистра. Методика «воспроизвести, локализовать, исправить, проверить» сработала на живом запуске в Visual Studio.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
