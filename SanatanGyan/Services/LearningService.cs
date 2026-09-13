using System.Text.Json;
using SanatanGyan.Models;

namespace SanatanGyan.Services;

public sealed class LearningService
{
    private readonly SemaphoreSlim _gate = new(1, 1);
    private LearningCatalog? _catalog;

    public async Task<IReadOnlyList<LearningPathDefinition>> GetPathsAsync()
    {
        await EnsureLoadedAsync();
        return _catalog!.Paths;
    }

    public async Task<LearningPathDefinition?> GetPathAsync(string id)
    {
        await EnsureLoadedAsync();
        return _catalog!.Paths.FirstOrDefault(x => string.Equals(x.Id, id, StringComparison.OrdinalIgnoreCase));
    }

    public async Task<QuizDefinition?> GetQuizAsync(string id)
    {
        await EnsureLoadedAsync();
        return _catalog!.Quizzes.FirstOrDefault(x => string.Equals(x.Id, id, StringComparison.OrdinalIgnoreCase));
    }

    public async Task<IReadOnlyList<QuizDefinition>> GetQuizzesAsync()
    {
        await EnsureLoadedAsync();
        return _catalog!.Quizzes;
    }

    private async Task EnsureLoadedAsync()
    {
        if (_catalog is not null) return;

        await _gate.WaitAsync();
        try
        {
            if (_catalog is not null) return;

            await using var stream = await FileSystem.OpenAppPackageFileAsync("sanatan_learning.json");
            _catalog = await JsonSerializer.DeserializeAsync<LearningCatalog>(stream, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            }) ?? new LearningCatalog();
        }
        finally
        {
            _gate.Release();
        }
    }
}
