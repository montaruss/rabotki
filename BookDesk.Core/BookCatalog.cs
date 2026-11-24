using System.Diagnostics;

namespace BookDesk.Core;

public class BookCatalog
{
    private readonly List<Book> _items = new();

    public IReadOnlyList<Book> Items => _items;

    public string? TryAdd(Book book, string priceText)
    {
        Debug.WriteLine("TryAdd: начало добавления книги");
        Debug.WriteLine($"TryAdd: title='{book.Title}', copies={book.Copies}");
        Trace.WriteLine($"Trace TryAdd: priceText='{priceText}'");

        var errors = BookValidator.Validate(book, priceText);
        if (errors.Count > 0)
        {
            Debug.WriteLine($"TryAdd: валидация не прошла ({errors.Count})");
            return string.Join(" ", errors);
        }

        book.RecalcTotal();
        Debug.Assert(book.Total >= 0, "Итоговая стоимость не должна быть отрицательной");
        Debug.WriteLine($"TryAdd: итог={book.Total}, книг до добавления={_items.Count}");
        _items.Add(book);
        Debug.WriteLine("TryAdd: книга добавлена");
        return null;
    }

    public string? TryUpdate(Book existing, Book edited, string priceText)
    {
        var errors = BookValidator.Validate(edited, priceText);
        if (errors.Count > 0)
            return string.Join(" ", errors);

        existing.Title = edited.Title;
        existing.Genre = edited.Genre;
        existing.Copies = edited.Copies;
        existing.Price = edited.Price;
        existing.RecalcTotal();
        return null;
    }

    /// <summary>
    /// Удаление. BUG-03: при selected == null раньше удалялась первая запись.
    /// </summary>
    public string? TryDelete(Book? selected)
    {
        if (DefectMode.Enabled)
        {
            if (selected == null)
            {
                if (_items.Count > 0)
                    _items.RemoveAt(0);
                return null;
            }

            _items.Remove(selected);
            return null;
        }

        if (selected == null)
            return "Выберите книгу для удаления.";

        _items.Remove(selected);
        return null;
    }

    /// <summary>
    /// Поиск по названию. BUG-04: раньше сравнение шло с учётом регистра.
    /// </summary>
    public IReadOnlyList<Book> Search(string? query)
    {
        if (string.IsNullOrWhiteSpace(query))
            return _items.ToList();

        if (DefectMode.Enabled)
        {
            return _items
                .Where(b => b.Title.Contains(query))
                .ToList();
        }

        return _items
            .Where(b => b.Title.Contains(query, StringComparison.OrdinalIgnoreCase))
            .ToList();
    }

    public void SeedDemo()
    {
        _items.Clear();
        AddSeed("Мастер и Маргарита", "Роман", 3, 450m);
        AddSeed("Мышь компьютерная: справочник", "Справочник", 2, 320m);
        AddSeed("Алгоритмы", "Учебник", 5, 890m);
    }

    private void AddSeed(string title, string genre, int copies, decimal price)
    {
        var book = new Book
        {
            Title = title,
            Genre = genre,
            Copies = copies,
            Price = price
        };
        book.RecalcTotal();
        _items.Add(book);
    }
}
