namespace SanatanGyan.Models;

public sealed class KnowledgeItem
{
    public string Id { get; set; } = Guid.NewGuid().ToString("N");
    public string Slug { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string TitleEn { get; set; } = string.Empty;
    public string TitleHi { get; set; } = string.Empty;
    public string Subtitle { get; set; } = string.Empty;
    public string SubtitleEn { get; set; } = string.Empty;
    public string SubtitleHi { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public string Level { get; set; } = "Beginner";
    public string Summary { get; set; } = string.Empty;
    public string SummaryEn { get; set; } = string.Empty;
    public string SummaryHi { get; set; } = string.Empty;
    public string Body { get; set; } = string.Empty;
    public string BodyEn { get; set; } = string.Empty;
    public string BodyHi { get; set; } = string.Empty;
    public string EvidenceLevel { get; set; } = string.Empty;
    public string ClaimVerdict { get; set; } = string.Empty;
    public string DateLabel { get; set; } = string.Empty;
    public string EvidenceTypeEn { get; set; } = string.Empty;
    public string EvidenceTypeHi { get; set; } = string.Empty;
    public string EvidenceScopeEn { get; set; } = string.Empty;
    public string EvidenceScopeHi { get; set; } = string.Empty;
    public bool Featured { get; set; }
    public List<string> Tags { get; set; } = [];
    public List<string> Aliases { get; set; } = [];
    public List<string> RelatedSlugs { get; set; } = [];
    public List<KnowledgeSection> Sections { get; set; } = [];
    public List<SourceReference> Sources { get; set; } = [];
}

public sealed class KnowledgeSection
{
    public string Title { get; set; } = string.Empty;
    public string TitleEn { get; set; } = string.Empty;
    public string TitleHi { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public string ContentEn { get; set; } = string.Empty;
    public string ContentHi { get; set; } = string.Empty;
}

public sealed class SourceReference
{
    public string Title { get; set; } = string.Empty;
    public string Publisher { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
    public string Note { get; set; } = string.Empty;
}
