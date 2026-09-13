namespace SanatanGyan.Services;

public static class QueryStringHelper
{
    public static string? Get(Uri uri, string key)
    {
        var query = uri.Query.TrimStart('?');
        if (string.IsNullOrWhiteSpace(query)) return null;
        foreach (var pair in query.Split('&', StringSplitOptions.RemoveEmptyEntries))
        {
            var parts = pair.Split('=', 2);
            var name = Uri.UnescapeDataString(parts[0].Replace('+', ' '));
            if (!string.Equals(name, key, StringComparison.OrdinalIgnoreCase)) continue;
            return parts.Length == 2 ? Uri.UnescapeDataString(parts[1].Replace('+', ' ')) : string.Empty;
        }
        return null;
    }
}
