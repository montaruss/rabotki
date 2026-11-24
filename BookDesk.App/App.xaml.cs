using System.Windows;
using BookDesk.Core;

namespace BookDesk.App;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        DefectMode.ConfigureFromEnvironment(e.Args);
        base.OnStartup(e);
    }
}
