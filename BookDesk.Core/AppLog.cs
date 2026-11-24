using System.Diagnostics;
using System.Text;

namespace BookDesk.Core;

/// <summary>
/// Простой файл-лог для ИСРПО Пр.7.
/// </summary>
public static class AppLog
{
    private static readonly object Gate = new();
    public static string LogPath { get; } = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
        "BookDesk", "bookdesk.log");

    public static void Info(string message) => Write("INFO", message);
    public static void Warn(string message) => Write("WARN", message);
    public static void Error(string message, Exception? ex = null)
    {
        var sb = new StringBuilder(message);
        if (ex != null)
            sb.Append(" | ").Append(ex.GetType().Name).Append(": ").Append(ex.Message);
        Write("ERROR", sb.ToString());
        if (ex != null)
            Debug.WriteLine($"[BookDesk] {ex}");
    }

    private static void Write(string level, string message)
    {
        try
        {
            var dir = Path.GetDirectoryName(LogPath);
            if (!string.IsNullOrEmpty(dir))
                Directory.CreateDirectory(dir);
            var line = $"{DateTime.Now:yyyy-MM-dd HH:mm:ss} [{level}] {message}{Environment.NewLine}";
            lock (Gate)
                File.AppendAllText(LogPath, line, Encoding.UTF8);
        }
        catch
        {
            // лог не должен валить приложение
        }
    }
}
