using System.Globalization;
using SanatanGyan.Models;

namespace SanatanGyan.Services;

public sealed class DailySanatanService(KnowledgeService knowledge)
{
    private static readonly string[] VaraEn = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    private static readonly string[] VaraHi = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार"];

    public async Task<DailySanatanSnapshot> GetTodayAsync(DateTime? localDate = null)
    {
        var date = (localDate ?? DateTime.Now).Date;
        var all = (await knowledge.GetAllAsync()).ToList();

        return new DailySanatanSnapshot
        {
            Date = date,
            VaraEn = VaraEn[(int)date.DayOfWeek],
            VaraHi = VaraHi[(int)date.DayOfWeek],
            Knowledge = Pick(all, date, x => x.Category is "Sanatan Basics" or "Philosophy" or "Practices & Symbols"),
            Pride = Pick(all, date.AddDays(3), x => x.Category == "Garv with Proof" && IsVerified(x)),
            Fact = Pick(all, date.AddDays(7), x => x.Category == "Verified Facts" && IsVerified(x))
        };
    }

    public static string FormatDate(DateTime date, bool hindi)
    {
        if (!hindi) return date.ToString("dddd, d MMMM yyyy", CultureInfo.InvariantCulture);
        string[] months = ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"];
        string[] days = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार"];
        return $"{days[(int)date.DayOfWeek]}, {date.Day} {months[date.Month - 1]} {date.Year}";
    }

    private static bool IsVerified(KnowledgeItem item) =>
        string.Equals(item.EvidenceLevel, "Strong Evidence", StringComparison.OrdinalIgnoreCase) && item.Sources.Count > 0;

    private static KnowledgeItem? Pick(List<KnowledgeItem> all, DateTime date, Func<KnowledgeItem, bool> predicate)
    {
        var candidates = all.Where(predicate).OrderBy(x => x.Slug, StringComparer.OrdinalIgnoreCase).ToList();
        if (candidates.Count == 0) return null;
        var seed = date.Year * 1000 + date.DayOfYear;
        var index = Math.Abs(seed) % candidates.Count;
        return candidates[index];
    }
}
