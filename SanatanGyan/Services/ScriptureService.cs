using System.Text.Json;
using SanatanGyan.Models;

namespace SanatanGyan.Services;

public sealed class ScriptureService
{
    private IReadOnlyList<ScriptureInfo>? _cache;
    private readonly SemaphoreSlim _gate = new(1, 1);

    public async Task<IReadOnlyList<ScriptureInfo>> GetAllAsync()
    {
        if (_cache is not null) return _cache;
        await _gate.WaitAsync();
        try
        {
            if (_cache is not null) return _cache;
            await using var stream = await FileSystem.OpenAppPackageFileAsync("sanatan_texts.json");
            var data = await JsonSerializer.DeserializeAsync<List<ScriptureInfo>>(stream, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            }) ?? [];
            _cache = data;
            return _cache;
        }
        finally
        {
            _gate.Release();
        }
    }

    public async Task<ScriptureInfo?> GetBySlugAsync(string slug) =>
        (await GetAllAsync()).FirstOrDefault(x => string.Equals(x.Slug, slug, StringComparison.OrdinalIgnoreCase));

    public async Task<IReadOnlyList<ScriptureInfo>> SearchAsync(string query)
    {
        var all = await GetAllAsync();
        if (string.IsNullOrWhiteSpace(query)) return all;
        var q = query.Trim();
        return all.Where(x =>
                x.TitleEn.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                x.TitleHi.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                x.Category.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                x.CategoryHi.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                x.KindEn.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                x.KindHi.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                x.DescriptionEn.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                x.DescriptionHi.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                x.TraditionEn.Contains(q, StringComparison.OrdinalIgnoreCase) ||
                x.TraditionHi.Contains(q, StringComparison.OrdinalIgnoreCase))
            .ToList();
    }
}
