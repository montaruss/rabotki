namespace BookDesk.Core;

/// <summary>
/// Переключатель учебной дефектной версии.
/// Включено по умолчанию. Выключается переменной BOOKDESK_FIXED=1 или аргументом --fixed.
/// </summary>
public static class DefectMode
{
    public static bool Enabled { get; set; } = true;

    public static void ConfigureFromEnvironment(string[]? args = null)
    {
        // Флаг-файл рядом с решением: удобно переключать режим для Test Explorer
        var flagPaths = new[]
        {
            Path.Combine(AppContext.BaseDirectory, "BOOKDESK_FIXED.flag"),
            Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "BOOKDESK_FIXED.flag"),
            @"C:\Users\user\BookDesk\BOOKDESK_FIXED.flag"
        };
        if (flagPaths.Any(File.Exists))
        {
            Enabled = false;
            return;
        }

        var env = Environment.GetEnvironmentVariable("BOOKDESK_FIXED");
        if (string.Equals(env, "1", StringComparison.OrdinalIgnoreCase) ||
            string.Equals(env, "true", StringComparison.OrdinalIgnoreCase))
        {
            Enabled = false;
            return;
        }

        if (args != null && args.Any(a => string.Equals(a, "--fixed", StringComparison.OrdinalIgnoreCase)))
        {
            Enabled = false;
            return;
        }

        Enabled = true;
    }
}
