using System.Text.Json;

namespace SanatanGyan.Services;

public sealed class BookmarkService
{
    private const string Key = "sanatan.bookmarks.v1";

    public IReadOnlyCollection<string> GetAll()
    {
        var json = Preferences.Default.Get(Key, "[]");
        try { return JsonSerializer.Deserialize<HashSet<string>>(json) ?? []; }
        catch { return []; }
    }

    public bool IsSaved(string id) => GetAll().Contains(id);

    public void Toggle(string id)
    {
        var set = new HashSet<string>(GetAll(), StringComparer.OrdinalIgnoreCase);
        if (!set.Add(id)) set.Remove(id);
        Preferences.Default.Set(Key, JsonSerializer.Serialize(set));
    }
}
