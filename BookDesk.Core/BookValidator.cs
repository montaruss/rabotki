using System.Globalization;

namespace BookDesk.Core;

public static class BookValidator
{
    public static IReadOnlyList<string> Validate(Book book, string priceText)
    {
        var errors = new List<string>();

        if (string.IsNullOrWhiteSpace(book.Title))
            errors.Add("Укажите название.");

        if (string.IsNullOrWhiteSpace(book.Genre))
            errors.Add("Укажите жанр.");

        // BUG-01 (дефектная версия): нет проверки Copies < 0
        if (DefectMode.Enabled)
        {
            if (book.Copies > 5000)
                errors.Add("Число экземпляров должно быть от 0 до 5000.");
        }
        else
        {
            if (book.Copies < 0 || book.Copies > 5000)
                errors.Add("Число экземпляров должно быть от 0 до 5000.");
        }

        // BUG-05 (дефектная): пустая цена становится 0 и проходит дальше
        var normalized = (priceText ?? string.Empty).Trim().Replace(',', '.');

        if (DefectMode.Enabled)
        {
            if (string.IsNullOrWhiteSpace(normalized))
            {
                book.Price = 0;
            }
            else if (!decimal.TryParse(normalized, NumberStyles.Number, CultureInfo.InvariantCulture, out var price))
            {
                errors.Add("Цена должна быть числом.");
            }
            else
            {
                book.Price = price;
                if (book.Price <= 0)
                    errors.Add("Цена должна быть больше нуля.");
            }
        }
        else
        {
            if (string.IsNullOrWhiteSpace(normalized) ||
                !decimal.TryParse(normalized, NumberStyles.Number, CultureInfo.InvariantCulture, out var price))
            {
                errors.Add("Цена должна быть числом.");
            }
            else
            {
                book.Price = price;
                if (book.Price <= 0)
                    errors.Add("Цена должна быть больше нуля.");
            }
        }

        return errors;
    }
}
