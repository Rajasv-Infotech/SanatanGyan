from __future__ import annotations
import json, pathlib, hashlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / 'SanatanGyan' / 'Resources' / 'Raw'
CONTENT = RAW / 'sanatan_content.json'
TEXTS = RAW / 'sanatan_texts.json'

# ---------- helpers ----------
def stable_variant(slug: str, n: int) -> int:
    return int(hashlib.sha256(slug.encode('utf-8')).hexdigest()[:8], 16) % n

def clean_hi(s: str) -> str:
    s = (s or '').strip()
    replacements = {
        'TKDL': 'टीकेडीएल',
        'Painted Grey Ware': 'चित्रित धूसर मृद्भांड संस्कृति',
        'NBPW': 'उत्तरी कृष्ण मार्जित मृद्भांड',
        'religion': 'रिलिजन',
        'Rigveda': 'ऋग्वेद',
        'Yajurveda': 'यजुर्वेद',
        'Samaveda': 'सामवेद',
        'Atharvaveda': 'अथर्ववेद',
        'Internet Archive': 'इंटरनेट आर्काइव',
        'UNESCO': 'यूनेस्को',
        'NASA': 'नासा',
        'ISRO': 'इसरो',
        'ASI': 'भारतीय पुरातत्व सर्वेक्षण',
        'CSIR': 'सीएसआईआर',
        'PGW': 'चित्रित धूसर मृद्भांड',
        'DNA': 'डीएनए',
        'PDF': 'पीडीएफ',
    }
    for a, b in replacements.items():
        s = s.replace(a, b)
    s = s.replace(' .', '।').replace('.', '।')
    s = re.sub(r'\s+([,;:!?])', r'\1', s)
    s = re.sub(r'\s{2,}', ' ', s).strip()
    return s

def clean_en(s: str) -> str:
    return re.sub(r'\s{2,}', ' ', (s or '').strip())

def join_names(names, hi=True):
    names = [n for n in names if n]
    if not names:
        return ''
    sep = ' • '
    return sep.join(names[:4])

CATEGORY_CONTEXT_HI = {
    'Sanatan Basics': 'सनातन परंपरा की मूल अवधारणाओं, जीवन-दृष्टि और साधना-पथों',
    'Philosophy': 'भारतीय दर्शन की प्रश्नपरक, तर्कप्रधान और साधना-संबंधी परंपराओं',
    'Practices & Symbols': 'जीवित आचार, प्रतीक, भक्ति और सांस्कृतिक व्यवहार',
    'Deities': 'भक्ति, दर्शन, पुराण-कथाओं और विविध संप्रदायों',
    'Thinkers & Acharyas': 'ग्रंथ, वाद-विवाद, शिक्षण-परंपरा और बौद्धिक विरासत',
    'History': 'ग्रंथीय विकास, सामाजिक-सांस्कृतिक परिवर्तन और उपलब्ध ऐतिहासिक स्रोत',
    'Indian Knowledge Systems': 'भारतीय ज्ञान-विज्ञान, गणना, भाषा, चिकित्सा, कला और शास्त्रीय अध्ययन',
    'Garv with Proof': 'दस्तावेजीकृत भारतीय उपलब्धियों और सत्यापित स्रोतों',
    'Verified Facts': 'प्रत्यक्ष स्रोत, आधिकारिक अभिलेख और जाँच योग्य प्रमाण',
    'Epic Evidence': 'पुरातत्त्व, अभिलेख, भूगोल, पांडुलिपि और महाकाव्य-परंपरा',
    'Sanatan Understanding': 'सनातन दर्शन, भाषा, प्रतीक और जीवित परंपराओं की सम्मानपूर्ण समझ',
}
CATEGORY_CONTEXT_EN = {
    'Sanatan Basics': 'the foundational ideas, ways of life and spiritual paths within Sanatan traditions',
    'Philosophy': 'the questioning, reasoning and contemplative traditions of Indian philosophy',
    'Practices & Symbols': 'living practice, symbolism, devotion and cultural expression',
    'Deities': 'devotion, philosophy, sacred narratives and diverse sampradayas',
    'Thinkers & Acharyas': 'texts, debate, teaching lineages and intellectual legacy',
    'History': 'textual development, cultural change and available historical evidence',
    'Indian Knowledge Systems': 'Indian traditions of mathematics, language, medicine, astronomy, arts and systematic learning',
    'Garv with Proof': 'documented Indian achievements and verifiable sources',
    'Verified Facts': 'primary evidence, official records and checkable sources',
    'Epic Evidence': 'archaeology, inscriptions, geography, manuscripts and epic traditions',
    'Sanatan Understanding': 'a respectful understanding of Sanatan philosophy, language, symbolism and living traditions',
}

HEADINGS = {
    'Sanatan Basics': [('अवधारणा को गहराई से समझें','Understanding the idea in depth'),('परंपरा में इसका स्थान','Place in the tradition'),('जीवन-दृष्टि से संबंध','Connection with lived philosophy')],
    'Philosophy': [('मुख्य दार्शनिक प्रश्न','The central philosophical question'),('तर्क और साधना का संबंध','Reasoning and practice'),('अन्य दर्शनों से संवाद','Dialogue with other schools')],
    'Practices & Symbols': [('परंपरागत अर्थ','Traditional meaning'),('आचार और प्रतीक का संबंध','Practice and symbolism'),('विविध परंपराओं में रूप','Variation across traditions')],
    'Deities': [('परंपरा में स्वरूप','Form within the tradition'),('दार्शनिक और प्रतीकात्मक अर्थ','Philosophical and symbolic meaning'),('भक्ति और ग्रंथ-परंपरा','Devotion and textual tradition')],
    'Thinkers & Acharyas': [('बौद्धिक योगदान','Intellectual contribution'),('ग्रंथ और शिक्षण-परंपरा','Texts and teaching lineage'),('दीर्घकालिक प्रभाव','Long-term influence')],
    'History': [('ऐतिहासिक संदर्भ','Historical context'),('स्रोतों को कैसे पढ़ें','How to read the evidence'),('इस चरण का महत्व','Why this phase matters')],
    'Indian Knowledge Systems': [('ज्ञान-क्षेत्र का परिचय','Knowledge field'),('पद्धति और योगदान','Method and contribution'),('आज के अध्ययन में महत्व','Why it still matters')],
    'Garv with Proof': [('दस्तावेजीकृत उपलब्धि','The documented achievement'),('प्रमाण का आधार','Evidence base'),('यह क्यों महत्वपूर्ण है','Why it matters')],
    'Verified Facts': [('क्या प्रमाणित है','What is verified'),('प्रमाण कहाँ से आता है','Where the evidence comes from'),('सटीक निष्कर्ष','Precise conclusion')],
    'Epic Evidence': [('भौतिक या दस्तावेजी प्रमाण','Material or documentary evidence'),('महाकाव्य-परंपरा से संबंध','Connection with epic tradition'),('प्रमाण की सीमा और महत्व','Scope and significance of the evidence')],
    'Sanatan Understanding': [('वास्तविक अर्थ','Meaning in context'),('परंपरा को सम्मानपूर्वक समझें','A respectful reading'),('सरल निष्कर्ष','Clear takeaway')],
}

BODY_HI = [
    '{title} को केवल एक परिभाषा या एक पंक्ति में समेटना पर्याप्त नहीं है। इसे {context} के व्यापक संदर्भ में पढ़ने पर विषय का अर्थ अधिक स्पष्ट होता है। इस पृष्ठ में मूल विचार, उसका स्थान और उससे जुड़े प्रमुख विषय क्रमबद्ध रूप से रखे गए हैं, ताकि पाठक परिचय से आगे बढ़कर एक संतुलित समझ बना सके।',
    '{title} का महत्व उसके नाम या लोकप्रिय परिचय से कहीं अधिक व्यापक है। {context} के साथ इसे जोड़कर देखने से यह समझ आता है कि यह विषय विचार, आचार और ऐतिहासिक परंपरा में किस प्रकार स्थान पाता है। आगे के खंड उसी व्यापक संदर्भ को सरल लेकिन पर्याप्त विस्तार से समझाते हैं।',
    '{title} को समझने का अच्छा तरीका है कि पहले उसके मूल अर्थ को पहचाना जाए और फिर उसे {context} से जोड़ा जाए। ऐसा करने पर विषय अलग-थलग जानकारी न रहकर सनातन ज्ञान-परंपरा के बड़े चित्र का हिस्सा बन जाता है। यह पृष्ठ उसी संबंध को स्पष्ट, सम्मानपूर्ण और क्रमबद्ध रूप में प्रस्तुत करता है।',
]
BODY_EN = [
    '{title} cannot be understood fully through a one-line definition. It becomes clearer when placed within {context}. This page therefore moves from the basic idea to its wider setting and related themes, so the reader can build a connected understanding rather than remember an isolated fact.',
    'The significance of {title} is broader than its short popular description. Reading it alongside {context} shows how the topic fits into thought, practice and historical tradition. The sections below expand that setting in a clear, structured way without reducing a diverse tradition to a single formula.',
    'A useful way to study {title} is to begin with its core meaning and then connect it with {context}. That turns the topic from a standalone fact into part of a larger intellectual and cultural landscape. This page follows that approach with a concise but substantial explanation.',
]

# Specific richer wording for high-visibility/source-backed pages.
CURATED = {
    'traditional-knowledge-digital-library': {
        'bodyHi': 'पारंपरिक ज्ञान डिजिटल पुस्तकालय भारत की एक महत्वपूर्ण बौद्धिक-संपदा पहल है। इसका उद्देश्य आयुर्वेद, सिद्ध, यूनानी और योग जैसी परंपराओं में पहले से उपलब्ध ज्ञान को ऐसे व्यवस्थित और खोजयोग्य रूप में प्रस्तुत करना है, जिसे पेटेंट परीक्षक पूर्व-विद्यमान ज्ञान की जाँच के समय उपयोग कर सकें। इससे पारंपरिक ज्ञान को आधुनिक पेटेंट व्यवस्था की भाषा में पहचाने जाने योग्य बनाया गया।',
        'bodyEn': 'The Traditional Knowledge Digital Library is an Indian initiative for protecting documented traditional knowledge within the modern patent system. It organizes knowledge from traditions such as Ayurveda, Siddha, Unani and Yoga into searchable forms that patent examiners can consult while checking prior art. Its importance lies in making already-known knowledge visible within formal patent examination.',
        'sections': [
            ('दस्तावेजीकरण की आवश्यकता','Why documentation matters','बहुत-सा पारंपरिक ज्ञान पुराने ग्रंथों और भारतीय भाषाओं में उपलब्ध था, लेकिन अंतरराष्ट्रीय पेटेंट-जाँच में उसे ढूँढना कठिन हो सकता था। टीकेडीएल ने इस ज्ञान को वर्गीकृत, अनुवादित और खोजयोग्य रूप में व्यवस्थित करने की दिशा में काम किया, ताकि पहले से ज्ञात विधियों पर नएपन का अनुचित दावा न किया जा सके।','A large body of traditional knowledge existed in classical texts and Indian languages, but it was not always easy for international patent examiners to search. TKDL was created to classify, translate and organize such material so that existing knowledge can be recognized during novelty and prior-art examination.'),
            ('पेटेंट व्यवस्था में भूमिका','Role in patent examination','टीकेडीएल का उद्देश्य किसी परंपरा को “पेटेंट कराना” नहीं, बल्कि पहले से उपलब्ध ज्ञान को पूर्व-ज्ञान के रूप में सामने लाना है। इस प्रकार यह पारंपरिक ज्ञान की रक्षा और गलत या अनुचित पेटेंट दावों को चुनौती देने में सहायक आधार प्रदान करता है।','TKDL is not a system for patenting a tradition. Its role is to make already-existing knowledge visible as prior art. In that way it supports the protection of traditional knowledge and can help patent offices identify or challenge claims that are not genuinely novel.'),
            ('भारत की ज्ञान-विरासत के लिए महत्व','Why it matters for Indian knowledge heritage','यह पहल दिखाती है कि प्राचीन और पारंपरिक ज्ञान की रक्षा केवल भावनात्मक स्मृति से नहीं, बल्कि व्यवस्थित दस्तावेजीकरण, वर्गीकरण और संस्थागत कार्य से भी होती है। इसलिए टीकेडीएल आधुनिक बौद्धिक-संपदा व्यवस्था और भारतीय ज्ञान-परंपरा के बीच एक व्यावहारिक सेतु है।','The initiative shows that preserving traditional knowledge requires more than cultural memory; it also benefits from systematic documentation, classification and institutional work. TKDL therefore acts as a practical bridge between Indian knowledge traditions and the modern intellectual-property system.')
        ]
    },
    'dharma-not-only-religion': {
        'titleHi': 'धर्म का अर्थ केवल “रिलिजन” नहीं है',
        'bodyHi': '“धर्म” भारतीय भाषाओं और दर्शन-परंपराओं का बहुत व्यापक शब्द है। किसी संदर्भ में यह कर्तव्य का अर्थ देता है, किसी में सदाचार, व्यवस्था, विधि, शिक्षा, आचार या किसी वस्तु के स्वभाव का। इसलिए धर्म को केवल आधुनिक अंग्रेज़ी शब्द “रिलिजन” के बराबर रख देने से उसके अनेक अर्थ छूट जाते हैं।',
        'bodyEn': 'Dharma is a much broader term than the modern English word “religion.” Depending on context it can refer to duty, ethical conduct, sustaining order, law, teaching, right action or the characteristic nature of something. Its meaning therefore has to be read from the specific text, school and situation in which it appears.',
    },
    'aryabhata-earth-rotation': {
        'bodyHi': 'आर्यभट की खगोलीय दृष्टि भारतीय गणितीय खगोल विज्ञान की परिपक्वता का महत्वपूर्ण उदाहरण है। आर्यभटीय में चलती नाव की उपमा के माध्यम से यह समझाया गया है कि देखने वाले की अपनी गति के कारण स्थिर वस्तुएँ विपरीत दिशा में चलती हुई प्रतीत हो सकती हैं। इसी संदर्भ को विद्वान पृथ्वी के अक्षीय घूर्णन की व्याख्या से जोड़ते हैं।',
        'bodyEn': 'Aryabhata’s astronomy is an important example of the maturity of classical Indian mathematical astronomy. In the Aryabhatiya, the analogy of a person in a moving boat is used to explain how stationary objects can appear to move in the opposite direction because of the observer’s own motion. Scholars connect this passage with Aryabhata’s treatment of Earth’s axial rotation.',
    },
    'sushruta-samhita-surgery': {
        'bodyHi': 'सुश्रुत संहिता भारतीय चिकित्सा इतिहास में शल्य-चिकित्सा से जुड़े सबसे महत्वपूर्ण ग्रंथों में गिनी जाती है। इसमें शल्य-उपकरण, घाव, अस्थिभंग, शरीररचना, प्रशिक्षण और विभिन्न प्रक्रियाओं पर व्यवस्थित चर्चा मिलती है। इसका अध्ययन यह समझने में मदद करता है कि प्राचीन भारतीय चिकित्सा-परंपरा में निरीक्षण, अभ्यास और शल्य-कौशल को किस प्रकार महत्व दिया गया।',
        'bodyEn': 'The Sushruta Samhita is one of the most important texts for the history of surgery in the Indian medical tradition. It discusses instruments, wounds, fractures, anatomy, training and a range of surgical procedures in a systematic manner. Studying it helps show how observation, practice and surgical skill were treated within classical Indian medicine.',
    },
}

GENERIC_TITLES = {
    'Context in the tradition','Connected topics','Understanding the idea','Respectful reading note','Knowledge focus',
    'Historical lens','Place in the wider framework','Practice and meaning','How to study this philosophy',
    'Intellectual legacy','Knowledge tradition in context','Living practice','Place in Hindu traditions',
    'Questions to compare','How to study the legacy','Why it matters','Many layers of meaning','Evidence-based reading'
}

def make_sections(item, lookup):
    cat = item['category']
    hi_title = clean_hi(item.get('titleHi') or item.get('title') or '')
    en_title = clean_en(item.get('titleEn') or item.get('title') or '')
    related = [lookup[s] for s in item.get('relatedSlugs', []) if s in lookup]
    rel_hi = join_names([r.get('titleHi') or r.get('title') for r in related], True)
    rel_en = join_names([r.get('titleEn') or r.get('title') for r in related], False)
    sources = item.get('sources', [])
    publishers = []
    for s in sources:
        p = s.get('publisher','').strip()
        if p and p not in publishers: publishers.append(p)
    pubs_en = ', '.join(publishers[:3])

    # Preserve genuinely specific sections.
    specific=[]
    for s in item.get('sections',[]):
        t = s.get('titleEn') or s.get('title') or ''
        c_hi = clean_hi(s.get('contentHi') or '')
        c_en = clean_en(s.get('contentEn') or s.get('content') or '')
        if t not in GENERIC_TITLES and len(c_hi) >= 90 and len(c_en) >= 90:
            ss=dict(s)
            ss['titleHi']=clean_hi(ss.get('titleHi') or '')
            ss['contentHi']=c_hi
            ss['titleEn']=clean_en(ss.get('titleEn') or t)
            ss['contentEn']=c_en
            ss['title']=ss['titleEn']; ss['content']=ss['contentEn']
            specific.append(ss)
    # Source-backed/evidence pages benefit from their specific sections first.
    if cat in ('Garv with Proof','Verified Facts','Epic Evidence') and specific:
        kept=specific[:2]
    else:
        kept=specific[:1]

    headings = HEADINGS[cat]
    v=stable_variant(item['slug'],3)
    context_hi=CATEGORY_CONTEXT_HI[cat]
    context_en=CATEGORY_CONTEXT_EN[cat]

    generated=[]
    # 1
    h1hi,h1en=headings[0]
    if cat in ('Verified Facts','Garv with Proof'):
        c1hi=f'“{hi_title}” से जुड़ी जानकारी को इस पृष्ठ में केवल उसी सीमा तक प्रमाणित माना गया है जितना उपलब्ध स्रोत सीधे स्थापित करते हैं। इससे उपलब्धि का महत्व कम नहीं होता; बल्कि तथ्य अधिक विश्वसनीय और उद्धरण योग्य बनता है।'
        c1en=f'The statement about “{en_title}” is treated as verified only to the extent directly supported by the cited evidence. This does not diminish the achievement; it makes the claim more reliable, precise and suitable for responsible citation.'
    elif cat=='Epic Evidence':
        c1hi=f'“{hi_title}” से संबंधित सामग्री को महाकाव्य-परंपरा के सम्मान के साथ, भौतिक और दस्तावेजी प्रमाणों से अलग-अलग पहचानते हुए प्रस्तुत किया गया है। पुरातात्त्विक स्थल, अभिलेख या भूगोल जो स्थापित करता है, उसे उसी सीमा में रखा गया है।'
        c1en=f'The material related to “{en_title}” is presented with respect for the epic tradition while keeping material and documentary evidence clearly identified. Archaeology, inscriptions or geography are described according to what each form of evidence can actually establish.'
    elif cat=='Sanatan Understanding':
        c1hi=f'“{hi_title}” जैसे विषयों पर लोकप्रिय भाषा कई बार मूल दार्शनिक अर्थ को बहुत सरल बना देती है। इसे समझते समय ग्रंथ, संप्रदाय, प्रतीक और जीवित आचार—इन सबके संदर्भ को साथ रखना अधिक उचित है।'
        c1en=f'Popular explanations of “{en_title}” can sometimes flatten a much richer philosophical idea. A better reading keeps textual context, sampradaya, symbolism and living practice together rather than treating one simplified explanation as universal.'
    else:
        c1hi=f'“{hi_title}” को {context_hi} के संदर्भ में देखने से विषय की गहराई अधिक स्पष्ट होती है। केवल संक्षिप्त परिभाषा के बजाय यह देखना उपयोगी है कि यह विचार या परंपरा किन प्रश्नों, आचारों और संबंधित अवधारणाओं से जुड़ती है।'
        c1en=f'“{en_title}” becomes clearer when read within {context_en}. Instead of stopping at a short definition, it is useful to see the questions, practices and connected ideas that give the topic its wider meaning.'
    generated.append((h1hi,h1en,c1hi,c1en))

    # 2
    h2hi,h2en=headings[1]
    if sources:
        c2hi='इस विषय के साथ स्रोत दिए गए हैं ताकि पाठक मूल सामग्री तक पहुँच सके और कथन को स्वयं जाँच सके। आधिकारिक संस्था, शोध-पत्र, पुरातात्त्विक प्रकाशन या प्रामाणिक ग्रंथ-संदर्भ को प्राथमिकता देना इस पृष्ठ की अध्ययन-पद्धति का महत्वपूर्ण भाग है।'
        c2en='Sources are provided so the reader can reach the underlying material and verify the statement independently. Preference is given to official institutions, research publications, archaeological reports or identifiable textual references wherever they are available.'
    elif rel_hi:
        c2hi=f'इस विषय को {rel_hi} के साथ पढ़ना उपयोगी है। इन संबंधित अवधारणाओं को साथ देखने से “{hi_title}” का अर्थ अधिक व्यापक रूप में समझ आता है और अलग-अलग विचारों के बीच संबंध स्पष्ट होते हैं।'
        c2en=f'This topic is especially useful to read alongside {rel_en}. Seeing these related ideas together places “{en_title}” in a wider framework and makes the relationship between concepts easier to understand.'
    else:
        c2hi=f'“{hi_title}” किसी एक वाक्य, एक क्षेत्र या एक व्याख्या तक सीमित विषय नहीं है। हिंदू परंपराओं की विविधता को ध्यान में रखते हुए मूल अवधारणा और उसके अलग-अलग प्रयोगों में अंतर करना अधिक संतुलित अध्ययन देता है।'
        c2en=f'“{en_title}” should not be reduced to one sentence or one interpretation. A balanced study distinguishes the core idea from the different ways it may be expressed across Hindu traditions, regions and lineages.'
    generated.append((h2hi,h2en,c2hi,c2en))

    # 3
    h3hi,h3en=headings[2]
    if cat in ('Verified Facts','Garv with Proof','Indian Knowledge Systems'):
        c3hi=f'इस विषय का महत्व केवल अतीत की उपलब्धि के रूप में नहीं, बल्कि ज्ञान को व्यवस्थित रूप से सुरक्षित रखने, समझने और आगे अध्ययन करने में भी है। “{hi_title}” हमें यह देखने का अवसर देता है कि भारतीय बौद्धिक परंपराएँ अलग-अलग क्षेत्रों में किस प्रकार विकसित हुईं।'
        c3en=f'The importance of this topic is not limited to celebrating a past achievement. “{en_title}” also helps us see how knowledge was organized, preserved and developed within Indian intellectual traditions, and why careful historical study still matters today.'
    elif cat=='History':
        c3hi=f'इतिहास पढ़ते समय तिथि, ग्रंथ-परंपरा, पुरातत्त्व और बाद की सांस्कृतिक स्मृति को एक ही प्रकार का प्रमाण नहीं मानना चाहिए। “{hi_title}” को इन स्तरों को अलग पहचानकर पढ़ने से इतिहास अधिक स्पष्ट और सम्मानपूर्ण रूप में सामने आता है।'
        c3en=f'Historical study works best when dates, textual tradition, archaeology and later cultural memory are not treated as identical kinds of evidence. Reading “{en_title}” with these layers distinguished gives a clearer and more respectful historical picture.'
    elif cat=='Sanatan Understanding':
        c3hi=f'सरल निष्कर्ष यह है कि “{hi_title}” को समझने के लिए सनातन परंपरा की आंतरिक भाषा और संदर्भ को महत्व देना चाहिए। जहाँ अनेक व्याख्याएँ हैं, वहाँ उन्हें विरोध के रूप में नहीं बल्कि परंपरा की बहुलता के रूप में देखना अधिक उपयुक्त है।'
        c3en=f'The practical takeaway is to understand “{en_title}” in the language and context of the tradition itself. Where multiple interpretations exist, they are better approached as part of Hinduism’s internal diversity rather than forced into a single universal formula.'
    else:
        c3hi=f'अध्ययन का अगला चरण “{hi_title}” को संबंधित ग्रंथों, विचारों और जीवित परंपराओं से जोड़ना है। इससे पाठक केवल जानकारी याद नहीं करता, बल्कि यह समझता है कि विषय सनातन जीवन-दृष्टि और ज्ञान-परंपरा के बड़े ताने-बाने में कहाँ स्थित है।'
        c3en=f'The next step is to connect “{en_title}” with related texts, ideas and living traditions. This helps the reader move beyond memorizing information and understand where the topic sits within the wider fabric of Sanatan thought and culture.'
    generated.append((h3hi,h3en,c3hi,c3en))

    out=kept[:]
    existing_norm={re.sub(r'\s+',' ',(s.get('contentHi') or '').strip()).lower() for s in out}
    for hhi,hen,chi,cen in generated:
        norm=re.sub(r'\s+',' ',chi.strip()).lower()
        if norm in existing_norm: continue
        out.append({'title':hen,'titleEn':hen,'titleHi':hhi,'content':cen,'contentEn':cen,'contentHi':chi})
        existing_norm.add(norm)
    return out[:4]

def enrich_content():
    data=json.load(open(CONTENT,encoding='utf-8'))
    lookup={x['slug']:x for x in data}
    for item in data:
        item['titleHi']=clean_hi(item.get('titleHi') or item.get('title') or '')
        item['titleEn']=clean_en(item.get('titleEn') or item.get('title') or '')
        item['summaryHi']=clean_hi(item.get('summaryHi') or '')
        item['summaryEn']=clean_en(item.get('summaryEn') or item.get('summary') or '')
        item['subtitleHi']=clean_hi(item.get('subtitleHi') or '')
        item['subtitleEn']=clean_en(item.get('subtitleEn') or '')
        # Specific overrides first.
        cur=CURATED.get(item['slug'],{})
        if 'titleHi' in cur: item['titleHi']=cur['titleHi']
        v=stable_variant(item['slug'],len(BODY_HI))
        item['bodyHi']=clean_hi(cur.get('bodyHi') or BODY_HI[v].format(title=item['titleHi'],context=CATEGORY_CONTEXT_HI[item['category']]))
        item['bodyEn']=clean_en(cur.get('bodyEn') or BODY_EN[v].format(title=item['titleEn'],context=CATEGORY_CONTEXT_EN[item['category']]))
        item['body']=item['bodyEn']
        item['summary']=item['summaryEn']
        item['title']=item['titleEn']
        # Clean evidence fields.
        item['evidenceTypeHi']=clean_hi(item.get('evidenceTypeHi') or '')
        item['evidenceScopeHi']=clean_hi(item.get('evidenceScopeHi') or '')
        if 'sections' in cur:
            item['sections']=[{'title':en_t,'titleEn':en_t,'titleHi':hi_t,'content':en_c,'contentEn':en_c,'contentHi':hi_c} for hi_t,en_t,hi_c,en_c in cur['sections']]
        else:
            item['sections']=make_sections(item, lookup)
        # Final Hindi cleanup on sections.
        for s in item['sections']:
            s['titleHi']=clean_hi(s.get('titleHi') or '')
            s['contentHi']=clean_hi(s.get('contentHi') or '')
            s['titleEn']=clean_en(s.get('titleEn') or s.get('title') or '')
            s['contentEn']=clean_en(s.get('contentEn') or s.get('content') or '')
            s['title']=s['titleEn']; s['content']=s['contentEn']
    json.dump(data,open(CONTENT,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

TEXT_CATEGORY_HI_CONTEXT={
    'Vedas & Vedic Corpus':'वैदिक मंत्र, अनुष्ठान, चिंतन और श्रुति-परंपरा',
    'Principal Upanishads':'आत्मन्, ब्रह्मन्, ज्ञान, मृत्यु और मोक्ष पर उपनिषदिक चिंतन',
    'Itihasa & Gita':'कथा, धर्म, नीति, भक्ति और दर्शन की महाकाव्य परंपरा',
    'Mahapuranas':'देव-कथाओं, तीर्थ, वंशावलियों, धर्म और भक्ति की पुराण-परंपरा',
    'Dharma & Smriti':'आचार, धर्म, विधि और सामाजिक कर्तव्यों पर शास्त्रीय विचार',
    'Darshana & Sutra':'सूत्र-शैली में व्यवस्थित दार्शनिक और तर्कपरक चिंतन',
    'Vedanta':'उपनिषद, ब्रह्मसूत्र और गीता पर आधारित वेदांत-व्याख्या',
    'Agama & Tantra':'मंदिर, उपासना, मंत्र, ध्यान और साधना की आगमिक-तांत्रिक परंपरा',
    'Yoga':'योग-साधना, ध्यान, शरीर-मन अनुशासन और मुक्ति-पथ',
    'Bhakti & Regional Classics':'भक्ति, काव्य, संगीत और क्षेत्रीय धार्मिक साहित्य',
    'Knowledge Texts':'भारतीय ज्ञान-विज्ञान, व्याकरण, चिकित्सा, गणित, खगोल और कलाओं का शास्त्रीय साहित्य',
}
TEXT_CATEGORY_EN_CONTEXT={
    'Vedas & Vedic Corpus':'Vedic hymn, ritual, reflection and Shruti transmission',
    'Principal Upanishads':'Upanishadic inquiry into Atman, Brahman, knowledge, death and liberation',
    'Itihasa & Gita':'epic narrative, dharma, ethics, devotion and philosophy',
    'Mahapuranas':'Puranic traditions of deity narratives, pilgrimage, genealogy, dharma and devotion',
    'Dharma & Smriti':'classical reflection on conduct, dharma, law and social duties',
    'Darshana & Sutra':'systematic philosophical reasoning expressed in sutra traditions',
    'Vedanta':'Vedantic interpretation grounded in the Upanishads, Brahma Sutras and Bhagavad Gita',
    'Agama & Tantra':'Agamic and Tantric traditions of temple practice, mantra, meditation and worship',
    'Yoga':'yogic discipline, meditation, body-mind training and liberation',
    'Bhakti & Regional Classics':'devotional poetry, music and regional religious literature',
    'Knowledge Texts':'classical Indian literature on grammar, medicine, mathematics, astronomy, arts and systematic knowledge',
}

def text_cat_key(x):
    c=x.get('category','')
    # Map any unforeseen categories into best available context.
    for k in TEXT_CATEGORY_HI_CONTEXT:
        if c==k: return k
    if 'Veda' in c: return 'Vedas & Vedic Corpus'
    if 'Upanishad' in c: return 'Principal Upanishads'
    if 'Purana' in c: return 'Mahapuranas'
    if 'Yoga' in c: return 'Yoga'
    if 'Bhakti' in c: return 'Bhakti & Regional Classics'
    return 'Knowledge Texts'

def enrich_texts():
    data=json.load(open(TEXTS,encoding='utf-8'))
    for x in data:
        x['titleHi']=clean_hi(x.get('titleHi') or '')
        x['descriptionHi']=clean_hi(x.get('descriptionHi') or '')
        x['keyThemesHi']=clean_hi(x.get('keyThemesHi') or '')
        x['whyReadHi']=clean_hi(x.get('whyReadHi') or '')
        x['structureHi']=clean_hi(x.get('structureHi') or '')
        x['studyNoteHi']=clean_hi(x.get('studyNoteHi') or '')
        key=text_cat_key(x)
        ctx_hi=TEXT_CATEGORY_HI_CONTEXT[key]
        ctx_en=TEXT_CATEGORY_EN_CONTEXT[key]
        title_hi=x['titleHi']; title_en=x.get('titleEn','')
        # Description: preserve specific first sentence, then add context.
        base_hi=x['descriptionHi'].rstrip('।')
        base_en=clean_en(x.get('descriptionEn','')).rstrip('.')
        x['descriptionHi']=f'{base_hi}। {title_hi} को {ctx_hi} के संदर्भ में पढ़ने पर उसके उद्देश्य और परंपरा में स्थान को अधिक स्पष्ट रूप से समझा जा सकता है।'
        x['descriptionEn']=f'{base_en}. Reading {title_en} within the context of {ctx_en} makes its purpose and place in the wider textual tradition easier to understand.'
        # Richer sections, while still using only existing known description/context.
        x['keyThemesHi']=f'{title_hi} का मुख्य विषय उसके मूल ग्रंथ-विन्यास और परंपरागत उपयोग से समझा जाता है। {base_hi}। इसे पढ़ते समय यह देखना उपयोगी है कि ग्रंथ किन विचारों, अनुष्ठानों, कथाओं, तर्कों या साधना-पद्धतियों को केंद्र में रखता है और उसका संबंध उसी साहित्यिक परिवार के अन्य ग्रंथों से कैसे बनता है।'
        x['keyThemesEn']=f'The main themes of {title_en} are best understood from its own literary structure and traditional use. {base_en}. A careful reading asks which ideas, rituals, narratives, arguments or practices are central to the work and how it relates to other texts in the same literary family.'
        x['structureHi']=f'{title_hi} की रचना को उसके उपलब्ध संस्करण, शाखा, पाठ-परंपरा या संपादित प्रति के अनुसार समझना चाहिए। अलग-अलग संस्करणों में अध्याय, कांड, मंडल, पर्व, सूत्र, सर्ग या श्लोक-संख्या में अंतर हो सकता है। इसलिए किसी अंश को उद्धृत करते समय संस्करण, संपादक या अनुवादक का नाम देखना उपयोगी है।'
        x['structureEn']=f'The structure of {title_en} should be read according to the edition, recension or textual tradition being used. Numbering of chapters, kandas, mandalas, parvas, sutras, sargas or verses can differ between editions. When citing a passage, note the edition, editor or translator whenever possible.'
        x['whyReadHi']=f'{title_hi} का अध्ययन इसलिए महत्वपूर्ण है क्योंकि यह {ctx_hi} को समझने का प्रत्यक्ष द्वार देता है। केवल सारांश पढ़ने के बजाय मूल ग्रंथ या विश्वसनीय अनुवाद देखने से भाषा, तर्क, कथा और संदर्भ की वह सूक्ष्मता सामने आती है जो छोटे परिचय में नहीं आ सकती।'
        x['whyReadEn']=f'Studying {title_en} matters because it offers direct access to {ctx_en}. Reading the text itself, or a reliable translation, reveals nuances of language, argument, narrative and context that a short summary cannot fully preserve.'
        x['studyNoteHi']=f'{title_hi} का अध्ययन करते समय मूल पाठ, अनुवाद और बाद की टीका को अलग-अलग पहचानें। जहाँ एक से अधिक पाठ-परंपराएँ या व्याख्याएँ हों, वहाँ उन्हें विरोध मानने के बजाय उनके ऐतिहासिक और संप्रदायगत संदर्भ को समझना अधिक उपयोगी है। इस पृष्ठ पर दिए बाहरी लिंक से संस्करण खोलते समय प्रकाशक और अनुवादक की जानकारी अवश्य देखें।'
        x['studyNoteEn']=f'When studying {title_en}, keep the base text, translation and later commentary distinct. Where multiple recensions or interpretations exist, understanding their historical and sectarian settings is more useful than forcing them into one reading. When opening an external edition, always note the publisher and translator.'
        x['archiveLabelHi']='इंटरनेट आर्काइव पर सार्वजनिक संस्करण देखें'
        if x.get('readOnlineLabelHi'):
            x['readOnlineLabelHi']='ऑनलाइन उपलब्ध प्रति पढ़ें'
    json.dump(data,open(TEXTS,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

if __name__=='__main__':
    enrich_content(); enrich_texts()
    print('Enhanced bilingual content and scripture catalog.')
