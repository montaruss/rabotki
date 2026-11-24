# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

MEDIA = Path(r"C:\Users\user\AppData\Local\Cursor\AgentStores\cursor_agent_stores\bc-8b5ca42b-4d1c-4114-9c7f-ca34f8a7da2d\files\media\isrpo8")
OUT = Path(r"C:\Users\user\AppData\Local\Cursor\AgentStores\cursor_agent_stores\bc-8b5ca42b-4d1c-4114-9c7f-ca34f8a7da2d\files\docs\ISRPO_Praktika_8.docx")
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

def heading(doc, text):
    p(doc, text, size=14, bold=True, justify=False, indent=False, after=8, before=10)

def fig(doc, name, caption):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.first_line_indent = Cm(0)
    para.add_run().add_picture(str(MEDIA / name), width=Cm(14))
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
        s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = MARGIN

    for line in [
        "МИНИСТЕРСТВО ОБРАЗОВАНИЯ МОСКОВСКОЙ ОБЛАСТИ",
        "ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ПРОФЕССИОНАЛЬНОЕ",
        "ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ МОСКОВСКОЙ ОБЛАСТИ",
        "«СЕРПУХОВСКИЙ КОЛЛЕДЖ»",
    ]:
        p(doc, line, size=12, bold=True, center=True, indent=False, after=2)
    for _ in range(3):
        p(doc, "", indent=False)
    p(doc, "Практическая работа №8", size=16, bold=True, center=True, indent=False)
    p(doc, "по дисциплине «Инструментальные средства разработки программного обеспечения»", size=12, center=True, indent=False, after=2)
    p(doc, "по теме «Применение отладочных классов в проекте»", size=14, bold=True, center=True, indent=False)
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
    p(doc, "Получить навыки применения отладочных классов Debug и Trace в проекте BookDesk: диагностические сообщения, вывод значений и проверка состояния через Debug.Assert.")

    heading(doc, "2. Подготовка")
    table(doc, [
        ("Параметр", "Значение"),
        ("Проект", "BookDesk (WPF + Core + DebugHost + Tests)"),
        ("Сценарий", "Добавление книги в каталог (метод BookCatalog.TryAdd)"),
        ("Метод", "TryAdd(Book book, string priceText)"),
        ("Данные", "название «Отладка на практике», жанр «Учебник», 2 экз., цена 350"),
        ("Запуск", "BookDesk.DebugHost в режиме отладки Visual Studio"),
    ])
    p(doc, "Репозиторий: https://github.com/montaruss/rabotki", indent=False)

    heading(doc, "3. Debug.WriteLine")
    p(doc, "В TryAdd добавил несколько Debug.WriteLine в разных точках: старт метода, входные значения, отказ валидации, итог после RecalcTotal и факт добавления в список. Так по окну вывода видно, на каком шаге сценарий остановился.")
    fig(doc, "01_debug_writeline_code.png", "Рисунок 1 - Debug.WriteLine и Trace в BookCatalog.TryAdd")

    heading(doc, "4. Вывод значений")
    p(doc, "В сообщениях выводятся title, copies, priceText, Total и число книг до добавления. Этого хватает, чтобы сверить ввод с результатом расчёта.")
    table(doc, [
        ("№", "Сообщение", "Что показывает"),
        ("1", "title / copies", "входные поля книги"),
        ("2", "priceText", "строка цены до разбора"),
        ("3", "итог / count", "Total после RecalcTotal и размер списка"),
    ])

    heading(doc, "5. Debug.Assert")
    p(doc, "После RecalcTotal стоит проверка Debug.Assert(book.Total >= 0, \"Итоговая стоимость не должна быть отрицательной\"). При нормальном добавлении Total = 700, утверждение проходит.")
    fig(doc, "03_assert_code.png", "Рисунок 2 - Debug.Assert в TryAdd")

    heading(doc, "6. Проверка в режиме отладки")
    p(doc, "Запустил DebugHost через F5. В консоли отладки Visual Studio появились строки TryAdd и Trace, затем TryAdd -> OK и Search -> 1. Сценарий отработал без срабатывания Assert.")
    fig(doc, "02_output_window.png", "Рисунок 3 - консоль отладки с Debug/Trace сообщениями")
    fig(doc, "02_vs_with_output.png", "Рисунок 4 - успешный проход сценария в Visual Studio (Assert не сработал)")

    heading(doc, "7. Срабатывание Assert")
    p(doc, "Для проверки ошибочного состояния в DebugHost добавил ключ --assert-fail: после обычного TryAdd выставляю Copies = -3, пересчитываю Total и снова вызываю Debug.Assert(Total >= 0). Total становится отрицательным, среда показывает диалог Assertion Failed с текстом про итоговую стоимость.")
    fig(doc, "05_assert_fail.png", "Рисунок 5 - срабатывание Debug.Assert при Total < 0")
    p(doc, "После проверки ключ запуска убрал, корректный сценарий снова отрабатывает с кодом 0.")

    heading(doc, "8. Trace.WriteLine")
    p(doc, "Рядом с Debug добавил Trace.WriteLine($\"Trace TryAdd: priceText='{priceText}'\"). В DebugHost повесил TextWriterTraceListener на Console.Out, поэтому Trace видно в той же консоли отладки.")
    p(doc, "Отличие в моём случае: Debug удобен для сообщений только под отладчиком, Trace идёт через listeners и его проще направить в консоль/файл. Сообщение Trace на рисунке 3 помечено префиксом Trace TryAdd.")

    heading(doc, "9. Результат")
    table(doc, [
        ("Требование", "Факт"),
        ("≥ 3 Debug.WriteLine", "старт, title/copies, валидация, итог, добавление"),
        ("≥ 2 значения", "title, copies, priceText, Total, count"),
        ("≥ 1 Debug.Assert", "Total >= 0 в TryAdd"),
        ("≥ 1 Trace.WriteLine", "Trace TryAdd: priceText"),
        ("Вывод сообщений", "консоль отладки VS, рис. 3"),
        ("Сбой Assert", "диалог Assertion Failed, рис. 5"),
    ])

    heading(doc, "10. Вывод")
    p(doc, "В сценарии добавления книги BookDesk видны шаги выполнения и ключевые значения. Assert ловит отрицательный итог, Trace дублирует диагностику через listener. Для повседневной отладки этого набора достаточно.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("Wrote", OUT, "size", OUT.stat().st_size)

if __name__ == "__main__":
    main()
