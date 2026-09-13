using CosineKitty;
using Microsoft.Maui.Storage;
using SanatanGyan.Models;

namespace SanatanGyan.Services;

public sealed class PanchangService
{
    private const string LocationPreferenceKey = "sanatan_panchang_location";
    private const double NakshatraSpan = 360.0 / 27.0;

    private static readonly string[] VaraEn = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    private static readonly string[] VaraHi = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार"];
    private static readonly string[] TithiEn = ["Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima / Amavasya"];
    private static readonly string[] TithiHi = ["प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", "षष्ठी", "सप्तमी", "अष्टमी", "नवमी", "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा / अमावस्या"];
    private static readonly string[] NakshatraEn = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"];
    private static readonly string[] NakshatraHi = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशीर्ष", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्व फाल्गुनी", "उत्तर फाल्गुनी", "हस्त", "चित्रा", "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्व भाद्रपद", "उत्तर भाद्रपद", "रेवती"];
    private static readonly string[] YogaEn = ["Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"];
    private static readonly string[] YogaHi = ["विष्कम्भ", "प्रीति", "आयुष्मान", "सौभाग्य", "शोभन", "अतिगण्ड", "सुकर्मा", "धृति", "शूल", "गण्ड", "वृद्धि", "ध्रुव", "व्याघात", "हर्षण", "वज्र", "सिद्धि", "व्यतीपात", "वरीयान", "परिघ", "शिव", "सिद्ध", "साध्य", "शुभ", "शुक्ल", "ब्रह्म", "इन्द्र", "वैधृति"];
    private static readonly string[] MovableKaranaEn = ["Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti"];
    private static readonly string[] MovableKaranaHi = ["बव", "बालव", "कौलव", "तैतिल", "गर", "वणिज", "विष्टि"];
    private static readonly string[] MasaEn = ["Chaitra", "Vaishakha", "Jyeshtha", "Ashadha", "Shravana", "Bhadrapada", "Ashwin", "Kartika", "Margashirsha", "Pausha", "Magha", "Phalguna"];
    private static readonly string[] MasaHi = ["चैत्र", "वैशाख", "ज्येष्ठ", "आषाढ़", "श्रावण", "भाद्रपद", "आश्विन", "कार्तिक", "मार्गशीर्ष", "पौष", "माघ", "फाल्गुन"];
    private static readonly string[] RituEn = ["Vasanta", "Grishma", "Varsha", "Sharad", "Hemanta", "Shishira"];
    private static readonly string[] RituHi = ["वसंत", "ग्रीष्म", "वर्षा", "शरद", "हेमंत", "शिशिर"];

    public IReadOnlyList<PanchangLocation> Locations { get; } =
    [
        new("delhi", "New Delhi", "नई दिल्ली", 28.6139, 77.2090),
        new("mumbai", "Mumbai", "मुंबई", 19.0760, 72.8777),
        new("kolkata", "Kolkata", "कोलकाता", 22.5726, 88.3639),
        new("chennai", "Chennai", "चेन्नई", 13.0827, 80.2707),
        new("bengaluru", "Bengaluru", "बेंगलुरु", 12.9716, 77.5946),
        new("hyderabad", "Hyderabad", "हैदराबाद", 17.3850, 78.4867),
        new("ahmedabad", "Ahmedabad", "अहमदाबाद", 23.0225, 72.5714),
        new("pune", "Pune", "पुणे", 18.5204, 73.8567),
        new("jaipur", "Jaipur", "जयपुर", 26.9124, 75.7873),
        new("lucknow", "Lucknow", "लखनऊ", 26.8467, 80.9462),
        new("kanpur", "Kanpur", "कानपुर", 26.4499, 80.3319),
        new("varanasi", "Varanasi", "वाराणसी", 25.3176, 82.9739),
        new("prayagraj", "Prayagraj", "प्रयागराज", 25.4358, 81.8463),
        new("ayodhya", "Ayodhya", "अयोध्या", 26.7922, 82.1998),
        new("mathura", "Mathura", "मथुरा", 27.4924, 77.6737),
        new("haridwar", "Haridwar", "हरिद्वार", 29.9457, 78.1642),
        new("rishikesh", "Rishikesh", "ऋषिकेश", 30.0869, 78.2676),
        new("ujjain", "Ujjain", "उज्जैन", 23.1765, 75.7885),
        new("nashik", "Nashik", "नासिक", 19.9975, 73.7898),
        new("patna", "Patna", "पटना", 25.5941, 85.1376),
        new("bhopal", "Bhopal", "भोपाल", 23.2599, 77.4126),
        new("indore", "Indore", "इंदौर", 22.7196, 75.8577),
        new("chandigarh", "Chandigarh", "चंडीगढ़", 30.7333, 76.7794),
        new("amritsar", "Amritsar", "अमृतसर", 31.6340, 74.8723),
        new("jammu", "Jammu", "जम्मू", 32.7266, 74.8570),
        new("srinagar", "Srinagar", "श्रीनगर", 34.0837, 74.7973),
        new("bhubaneswar", "Bhubaneswar", "भुवनेश्वर", 20.2961, 85.8245),
        new("guwahati", "Guwahati", "गुवाहाटी", 26.1445, 91.7362),
        new("kochi", "Kochi", "कोच्चि", 9.9312, 76.2673),
        new("thiruvananthapuram", "Thiruvananthapuram", "तिरुवनंतपुरम", 8.5241, 76.9366)
    ];

    public PanchangLocation SelectedLocation
    {
        get
        {
            var id = Preferences.Default.Get(LocationPreferenceKey, "delhi");
            return Locations.FirstOrDefault(x => x.Id == id) ?? Locations[0];
        }
    }

    public void SetLocation(string id)
    {
        if (Locations.Any(x => x.Id == id)) Preferences.Default.Set(LocationPreferenceKey, id);
    }

    public Task<PanchangDay> GetTodayAsync() => CalculateAsync(GetLocalNow(SelectedLocation).Date, SelectedLocation);

    public Task<PanchangDay> CalculateAsync(DateTime localDate, PanchangLocation location) => Task.Run(() => Calculate(localDate.Date, location));

    private PanchangDay Calculate(DateTime localDate, PanchangLocation location)
    {
        try
        {
            var observer = new Observer(location.Latitude, location.Longitude, 0.0);
            var localMidnight = DateTime.SpecifyKind(localDate.Date, DateTimeKind.Unspecified);
            var startUtc = new DateTimeOffset(localMidnight, TimeSpan.FromMinutes(location.UtcOffsetMinutes)).UtcDateTime;
            var start = new AstroTime(startUtc);
            var sunriseAstro = Astronomy.SearchRiseSet(Body.Sun, observer, Direction.Rise, start, 1.5, 0.0);
            var sunsetAstro = Astronomy.SearchRiseSet(Body.Sun, observer, Direction.Set, start, 1.5, 0.0);
            if (sunriseAstro is null)
                return Unavailable(localDate, location, "Sunrise could not be calculated for this date/location.", "इस तारीख और स्थान के लिए सूर्योदय की गणना उपलब्ध नहीं हुई।");

            var sunriseUtc = AstroToUtc(sunriseAstro);
            var sunriseLocal = sunriseUtc.AddMinutes(location.UtcOffsetMinutes);
            DateTime? sunsetLocal = sunsetAstro is null ? null : AstroToUtc(sunsetAstro).AddMinutes(location.UtcOffsetMinutes);
            var atSunrise = new AstroTime(sunriseUtc);

            var elongation = Astronomy.MoonPhase(atSunrise);
            var tithiNumber = Math.Clamp((int)Math.Floor(elongation / 12.0) + 1, 1, 30);
            var inPaksha = ((tithiNumber - 1) % 15) + 1;
            var shukla = tithiNumber <= 15;
            var tithiEn = inPaksha == 15 ? (shukla ? "Purnima" : "Amavasya") : TithiEn[inPaksha - 1];
            var tithiHi = inPaksha == 15 ? (shukla ? "पूर्णिमा" : "अमावस्या") : TithiHi[inPaksha - 1];

            var sunLon = Astronomy.SunPosition(atSunrise).elon;
            var moonLon = Astronomy.EclipticGeoMoon(atSunrise).lon;
            var ayanamsa = LahiriAyanamsa(sunriseUtc);
            var sunSidereal = Normalize(sunLon - ayanamsa);
            var moonSidereal = Normalize(moonLon - ayanamsa);
            var nakIndex = Math.Clamp((int)Math.Floor(moonSidereal / NakshatraSpan), 0, 26);
            var yogaIndex = Math.Clamp((int)Math.Floor(Normalize(sunSidereal + moonSidereal) / NakshatraSpan), 0, 26);
            var karana = GetKarana(elongation);

            var month = CalculateMasa(atSunrise, sunriseUtc);
            var rituIndex = month.Index / 2;

            return new PanchangDay
            {
                LocalDate = localDate,
                Location = location,
                IsAvailable = true,
                SunriseLocal = sunriseLocal,
                SunsetLocal = sunsetLocal,
                VaraEn = VaraEn[(int)localDate.DayOfWeek],
                VaraHi = VaraHi[(int)localDate.DayOfWeek],
                TithiEn = tithiEn,
                TithiHi = tithiHi,
                PakshaEn = shukla ? "Shukla Paksha" : "Krishna Paksha",
                PakshaHi = shukla ? "शुक्ल पक्ष" : "कृष्ण पक्ष",
                NakshatraEn = NakshatraEn[nakIndex],
                NakshatraHi = NakshatraHi[nakIndex],
                YogaEn = YogaEn[yogaIndex],
                YogaHi = YogaHi[yogaIndex],
                KaranaEn = karana.En,
                KaranaHi = karana.Hi,
                MasaEn = (month.Adhika ? "Adhika " : string.Empty) + MasaEn[month.Index],
                MasaHi = (month.Adhika ? "अधिक " : string.Empty) + MasaHi[month.Index],
                RituEn = RituEn[Math.Clamp(rituIndex, 0, 5)],
                RituHi = RituHi[Math.Clamp(rituIndex, 0, 5)],
                IsAdhikaMasa = month.Adhika,
                MoonSunElongation = elongation
            };
        }
        catch (Exception ex)
        {
            return Unavailable(localDate, location, $"Panchang calculation could not be completed: {ex.Message}", "पंचांग गणना पूर्ण नहीं हो सकी। कृपया पुनः प्रयास करें।");
        }
    }

    private static (int Index, bool Adhika) CalculateMasa(AstroTime atSunrise, DateTime sunriseUtc)
    {
        var previousSearch = atSunrise.AddDays(-35.0);
        var lastNew = Astronomy.SearchMoonPhase(0.0, previousSearch, 35.1);
        var nextNew = Astronomy.SearchMoonPhase(0.0, atSunrise, 35.0);
        if (lastNew is null || nextNew is null)
        {
            var fallbackSun = Normalize(Astronomy.SunPosition(atSunrise).elon - LahiriAyanamsa(sunriseUtc));
            return (((int)Math.Floor(fallbackSun / 30.0) + 1) % 12, false);
        }

        var lastUtc = AstroToUtc(lastNew);
        var nextUtc = AstroToUtc(nextNew);
        var lastSun = Normalize(Astronomy.SunPosition(lastNew).elon - LahiriAyanamsa(lastUtc));
        var nextSun = Normalize(Astronomy.SunPosition(nextNew).elon - LahiriAyanamsa(nextUtc));
        var lastRasi = (int)Math.Floor(lastSun / 30.0);
        var nextRasi = (int)Math.Floor(nextSun / 30.0);
        var monthIndex = (lastRasi + 1) % 12;
        return (monthIndex, lastRasi == nextRasi);
    }

    private static (string En, string Hi) GetKarana(double elongation)
    {
        var halfIndex = Math.Clamp((int)Math.Floor(elongation / 6.0), 0, 59);
        if (halfIndex == 0) return ("Kimstughna", "किंस्तुघ्न");
        if (halfIndex <= 56)
        {
            var index = (halfIndex - 1) % 7;
            return (MovableKaranaEn[index], MovableKaranaHi[index]);
        }
        return halfIndex switch
        {
            57 => ("Shakuni", "शकुनि"),
            58 => ("Chatushpada", "चतुष्पाद"),
            _ => ("Naga", "नाग")
        };
    }

    // Lahiri/Chitrapaksha approximation around J2000, suitable for the daily educational Panchang display.
    private static double LahiriAyanamsa(DateTime utc)
    {
        var j2000 = new DateTime(2000, 1, 1, 12, 0, 0, DateTimeKind.Utc);
        var years = (utc.ToUniversalTime() - j2000).TotalDays / 365.2425;
        return 23.85709 + years * (50.290966 / 3600.0);
    }

    private static DateTime AstroToUtc(AstroTime time) => time.ToUtcDateTime();

    private static double Normalize(double degrees)
    {
        var value = degrees % 360.0;
        return value < 0 ? value + 360.0 : value;
    }

    private static DateTime GetLocalNow(PanchangLocation location) => DateTime.UtcNow.AddMinutes(location.UtcOffsetMinutes);

    private static PanchangDay Unavailable(DateTime date, PanchangLocation location, string en, string hi) => new()
    {
        LocalDate = date,
        Location = location,
        IsAvailable = false,
        ErrorEn = en,
        ErrorHi = hi,
        VaraEn = VaraEn[(int)date.DayOfWeek],
        VaraHi = VaraHi[(int)date.DayOfWeek]
    };
}
