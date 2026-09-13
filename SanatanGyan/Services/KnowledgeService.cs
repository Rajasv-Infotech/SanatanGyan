using System.Text.Json;
using SanatanGyan.Models;

namespace SanatanGyan.Services;

public sealed class KnowledgeService
{
    private readonly SemaphoreSlim _gate = new(1, 1);
    private List<KnowledgeItem>? _items;

    public async Task<IReadOnlyList<KnowledgeItem>> GetAllAsync()
    {
        await EnsureLoadedAsync();
        return _items!;
    }

    public async Task<IReadOnlyList<KnowledgeItem>> GetByCategoryAsync(string category)
    {
        await EnsureLoadedAsync();
        return _items!
            .Where(x => string.Equals(x.Category, category, StringComparison.OrdinalIgnoreCase))
            .OrderByDescending(x => x.Featured)
            .ThenBy(x => x.Title)
            .ToList();
    }

    public async Task<KnowledgeItem?> GetBySlugAsync(string slug)
    {
        await EnsureLoadedAsync();
        return _items!.FirstOrDefault(x => string.Equals(x.Slug, slug, StringComparison.OrdinalIgnoreCase));
    }

    public async Task<IReadOnlyList<KnowledgeItem>> SearchAsync(string query)
    {
        await EnsureLoadedAsync();
        if (string.IsNullOrWhiteSpace(query)) return [];

        var terms = query
            .Trim()
            .ToLowerInvariant()
            .Split(' ', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);

        return _items!
            .Select(x => new { Item = x, Score = Score(x, terms) })
            .Where(x => x.Score > 0)
            .OrderByDescending(x => x.Score)
            .ThenBy(x => x.Item.Title)
            .Take(100)
            .Select(x => x.Item)
            .ToList();
    }

    public async Task<IReadOnlyList<KnowledgeItem>> GetRelatedAsync(KnowledgeItem item)
    {
        await EnsureLoadedAsync();

        var direct = item.RelatedSlugs
            .Select(slug => _items!.FirstOrDefault(x => string.Equals(x.Slug, slug, StringComparison.OrdinalIgnoreCase)))
            .Where(x => x is not null)
            .Cast<KnowledgeItem>()
            .DistinctBy(x => x.Id)
            .Take(6)
            .ToList();

        if (direct.Count >= 4) return direct;

        var extra = _items!
            .Where(x => !string.Equals(x.Id, item.Id, StringComparison.OrdinalIgnoreCase) &&
                        string.Equals(x.Category, item.Category, StringComparison.OrdinalIgnoreCase))
            .Where(x => x.Tags.Intersect(item.Tags, StringComparer.OrdinalIgnoreCase).Any())
            .Where(x => direct.All(d => !string.Equals(d.Id, x.Id, StringComparison.OrdinalIgnoreCase)))
            .Take(6 - direct.Count);

        direct.AddRange(extra);
        return direct;
    }

    private static int Score(KnowledgeItem item, string[] terms)
    {
        var sectionText = string.Join(" ", item.Sections.SelectMany(x => new[] { x.Title, x.TitleEn, x.TitleHi, x.Content, x.ContentEn, x.ContentHi }));
        var haystack = string.Join(" ", new[]
        {
            item.Title, item.TitleEn, item.TitleHi,
            item.Subtitle, item.SubtitleEn, item.SubtitleHi,
            item.Summary, item.SummaryEn, item.SummaryHi,
            item.Body, item.BodyEn, item.BodyHi,
            item.Category,
            item.ClaimVerdict,
            item.DateLabel,
            string.Join(" ", item.Tags),
            string.Join(" ", item.Aliases),
            sectionText
        }).ToLowerInvariant();

        var score = 0;
        foreach (var term in terms)
        {
            if (item.Title.Contains(term, StringComparison.OrdinalIgnoreCase) || item.TitleEn.Contains(term, StringComparison.OrdinalIgnoreCase) || item.TitleHi.Contains(term, StringComparison.OrdinalIgnoreCase)) score += 14;
            if (item.Aliases.Any(x => x.Contains(term, StringComparison.OrdinalIgnoreCase))) score += 11;
            if (item.Tags.Any(x => x.Contains(term, StringComparison.OrdinalIgnoreCase))) score += 8;
            if (item.Category.Contains(term, StringComparison.OrdinalIgnoreCase)) score += 4;
            if (haystack.Contains(term)) score += 2;
        }

        return score;
    }

    private async Task EnsureLoadedAsync()
    {
        if (_items is not null) return;

        await _gate.WaitAsync();
        try
        {
            if (_items is not null) return;

            await using var stream = await FileSystem.OpenAppPackageFileAsync("sanatan_content.json");
            _items = await JsonSerializer.DeserializeAsync<List<KnowledgeItem>>(stream, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            }) ?? [];

            _items = _items
                .Where(x => !string.IsNullOrWhiteSpace(x.Slug) && !string.IsNullOrWhiteSpace(x.Title))
                .GroupBy(x => x.Slug, StringComparer.OrdinalIgnoreCase)
                .Select(x => x.First())
                .ToList();
        }
        finally
        {
            _gate.Release();
        }
    }
}
