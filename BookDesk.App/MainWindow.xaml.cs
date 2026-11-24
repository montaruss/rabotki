using System.Collections.ObjectModel;
using System.IO;
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
        try
        {
            _catalog.SeedDemo();
            RefreshView(_catalog.Items);
            BooksGrid.ItemsSource = _view;
            AppLog.Info("Приложение запущено, каталог загружен.");
        }
        catch (Exception ex)
        {
            AppLog.Error("Ошибка при старте", ex);
            MessageBox.Show("Не удалось загрузить каталог.", "BookDesk", MessageBoxButton.OK, MessageBoxImage.Error);
        }
    }

    private void RefreshView(IReadOnlyList<Book> items)
    {
        _view.Clear();
        foreach (var book in items)
            _view.Add(book);
    }

    private void ShowUserError(string text)
    {
        StatusLabel.Text = text;
        MessageBox.Show(text, "BookDesk", MessageBoxButton.OK, MessageBoxImage.Warning);
    }

    private void SearchButton_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            var result = _catalog.Search(SearchBox.Text);
            RefreshView(result);
            StatusLabel.Text = $"Найдено: {result.Count}";
            AppLog.Info($"Поиск '{SearchBox.Text}' -> {result.Count}");
        }
        catch (Exception ex)
        {
            AppLog.Error("Сбой поиска", ex);
            ShowUserError("Поиск не выполнен. Проверьте строку запроса.");
        }
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
        try
        {
            var book = ReadForm(out var parseError);
            if (parseError != null)
            {
                ShowUserError(parseError);
                AppLog.Warn($"Добавление отклонено: {parseError}");
                return;
            }

            var error = _catalog.TryAdd(book, PriceBox.Text);
            if (error != null)
            {
                ShowUserError(error);
                AppLog.Warn($"Добавление отклонено валидатором: {error}");
                return;
            }

            ClearForm();
            RefreshView(_catalog.Items);
            StatusLabel.Text = "Добавлено.";
            AppLog.Info($"Добавлена книга '{book.Title}'");
        }
        catch (Exception ex)
        {
            AppLog.Error("Сбой при добавлении", ex);
            ShowUserError("Не удалось добавить книгу.");
        }
    }

    private void EditButton_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            if (BooksGrid.SelectedItem is not Book selected)
            {
                ShowUserError("Выберите книгу для изменения.");
                return;
            }

            var edited = ReadForm(out var parseError);
            if (parseError != null)
            {
                ShowUserError(parseError);
                return;
            }

            var error = _catalog.TryUpdate(selected, edited, PriceBox.Text);
            if (error != null)
            {
                ShowUserError(error);
                return;
            }

            RefreshView(_catalog.Items);
            StatusLabel.Text = "Изменено.";
            AppLog.Info($"Изменена книга '{selected.Title}'");
        }
        catch (Exception ex)
        {
            AppLog.Error("Сбой при изменении", ex);
            ShowUserError("Не удалось изменить книгу.");
        }
    }

    private void DeleteButton_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            var selected = BooksGrid.SelectedItem as Book;
            var error = _catalog.TryDelete(selected);
            if (error != null)
            {
                ShowUserError(error);
                AppLog.Warn($"Удаление отклонено: {error}");
                return;
            }

            ClearForm();
            RefreshView(_catalog.Items);
            StatusLabel.Text = "Удалено.";
            AppLog.Info("Книга удалена");
        }
        catch (Exception ex)
        {
            AppLog.Error("Сбой при удалении", ex);
            ShowUserError("Не удалось удалить книгу.");
        }
    }

    private void ExportButton_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            // Искусственно опасный путь для проверки обработки IOException
            var path = Path.Combine("Z:\\bookdesk_no_drive", "catalog.txt");
            Directory.CreateDirectory(Path.GetDirectoryName(path)!);
            File.WriteAllLines(path, _catalog.Items.Select(b => $"{b.Title};{b.Genre};{b.Copies};{b.Price}"));
            StatusLabel.Text = "Каталог сохранён.";
            AppLog.Info($"Экспорт в {path}");
        }
        catch (IOException ex)
        {
            AppLog.Error("Ошибка записи каталога", ex);
            ShowUserError("Не удалось сохранить файл каталога. Проверьте путь и диск.");
        }
        catch (UnauthorizedAccessException ex)
        {
            AppLog.Error("Нет доступа к файлу", ex);
            ShowUserError("Нет прав на запись файла каталога.");
        }
        catch (Exception ex)
        {
            AppLog.Error("Неожиданная ошибка экспорта", ex);
            ShowUserError("Сохранение прервано из-за ошибки.");
        }
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
