using System.Collections.ObjectModel;
using System.Windows;
using System.Windows.Controls;
using BookDesk.Core;

namespace BookDesk.App;

public partial class MainWindow : Window
{
    private readonly BookCatalog _catalog = new();
    private readonly ObservableCollection<Book> _view = new();

    public MainWindow()
    {
        InitializeComponent();
        ModeLabel.Text = DefectMode.Enabled
            ? "Режим: дефектная учебная версия (DefectMode=ON)"
            : "Режим: исправленная версия (DefectMode=OFF)";

        _catalog.SeedDemo();
        RefreshView(_catalog.Items);
        BooksGrid.ItemsSource = _view;
        SearchBox.Text = string.Empty;
        SearchBox.ToolTip = "Поиск по названию";
    }

    private void RefreshView(IReadOnlyList<Book> items)
    {
        _view.Clear();
        foreach (var book in items)
            _view.Add(book);
    }

    private void SearchButton_Click(object sender, RoutedEventArgs e)
    {
        var result = _catalog.Search(SearchBox.Text);
        RefreshView(result);
        StatusLabel.Text = $"Найдено: {result.Count}";
    }

    private void ResetButton_Click(object sender, RoutedEventArgs e)
    {
        SearchBox.Text = string.Empty;
        RefreshView(_catalog.Items);
        StatusLabel.Text = "Список сброшен.";
    }

    private void BooksGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (BooksGrid.SelectedItem is Book book)
        {
            TitleBox.Text = book.Title;
            GenreBox.Text = book.Genre;
            CopiesBox.Text = book.Copies.ToString();
            PriceBox.Text = book.Price.ToString(System.Globalization.CultureInfo.InvariantCulture);
        }
    }

    private Book ReadForm(out string? parseError)
    {
        parseError = null;
        var book = new Book
        {
            Title = TitleBox.Text.Trim(),
            Genre = GenreBox.Text.Trim()
        };

        if (!int.TryParse(CopiesBox.Text.Trim(), out var copies))
        {
            parseError = "Число экземпляров должно быть целым.";
            return book;
        }

        book.Copies = copies;
        return book;
    }

    private void AddButton_Click(object sender, RoutedEventArgs e)
    {
        var book = ReadForm(out var parseError);
        if (parseError != null)
        {
            StatusLabel.Text = parseError;
            return;
        }

        var error = _catalog.TryAdd(book, PriceBox.Text);
        if (error != null)
        {
            StatusLabel.Text = error;
            return;
        }

        ClearForm();
        RefreshView(_catalog.Items);
        StatusLabel.Text = "Добавлено.";
    }

    private void EditButton_Click(object sender, RoutedEventArgs e)
    {
        if (BooksGrid.SelectedItem is not Book selected)
        {
            StatusLabel.Text = "Выберите книгу для изменения.";
            return;
        }

        var edited = ReadForm(out var parseError);
        if (parseError != null)
        {
            StatusLabel.Text = parseError;
            return;
        }

        var error = _catalog.TryUpdate(selected, edited, PriceBox.Text);
        if (error != null)
        {
            StatusLabel.Text = error;
            return;
        }

        RefreshView(_catalog.Items);
        StatusLabel.Text = "Изменено.";
    }

    private void DeleteButton_Click(object sender, RoutedEventArgs e)
    {
        var selected = BooksGrid.SelectedItem as Book;
        var error = _catalog.TryDelete(selected);
        if (error != null)
        {
            StatusLabel.Text = error;
            return;
        }

        ClearForm();
        RefreshView(_catalog.Items);
        StatusLabel.Text = "Удалено.";
    }

    private void ClearForm()
    {
        TitleBox.Text = string.Empty;
        GenreBox.Text = string.Empty;
        CopiesBox.Text = string.Empty;
        PriceBox.Text = string.Empty;
        BooksGrid.SelectedItem = null;
    }
}
