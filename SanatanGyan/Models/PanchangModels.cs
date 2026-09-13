namespace SanatanGyan.Models;

public sealed record PanchangLocation(string Id, string NameEn, string NameHi, double Latitude, double Longitude, int UtcOffsetMinutes = 330);

public sealed class PanchangDay
{
    public DateTime LocalDate { get; init; }
    public PanchangLocation Location { get; init; } = new("delhi", "New Delhi", "नई दिल्ली", 28.6139, 77.2090);
    public bool IsAvailable { get; init; }
    public string ErrorEn { get; init; } = string.Empty;
    public string ErrorHi { get; init; } = string.Empty;
    public DateTime? SunriseLocal { get; init; }
    public DateTime? SunsetLocal { get; init; }
    public string VaraEn { get; init; } = string.Empty;
    public string VaraHi { get; init; } = string.Empty;
    public string TithiEn { get; init; } = string.Empty;
    public string TithiHi { get; init; } = string.Empty;
    public string PakshaEn { get; init; } = string.Empty;
    public string PakshaHi { get; init; } = string.Empty;
    public string NakshatraEn { get; init; } = string.Empty;
    public string NakshatraHi { get; init; } = string.Empty;
    public string YogaEn { get; init; } = string.Empty;
    public string YogaHi { get; init; } = string.Empty;
    public string KaranaEn { get; init; } = string.Empty;
    public string KaranaHi { get; init; } = string.Empty;
    public string MasaEn { get; init; } = string.Empty;
    public string MasaHi { get; init; } = string.Empty;
    public string RituEn { get; init; } = string.Empty;
    public string RituHi { get; init; } = string.Empty;
    public bool IsAdhikaMasa { get; init; }
    public double MoonSunElongation { get; init; }
}
