using System.Text.Json;
using Microsoft.Maui.Storage;

namespace SanatanGyan.Services;

public sealed class LearningProgressService
{
    private const string CompletedKey = "sanatan_completed_lessons_v1";
    private const string QuizScoresKey = "sanatan_quiz_scores_v1";
    private readonly HashSet<string> _completed;
    private readonly Dictionary<string, int> _quizScores;

    public event Action? Changed;

    public LearningProgressService()
    {
        _completed = LoadCompleted();
        _quizScores = LoadQuizScores();
    }

    public bool IsCompleted(string slug) => _completed.Contains(slug);

    public void ToggleLesson(string slug)
    {
        if (string.IsNullOrWhiteSpace(slug)) return;
        if (!_completed.Add(slug)) _completed.Remove(slug);
        SaveCompleted();
        Changed?.Invoke();
    }

    public int CompletedCount(IEnumerable<string> slugs) => slugs.Count(IsCompleted);

    public double Progress(IEnumerable<string> slugs)
    {
        var list = slugs.Where(x => !string.IsNullOrWhiteSpace(x)).Distinct(StringComparer.OrdinalIgnoreCase).ToList();
        if (list.Count == 0) return 0;
        return (double)CompletedCount(list) / list.Count;
    }

    public void SaveQuizScore(string quizId, int scorePercent)
    {
        if (string.IsNullOrWhiteSpace(quizId)) return;
        scorePercent = Math.Clamp(scorePercent, 0, 100);
        if (!_quizScores.TryGetValue(quizId, out var previous) || scorePercent > previous)
        {
            _quizScores[quizId] = scorePercent;
            SaveQuizScores();
            Changed?.Invoke();
        }
    }

    public int? BestQuizScore(string quizId) => _quizScores.TryGetValue(quizId, out var score) ? score : null;

    private static HashSet<string> LoadCompleted()
    {
        try
        {
            var json = Preferences.Default.Get(CompletedKey, "[]");
            return (JsonSerializer.Deserialize<List<string>>(json) ?? [])
                .ToHashSet(StringComparer.OrdinalIgnoreCase);
        }
        catch
        {
            return new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        }
    }

    private static Dictionary<string, int> LoadQuizScores()
    {
        try
        {
            var json = Preferences.Default.Get(QuizScoresKey, "{}");
            return new Dictionary<string, int>(JsonSerializer.Deserialize<Dictionary<string, int>>(json) ?? [], StringComparer.OrdinalIgnoreCase);
        }
        catch
        {
            return new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
        }
    }

    private void SaveCompleted() => Preferences.Default.Set(CompletedKey, JsonSerializer.Serialize(_completed.OrderBy(x => x).ToList()));
    private void SaveQuizScores() => Preferences.Default.Set(QuizScoresKey, JsonSerializer.Serialize(_quizScores));
}
