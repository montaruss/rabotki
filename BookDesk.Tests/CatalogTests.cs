using BookDesk.Core;
using NUnit.Framework;

namespace BookDesk.Tests;

[TestFixture]
public class CatalogTests
{
    [SetUp]
    public void SetUp()
    {
        DefectMode.ConfigureFromEnvironment();
    }

    private static BookCatalog CatalogWith(params Book[] books)
    {
        var catalog = new BookCatalog();
        foreach (var book in books)
        {
            var err = catalog.TryAdd(Clone(book), book.Price.ToString(System.Globalization.CultureInfo.InvariantCulture));
            // Seed bypass for defective cases that must enter list despite validation
            if (err != null)
            {
                // force-add for scenario setup when needed below uses SeedForce
            }
        }
        return catalog;
    }

    private static void SeedForce(BookCatalog catalog, Book book)
    {
        book.RecalcTotal();
        typeof(BookCatalog)
            .GetField("_items", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)!
            .GetValue(catalog);
        var list = (List<Book>)typeof(BookCatalog)
            .GetField("_items", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)!
            .GetValue(catalog)!;
        list.Add(book);
    }

    private static Book Clone(Book b) => new()
    {
        Title = b.Title,
        Genre = b.Genre,
        Copies = b.Copies,
        Price = b.Price
    };

    [Test]
    public void TC01_ValidBook_IsSaved_Total5000()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Тест", Genre = "Роман", Copies = 5 };
        var err = catalog.TryAdd(book, "1000");
        Assert.That(err, Is.Null);
        Assert.That(catalog.Items.Count, Is.EqualTo(1));
        Assert.That(catalog.Items[0].Total, Is.EqualTo(5000m));
    }

    [Test]
    public void TC02_EmptyTitleAndGenre_Rejected()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "", Genre = "", Copies = 1 };
        var err = catalog.TryAdd(book, "100");
        Assert.That(err, Is.Not.Null);
        Assert.That(err, Does.Contain("название").IgnoreCase);
        Assert.That(err, Does.Contain("жанр").IgnoreCase);
        Assert.That(catalog.Items.Count, Is.EqualTo(0));
    }

    [Test]
    public void TC03_NegativeCopies_Rejected()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = -1 };
        var err = catalog.TryAdd(book, "100");
        Assert.That(err, Is.Not.Null);
        Assert.That(err, Does.Contain("экземпляров").IgnoreCase);
        Assert.That(catalog.Items.Count, Is.EqualTo(0));
    }

    [Test]
    public void TC04_ZeroCopies_Allowed()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = 0 };
        var err = catalog.TryAdd(book, "100");
        Assert.That(err, Is.Null);
        Assert.That(catalog.Items[0].Copies, Is.EqualTo(0));
        Assert.That(catalog.Items[0].Total, Is.EqualTo(0m));
    }

    [Test]
    public void TC05_Copies5000_Allowed()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = 5000 };
        var err = catalog.TryAdd(book, "1");
        Assert.That(err, Is.Null);
        Assert.That(catalog.Items[0].Copies, Is.EqualTo(5000));
    }

    [Test]
    public void TC06_NegativeCopies_DoNotSpoilTotal()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = -3 };
        var err = catalog.TryAdd(book, "100");
        Assert.That(err, Is.Not.Null);
        Assert.That(catalog.Items.Count, Is.EqualTo(0));
    }

    [Test]
    public void TC07_DeleteWithoutSelection_DoesNotChangeList()
    {
        var catalog = new BookCatalog();
        catalog.SeedDemo();
        var before = catalog.Items.Count;
        var err = catalog.TryDelete(null);
        Assert.That(err, Is.Not.Null);
        Assert.That(err, Does.Contain("Выберите книгу"));
        Assert.That(catalog.Items.Count, Is.EqualTo(before));
    }

    [Test]
    public void TC08_SearchIgnoreCase_FindsMouse()
    {
        var catalog = new BookCatalog();
        catalog.SeedDemo();
        var found = catalog.Search("мышь");
        Assert.That(found.Count, Is.EqualTo(1));
        Assert.That(found[0].Title, Does.Contain("Мышь"));
    }

    [Test]
    public void TC09_EmptyPrice_IsRejected()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = 1 };
        var err = catalog.TryAdd(book, "   ");
        Assert.That(err, Is.Not.Null);
        Assert.That(err, Does.Contain("Цена").IgnoreCase);
        Assert.That(catalog.Items.Count, Is.EqualTo(0));
    }

    [Test]
    public void TC10_EditNegativeCopies_KeepsOldTotal()
    {
        var catalog = new BookCatalog();
        var existing = new Book { Title = "Книга", Genre = "Роман", Copies = 2 };
        Assert.That(catalog.TryAdd(existing, "100"), Is.Null);
        var oldTotal = catalog.Items[0].Total;

        var edited = new Book { Title = "Книга", Genre = "Роман", Copies = -5 };
        var err = catalog.TryUpdate(catalog.Items[0], edited, "100");
        Assert.That(err, Is.Not.Null);
        Assert.That(catalog.Items[0].Total, Is.EqualTo(oldTotal));
        Assert.That(catalog.Items[0].Copies, Is.EqualTo(2));
    }

    [Test]
    public void TC11_Copies5001_Rejected()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = 5001 };
        var err = catalog.TryAdd(book, "10");
        Assert.That(err, Is.Not.Null);
        Assert.That(catalog.Items.Count, Is.EqualTo(0));
    }

    [Test]
    public void TC12_PriceZero_Rejected()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = 1 };
        var err = catalog.TryAdd(book, "0");
        Assert.That(err, Is.Not.Null);
        Assert.That(err, Does.Contain("больше нуля").IgnoreCase);
    }

    [Test]
    public void TC13_DeleteSelectedOnly()
    {
        var catalog = new BookCatalog();
        catalog.SeedDemo();
        var target = catalog.Items[1];
        var title = target.Title;
        Assert.That(catalog.TryDelete(target), Is.Null);
        Assert.That(catalog.Items.Count, Is.EqualTo(2));
        Assert.That(catalog.Items.Any(b => b.Title == title), Is.False);
    }

    [Test]
    public void TC14_PartialSearch_EmptyQuery_NoMatch()
    {
        var catalog = new BookCatalog();
        catalog.SeedDemo();

        var partial = catalog.Search("Алго");
        Assert.That(partial.Count, Is.EqualTo(1));

        var empty = catalog.Search("");
        Assert.That(empty.Count, Is.EqualTo(3));

        var none = catalog.Search("zzzzzz");
        Assert.That(none.Count, Is.EqualTo(0));
    }

    [Test]
    public void TC15_NonNumericPrice_Rejected()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = 1 };
        var err = catalog.TryAdd(book, "abc");
        Assert.That(err, Is.Not.Null);
        Assert.That(err, Does.Contain("числом").IgnoreCase);
    }

    [Test]
    public void TC16_ValidEdit_RecalculatesTotal()
    {
        var catalog = new BookCatalog();
        var existing = new Book { Title = "Книга", Genre = "Роман", Copies = 2 };
        Assert.That(catalog.TryAdd(existing, "100"), Is.Null);

        var edited = new Book { Title = "Книга 2", Genre = "Учебник", Copies = 4 };
        Assert.That(catalog.TryUpdate(catalog.Items[0], edited, "250"), Is.Null);
        Assert.That(catalog.Items[0].Title, Is.EqualTo("Книга 2"));
        Assert.That(catalog.Items[0].Total, Is.EqualTo(1000m));
    }

    [Test]
    public void TC17_OneCopy_Price001()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = 1 };
        Assert.That(catalog.TryAdd(book, "0.01"), Is.Null);
        Assert.That(catalog.Items[0].Total, Is.EqualTo(0.01m));
    }

    [Test]
    public void TC18_Total_3x12000_Equals36000()
    {
        var catalog = new BookCatalog();
        var book = new Book { Title = "Книга", Genre = "Роман", Copies = 3 };
        Assert.That(catalog.TryAdd(book, "12000"), Is.Null);
        Assert.That(catalog.Items[0].Total, Is.EqualTo(36000m));
    }
}
