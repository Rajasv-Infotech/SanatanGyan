using Microsoft.Maui.Storage;
using System.Text.RegularExpressions;
using SanatanGyan.Models;

namespace SanatanGyan.Services;

public sealed class LanguageService
{
    private const string PreferenceKey = "sanatan_language";
    private string _language = LoadSavedLanguage();

    public event Action? Changed;
    public string Current => _language;
    public bool IsHindi => _language == "hi";

    public void SetLanguage(string language)
    {
        var normalized = string.Equals(language, "hi", StringComparison.OrdinalIgnoreCase) ? "hi" : "en";
        if (_language == normalized) return;
        _language = normalized;
        Preferences.Default.Set(PreferenceKey, _language);
        Changed?.Invoke();
    }

    public string T(string key) => Ui.TryGetValue(key, out var pair)
        ? (IsHindi ? pair.Hi : pair.En)
        : key;

    public string Category(string value) => IsHindi && CategoryHi.TryGetValue(value, out var hi) ? hi : value;
    public string Level(string value) => IsHindi && LevelHi.TryGetValue(value, out var hi) ? hi : value;
    public string Evidence(string value) => IsHindi && EvidenceHi.TryGetValue(value, out var hi) ? hi : value;
    public string Verdict(string value) => IsHindi && VerdictHi.TryGetValue(value, out var hi) ? hi : value;
    public string DateLabel(string value) => IsHindi && DateHi.TryGetValue(value, out var hi) ? hi : value;

    public string ItemTitle(KnowledgeItem item) => Pick(item.TitleEn, item.TitleHi, item.Title);
    public string ItemSubtitle(KnowledgeItem item) => Pick(item.SubtitleEn, item.SubtitleHi, item.Subtitle);
    public string ItemSummary(KnowledgeItem item) => Pick(item.SummaryEn, item.SummaryHi, item.Summary);
    public string ItemBody(KnowledgeItem item) => Pick(item.BodyEn, item.BodyHi, item.Body);
    public string SectionTitle(KnowledgeSection section) => Pick(section.TitleEn, section.TitleHi, section.Title);
    public string SectionContent(KnowledgeSection section) => Pick(section.ContentEn, section.ContentHi, section.Content);

    private string Pick(string? en, string? hi, string fallback)
    {
        if (IsHindi)
        {
            if (!string.IsNullOrWhiteSpace(hi)) return hi!;
            return OfflineTranslateToHindi(fallback);
        }

        if (!string.IsNullOrWhiteSpace(en)) return en!;
        return OfflineTranslateToEnglish(fallback);
    }

    private static string LoadSavedLanguage()
    {
        try
        {
            var saved = Preferences.Default.Get(PreferenceKey, "en");
            return saved == "hi" ? "hi" : "en";
        }
        catch
        {
            return "en";
        }
    }

    // The packaged v0.5 corpus has exact bilingual fields for every article and section.
    // These lightweight normalizers remain only as a defensive fallback for future incomplete imports.
    private static string OfflineTranslateToEnglish(string input)
    {
        if (string.IsNullOrWhiteSpace(input)) return input;
        var text = input;
        foreach (var (from, to) in HinglishToEnglishPhrases)
            text = Regex.Replace(text, $@"\b{Regex.Escape(from)}\b", to, RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);
        return Cleanup(text);
    }

    private static string OfflineTranslateToHindi(string input)
    {
        if (string.IsNullOrWhiteSpace(input)) return input;
        var text = input;
        foreach (var (from, to) in HinglishToHindiPhrases)
            text = Regex.Replace(text, $@"\b{Regex.Escape(from)}\b", to, RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);
        return Cleanup(text);
    }

    private static string Cleanup(string text)
    {
        text = Regex.Replace(text, @"\s+([,.;:!?])", "$1");
        text = Regex.Replace(text, @"\s{2,}", " ");
        return text.Trim();
    }

    private static readonly (string From, string To)[] HinglishToEnglishPhrases =
    [
        ("kya hai", "what it is"), ("ke roop mein", "as"), ("ke through", "through"),
        ("ke liye", "for"), ("ke saath", "with"), ("ke basis par", "on the basis of"),
        ("ke hisaab se", "according to"), ("se juda", "connected with"), ("se joda", "connected"),
        ("alag-alag", "different"), ("alag", "different"), ("kai", "many"), ("kuch", "some"),
        ("jisme", "in which"), ("jahan", "where"), ("lekin", "but"), ("aur", "and"),
        ("mein", "in"), ("par", "on"), ("ko", ""), ("ka", "of"), ("ki", "of"), ("ke", "of"),
        ("hai", "is"), ("hain", "are"), ("tha", "was"), ("thi", "was"), ("the", "were"),
        ("maana jata", "is regarded"), ("mana jata", "is regarded"), ("batata", "describes"),
        ("batati", "describes"), ("dikhata", "shows"), ("dikhati", "shows"), ("karta", "does"),
        ("karti", "does"), ("karte", "do"), ("rakhta", "holds"), ("rakhti", "holds"),
        ("samjha", "understood"), ("samajh", "understanding"), ("arth", "meaning"),
        ("gyan", "knowledge"), ("vigyan", "science"), ("itihas", "history"), ("darshan", "philosophy"),
        ("parampara", "tradition"), ("pramana", "evidence"), ("pramaan", "evidence"),
        ("vichar", "idea"), ("samay", "time"), ("ganana", "calculation"), ("grah", "graha"),
        ("nakshatra", "nakshatra"), ("rishi", "rishi"), ("muni", "sage")
    ];

    private static readonly (string From, string To)[] HinglishToHindiPhrases =
    [
        ("Sanatan Dharma", "सनातन धर्म"), ("Hinduism", "हिंदू धर्म"), ("Traditional", "पारंपरिक"),
        ("tradition", "परंपरा"), ("traditions", "परंपराएँ"), ("Philosophy", "दर्शन"),
        ("philosophy", "दर्शन"), ("history", "इतिहास"), ("historical", "ऐतिहासिक"),
        ("science", "विज्ञान"), ("scientific", "वैज्ञानिक"), ("research", "अनुसंधान"),
        ("evidence", "प्रमाण"), ("concept", "अवधारणा"), ("meaning", "अर्थ"),
        ("knowledge", "ज्ञान"), ("system", "प्रणाली"), ("systems", "प्रणालियाँ"),
        ("mathematics", "गणित"), ("astronomy", "खगोल विज्ञान"), ("medicine", "चिकित्सा"),
        ("surgery", "शल्य चिकित्सा"), ("grammar", "व्याकरण"), ("logic", "तर्कशास्त्र"),
        ("calendar", "पंचांग/कैलेंडर"), ("calculation", "गणना"), ("calculations", "गणनाएँ"),
        ("planet", "ग्रह"), ("planets", "ग्रह"), ("Earth", "पृथ्वी"), ("Sun", "सूर्य"),
        ("Moon", "चंद्रमा"), ("star", "तारा"), ("stars", "तारे"),
        ("different", "अलग"), ("many", "अनेक"), ("some", "कुछ"),
        ("important", "महत्वपूर्ण"), ("modern", "आधुनिक"), ("ancient", "प्राचीन"),
        ("Indian", "भारतीय"), ("India", "भारत"), ("text", "ग्रंथ"), ("texts", "ग्रंथ"),
        ("source", "स्रोत"), ("sources", "स्रोत"), ("claim", "दावा"), ("claims", "दावे"),
        ("proof", "प्रमाण"), ("supported", "समर्थित"), ("unsupported", "असमर्थित"),
        ("what it is", "क्या है"), ("kya hai", "क्या है"), ("ke roop mein", "के रूप में"),
        ("ke through", "के माध्यम से"), ("ke liye", "के लिए"), ("ke saath", "के साथ"),
        ("ke basis par", "के आधार पर"), ("ke hisaab se", "के अनुसार"),
        ("se juda", "से जुड़ा"), ("se joda", "से जोड़ा"), ("alag-alag", "अलग-अलग"),
        ("alag", "अलग"), ("kai", "कई"), ("kuch", "कुछ"), ("jisme", "जिसमें"),
        ("jahan", "जहाँ"), ("lekin", "लेकिन"), ("aur", "और"), ("mein", "में"),
        ("par", "पर"), ("ko", "को"), ("ka", "का"), ("ki", "की"), ("ke", "के"),
        ("hai", "है"), ("hain", "हैं"), ("tha", "था"), ("thi", "थी"), ("the", "थे"),
        ("maana jata", "माना जाता"), ("mana jata", "माना जाता"), ("batata", "बताता"),
        ("batati", "बताती"), ("dikhata", "दिखाता"), ("dikhati", "दिखाती"),
        ("karta", "करता"), ("karti", "करती"), ("karte", "करते"),
        ("samajh", "समझ"), ("arth", "अर्थ"), ("gyan", "ज्ञान"), ("vigyan", "विज्ञान"),
        ("itihas", "इतिहास"), ("darshan", "दर्शन"), ("parampara", "परंपरा"),
        ("pramana", "प्रमाण"), ("pramaan", "प्रमाण"), ("vichar", "विचार"),
        ("samay", "समय"), ("ganana", "गणना"), ("rishi", "ऋषि"), ("muni", "मुनि"),
        ("nakshatra", "नक्षत्र"), ("grah", "ग्रह"), ("yoga", "योग"), ("ayurveda", "आयुर्वेद"),
        ("atma", "आत्मा"), ("atman", "आत्मन्"), ("karma", "कर्म"), ("dharma", "धर्म"),
        ("moksha", "मोक्ष"), ("brahman", "ब्रह्मन्"), ("vedic", "वैदिक"), ("sanskrit", "संस्कृत")
    ];

    private static readonly Dictionary<string, (string En, string Hi)> Ui = new(StringComparer.OrdinalIgnoreCase)
    {
        ["app_tagline"] = ("Knowledge • Science • History • Philosophy", "ज्ञान • विज्ञान • इतिहास • दर्शन"),
        ["home"] = ("Home", "होम"), ["learn"] = ("Learn", "सीखें"), ["explore"] = ("Explore", "खोजें"),
        ["search"] = ("Search", "खोज"), ["saved"] = ("Saved", "सहेजे गए"),
        ["language"] = ("Language", "भाषा"), ["english"] = ("English", "अंग्रेज़ी"), ["hindi"] = ("Hindi", "हिंदी"),
        ["sanatan_knowledge"] = ("SANATAN KNOWLEDGE", "सनातन ज्ञान"),
        ["hero_description"] = ("Understand Sanatan Dharma from basics to advanced topics with tradition, philosophy, history, scientific evidence and verified sources.", "सनातन धर्म को मूल बातों से उन्नत विषयों तक परंपरा, दर्शन, इतिहास, वैज्ञानिक प्रमाण और सत्यापित स्रोतों के साथ समझें।"),
        ["search_placeholder"] = ("Karma, Atman, Yoga, Aryabhata, Sushruta...", "कर्म, आत्मा, योग, आर्यभट, सुश्रुत..."),
        ["knowledge_entries"] = ("Knowledge entries", "ज्ञान प्रविष्टियाँ"), ["knowledge_worlds"] = ("Knowledge worlds", "ज्ञान क्षेत्र"),
        ["offline_first"] = ("Offline-first", "ऑफलाइन-फर्स्ट"), ["explore_sanatan"] = ("Explore Sanatan", "सनातन को जानें"),
        ["view_all"] = ("View all", "सभी देखें"), ["garv_with_proof"] = ("Pride with Proof", "प्रमाण के साथ गर्व"),
        ["verified_heritage"] = ("Verified heritage", "सत्यापित विरासत"), ["read"] = ("Read", "पढ़ें"),
        ["science_research"] = ("Verified Science & Knowledge", "प्रमाणित विज्ञान एवं ज्ञान"), ["history_timeline"] = ("History Timeline", "इतिहास समयरेखा"),
        ["open_timeline"] = ("Open timeline", "समयरेखा खोलें"), ["claim_checker"] = ("Verified Facts", "प्रमाणित तथ्य"),
        ["check_claims"] = ("See verified facts", "प्रमाणित तथ्य देखें"),
        ["pride_note_title"] = ("Verified knowledge, presented with respect.", "सत्यापित ज्ञान, श्रद्धा और सम्मान के साथ।"),
        ["pride_note"] = ("The Facts and Pride with Proof sections contain only entries backed by clear, traceable sources.", "प्रमाणित तथ्य और प्रमाण के साथ गर्व अनुभाग में केवल स्पष्ट और जाँच योग्य स्रोतों से समर्थित प्रविष्टियाँ दिखाई जाती हैं।"),
        ["all"] = ("All", "सभी"), ["loading"] = ("Loading...", "लोड हो रहा है..."),
        ["save"] = ("Save", "सहेजें"), ["saved_done"] = ("Saved", "सहेजा गया"), ["search_related"] = ("Search related", "संबंधित खोजें"),
        ["verdict"] = ("Verdict", "निष्कर्ष"), ["scientific_note"] = ("Scientific note", "वैज्ञानिक टिप्पणी"),
        ["scientific_note_text"] = ("Evidence levels are outcome-specific. A traditional or philosophical claim is not automatically biomedical proof.", "प्रमाण का स्तर प्रत्येक परिणाम के अनुसार अलग हो सकता है। किसी पारंपरिक या दार्शनिक कथन को अपने-आप जैव-चिकित्सीय प्रमाण नहीं माना जाता।"),
        ["evidence_sources"] = ("Evidence & Sources", "प्रमाण और स्रोत"), ["open_source"] = ("Open source ↗", "स्रोत खोलें ↗"),
        ["related_knowledge"] = ("Related knowledge", "संबंधित ज्ञान"), ["search_knowledge"] = ("Search Knowledge", "ज्ञान खोजें"),
        ["search_help"] = ("You can search in Hindi, English or common Hinglish keywords.", "आप हिंदी, अंग्रेज़ी या सामान्य हिंग्लिश शब्दों में खोज सकते हैं।"),
        ["results"] = ("results", "परिणाम"), ["no_result"] = ("No exact result found", "कोई सटीक परिणाम नहीं मिला"),
        ["no_result_help"] = ("Try a shorter keyword such as atma, karma, yoga, Aryabhata, Sushruta or nakshatra.", "छोटा शब्द आज़माएँ, जैसे आत्मा, कर्म, योग, आर्यभट, सुश्रुत या नक्षत्र।"),
        ["popular_searches"] = ("Popular searches", "लोकप्रिय खोज"), ["learn_title"] = ("Learn Sanatan Dharma", "सनातन धर्म सीखें"),
        ["learn_desc"] = ("Structured learning from basics to advanced. Understand faith, philosophy, history and evidence in their proper context.", "मूल बातों से उन्नत स्तर तक क्रमबद्ध अध्ययन। आस्था, दर्शन, इतिहास और प्रमाण को उनके सही संदर्भ में समझें।"),
        ["start_here"] = ("Start here", "यहाँ से शुरू करें"), ["view_basics"] = ("View all basics", "सभी मूल विषय देखें"),
        ["lessons"] = ("lessons", "पाठ"), ["pride_page_desc"] = ("Documented Indian intellectual and cultural achievements supported by clear sources.", "स्पष्ट स्रोतों से समर्थित भारतीय बौद्धिक और सांस्कृतिक उपलब्धियाँ।"),
        ["saved_desc"] = ("Bookmarks are stored locally on this device. No login or internet is required.", "बुकमार्क इसी डिवाइस पर स्थानीय रूप से सहेजे जाते हैं। लॉगिन या इंटरनेट की आवश्यकता नहीं है।"),
        ["nothing_saved"] = ("Nothing saved yet", "अभी कुछ सहेजा नहीं गया"), ["nothing_saved_help"] = ("Open a knowledge article and tap Save.", "किसी ज्ञान लेख को खोलें और सहेजें दबाएँ।"),
        ["science_title"] = ("Verified Science & Knowledge", "प्रमाणित विज्ञान एवं ज्ञान"), ["science_desc"] = ("Only strongly sourced, documented entries are shown in this section.", "इस अनुभाग में केवल मज़बूत स्रोतों से प्रमाणित और दस्तावेज़ित प्रविष्टियाँ दिखाई जाती हैं।"),
        ["timeline_desc"] = ("Dates are labelled by certainty. Traditional chronology and academic dating are not mixed.", "तिथियों को उनकी निश्चितता के अनुसार चिन्हित किया गया है। पारंपरिक कालक्रम और अकादमिक तिथि-निर्धारण को मिलाया नहीं गया है।"),
        ["timeline_warning"] = ("Ancient texts and traditions often have debated dates; ranges should not be read as exact fixed dates.", "प्राचीन ग्रंथों और परंपराओं की तिथियाँ कई बार विवादित होती हैं; समय-सीमाओं को निश्चित तारीख न मानें।"),
        ["claim_title"] = ("Verified Facts", "प्रमाणित तथ्य"),
        ["claim_desc"] = ("A focused collection of positive, well-sourced facts from Indian knowledge, history and Sanatan traditions.", "भारतीय ज्ञान, इतिहास और सनातन परंपराओं से जुड़े सकारात्मक और मज़बूत स्रोतों वाले प्रमाणित तथ्यों का संग्रह।"),
        ["important"] = ("Important", "महत्वपूर्ण"),
        ["source_original_language_note"] = ("Source titles are kept in their official/original publication language for accurate verification.", "सत्यापन की सटीकता के लिए स्रोतों के आधिकारिक शीर्षक उनकी मूल प्रकाशन भाषा में ही दिखाए जाते हैं।"),
        ["today_sanatan"] = ("Today in Sanatan", "आज का सनातन"),
        ["today_desc"] = ("Today’s offline Sanatan dashboard with Panchang, learning and verified knowledge.", "आज का ऑफलाइन सनातन डैशबोर्ड — पंचांग, अध्ययन और प्रमाणित ज्ञान के साथ।"),
        ["today_date"] = ("Today", "आज"), ["vara"] = ("Vara / Weekday", "वार"),
        ["panchang_foundation"] = ("Today’s Panchang", "आज का पंचांग"),
        ["panchang_safe_note"] = ("Offline astronomical Panchang calculated for the selected Indian city at local sunrise.", "चुने हुए भारतीय शहर के स्थानीय सूर्योदय के आधार पर ऑफलाइन खगोलीय पंचांग गणना।"),
        ["learn_panchang"] = ("Learn the five parts of Panchang", "पंचांग के पाँच अंग समझें"),
        ["daily_knowledge"] = ("Knowledge of the Day", "आज का ज्ञान"),
        ["daily_pride"] = ("Pride with Proof Today", "आज का प्रमाण-सहित गर्व"),
        ["daily_science"] = ("Verified Fact Today", "आज का प्रमाणित तथ्य"),
        ["daily_claim"] = ("Verified Fact Today", "आज का प्रमाणित तथ्य"),
        ["open_today"] = ("Open today's dashboard", "आज का डैशबोर्ड खोलें"),
        ["verified_facts"] = ("Verified Facts", "प्रमाणित तथ्य"),
        ["verified_only"] = ("Verified only", "केवल प्रमाणित"),
        ["texts_library"] = ("Hindu Texts Library", "हिंदू ग्रंथ परिचय"),
        ["texts_desc"] = ("Explore major Vedas, Upanishads, Itihasa, Puranas, Darshanas, Agamas, Yoga, Bhakti and knowledge texts in one structured catalog.", "वेद, उपनिषद, इतिहास, पुराण, दर्शन, आगम, योग, भक्ति और ज्ञान-विज्ञान ग्रंथों का एक व्यवस्थित परिचय देखें।"),
        ["texts_search"] = ("Search a text or tradition...", "ग्रंथ या परंपरा खोजें..."),
        ["major_texts"] = ("Major texts", "प्रमुख ग्रंथ"),
        ["all_texts"] = ("All texts", "सभी ग्रंथ"),
        ["text_kind"] = ("Type", "प्रकार"),
        ["text_language"] = ("Language", "भाषा"),
        ["text_tradition"] = ("Tradition", "परंपरा"),
        ["text_attribution"] = ("Traditional attribution", "पारंपरिक संबद्धता"),
        ["text_catalog_note"] = ("This catalog introduces texts and their place in Hindu traditions; full scripture readers can be added in later releases.", "यह सूची ग्रंथों और हिंदू परंपराओं में उनके स्थान का परिचय देती है; आगे के संस्करणों में पूर्ण ग्रंथ-पाठ जोड़े जा सकते हैं।"),
        ["panchang_location"] = ("Panchang location", "पंचांग स्थान"),
        ["change_city"] = ("Select city", "शहर चुनें"),
        ["tithi"] = ("Tithi", "तिथि"),
        ["paksha"] = ("Paksha", "पक्ष"),
        ["nakshatra"] = ("Nakshatra", "नक्षत्र"),
        ["yoga"] = ("Yoga", "योग"),
        ["karana"] = ("Karana", "करण"),
        ["masa"] = ("Masa", "मास"),
        ["ritu"] = ("Ritu", "ऋतु"),
        ["sunrise"] = ("Sunrise", "सूर्योदय"),
        ["sunset"] = ("Sunset", "सूर्यास्त"),
        ["panchang_basis"] = ("Calculated offline for the selected city at local sunrise using astronomical Sun–Moon positions and Lahiri/Chitrapaksha ayanamsa.", "चुने हुए शहर के स्थानीय सूर्योदय पर सूर्य–चंद्र की खगोलीय स्थितियों और लाहिड़ी/चित्रपक्ष अयनांश के आधार पर ऑफलाइन गणना।"),
        ["panchang_refresh"] = ("Refresh Panchang", "पंचांग पुनः गणना करें"),
        ["course"] = ("Course", "पाठ्यक्रम"), ["courses"] = ("Learning Paths", "अध्ययन-पथ"),
        ["course_progress"] = ("Course progress", "पाठ्यक्रम प्रगति"), ["complete"] = ("Complete", "पूर्ण"),
        ["completed"] = ("Completed", "पूर्ण किया"), ["mark_learned"] = ("Mark learned", "सीखा हुआ चिन्हित करें"),
        ["mark_unlearned"] = ("Mark not learned", "सीखा हुआ हटाएँ"), ["continue_course"] = ("Continue course", "पाठ्यक्रम जारी रखें"),
        ["start_course"] = ("Start course", "पाठ्यक्रम शुरू करें"), ["lesson"] = ("Lesson", "पाठ"),
        ["quiz"] = ("Quiz", "क्विज़"), ["take_quiz"] = ("Take quiz", "क्विज़ दें"),
        ["best_score"] = ("Best score", "सर्वश्रेष्ठ स्कोर"), ["question"] = ("Question", "प्रश्न"),
        ["of"] = ("of", "में से"), ["check_answer"] = ("Check answer", "उत्तर जाँचें"),
        ["correct"] = ("Correct", "सही"), ["incorrect"] = ("Not quite", "अभी सही नहीं"),
        ["next_question"] = ("Next question", "अगला प्रश्न"), ["finish_quiz"] = ("Finish quiz", "क्विज़ पूरा करें"),
        ["quiz_complete"] = ("Quiz complete", "क्विज़ पूर्ण"), ["try_again"] = ("Try again", "फिर प्रयास करें"),
        ["review_topic"] = ("Review topic", "विषय दोहराएँ"), ["knowledge_graph"] = ("Knowledge Graph", "ज्ञान-जाल"),
        ["graph_desc"] = ("Explore how this topic connects to related ideas in the offline knowledge base.", "देखें कि यह विषय ऑफलाइन ज्ञान-भंडार के अन्य विचारों से कैसे जुड़ा है।"),
        ["open_graph"] = ("Explore connections", "संबंध देखें"), ["center_topic"] = ("Core topic", "मुख्य विषय"),
        ["related_nodes"] = ("Related topics", "संबंधित विषय"), ["no_connections"] = ("No explicit connections yet.", "अभी स्पष्ट संबंध उपलब्ध नहीं हैं।"),
        ["learning_progress"] = ("Learning Progress", "अध्ययन प्रगति"), ["lessons_completed"] = ("lessons completed", "पाठ पूर्ण"),
        ["visual_studio_ready"] = ("Windows + Android ready", "Windows + Android तैयार"),
        ["brand_subtitle"] = ("Knowledge • Tradition • History", "ज्ञान • परंपरा • इतिहास"),
        ["history"] = ("History", "इतिहास"), ["evidence_short"] = ("Evidence", "प्रमाण"), ["texts_library_short"] = ("Texts", "ग्रंथ"),
        ["epic_evidence"] = ("Ramayana & Mahabharata Evidence", "रामायण–महाभारत प्रमाण"),
        ["epic_evidence_title"] = ("Ramayana & Mahabharata: Evidence Explorer", "रामायण और महाभारत: प्रमाण-संदर्भ"),
        ["epic_evidence_desc"] = ("Explore verified archaeology, inscriptions, geography, manuscripts and material evidence connected with the two great Itihasa traditions.", "दो महान इतिहास-परंपराओं से जुड़े सत्यापित पुरातत्त्व, अभिलेख, भूगोल, पांडुलिपि और भौतिक प्रमाणों को एक स्थान पर समझें।"),
        ["epic_evidence_home_desc"] = ("Hastinapura, Dwarka, Ram Setu, ancient inscriptions and Ramayana-site archaeology — with source links and clear evidence labels.", "हस्तिनापुर, द्वारका, राम सेतु, प्राचीन अभिलेख और रामायण-स्थल पुरातत्त्व — स्रोत और स्पष्ट प्रमाण-लेबल के साथ।"),
        ["evidence_principle_title"] = ("Evidence stays precise", "प्रमाण को सटीक रखा गया है"),
        ["evidence_principle_desc"] = ("A verified ancient place, inscription or archaeological layer is presented as exactly that. Sacred chronology and historical-material evidence are shown together, but never silently merged into one claim.", "किसी सत्यापित प्राचीन स्थल, अभिलेख या पुरातात्त्विक परत को उतना ही कहा जाता है जितना प्रमाण स्थापित करता है। पवित्र कालक्रम और भौतिक-ऐतिहासिक प्रमाण साथ दिखते हैं, पर उन्हें चुपचाप एक ही दावा नहीं बनाया जाता।"),
        ["archaeology"] = ("Archaeology", "पुरातत्त्व"), ["archaeology_desc"] = ("Excavated layers, pottery, structures and settlement history", "उत्खनित परतें, मृद्भांड, संरचनाएँ और बसावट-इतिहास"),
        ["epigraphy"] = ("Inscriptions", "अभिलेख"), ["epigraphy_desc"] = ("Dated records carved or written in historical settings", "ऐतिहासिक संदर्भ में उत्कीर्ण या लिखित तिथि-योग्य अभिलेख"),
        ["geography"] = ("Geography", "भूगोल"), ["geography_desc"] = ("Observable landscapes, satellite imagery and mapped locations", "प्रत्यक्ष भू-दृश्य, उपग्रह चित्र और मानचित्रित स्थान"),
        ["manuscript_art"] = ("Manuscripts & art", "पांडुलिपि और कला"), ["manuscript_art_desc"] = ("Material continuity of stories, images and textual transmission", "कथा, चित्र और ग्रंथ-परंपरा की भौतिक निरंतरता"),
        ["ramayana_evidence"] = ("Ramayana-linked evidence", "रामायण से जुड़े प्रमाण"), ["mahabharata_evidence"] = ("Mahabharata & Krishna-linked evidence", "महाभारत और कृष्ण से जुड़े प्रमाण"),
        ["treta_yuga"] = ("Treta Yuga • sacred chronology", "त्रेता युग • पवित्र कालक्रम"), ["dvapara_yuga"] = ("Dvapara Yuga • sacred chronology", "द्वापर युग • पवित्र कालक्रम"),
        ["open_sacred_timeline"] = ("Open sacred timeline", "पारंपरिक कालक्रम देखें"), ["reading_note"] = ("Reading note", "पढ़ने की टिप्पणी"),
        ["epic_evidence_reading_note"] = ("The strongest claim on each card is the material or documentary fact stated there. Traditional identification and sacred meaning are preserved respectfully in their own labels.", "हर कार्ड पर सबसे मजबूत दावा वही है जो भौतिक या दस्तावेज़ी प्रमाण सीधे स्थापित करता है। पारंपरिक पहचान और पवित्र अर्थ को सम्मानपूर्वक उनके अपने लेबल में रखा गया है।"),
        ["verified"] = ("Verified", "प्रमाणित"), ["evidence_scope"] = ("What this evidence establishes", "यह प्रमाण क्या स्थापित करता है"),
        ["source_backed"] = ("Source-backed", "स्रोत-समर्थित"), ["in_this_article"] = ("In this article", "इस लेख में"),
        ["timeline_desc_v07"] = ("See sacred chronology and historically dated textual-material developments in separate, clearly labelled lanes.", "पवित्र कालक्रम और ऐतिहासिक रूप से तिथि-निर्धारित ग्रंथीय-भौतिक विकास को अलग और स्पष्ट पट्टियों में देखें।"),
        ["sacred_chronology"] = ("Sacred chronology", "पवित्र कालक्रम"), ["historical_textual_timeline"] = ("Historical & textual timeline", "ऐतिहासिक और ग्रंथीय समयरेखा"),
        ["traditional_timeline"] = ("Traditional chronology", "पारंपरिक कालक्रम"), ["academic_history"] = ("History & textual development", "इतिहास और ग्रंथीय विकास"),
        ["sacred_timeline_desc"] = ("This lane preserves the traditional sequence of Treta Yuga and Dvapara Yuga without forcing it into one disputed modern date.", "यह पट्टी त्रेता और द्वापर युग के पारंपरिक क्रम को सुरक्षित रखती है, बिना उसे किसी एक विवादित आधुनिक तारीख में बाँधे।"),
        ["historical_timeline_desc"] = ("This lane uses broad scholarly ranges or securely dated historical milestones for texts, institutions and intellectual traditions.", "यह पट्टी ग्रंथों, संस्थाओं और बौद्धिक परंपराओं के लिए व्यापक विद्वत् समय-सीमाएँ या सुरक्षित ऐतिहासिक पड़ाव दिखाती है।"),
        ["timeline_integrity_note"] = ("Different kinds of chronology answer different questions. The app therefore keeps sacred time, textual formation and archaeology distinct while allowing you to explore their connections.", "अलग प्रकार के कालक्रम अलग प्रश्नों के उत्तर देते हैं। इसलिए ऐप पवित्र समय, ग्रंथीय विकास और पुरातत्त्व को अलग रखता है, लेकिन उनके संबंधों को साथ समझने देता है।"),
        ["texts_desc_v07"] = ("A structured map of major Hindu scriptures, philosophical works, devotional literature and classical knowledge texts — now with richer explanations of what each text contains and why it matters.", "हिंदू धर्म के प्रमुख ग्रंथों, दर्शन-रचनाओं, भक्ति-साहित्य और शास्त्रीय ज्ञान-ग्रंथों का व्यवस्थित मानचित्र — अब प्रत्येक ग्रंथ में क्या है और उसका महत्व क्या है, इसकी विस्तृत जानकारी के साथ।"),
        ["catalogued_texts"] = ("catalogued texts", "सूचीबद्ध ग्रंथ"), ["text_families"] = ("text families", "ग्रंथ-परिवार"), ["major_text"] = ("Major text", "प्रमुख ग्रंथ"),
        ["start_here"] = ("Start here", "यहाँ से शुरू करें"), ["open_details"] = ("Open detailed guide", "विस्तृत परिचय खोलें"),
        ["text_catalog_note_v07"] = ("This is a guided knowledge catalog, not a substitute for the original scripture. Full chapter/verse readers can be added as the next major content phase.", "यह मार्गदर्शित ज्ञान-सूची है, मूल ग्रंथ का स्थानापन्न नहीं। अगले बड़े चरण में अध्याय/श्लोक आधारित पूर्ण पाठक जोड़ा जा सकता है।"),
        ["what_it_contains"] = ("What it contains", "इसमें क्या है"), ["text_structure"] = ("Structure & form", "रचना और स्वरूप"),
        ["why_read_this"] = ("Why it matters", "यह क्यों महत्वपूर्ण है"), ["study_note"] = ("How to study it", "इसे कैसे पढ़ें"),
        ["connect_text_with_evidence"] = ("Connect the epic text with archaeology, inscriptions and geography.", "महाकाव्य ग्रंथ को पुरातत्त्व, अभिलेख और भूगोल से जोड़कर समझें।"),
        ["open_evidence_hub"] = ("Open Evidence Explorer", "प्रमाण-संदर्भ खोलें"), ["new_in_v07"] = ("New • Evidence Explorer", "नया • प्रमाण-संदर्भ"),
        ["deep_study"] = ("Deep study", "गहन अध्ययन"), ["texts_home_desc"] = ("136 texts organised by family, type, language, themes and importance.", "136 ग्रंथ — परिवार, प्रकार, भाषा, विषय और महत्व के अनुसार व्यवस्थित।"),
        ["page_not_found"] = ("Page not found", "पृष्ठ नहीं मिला"),
        ["go_home"] = ("Go to Home", "होम पर जाएँ"),
        ["understand_sanatan_eyebrow"] = ("SANATAN UNDERSTANDING", "सनातन को समझें"),
        ["understand_sanatan_title"] = ("Questions, meanings and living philosophy", "प्रश्न, वास्तविक अर्थ और जीवित दर्शन"),
        ["understand_sanatan_desc"] = ("Respectful explanations of commonly misunderstood Hindu ideas, symbols, practices and philosophy.", "हिंदू विचारों, प्रतीकों, परंपराओं और दर्शन से जुड़े सामान्य प्रश्नों को श्रद्धा, संदर्भ और सम्मान के साथ समझें।"),
        ["understand_sanatan_note"] = ("This section explains ideas without mocking faith or treating every sampradaya as identical. Where traditions differ, the wording stays inclusive and respectful.", "यह अनुभाग आस्था का उपहास किए बिना और सभी संप्रदायों को एक जैसा माने बिना विषयों को समझाता है। जहाँ परंपराएँ भिन्न हैं, वहाँ भाषा समावेशी और सम्मानपूर्ण रखी गई है।"),
        ["understand_search"] = ("Search a question or concept...", "प्रश्न या अवधारणा खोजें..."),
        ["understand_sanatan"] = ("Understand Sanatan", "सनातन को समझें"),
        ["read_text_online"] = ("Read this text online", "यह ग्रंथ ऑनलाइन पढ़ें"),
        ["read_text_online_note"] = ("Open a public online edition or browse digitized public copies. External editions can differ in recension, translation and commentary.", "सार्वजनिक ऑनलाइन संस्करण खोलें या डिजिटाइज्ड प्रतियाँ देखें। बाहरी संस्करण शाखा, अनुवाद और टीका के अनुसार अलग हो सकते हैं।"),
        ["external_edition_note"] = ("External links open in your browser. Always note the edition, translator and publisher before quoting a passage.", "बाहरी लिंक आपके ब्राउज़र में खुलते हैं। किसी अंश को उद्धृत करने से पहले संस्करण, अनुवादक और प्रकाशक अवश्य देखें।")
    };

    private static readonly Dictionary<string, string> CategoryHi = new(StringComparer.OrdinalIgnoreCase)
    {
        ["Sanatan Basics"] = "सनातन मूल बातें", ["Philosophy"] = "दर्शन", ["Science & Research"] = "विज्ञान और अनुसंधान",
        ["History"] = "इतिहास", ["Practices & Symbols"] = "परंपराएँ और प्रतीक", ["Indian Knowledge Systems"] = "भारतीय ज्ञान परंपराएँ",
        ["Deities"] = "देव-परंपराएँ", ["Thinkers & Acharyas"] = "ऋषि, विचारक और आचार्य", ["Garv with Proof"] = "प्रमाण के साथ गर्व", ["Verified Facts"] = "प्रमाणित तथ्य",
        ["Claim Checker"] = "प्रमाणित तथ्य", ["Epic Evidence"] = "रामायण–महाभारत प्रमाण-संदर्भ", ["Sanatan Understanding"] = "सनातन को समझें"
    };

    private static readonly Dictionary<string, string> LevelHi = new(StringComparer.OrdinalIgnoreCase)
    {
        ["Beginner"] = "प्रारंभिक", ["Intermediate"] = "मध्यम", ["Advanced"] = "उन्नत"
    };

    private static readonly Dictionary<string, string> EvidenceHi = new(StringComparer.OrdinalIgnoreCase)
    {
        ["Strong Evidence"] = "प्रमाणित", ["Moderate Evidence"] = "मध्यम प्रमाण", ["Preliminary Evidence"] = "प्रारंभिक प्रमाण",
        ["Traditional / Philosophical"] = "पारंपरिक / दार्शनिक", ["Unsupported"] = "असमर्थित", ["Historical Evidence"] = "ऐतिहासिक प्रमाण"
    };

    private static readonly Dictionary<string, string> DateHi = new(StringComparer.OrdinalIgnoreCase)
    {
        ["c. 1500–500 BCE (broad scholarly range)"] = "लगभग 1500–500 ईसा पूर्व (व्यापक विद्वत् समय-सीमा)",
        ["c. 700–300 BCE"] = "लगभग 700–300 ईसा पूर्व",
        ["c. 400 BCE–400 CE (textual development)"] = "लगभग 400 ईसा पूर्व–400 ईस्वी (ग्रंथीय विकास)",
        ["c. 200 BCE–500 CE"] = "लगभग 200 ईसा पूर्व–500 ईस्वी",
        ["c. 200 BCE–800 CE"] = "लगभग 200 ईसा पूर्व–800 ईस्वी",
        ["c. 300–1000 CE"] = "लगभग 300–1000 ईस्वी",
        ["c. 600–1700 CE"] = "लगभग 600–1700 ईस्वी",
        ["c. 8th century CE"] = "लगभग 8वीं शताब्दी ईस्वी",
        ["11th–12th century CE"] = "11वीं–12वीं शताब्दी ईस्वी",
        ["13th century CE"] = "13वीं शताब्दी ईस्वी",
        ["15th–17th centuries CE"] = "15वीं–17वीं शताब्दियाँ ईस्वी",
        ["19th century CE"] = "19वीं शताब्दी ईस्वी",
        ["1893 CE"] = "1893 ईस्वी",
        ["20th century CE"] = "20वीं शताब्दी ईस्वी",
        ["20th–21st centuries CE"] = "20वीं–21वीं शताब्दियाँ ईस्वी",
        ["c. 1st millennium CE"] = "लगभग प्रथम सहस्राब्दी ईस्वी",
        ["c. 6th–9th centuries CE"] = "लगभग 6वीं–9वीं शताब्दियाँ ईस्वी",
        ["c. 7th–18th centuries CE"] = "लगभग 7वीं–18वीं शताब्दियाँ ईस्वी",
        ["Traditional sacred chronology: Treta Yuga"] = "पारंपरिक पवित्र कालक्रम: त्रेता युग",
        ["Traditional sacred chronology: end of Dvapara Yuga"] = "पारंपरिक पवित्र कालक्रम: द्वापर युग का अंतिम चरण",
        ["ASI/IIAS project, excavations from the 1970s onward"] = "ASI/IIAS परियोजना: 1970 के दशक से उत्खनन",
        ["Excavations from 1976–77 onward"] = "1976–77 से आगे उत्खनन",
        ["Modern satellite and bathymetric observations"] = "आधुनिक उपग्रह और समुद्र-तल अध्ययन",
        ["7th–8th centuries CE and later"] = "7वीं–8वीं शताब्दी ईस्वी और बाद",
        ["Medieval to modern manuscript collections"] = "मध्यकाल से आधुनिक काल की पांडुलिपि-संग्रह परंपरा",
        ["ASI excavations 1950–52"] = "ASI उत्खनन 1950–52",
        ["Excavations 1954 onward; renewed 2013–14, 2017–18, 2023"] = "1954 से उत्खनन; 2013–14, 2017–18 और 2023 में नए चरण",
        ["NIO underwater explorations since the 1980s"] = "1980 के दशक से NIO का समुद्री पुरातत्त्व",
        ["2nd century BCE"] = "दूसरी शताब्दी ईसा पूर्व",
        ["Late centuries BCE"] = "ईसा पूर्व की अंतिम शताब्दियाँ",
        ["Iron Age, broadly first millennium BCE"] = "लौह युग, व्यापक रूप से प्रथम सहस्राब्दी ईसा पूर्व"
    };

    private static readonly Dictionary<string, string> VerdictHi = new(StringComparer.OrdinalIgnoreCase)
    {
        ["Supported"] = "समर्थित", ["Mostly Supported"] = "अधिकांशतः समर्थित", ["Partially Supported"] = "आंशिक रूप से समर्थित",
        ["Uncertain"] = "अनिश्चित", ["Traditional / Faith Claim"] = "पारंपरिक / आस्था-आधारित कथन", ["Unsupported"] = "असमर्थित",
        ["False / Misleading"] = "गलत / भ्रामक"
    };
}
