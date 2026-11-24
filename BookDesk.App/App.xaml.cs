using System.Windows;
using BookDesk.Core;

namespace BookDesk.App;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        DefectMode.ConfigureFromEnvironment(e.Args);
        // Обычный запуск приложения без учебной «дефектной» ветки
        if (e.Args == null || !e.Args.Any(a => string.Equals(a, "--defect", StringComparison.OrdinalIgnoreCase)))
            DefectMode.Enabled = false;
        base.OnStartup(e);
    }
}
