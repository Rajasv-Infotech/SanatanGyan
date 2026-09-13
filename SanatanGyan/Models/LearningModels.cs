namespace SanatanGyan.Models;

public sealed class LearningCatalog
{
    public List<LearningPathDefinition> Paths { get; set; } = [];
    public List<QuizDefinition> Quizzes { get; set; } = [];
}

public sealed class LearningPathDefinition
{
    public string Id { get; set; } = string.Empty;
    public string Icon { get; set; } = "🕉";
    public string TitleEn { get; set; } = string.Empty;
    public string TitleHi { get; set; } = string.Empty;
    public string DescriptionEn { get; set; } = string.Empty;
    public string DescriptionHi { get; set; } = string.Empty;
    public string Level { get; set; } = "Beginner";
    public string QuizId { get; set; } = string.Empty;
    public List<string> LessonSlugs { get; set; } = [];
}

public sealed class QuizDefinition
{
    public string Id { get; set; } = string.Empty;
    public string TitleEn { get; set; } = string.Empty;
    public string TitleHi { get; set; } = string.Empty;
    public string DescriptionEn { get; set; } = string.Empty;
    public string DescriptionHi { get; set; } = string.Empty;
    public List<QuizQuestion> Questions { get; set; } = [];
}

public sealed class QuizQuestion
{
    public string Id { get; set; } = string.Empty;
    public string PromptEn { get; set; } = string.Empty;
    public string PromptHi { get; set; } = string.Empty;
    public List<string> OptionsEn { get; set; } = [];
    public List<string> OptionsHi { get; set; } = [];
    public int CorrectIndex { get; set; }
    public string ExplanationEn { get; set; } = string.Empty;
    public string ExplanationHi { get; set; } = string.Empty;
    public string RelatedSlug { get; set; } = string.Empty;
}

public sealed class DailySanatanSnapshot
{
    public DateTime Date { get; init; }
    public string VaraEn { get; init; } = string.Empty;
    public string VaraHi { get; init; } = string.Empty;
    public KnowledgeItem? Knowledge { get; init; }
    public KnowledgeItem? Pride { get; init; }
    public KnowledgeItem? Fact { get; init; }
}
