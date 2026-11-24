# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

MEDIA = Path(r"C:\Users\user\AppData\Local\Cursor\AgentStores\cursor_agent_stores\bc-8b5ca42b-4d1c-4114-9c7f-ca34f8a7da2d\files\media\isrpo7")
OUT = Path(r"C:\Users\user\AppData\Local\Cursor\AgentStores\cursor_agent_stores\bc-8b5ca42b-4d1c-4114-9c7f-ca34f8a7da2d\files\docs\ISRPO_Praktika_7.docx")
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
    p(doc, "Практическая работа №7", size=16, bold=True, center=True, indent=False)
    p(doc, "по дисциплине «Инструментальные средства разработки программного обеспечения»", size=12, center=True, indent=False, after=2)
    p(doc, "по теме «Организация обработки исключений»", size=14, bold=True, center=True, indent=False)
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
    p(doc, "Организовать обработку исключительных ситуаций в проекте BookDesk: понятные сообщения пользователю и запись технической информации в лог.")

    heading(doc, "2. Потенциально опасные участки")
    table(doc, [
        ("№", "Элемент", "Описание", "Риск"),
        ("1", "Добавление книги", "Разбор цены и экземпляров", "FormatException / неверный ввод"),
        ("2", "Удаление", "Нет выбранной строки", "Логическая ошибка операции"),
        ("3", "Поиск", "Пустой/странный запрос", "Сбой фильтра"),
        ("4", "Сохранение в файл", "Запись на недоступный диск", "IOException"),
        ("5", "Старт приложения", "Загрузка каталога", "Общий Exception"),
    ])

    heading(doc, "3. Реализация обработки")
    p(doc, "Обработку повесил там, где UI может принять решение: обработчики кнопок в MainWindow и экспорт в файл. Пустой catch не использовал. Технический лог - класс AppLog (файл %LocalAppData%\\BookDesk\\bookdesk.log).")
    p(doc, "BookDesk.App/MainWindow.xaml.cs", indent=False)
    p(doc, "BookDesk.Core/AppLog.cs", indent=False)
    fig(doc, "04_trycatch_code.png", "Рисунок 1 - try/catch при сохранении каталога")

    heading(doc, "4. Ошибки и сообщения пользователю")
    table(doc, [
        ("№", "Ситуация", "Сообщение", "Результат"),
        ("1", "Удаление без выбора", "Выберите книгу для удаления.", "MessageBox + WARN в лог"),
        ("2", "Плохой путь экспорта", "Не удалось сохранить файл каталога...", "MessageBox + ERROR"),
        ("3", "Неверный ввод экземпляров", "Число экземпляров должно быть целым.", "MessageBox + WARN"),
    ])
    fig(doc, "01_user_message.png", "Рисунок 2 - сообщение при удалении без выбора")
    fig(doc, "02_io_error_message.png", "Рисунок 3 - сообщение при ошибке записи файла")

    heading(doc, "5. Логирование")
    p(doc, "AppLog пишет строки вида дата [уровень] текст. На ошибки добавляется тип исключения. Лог не валит приложение, если файл недоступен.")
    fig(doc, "03_logfile.png", "Рисунок 4 - фрагмент bookdesk.log")

    heading(doc, "6. Тестирование")
    table(doc, [
        ("№", "Действие", "Ожидание", "Факт"),
        ("1", "Удалить без выбора", "Сообщение, список целый", "OK"),
        ("2", "Сохранить на Z:\\...", "Сообщение + ERROR в лог", "OK"),
        ("3", "Добавить с буквами в «Экземпляры»", "Сообщение о целом числе", "OK"),
        ("4", "Обычное добавление", "Книга в списке, INFO в лог", "OK"),
        ("5", "Поиск", "Список фильтруется", "OK"),
    ])

    heading(doc, "7. Результат")
    p(doc, "Обработаны минимум три ситуации (удаление без выбора, ошибка записи файла, неверный ввод). Пользователь видит понятный текст, в лог уходит техническая деталь. Пустых catch нет.")

    heading(doc, "8. Вывод")
    p(doc, "В BookDesk исключения обрабатываются рядом с UI-действиями. Сообщения отделены от лога: пользователю коротко, в файл - тип и текст ошибки. Так приложение не падает на типовых сбоях ввода и записи.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
