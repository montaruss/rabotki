using System.Diagnostics;
using System.Runtime.InteropServices;
using BookDesk.Core;

DefectMode.Enabled = false;

Trace.Listeners.Clear();
Trace.Listeners.Add(new TextWriterTraceListener(Console.Out));
Trace.AutoFlush = true;

var failAssert = args.Any(a => a == "--assert-fail");
if (failAssert)
    Trace.Listeners.Add(new AssertMessageListener());

var catalog = new BookCatalog();
catalog.SeedDemo();
Console.WriteLine($"Книг в каталоге: {catalog.Items.Count}");

var book = new Book { Title = "Отладка на практике", Genre = "Учебник", Copies = 2 };
var err = catalog.TryAdd(book, "350");
Console.WriteLine($"TryAdd -> {(err ?? "OK")}, total={book.Total}");

var found = catalog.Search("отладка");
Console.WriteLine($"Search -> {found.Count}");

if (failAssert)
{
    book.Copies = -3;
    book.RecalcTotal();
    Debug.WriteLine($"assert-fail demo: total={book.Total}");
    Debug.Assert(book.Total >= 0, "Итоговая стоимость не должна быть отрицательной");
}

Console.WriteLine("готово");

if (args.Any(a => a == "--pause"))
{
    Console.WriteLine("Нажмите Enter для выхода...");
    try { Console.ReadLine(); } catch { /* нет консоли */ }
}

internal sealed class AssertMessageListener : TraceListener
{
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int MessageBox(IntPtr hWnd, string text, string caption, uint type);

    public override void Write(string? message) { }

    public override void WriteLine(string? message) { }

    public override void Fail(string? message, string? detailMessage)
    {
        var body = string.IsNullOrWhiteSpace(detailMessage)
            ? (message ?? "Assertion Failed")
            : $"{message}\n\n{detailMessage}";
        MessageBox(
            IntPtr.Zero,
            body,
            "Assertion Failed",
            0x00000010u); // MB_ICONHAND
    }
}
