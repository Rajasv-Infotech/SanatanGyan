from __future__ import annotations
import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'SanatanGyan'/'Resources'/'Raw'
content_path=RAW/'sanatan_content.json'
texts_path=RAW/'sanatan_texts.json'
items=json.loads(content_path.read_text(encoding='utf-8'))
by_slug={x['slug']:x for x in items}

# ---------- High-quality curated rewrites for the History lane ----------
history = {
'vedic-textual-traditions':(
'Vedic Textual Traditions', 'वैदिक ग्रंथ-परंपराएँ',
'The Vedic corpus preserves some of South Asia’s oldest surviving religious poetry, ritual language and speculative thought. Its hymns, ritual prose and later reflective layers became foundational reference points for many Hindu traditions.',
'वैदिक साहित्य दक्षिण एशिया की सबसे प्राचीन संरक्षित धार्मिक काव्य, अनुष्ठानिक भाषा और चिंतन-परंपराओं में से है। संहिताएँ, ब्राह्मण, आरण्यक और उपनिषद बाद की अनेक हिंदू परंपराओं के लिए आधारभूत संदर्भ बने।'),
'early-upanishadic-thought':(
'Early Upanishadic Thought','प्रारंभिक उपनिषदिक चिंतन',
'Early Upanishads shifted attention from ritual alone toward questions about the self, ultimate reality, consciousness, death, rebirth and liberation. Dialogues involving teachers such as Yajnavalkya, Gargi and Maitreyi became central to later Vedanta.',
'प्रारंभिक प्रमुख उपनिषदों ने केवल अनुष्ठान से आगे बढ़कर आत्मन्, परम वास्तविकता, चेतना, मृत्यु, पुनर्जन्म और मोक्ष जैसे प्रश्नों पर गहरा विचार किया। याज्ञवल्क्य, गार्गी और मैत्रेयी जैसे संवाद बाद के वेदांत के लिए अत्यंत महत्वपूर्ण बने।'),
'formation-of-epic-traditions':(
'Formation of the Epic Traditions','महाकाव्य परंपराओं का विकास',
'The Ramayana and Mahabharata grew through long textual and oral transmission. They preserve narratives, ethics, political reflection, pilgrimage geography and philosophical teaching that became deeply embedded in Indian cultural memory.',
'रामायण और महाभारत दीर्घ मौखिक तथा ग्रंथीय परंपराओं में विकसित हुए। इनमें कथा, धर्म-चिंतन, राजनीति, तीर्थ-भूगोल और दर्शन का ऐसा विशाल संसार है जो भारतीय सांस्कृतिक स्मृति का स्थायी हिस्सा बन गया।'),
'classical-dharmashastra-development':(
'Classical Dharmashastra Development','शास्त्रीय धर्मशास्त्र का विकास',
'Dharmasutra and Dharmashastra literature systematized discussions of conduct, duties, legal procedure, inheritance, penance and social norms. Different texts emerged in different periods and never represented a single, uniform legal code for all of India.',
'धर्मसूत्र और धर्मशास्त्र साहित्य ने आचरण, कर्तव्य, न्याय-प्रक्रिया, उत्तराधिकार, प्रायश्चित्त और सामाजिक नियमों पर व्यवस्थित चर्चा की। अलग-अलग ग्रंथ अलग कालों में बने और पूरे भारत के लिए एक ही समान कानून-पुस्तक नहीं थे।'),
'classical-philosophical-systems':(
'Classical Philosophical Systems','शास्त्रीय दार्शनिक प्रणालियाँ',
'Indian philosophical schools developed rigorous debates about valid knowledge, language, causation, matter, consciousness, God, self and liberation. Nyaya, Vaisheshika, Samkhya, Yoga, Mimamsa and Vedanta became especially influential frameworks.',
'भारतीय दर्शन-परंपराओं ने प्रमाण, भाषा, कारण-कार्य, पदार्थ, चेतना, ईश्वर, आत्मन् और मोक्ष पर अत्यंत विकसित तर्क-वितर्क किए। न्याय, वैशेषिक, सांख्य, योग, मीमांसा और वेदांत विशेष रूप से प्रभावशाली बने।'),
'puranic-and-temple-traditions-expand':(
'Expansion of Puranic and Temple Traditions','पुराण और मंदिर परंपराओं का विस्तार',
'Puranic literature and temple traditions helped shape devotional Hinduism through narratives of Shiva, Vishnu, Devi and other deities, sacred geography, pilgrimage, festivals, ritual manuals, iconography and regional traditions.',
'पुराण-साहित्य और मंदिर परंपराओं ने शिव, विष्णु, देवी तथा अन्य देव-रूपों की कथाओं, तीर्थ-भूगोल, पर्वों, अनुष्ठानों, मूर्तिशास्त्र और क्षेत्रीय परंपराओं के माध्यम से भक्ति-प्रधान हिंदू जीवन को व्यापक रूप दिया।'),
'bhakti-movements-diversify':(
'Diversification of Bhakti Movements','भक्ति आंदोलनों का विविध विकास',
'Bhakti traditions flourished in many languages and regions. Poet-saints and teachers expressed devotion through songs, philosophical works, temple communities and personal relationships with the divine.',
'भक्ति परंपराएँ अनेक भाषाओं और क्षेत्रों में विकसित हुईं। संत-कवियों और आचार्यों ने पद, भजन, दर्शन, मंदिर-समुदाय और ईश्वर के साथ व्यक्तिगत संबंध के माध्यम से भक्ति को व्यापक रूप दिया।'),
'adi-shankara-and-advaita-consolidation':(
'Adi Shankara and the Consolidation of Advaita','आदि शंकर और अद्वैत का सुदृढ़ीकरण',
'Adi Shankaracharya became a major interpreter of the Upanishads, Bhagavad Gita and Brahma Sutras. His Advaita tradition emphasized non-duality and profoundly shaped later debates within Vedanta.',
'आदि शंकराचार्य उपनिषद, भगवद्गीता और ब्रह्मसूत्र के प्रमुख व्याख्याकार बने। उनके अद्वैत वेदांत ने अद्वैत या अभेद की व्याख्या को केंद्र में रखा और बाद के वेदांत-विवादों पर गहरा प्रभाव डाला।'),
'ramanuja-and-sri-vaishnava-theology':(
'Ramanuja and Sri Vaishnava Theology','रामानुज और श्रीवैष्णव दर्शन',
'Ramanuja articulated Vishishtadvaita Vedanta, interpreting Brahman as personal and qualified by sentient souls and the universe. His theology became central to the Sri Vaishnava tradition.',
'रामानुजाचार्य ने विशिष्टाद्वैत वेदांत का व्यवस्थित प्रतिपादन किया, जिसमें ब्रह्मन् को चेतन जीवों और जगत से विशिष्ट परम सत्ता के रूप में समझाया गया। उनका दर्शन श्रीवैष्णव परंपरा का प्रमुख आधार बना।'),
'madhva-and-dvaita-vedanta':(
'Madhva and Dvaita Vedanta','मध्व और द्वैत वेदांत',
'Madhvacharya developed Dvaita Vedanta, emphasizing a real distinction between God, individual souls and the world. His school became a major Vaishnava philosophical tradition, especially in Karnataka.',
'मध्वाचार्य ने द्वैत वेदांत का प्रतिपादन किया, जिसमें ईश्वर, जीव और जगत के वास्तविक भेद पर बल है। विशेषकर कर्नाटक में यह एक प्रमुख वैष्णव दार्शनिक परंपरा बनी।'),
'early-modern-bhakti-literature':(
'Early-Modern Bhakti Literature','आरंभिक आधुनिक भक्ति साहित्य',
'From Tulsidas and Mirabai to Surdas and many regional poet-saints, vernacular devotional literature brought theological and ethical ideas into widely accessible poetic forms.',
'तुलसीदास, मीराबाई, सूरदास और अनेक क्षेत्रीय संत-कवियों की रचनाओं ने भक्ति, धर्म और दर्शन को लोकभाषाओं के अत्यंत लोकप्रिय काव्य-रूपों में व्यक्त किया।'),
'colonial-encounter-and-hindu-reform':(
'Colonial Encounter and Hindu Reform','औपनिवेशिक काल और हिंदू सुधार आंदोलन',
'Colonial rule brought new institutions, print culture, legal categories and encounters with European scholarship. Hindu thinkers responded in many ways, including reform, revival, social criticism and new presentations of Vedanta and bhakti.',
'औपनिवेशिक शासन के साथ नई संस्थाएँ, मुद्रण, कानूनी वर्गीकरण और यूरोपीय अध्ययन आए। हिंदू चिंतकों ने सुधार, पुनर्जागरण, सामाजिक आलोचना और वेदांत-भक्ति की नई प्रस्तुतियों सहित अनेक प्रकार से प्रतिक्रिया दी।'),
'vivekananda-at-chicago':(
'Vivekananda at the Parliament of Religions','धर्म संसद में विवेकानंद',
'In 1893 Swami Vivekananda addressed the World’s Parliament of Religions in Chicago. His speeches became a landmark in the global presentation of Vedanta, yoga and Hindu thought.',
'1893 में स्वामी विवेकानंद ने शिकागो की विश्व धर्म संसद में संबोधन दिया। उनके भाषण वेदांत, योग और हिंदू चिंतन की वैश्विक प्रस्तुति के इतिहास में एक महत्वपूर्ण पड़ाव बने।'),
'indian-independence-and-constitutional-era':(
'Independence and the Constitutional Era','स्वतंत्रता और संवैधानिक युग',
'Modern India combined a civilizational inheritance with a democratic constitutional order. Hindu traditions continued to evolve through institutions, temples, movements, scholarship and public culture.',
'आधुनिक भारत ने अपनी सभ्यतागत विरासत के साथ लोकतांत्रिक संवैधानिक व्यवस्था को जोड़ा। हिंदू परंपराएँ मंदिरों, संस्थाओं, आंदोलनों, शिक्षा और सार्वजनिक संस्कृति के माध्यम से नए रूपों में विकसित होती रहीं।'),
'global-yoga-and-diaspora-hinduism':(
'Global Yoga and Diaspora Hinduism','वैश्विक योग और प्रवासी हिंदू परंपराएँ',
'In the twentieth and twenty-first centuries, yoga, Vedanta, temple networks and Hindu communities expanded across the world. Global transmission created both new audiences and new forms of practice.',
'20वीं और 21वीं शताब्दी में योग, वेदांत, मंदिर-नेटवर्क और प्रवासी हिंदू समुदाय विश्वभर में फैले। वैश्विक प्रसार ने नई पीढ़ियों, नए संस्थागत रूपों और नई अभ्यास-पद्धतियों को जन्म दिया।'),
'classical-sanskrit-knowledge-culture':(
'Classical Sanskrit Knowledge Culture','शास्त्रीय संस्कृत ज्ञान-संस्कृति',
'Sanskrit intellectual culture produced sophisticated works in grammar, logic, poetics, mathematics, astronomy, medicine, law, philosophy and the arts. These disciplines interacted through commentaries and long teacher-student lineages.',
'संस्कृत ज्ञान-परंपरा में व्याकरण, तर्क, काव्यशास्त्र, गणित, खगोल, चिकित्सा, धर्मशास्त्र, दर्शन और कलाओं पर अत्यंत विकसित ग्रंथ बने। टीका-परंपरा और गुरु-शिष्य परंपरा ने इन विषयों को सदियों तक जीवित रखा।'),
'south-indian-bhakti-traditions':(
'South Indian Bhakti Traditions','दक्षिण भारतीय भक्ति परंपराएँ',
'Tamil Alvars and Nayanars, followed by later teachers and temple traditions, created a vast devotional corpus centered on Vishnu and Shiva and helped shape regional temple culture.',
'तमिल आलवार और नयनार संतों तथा बाद के आचार्यों ने विष्णु और शिव-केंद्रित विशाल भक्ति-साहित्य रचा। इन परंपराओं ने दक्षिण भारतीय मंदिर-संस्कृति और भक्ति के विकास पर गहरा प्रभाव डाला।'),
'temple-networks-and-pilgrimage':(
'Temple Networks and Pilgrimage','मंदिर नेटवर्क और तीर्थयात्रा',
'Temples and pilgrimage routes linked sacred geography with local communities, royal patronage, ritual specialists, art, music, festivals and long-distance movement across the subcontinent.',
'मंदिरों और तीर्थमार्गों ने पवित्र भूगोल को स्थानीय समाज, राजकीय संरक्षण, पुरोहित परंपराओं, कला, संगीत, पर्व और दूर-दूर की यात्राओं से जोड़ा।'),
'saka-calendar':(
'The Saka Calendar and Modern India','शक कैलेंडर और आधुनिक भारत',
'India’s national calendar uses the Saka Era and a standardized solar framework. It illustrates how historical Indian calendrical traditions continue alongside regional lunisolar Panchangas.',
'भारत का राष्ट्रीय कैलेंडर शक संवत और मानकीकृत सौर प्रणाली का उपयोग करता है। यह दिखाता है कि आधुनिक राष्ट्रीय कालगणना के साथ क्षेत्रीय चंद्र-सौर पंचांग परंपराएँ भी जीवित हैं।'),
}
for slug,(en_title,hi_title,en,hi) in history.items():
    x=by_slug.get(slug)
    if not x: continue
    x['titleEn']=en_title; x['titleHi']=hi_title; x['summaryEn']=en; x['summaryHi']=hi
    x['bodyEn']=''; x['bodyHi']=''

# Curated foundation articles most likely to be read first.
foundation={
'sanatan-dharma-kya-hai':(
'Sanatan Dharma is a broad civilizational and spiritual tradition rather than a single-creed system. It includes Vedic and Agamic traditions, many schools of philosophy, devotional paths, yoga, ritual, ethics, sacred narratives and regionally diverse practices.',
'सनातन धर्म किसी एक मत या एक ही आचार-पद्धति तक सीमित नहीं है। इसमें वैदिक और आगमिक परंपराएँ, अनेक दर्शन, भक्ति-पथ, योग, अनुष्ठान, नैतिक चिंतन, पवित्र कथाएँ और विविध क्षेत्रीय परंपराएँ शामिल हैं।'),
'dharma':(
'Dharma is a central Indian concept whose meaning changes with context: sustaining order, ethical responsibility, appropriate conduct, duty, law or the characteristic nature of a thing. Hindu texts therefore discuss dharma at personal, social, political and spiritual levels.',
'धर्म भारतीय चिंतन की केंद्रीय अवधारणा है। संदर्भ के अनुसार इसका अर्थ जीवन और समाज को धारण करने वाली व्यवस्था, नैतिक जिम्मेदारी, उचित आचरण, कर्तव्य, नियम या किसी वस्तु का स्वभाव हो सकता है। इसलिए हिंदू ग्रंथ धर्म को व्यक्तिगत, सामाजिक, राजकीय और आध्यात्मिक स्तरों पर देखते हैं।'),
'karma':(
'Karma literally means action. In Hindu philosophical traditions it also refers to the moral and causal significance of actions and intentions, especially when discussing character, rebirth and liberation. Karma is not simply “fate”; action, choice and discipline remain important.',
'कर्म का मूल अर्थ “कार्य” या “किया गया कर्म” है। हिंदू दर्शन में यह कर्म और अभिप्राय के नैतिक-कारणात्मक परिणामों से भी जुड़ता है, विशेषकर पुनर्जन्म और मोक्ष के संदर्भ में। कर्म को केवल “भाग्य” समझना अधूरा है; पुरुषार्थ, चुनाव और साधना भी महत्वपूर्ण हैं।'),
'atman':(
'Atman refers to the deepest self or principle of selfhood in many Hindu philosophical traditions. The Upanishads made inquiry into Atman central, while later Vedanta schools developed different explanations of its relation to Brahman, Ishvara and the world.',
'आत्मन् अनेक हिंदू दर्शनों में व्यक्ति के गहरे आत्म-स्वरूप या चेतन अस्तित्व की अवधारणा है। उपनिषदों ने आत्मन् की खोज को केंद्रीय विषय बनाया, जबकि बाद के वेदांत दर्शनों ने आत्मन्, ब्रह्मन्, ईश्वर और जगत के संबंध की अलग-अलग व्याख्याएँ कीं।'),
'brahman':(
'Brahman is the term used in the Upanishadic and Vedantic traditions for ultimate reality. Different Vedanta schools agree on its central importance but differ in how they describe its relation to the world, individual selves and the personal divine.',
'ब्रह्मन् उपनिषद और वेदांत परंपराओं में परम वास्तविकता का प्रमुख नाम है। सभी वेदांत परंपराएँ इसकी केंद्रीयता स्वीकार करती हैं, लेकिन जगत, जीव और व्यक्तिगत ईश्वर से ब्रह्मन् के संबंध को अलग-अलग ढंग से समझाती हैं।'),
'moksha':(
'Moksha means liberation from bondage and the cycle of samsara. Hindu traditions describe different paths—knowledge, devotion, disciplined action, meditation and divine grace—and disagree in detail about what the liberated state means.',
'मोक्ष बंधन और संसार-चक्र से मुक्ति की अवधारणा है। हिंदू परंपराएँ ज्ञान, भक्ति, निष्काम कर्म, ध्यान, योग और ईश-कृपा जैसे विभिन्न मार्ग बताती हैं; मुक्त अवस्था की प्रकृति को लेकर अलग-अलग दर्शन अपनी विशिष्ट व्याख्या देते हैं।'),
'ramayana-overview':('', ''),
}
for slug,(en,hi) in foundation.items():
    if slug in by_slug and en:
        by_slug[slug]['summaryEn']=en; by_slug[slug]['summaryHi']=hi; by_slug[slug]['bodyEn']=''; by_slug[slug]['bodyHi']=''

# Remove the v0.4/v0.5 repeated 'summary == body == simple meaning' pattern everywhere.
def norm(s:str)->str:
    return re.sub(r'\W+',' ',(s or '').lower(),flags=re.UNICODE).strip()

# Build title lookup before related sections.
lookup={x['slug']:(x.get('titleEn') or x.get('title') or x['slug'], x.get('titleHi') or x.get('title') or x['slug']) for x in items}

category_context={
'Sanatan Basics':(
'Context in the tradition','परंपरा में संदर्भ',
'{title} is best understood together with the texts, philosophical schools and living traditions that use the idea. Hindu thought often preserves more than one interpretation rather than reducing a concept to a single formula.',
'{title_hi} को उन ग्रंथों, दर्शन-परंपराओं और जीवित आचारों के संदर्भ में समझना सबसे उपयोगी है जिनमें यह अवधारणा प्रयुक्त होती है। हिंदू चिंतन अनेक बार किसी विचार को एक ही सूत्र में सीमित करने के बजाय विभिन्न व्याख्याओं को साथ रखता है।'),
'Philosophy':(
'How to study this philosophy','इस दर्शन को कैसे समझें',
'When studying {title}, look at the questions it asks about valid knowledge, self, world, causation, God and liberation. Its distinctiveness becomes clearer when compared with other Indian philosophical schools.',
'{title_hi} को समझते समय यह देखना उपयोगी है कि यह प्रमाण, आत्मा, जगत, कारण-कार्य, ईश्वर और मोक्ष जैसे प्रश्नों का क्या उत्तर देता है। अन्य भारतीय दर्शनों से तुलना करने पर इसकी विशिष्टता अधिक स्पष्ट होती है।'),
'Practices & Symbols':(
'Practice and meaning','आचार और अर्थ',
'{title} can have ritual, devotional and symbolic layers at the same time. Exact forms may vary by family, region, temple and sampradaya, so the practice should be read within its living context.',
'{title_hi} में अनुष्ठान, भक्ति और प्रतीक—तीनों स्तर एक साथ हो सकते हैं। इसका रूप परिवार, क्षेत्र, मंदिर और संप्रदाय के अनुसार बदल सकता है, इसलिए इसे जीवित परंपरा के संदर्भ में समझना चाहिए।'),
'Deities':(
'Place in Hindu traditions','हिंदू परंपराओं में स्थान',
'{title} is encountered through theology, devotional literature, temple worship, iconography, festivals and regional traditions. Different sampradayas may emphasize different names, forms and philosophical meanings.',
'{title_hi} का स्वरूप दर्शन, भक्ति-साहित्य, मंदिर-उपासना, मूर्तिशास्त्र, पर्व और क्षेत्रीय परंपराओं में दिखाई देता है। अलग-अलग संप्रदाय इनके नाम, रूप और दार्शनिक अर्थों पर अलग बल दे सकते हैं।'),
'Thinkers & Acharyas':(
'Intellectual legacy','बौद्धिक विरासत',
'To understand {title}, it is useful to distinguish historically attested works, works traditionally attributed to the teacher, later commentaries and the institutions or lineages that carried the teaching forward.',
'{title_hi} को समझते समय ऐतिहासिक रूप से प्रमाणित रचनाओं, परंपरागत रूप से संबद्ध ग्रंथों, बाद की टीकाओं और उस परंपरा को आगे बढ़ाने वाली गुरु-शिष्य या संस्थागत परंपराओं के बीच अंतर देखना उपयोगी है।'),
'History':(
'Historical lens','ऐतिहासिक दृष्टि',
'{title} is presented here as part of a long historical process. The app separates traditional sacred chronology, textual development and archaeologically or epigraphically dated evidence instead of forcing them into one date.',
'{title_hi} को यहाँ एक दीर्घ ऐतिहासिक प्रक्रिया के हिस्से के रूप में प्रस्तुत किया गया है। ऐप पारंपरिक पवित्र कालक्रम, ग्रंथीय विकास और पुरातात्त्विक/अभिलेखीय तिथियों को एक ही तारीख में मिलाने के बजाय अलग-अलग दिखाता है।'),
'Indian Knowledge Systems':(
'Knowledge focus','ज्ञान का केंद्र',
'{title} belongs to the broader history of Indian knowledge. The subject is studied through surviving texts, commentaries, manuscripts, instruments, calculations, material remains and the history of later transmission where available.',
'{title_hi} भारतीय ज्ञान-इतिहास के व्यापक परिप्रेक्ष्य का हिस्सा है। जहाँ संभव हो, इसे उपलब्ध ग्रंथों, टीकाओं, पांडुलिपियों, उपकरणों, गणनाओं, भौतिक अवशेषों और बाद की ज्ञान-परंपरा के आधार पर समझा जाता है।'),
'Garv with Proof':(
'What is established','क्या प्रमाणित है',
'This entry is included because its central claim can be checked against the listed documentary, institutional or scholarly sources. The wording is intentionally kept narrower than popular social-media versions of the claim.',
'यह प्रविष्टि इसलिए शामिल है क्योंकि इसका मुख्य कथन नीचे दिए गए दस्तावेज़ी, संस्थागत या शोध-स्रोतों से जाँचा जा सकता है। सोशल मीडिया में प्रचलित अतिरंजित रूपों की तुलना में यहाँ कथन को जानबूझकर सटीक और सीमित रखा गया है।'),
'Verified Facts':(
'What the evidence shows','प्रमाण क्या दिखाता है',
'The fact stated here is limited to what the cited source directly establishes. Broader interpretations are kept separate so that the “verified” label remains meaningful.',
'यहाँ दिया गया तथ्य केवल उतना ही कहा गया है जितना उद्धृत स्रोत सीधे स्थापित करता है। व्यापक व्याख्याओं को अलग रखा गया है ताकि “प्रमाणित” चिन्ह का अर्थ स्पष्ट और विश्वसनीय बना रहे।'),
'Epic Evidence':(
'How to read this evidence','इस प्रमाण को कैसे पढ़ें',
'This page records a verified archaeological, epigraphic, geographical or material fact connected with Ramayana or Mahabharata traditions. Evidence for an ancient place, inscription or cultural memory is labelled separately from a claim about a specific epic event.',
'यह पृष्ठ रामायण या महाभारत परंपरा से जुड़े किसी सत्यापित पुरातात्त्विक, अभिलेखीय, भौगोलिक या भौतिक तथ्य को दर्ज करता है। किसी प्राचीन स्थल, अभिलेख या सांस्कृतिक स्मृति के प्रमाण को किसी विशिष्ट महाकाव्य-घटना के दावे से अलग लेबल किया जाता है।'),
}

for x in items:
    summary_en=x.get('summaryEn','').strip(); summary_hi=x.get('summaryHi','').strip()
    if norm(x.get('bodyEn',''))==norm(summary_en): x['bodyEn']=''
    if norm(x.get('bodyHi',''))==norm(summary_hi): x['bodyHi']=''
    new=[]
    seen=set()
    for s in x.get('sections',[]):
        title=(s.get('titleEn') or '').strip().lower()
        cont_en=(s.get('contentEn') or s.get('content') or '').strip()
        cont_hi=(s.get('contentHi') or '').strip()
        if title in {'simple meaning','deep study'} or (s.get('titleHi') or '').strip() in {'सरल अर्थ','गहन अध्ययन'}: continue
        if norm(cont_en) in {norm(summary_en),norm(x.get('bodyEn',''))} and norm(cont_en): continue
        key=norm(cont_en)+'|'+norm(cont_hi)
        if key in seen: continue
        seen.add(key); new.append(s)
    x['sections']=new
    if x['category'] in category_context:
        en_t,hi_t,en_tpl,hi_tpl=category_context[x['category']]
        x['sections'].insert(0,{
            'title':en_t,'titleEn':en_t,'titleHi':hi_t,
            'content':en_tpl.format(title=x.get('titleEn') or x.get('title'),title_hi=x.get('titleHi') or x.get('title')),
            'contentEn':en_tpl.format(title=x.get('titleEn') or x.get('title'),title_hi=x.get('titleHi') or x.get('title')),
            'contentHi':hi_tpl.format(title=x.get('titleEn') or x.get('title'),title_hi=x.get('titleHi') or x.get('title')),
        })
    rel=[lookup[r] for r in x.get('relatedSlugs',[]) if r in lookup][:5]
    if rel:
        en=', '.join(a for a,b in rel); hi=' • '.join(b for a,b in rel)
        x['sections'].append({'title':'Connected topics','titleEn':'Connected topics','titleHi':'संबंधित विषय','content':f'Related topics in this app: {en}.','contentEn':f'Related topics in this app: {en}.','contentHi':f'इस विषय से जुड़े आगे के अध्ययन: {hi}।'})

# ---------- Epic chronology + evidence hub content ----------
def src(title,publisher,url,note=''):
    return {'title':title,'publisher':publisher,'url':url,'note':note}

def section(en_t,hi_t,en,hi):
    return {'title':en_t,'titleEn':en_t,'titleHi':hi_t,'content':en,'contentEn':en,'contentHi':hi}

def epic_item(slug,title_en,title_hi,summary_en,summary_hi,date_label,evidence_type_en,evidence_type_hi,scope_en,scope_hi,tags,sources,sections):
    return {
      'id':'v07'+re.sub('[^a-z0-9]','',slug)[:26], 'slug':slug, 'title':title_en, 'titleEn':title_en, 'titleHi':title_hi,
      'subtitle':'','subtitleEn':'','subtitleHi':'','category':'Epic Evidence','level':'Intermediate',
      'summary':summary_en,'summaryEn':summary_en,'summaryHi':summary_hi,'body':'','bodyEn':'','bodyHi':'',
      'evidenceLevel':'Strong Evidence','claimVerdict':'Supported','dateLabel':date_label,'featured':True,
      'tags':tags,'aliases':[],'relatedSlugs':[],'sections':sections,'sources':sources,
      'evidenceTypeEn':evidence_type_en,'evidenceTypeHi':evidence_type_hi,'evidenceScopeEn':scope_en,'evidenceScopeHi':scope_hi
    }

new=[]
new.append({
'id':'v07traditionalramayanaera','slug':'traditional-ramayana-era','title':'Ramayana Era in Sacred Chronology','titleEn':'Ramayana Era in Sacred Chronology','titleHi':'पारंपरिक कालक्रम में रामायण काल','subtitle':'Treta Yuga','subtitleEn':'Treta Yuga','subtitleHi':'त्रेता युग','category':'History','level':'Beginner',
'summary':'Hindu sacred chronology places the Ramayana narrative in Treta Yuga. The app shows this as traditional chronology rather than converting it into a single modern BCE date.','summaryEn':'Hindu sacred chronology places the Ramayana narrative in Treta Yuga. The app shows this as traditional chronology rather than converting it into a single modern BCE date.','summaryHi':'हिंदू पवित्र कालक्रम में रामायण की कथा त्रेता युग में रखी जाती है। ऐप इसे “पारंपरिक कालक्रम” के रूप में दिखाता है और इसे किसी एक निश्चित आधुनिक ईसा-पूर्व तारीख में बदलकर प्रस्तुत नहीं करता।','body':'','bodyEn':'','bodyHi':'','evidenceLevel':'Traditional / Philosophical','claimVerdict':'Traditional / Faith Claim','dateLabel':'Traditional sacred chronology: Treta Yuga','featured':True,'tags':['ramayana','rama','treta yuga','sacred chronology'],'aliases':['रामायण काल','त्रेता युग'],'relatedSlugs':['rama','itihasa','formation-of-epic-traditions','ramayana-sites-archaeology-project','rama-setu-geography'],'sections':[section('What this timeline means','इस समयरेखा का अर्थ','This lane represents sacred chronology used within Hindu tradition. Archaeological and textual dates are displayed on separate lanes so that each kind of knowledge keeps its own meaning.','यह पट्टी हिंदू परंपरा में प्रयुक्त पवित्र कालक्रम को दर्शाती है। पुरातात्त्विक और ग्रंथीय तिथियाँ अलग पट्टी पर दिखाई जाती हैं ताकि अलग प्रकार के ज्ञान को एक-दूसरे में न मिलाया जाए।')],'sources':[]
})
new.append({
'id':'v07traditionalmahabharataera','slug':'traditional-mahabharata-era','title':'Krishna–Mahabharata Era in Sacred Chronology','titleEn':'Krishna–Mahabharata Era in Sacred Chronology','titleHi':'पारंपरिक कालक्रम में कृष्ण–महाभारत काल','subtitle':'Dvapara Yuga','subtitleEn':'Dvapara Yuga','subtitleHi':'द्वापर युग','category':'History','level':'Beginner',
'summary':'Hindu sacred chronology places Krishna and the central Mahabharata narrative at the end of Dvapara Yuga, followed by the beginning of Kali Yuga. This is shown as sacred chronology, separate from archaeological dating.','summaryEn':'Hindu sacred chronology places Krishna and the central Mahabharata narrative at the end of Dvapara Yuga, followed by the beginning of Kali Yuga. This is shown as sacred chronology, separate from archaeological dating.','summaryHi':'हिंदू पवित्र कालक्रम में श्रीकृष्ण और महाभारत की मुख्य कथा को द्वापर युग के अंतिम चरण से जोड़ा जाता है, जिसके बाद कलियुग का आरंभ माना जाता है। इसे पुरातात्त्विक तिथि-निर्धारण से अलग “पारंपरिक कालक्रम” के रूप में दिखाया गया है।','body':'','bodyEn':'','bodyHi':'','evidenceLevel':'Traditional / Philosophical','claimVerdict':'Traditional / Faith Claim','dateLabel':'Traditional sacred chronology: end of Dvapara Yuga','featured':True,'tags':['mahabharata','krishna','dvapara yuga','sacred chronology'],'aliases':['महाभारत काल','कृष्ण काल','द्वापर युग'],'relatedSlugs':['krishna','itihasa','formation-of-epic-traditions','hastinapura-excavation-evidence','dwarka-underwater-archaeology','heliodorus-vasudeva-inscription'],'sections':[section('What this timeline means','इस समयरेखा का अर्थ','The sacred chronology lane preserves the traditional sequence without presenting a debated conversion as a settled scientific date. Archaeology, inscriptions and text history appear separately.','पवित्र कालक्रम की पट्टी पारंपरिक क्रम को सुरक्षित रखती है, लेकिन किसी विवादित आधुनिक तिथि को “निश्चित वैज्ञानिक तारीख” के रूप में प्रस्तुत नहीं करती। पुरातत्त्व, अभिलेख और ग्रंथ-इतिहास अलग दिखाए जाते हैं।')],'sources':[]
})

new += [
epic_item(
'ramayana-sites-archaeology-project','Archaeology of the Ramayana Sites Project','रामायण स्थलों की पुरातात्त्विक परियोजना',
'The Archaeological Survey of India and the Indian Institute of Advanced Study investigated several places traditionally associated with the Ramayana, including Ayodhya, Nandigrama, Sringaverapura, Bharadvaja Ashrama and Chitrakuta. The project established archaeological sequences at these locations.',
'भारतीय पुरातत्व सर्वेक्षण और भारतीय उच्च अध्ययन संस्थान ने अयोध्या, नंदीग्राम, श्रृंगवेरपुर, भरद्वाज आश्रम और चित्रकूट सहित रामायण परंपरा से जुड़े कई स्थलों पर पुरातात्त्विक अध्ययन किया। इस परियोजना ने इन स्थलों की पुरातात्त्विक परतों और प्राचीन बसावट-क्रम को दर्ज किया।',
'ASI/IIAS project, excavations from the 1970s onward','Archaeological project','पुरातात्त्विक परियोजना','Verified fact: the project and excavations took place; each site has its own archaeological chronology.','प्रमाणित तथ्य: परियोजना और उत्खनन हुए; प्रत्येक स्थल की अपनी अलग पुरातात्त्विक काल-श्रृंखला है।',['ramayana','archaeology','ayodhya','sringaverapura'],
[src('Archaeology of the Ramayana Sites — project introduction','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/82830.pdf','Official archaeological publication preserved by IGNCA.'),src('Ayodhya of the Valmiki Ramayana','IGNCA / archaeological publication','https://ignca.gov.in/Asi_data/74144.pdf','Discusses excavations and the archaeological debate around identification and antiquity.')],
[section('Sites investigated','किन स्थलों का अध्ययन हुआ','The project included excavations or investigations at Ayodhya, Nandigrama, Sringaverapura, Bharadvaja Ashrama, Chitrakuta and related locations. This is important because it replaces vague claims with site-by-site archaeological records.','परियोजना में अयोध्या, नंदीग्राम, श्रृंगवेरपुर, भरद्वाज आश्रम, चित्रकूट और संबंधित स्थलों का उत्खनन या सर्वेक्षण शामिल था। इसका महत्व यह है कि सामान्य दावों के स्थान पर प्रत्येक स्थल का अलग पुरातात्त्विक रिकॉर्ड उपलब्ध होता है।'),section('What the evidence establishes','प्रमाण क्या स्थापित करता है','The excavations establish the antiquity and occupation history of the investigated places. The app keeps this archaeological result separate from the sacred chronology of the Ramayana narrative.','उत्खनन इन स्थलों की प्राचीनता और बसावट-इतिहास के बारे में प्रमाण देते हैं। ऐप इस पुरातात्त्विक निष्कर्ष को रामायण के पवित्र कालक्रम से अलग और स्पष्ट रूप से दिखाता है।')]),
epic_item(
'sringaverapura-archaeology','Sringaverapura: Archaeology and Ramayana Geography','श्रृंगवेरपुर: पुरातत्त्व और रामायण भूगोल',
'Sringaverapura, a place associated in Ramayana tradition with Rama’s journey near the Ganga, was excavated in the Ramayana Sites project. Archaeology documented multiple occupation phases and important water-management remains at the site.',
'रामायण परंपरा में गंगा के निकट श्रीराम की यात्रा से जुड़े श्रृंगवेरपुर का “रामायण स्थलों” की परियोजना के अंतर्गत उत्खनन हुआ। यहाँ अनेक बसावट-चरण और महत्वपूर्ण जल-प्रबंधन अवशेष दर्ज किए गए।',
'Excavations from 1976–77 onward','Archaeology','पुरातत्त्व','Verified archaeological remains at a traditionally identified Ramayana-associated location.','रामायण परंपरा से पहचाने जाने वाले स्थल पर सत्यापित पुरातात्त्विक अवशेष।',['ramayana','sringaverapura','ganga','archaeology'],
[src('Archaeology of the Ramayana Sites — Sringaverapura','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/82830.pdf'),src('The Excavations — Ramayana Sites','IGNCA / archaeological publication','https://ignca.gov.in/Asi_data/87930.pdf')],
[section('Archaeological sequence','पुरातात्त्विक क्रम','Excavations documented occupation layers preceding and including Northern Black Polished Ware levels. The site therefore has a substantial archaeological history independent of its sacred association.','उत्खनन में उत्तरी कृष्ण मार्जित मृद्भांड (NBPW) स्तर से पहले और बाद की बसावट-परतें दर्ज हुईं। इसलिए यह स्थल अपनी धार्मिक पहचान के साथ-साथ स्वतंत्र पुरातात्त्विक इतिहास भी रखता है।'),section('Why it matters','महत्व','Sringaverapura is a good example of how sacred geography can be studied respectfully with archaeology: the traditional association is recorded, while excavated layers provide material history.','श्रृंगवेरपुर यह दिखाता है कि पवित्र भूगोल और पुरातत्त्व को सम्मानपूर्वक साथ पढ़ा जा सकता है—परंपरागत पहचान अपनी जगह रहती है और उत्खनित परतें भौतिक इतिहास बताती हैं।')]),
epic_item(
'rama-setu-geography','Rama Setu / Adam’s Bridge: Verified Geography','राम सेतु / एडम्स ब्रिज: प्रमाणित भूगोल',
'Satellite imagery and modern bathymetric studies document a chain of shoals and submerged ridges between India and Sri Lanka known as Adam’s Bridge and widely revered in India as Rama Setu.',
'उपग्रह चित्र और आधुनिक समुद्र-तल अध्ययन भारत और श्रीलंका के बीच स्थित उथली शृंखलाओं तथा जलमग्न रिज को स्पष्ट रूप से दर्ज करते हैं, जिसे एडम्स ब्रिज और भारत में व्यापक रूप से राम सेतु कहा जाता है।',
'Modern satellite and bathymetric observations','Geography / remote sensing','भूगोल / रिमोट सेंसिंग','Verified physical feature; sacred interpretation is presented as its living cultural significance.','भौतिक संरचना सत्यापित है; इसकी पवित्र पहचान को जीवित सांस्कृतिक महत्व के रूप में प्रस्तुत किया गया है।',['ramayana','rama setu','adam bridge','geography','satellite'],
[src("Adam's Bridge, India-Sri Lanka",'NASA Science','https://science.nasa.gov/photojournal/adams-bridge-india-sri-lanka/','NASA satellite imagery documents the chain of shoals.'),src("Physical features of Adam's Bridge interpreted from ICESat-2",'Scientific Reports','https://doi.org/10.1038/s41598-024-65908-2','Peer-reviewed bathymetric analysis of the submerged ridge and shoals.')],
[section('What can be seen scientifically','विज्ञान से क्या देखा जा सकता है','Remote sensing and bathymetry map the physical chain between Dhanushkodi and the Mannar region. These methods describe shape, depth and geomorphology.','रिमोट सेंसिंग और बाथिमेट्री धनुषकोडी और मन्नार क्षेत्र के बीच की भौतिक शृंखला का आकार, गहराई और समुद्र-तल संरचना दर्ज करती हैं।'),section('Cultural significance','सांस्कृतिक महत्व','For Hindu tradition, the landscape is associated with the Setubandha episode of the Ramayana. The app presents the observable geography and the sacred association together without treating them as the same type of claim.','हिंदू परंपरा में यह भू-दृश्य रामायण के सेतुबंध प्रसंग से जुड़ा है। ऐप प्रत्यक्ष भूगोल और पवित्र परंपरा—दोनों को साथ दिखाता है, लेकिन दोनों को एक ही प्रकार का दावा नहीं मानता।')]),
epic_item(
'ramayana-temple-reliefs','Ramayana Narratives in Early-Medieval Temple Reliefs','प्रारंभिक मध्यकालीन मंदिरों में रामायण शिल्प',
'Archaeological publications document extensive Ramayana narrative reliefs on early-medieval temples in Karnataka, with several scenes accompanied by old Kannada label inscriptions.',
'पुरातात्त्विक प्रकाशनों में कर्नाटक के प्रारंभिक मध्यकालीन मंदिरों पर रामायण के विस्तृत शिल्प-दृश्य दर्ज हैं। अनेक दृश्यों के साथ प्राचीन कन्नड़ में पहचान-लेख भी पाए गए हैं।',
'7th–8th centuries CE and later','Art history / inscriptions','कला-इतिहास / अभिलेख','Material evidence for the established cultural transmission of the Ramayana narrative.','रामायण कथा की स्थापित सांस्कृतिक निरंतरता का भौतिक प्रमाण।',['ramayana','temple','pattadakal','inscriptions','art'],
[src('Temples and Sculptures — Ramayana relief descriptions','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/36615.pdf','Archaeological publication records Ramayana scenes and label inscriptions.')],
[section('What survives','क्या संरक्षित है','Temple walls preserve episodes such as Dasharatha, Vishvamitra, Rama, Lakshmana, Sita, Surpanakha, Ravana, Jatayu and the Vanara army. Labels help identify scenes and show that the narrative was already widely recognizable.','मंदिर-भित्तियों पर दशरथ, विश्वामित्र, राम, लक्ष्मण, सीता, शूर्पणखा, रावण, जटायु और वानर-सेना से जुड़े दृश्य संरक्षित हैं। पहचान-लेख बताते हैं कि कथा के पात्र और प्रसंग व्यापक रूप से पहचाने जाते थे।'),section('Why this is evidence','यह प्रमाण क्यों महत्वपूर्ण है','These reliefs do not date the events of the Ramayana; they securely demonstrate the narrative’s established presence in public religious art by the early-medieval period.','ये शिल्प रामायण की घटनाओं की तारीख निर्धारित नहीं करते; वे यह दृढ़ता से दिखाते हैं कि प्रारंभिक मध्यकाल तक रामायण कथा सार्वजनिक धार्मिक कला में स्थापित थी।')]),
epic_item(
'ramayana-manuscript-tradition','The Ramayana Manuscript and Artistic Tradition','रामायण की पांडुलिपि और चित्रकला परंपरा',
'Large collections of handwritten and illustrated Ramayana manuscripts survive in Indian and international libraries and museums, documenting centuries of transmission across languages, regions and artistic schools.',
'भारत और विश्व के पुस्तकालयों व संग्रहालयों में हस्तलिखित तथा चित्रित रामायण पांडुलिपियों के बड़े संग्रह सुरक्षित हैं। वे अनेक भाषाओं, क्षेत्रों और चित्रकला-शैलियों में सदियों की जीवित परंपरा को दर्ज करते हैं।',
'Medieval to modern manuscript collections','Manuscript / cultural history','पांडुलिपि / सांस्कृतिक इतिहास','Verified manuscript tradition and cultural transmission.','सत्यापित पांडुलिपि परंपरा और सांस्कृतिक प्रसार।',['ramayana','manuscripts','art','cultural transmission'],
[src('Illustrated Ramayana Manuscripts','Indira Gandhi National Centre for the Arts','https://ignca.gov.in/illustrated-ramayana-manuscripts/','IGNCA documents illustrated Ramayana manuscripts in many collections.')],
[section('What the manuscripts show','पांडुलिपियाँ क्या दिखाती हैं','The manuscripts preserve text and imagery shaped by regional artistic traditions, including Mughal, Rajasthani, Pahari, Deccani and eastern Indian schools.','पांडुलिपियों में मुगल, राजस्थानी, पहाड़ी, दक्कनी और पूर्वी भारतीय कला-परंपराओं के अनुरूप रामकथा के पाठ और चित्र सुरक्षित हैं।'),section('Continuity','निरंतरता','They provide direct material evidence that Ramayana study, retelling and illustration continued across centuries and political settings.','ये प्रत्यक्ष भौतिक प्रमाण हैं कि अलग-अलग सदियों और राजनीतिक परिवेशों में रामायण का पाठ, पुनर्कथन और चित्रांकन निरंतर चलता रहा।')]),
epic_item(
'hastinapura-excavation-evidence','Hastinapura Excavations and Painted Grey Ware','हस्तिनापुर उत्खनन और चित्रित धूसर मृद्भांड',
'Excavations at Hastinapura documented a Painted Grey Ware cultural phase and flood-related stratigraphic evidence. Hastinapura is traditionally associated with the Mahabharata and became a major site in the archaeology of the epic geography.',
'हस्तिनापुर के उत्खनन में चित्रित धूसर मृद्भांड (Painted Grey Ware) संस्कृति और बाढ़ से जुड़ी पुरातात्त्विक परतें दर्ज की गईं। महाभारत परंपरा से जुड़े हस्तिनापुर ने महाकाव्य-भूगोल के पुरातात्त्विक अध्ययन में महत्वपूर्ण स्थान प्राप्त किया।',
'ASI excavations 1950–52','Archaeology / stratigraphy','पुरातत्त्व / स्तरक्रम','Verified excavation results at a site traditionally identified with Hastinapura.','परंपरागत हस्तिनापुर से पहचाने जाने वाले स्थल के सत्यापित उत्खनन-परिणाम।',['mahabharata','hastinapura','painted grey ware','archaeology'],
[src('Excavation at Hastinapura and Other Explorations','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/18158.pdf','B. B. Lal’s excavation report in Ancient India.'),src('Excavation at Hastinapura and Other Explorations — conclusions','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/87815.pdf','The original report explicitly treats the epic linkage as circumstantial/provisional while documenting the archaeology.')],
[section('What was found','क्या मिला','The excavation established a cultural sequence that includes Painted Grey Ware and evidence of flooding. The report also compared ceramics from other locations named in Mahabharata tradition.','उत्खनन में चित्रित धूसर मृद्भांड सहित एक स्पष्ट सांस्कृतिक क्रम और बाढ़ के प्रमाण दर्ज हुए। रिपोर्ट ने महाभारत परंपरा में उल्लिखित अन्य स्थानों से मिले मृद्भांडों की भी तुलना की।'),section('Evidence strength','प्रमाण की सीमा','The excavation itself is strong archaeological evidence for the ancient settlement and its material culture. The original archaeologist described the proposed identification with epic events as circumstantial and provisional; the app therefore labels the two levels separately.','उत्खनन प्राचीन बसावट और उसकी भौतिक संस्कृति के लिए मजबूत पुरातात्त्विक प्रमाण है। मूल उत्खननकर्ता ने विशिष्ट महाकाव्य-घटनाओं से संबंध को परिस्थितिजन्य और अस्थायी निष्कर्ष कहा था; इसलिए ऐप दोनों स्तरों को अलग लेबल करता है।')]),
epic_item(
'purana-qila-indraprastha-archaeology','Purana Qila, Indraprastha Tradition and Painted Grey Ware','पुराना किला, इंद्रप्रस्थ परंपरा और चित्रित धूसर मृद्भांड',
'Archaeological excavations at Delhi’s Purana Qila have documented long habitation and Painted Grey Ware finds. The site is traditionally identified with Indraprastha, the Pandava capital in Mahabharata tradition.',
'दिल्ली के पुराना किला में पुरातात्त्विक उत्खननों ने दीर्घकालीन बसावट और चित्रित धूसर मृद्भांड के अवशेष दर्ज किए हैं। परंपरा में इस स्थल की पहचान महाभारत के पांडवों की राजधानी इंद्रप्रस्थ से की जाती है।',
'Excavations 1954 onward; renewed 2013–14, 2017–18, 2023','Archaeology / settlement history','पुरातत्त्व / बसावट इतिहास','Verified Painted Grey Ware and habitation evidence at the traditional Indraprastha location.','परंपरागत इंद्रप्रस्थ स्थल पर सत्यापित PGW और बसावट के प्रमाण।',['mahabharata','indraprastha','purana qila','painted grey ware'],
[src('ASI excavation at Purana Qila','Press Information Bureau, Ministry of Culture','https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1891800','Official release describing Painted Grey Ware finds and excavation goals.'),src('Ancient India — Indrapat/Purana Qila','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/87815.pdf','Older archaeological report records Painted Grey Ware from Indrapat/Purana Qila.')],
[section('Archaeological record','पुरातात्त्विक रिकॉर्ड','ASI excavations have documented multiple historical layers and Painted Grey Ware at the site. Government archaeology publications describe the mound as Indrapat/Indraprastha in the context of the traditional identification.','ASI उत्खननों ने यहाँ अनेक ऐतिहासिक परतें और Painted Grey Ware दर्ज किया है। सरकारी पुरातात्त्विक प्रकाशन इस स्थल को परंपरागत पहचान के संदर्भ में इंद्रपत/इंद्रप्रस्थ नाम से भी दर्ज करते हैं।'),section('How the app labels it','ऐप इसे कैसे दिखाता है','The physical finds are presented as verified archaeology. The identification with the Pandava capital is presented as a longstanding historical tradition attached to the location.','भौतिक अवशेषों को प्रमाणित पुरातत्त्व के रूप में दिखाया जाता है। पांडव राजधानी से पहचान को इस स्थान से जुड़ी दीर्घकालीन ऐतिहासिक परंपरा के रूप में अलग दिखाया जाता है।')]),
epic_item(
'dwarka-underwater-archaeology','Dwarka and Bet Dwarka Underwater Archaeology','द्वारका और बेट द्वारका का समुद्री पुरातत्त्व',
'Underwater and coastal archaeology around Dwarka and Bet Dwarka has documented stone anchors, structural remains, pottery and evidence of long maritime activity. The region is also one of the central sacred landscapes of Krishna tradition.',
'द्वारका और बेट द्वारका के आसपास समुद्री तथा तटीय पुरातत्त्व में पत्थर के लंगर, संरचनात्मक अवशेष, मृद्भांड और दीर्घकालीन समुद्री गतिविधि के प्रमाण मिले हैं। यह क्षेत्र श्रीकृष्ण परंपरा का प्रमुख पवित्र भू-दृश्य भी है।',
'NIO underwater explorations since the 1980s','Marine archaeology','समुद्री पुरातत्त्व','Verified ancient maritime activity and archaeological remains in the Dwarka region.','द्वारका क्षेत्र में सत्यापित प्राचीन समुद्री गतिविधि और पुरातात्त्विक अवशेष।',['mahabharata','krishna','dwarka','marine archaeology','anchors'],
[src('Recent Underwater Explorations at Dwarka and Surroundings of Okha Mandal','CSIR–National Institute of Oceanography','https://drs.nio.org/drs/bitstream/2264/479/1/Man_Environ_25_67.pdf','Reports underwater and onshore archaeological finds.'),src('An ancient harbour at Dwarka','Current Science / NIO researchers','https://www.researchgate.net/publication/27667093_An_ancient_harbour_at_Dwarka_Study_based_on_the_recent_underwater_explorations','Research article on harbour remains and stone anchors.')],
[section('Key finds','मुख्य खोजें','Researchers recorded numerous stone anchors and submerged or intertidal structural remains, supporting the interpretation of Dwarka as an important historical harbour and maritime centre.','शोधकर्ताओं ने अनेक पत्थर के लंगर और जलमग्न/ज्वारीय संरचनात्मक अवशेष दर्ज किए, जो द्वारका के ऐतिहासिक बंदरगाह और समुद्री केंद्र होने को मजबूत करते हैं।'),section('Connection with Krishna tradition','कृष्ण परंपरा से संबंध','Dwarka has a deep and continuous sacred association with Krishna. Archaeology securely establishes ancient settlement and maritime activity in the region; the sacred narrative and the archaeological chronology are shown side by side.','द्वारका का श्रीकृष्ण से अत्यंत गहरा और जीवित पवित्र संबंध है। पुरातत्त्व क्षेत्र की प्राचीन बसावट और समुद्री गतिविधि को प्रमाणित करता है; पवित्र कथा और पुरातात्त्विक कालक्रम को ऐप साथ-साथ लेकिन अलग श्रेणी में दिखाता है।')]),
epic_item(
'heliodorus-vasudeva-inscription','Heliodorus Pillar and the Worship of Vasudeva','हेलियोडोरस स्तंभ और वासुदेव उपासना',
'The Heliodorus pillar at Besnagar records that Heliodorus, an ambassador associated with the Indo-Greek king Antialkidas, erected a Garuda pillar in honour of Vasudeva and identified himself as a Bhagavata. It is major epigraphic evidence for early Vasudeva-Krishna devotion.',
'बेसनगर का हेलियोडोरस स्तंभ दर्ज करता है कि इंडो-यूनानी राजा एंटियाल्किदास से जुड़े दूत हेलियोडोरस ने वासुदेव के सम्मान में गरुड़-ध्वज स्थापित किया और स्वयं को भागवत कहा। यह प्रारंभिक वासुदेव-कृष्ण भक्ति का महत्वपूर्ण अभिलेखीय प्रमाण है।',
'2nd century BCE','Inscription / epigraphy','अभिलेख / पुरालेख-विज्ञान','Direct inscriptional evidence for Vasudeva worship in the late centuries BCE.','ईसा पूर्व की अंतिम शताब्दियों में वासुदेव उपासना का प्रत्यक्ष अभिलेखीय प्रमाण।',['krishna','vasudeva','heliodorus','inscription','bhagavata'],
[src('The Garuda Pillar of Besnagar','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/21831.pdf','Early archaeological publication of the Heliodorus inscription.'),src('Early Inscriptions of Mathura','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/66430.pdf','Discusses Vasudeva-Krishna worship and related inscriptions.')],
[section('What the inscription says','अभिलेख क्या बताता है','The record identifies the monument as a Garudadhvaja dedicated to Vasudeva and calls Heliodorus a Bhagavata. Because the text is inscribed on the monument itself, it is direct epigraphic evidence.','अभिलेख स्मारक को वासुदेव के लिए स्थापित गरुड़ध्वज बताता है और हेलियोडोरस को भागवत कहता है। चूँकि यह सूचना स्वयं स्मारक पर उत्कीर्ण है, इसलिए यह प्रत्यक्ष अभिलेखीय प्रमाण है।'),section('Historical importance','ऐतिहासिक महत्व','The pillar demonstrates that Vasudeva devotion was established enough in the second century BCE to receive monumental patronage and to attract a foreign-born devotee or patron.','यह स्तंभ दिखाता है कि दूसरी शताब्दी ईसा पूर्व तक वासुदेव-भक्ति इतनी स्थापित थी कि उसके लिए स्मारकीय दान हुआ और एक विदेशी मूल के दूत ने स्वयं को भागवत कहा।')]),
epic_item(
'ghosundi-nanaghat-vasudeva-evidence','Ghosundi, Nanaghat and Early Vasudeva–Sankarshana Evidence','घोसुंडी, नाणेघाट और प्रारंभिक वासुदेव–संकर्षण प्रमाण',
'Early inscriptions from the centuries around the beginning of the Common Era contain references connected with Vasudeva and Sankarshana, adding to the epigraphic record of early Bhagavata/Vrishni-related worship.',
'ईसा-पूर्व की अंतिम और ईस्वी की आरंभिक शताब्दियों के अभिलेखों में वासुदेव और संकर्षण से जुड़े उल्लेख मिलते हैं। ये प्रारंभिक भागवत/वृष्णि-सम्बद्ध उपासना के अभिलेखीय रिकॉर्ड को मजबूत करते हैं।',
'Late centuries BCE','Epigraphy','अभिलेख-विज्ञान','Direct early inscriptional evidence for named deities associated with Krishna-Vasudeva traditions.','कृष्ण-वासुदेव परंपराओं से जुड़े नामित देव-रूपों का प्रारंभिक प्रत्यक्ष अभिलेखीय प्रमाण।',['krishna','vasudeva','sankarshana','ghosundi','nanaghat','inscription'],
[src('Historicity of Krishna — epigraphic evidence survey','IGNCA / Archaeological Survey publications','https://ignca.gov.in/Asi_data/4821.pdf','Summarizes Besnagar, Ghosundi, Nanaghat, Mora and related epigraphic evidence.'),src('Early Inscriptions of Mathura','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/66430.pdf')],
[section('Why inscriptions matter','अभिलेख क्यों महत्वपूर्ण हैं','Inscriptions are datable material records created in historical settings. They help establish when named forms such as Vasudeva and Sankarshana were publicly worshipped or commemorated.','अभिलेख ऐतिहासिक परिस्थितियों में बनाए गए तिथि-निर्धारण योग्य भौतिक दस्तावेज़ हैं। वे यह स्थापित करने में सहायता करते हैं कि वासुदेव और संकर्षण जैसे नामित देव-रूपों की सार्वजनिक उपासना या स्मृति कब तक स्थापित थी।')]),
epic_item(
'mahabharata-geography-pgw-network','Mahabharata Geography and the Painted Grey Ware Network','महाभारत भूगोल और Painted Grey Ware नेटवर्क',
'Painted Grey Ware has been reported from several sites that also carry names associated with Mahabharata geography, including Hastinapura, Kurukshetra and Indrapat/Indraprastha. Archaeology establishes a shared Iron Age material horizon across parts of the region.',
'Painted Grey Ware कई ऐसे स्थलों से मिला है जिनके नाम महाभारत भूगोल से भी जुड़े हैं—जैसे हस्तिनापुर, कुरुक्षेत्र और इंद्रपत/इंद्रप्रस्थ। पुरातत्त्व इस क्षेत्र के कई हिस्सों में लौह-युगीन साझा भौतिक संस्कृति की उपस्थिति स्थापित करता है।',
'Iron Age, broadly first millennium BCE','Regional archaeology','क्षेत्रीय पुरातत्त्व','Verified distribution of an archaeological culture across multiple epic-associated place names.','महाकाव्य-सम्बद्ध अनेक स्थान-नामों पर एक पुरातात्त्विक संस्कृति की सत्यापित उपस्थिति।',['mahabharata','painted grey ware','kurukshetra','hastinapura','indraprastha'],
[src('Excavation at Hastinapura and Other Explorations','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/87815.pdf','Lists Painted Grey Ware from multiple sites associated by tradition with Mahabharata geography.'),src('The Iron Age in India — Purana Qila','Archaeological Survey of India / IGNCA','https://ignca.gov.in/Asi_data/73624.pdf')],
[section('What is directly established','सीधे क्या स्थापित है','The ware, settlement layers and associated artefacts are archaeological facts. Their distribution helps reconstruct Iron Age settlement patterns in the upper Ganga-Yamuna region.','मृद्भांड, बसावट-परतें और संबंधित पुरावशेष पुरातात्त्विक तथ्य हैं। उनका वितरण ऊपरी गंगा-यमुना क्षेत्र के लौह-युगीन बसावट-पैटर्न को समझने में मदद करता है।'),section('Why the epic geography is interesting','महाकाव्य भूगोल क्यों महत्वपूर्ण है','The overlap between archaeological sites and traditional epic place names made these locations important for research. The app keeps the physical archaeological record distinct from any single proposed date for the Mahabharata war.','पुरातात्त्विक स्थलों और परंपरागत महाकाव्य-स्थान नामों का मेल इन्हें शोध के लिए महत्वपूर्ण बनाता है। ऐप भौतिक पुरातात्त्विक रिकॉर्ड को महाभारत युद्ध की किसी एक प्रस्तावित तारीख से अलग रखता है।')]),
]

for x in new:
    if x['slug'] in by_slug:
        by_slug[x['slug']].update(x)
    else:
        items.append(x); by_slug[x['slug']]=x

# Add relationships after new items exist.
relmap={
'ramayana-sites-archaeology-project':['traditional-ramayana-era','rama-setu-geography','sringaverapura-archaeology','ramayana-temple-reliefs','ramayana-manuscript-tradition'],
'sringaverapura-archaeology':['ramayana-sites-archaeology-project','traditional-ramayana-era','sacred-geography'],
'rama-setu-geography':['traditional-ramayana-era','ramayana-sites-archaeology-project','sacred-geography'],
'ramayana-temple-reliefs':['traditional-ramayana-era','ramayana-manuscript-tradition','temple-architecture'],
'ramayana-manuscript-tradition':['itihasa','traditional-ramayana-era','ramayana-temple-reliefs'],
'hastinapura-excavation-evidence':['traditional-mahabharata-era','mahabharata-geography-pgw-network','purana-qila-indraprastha-archaeology'],
'purana-qila-indraprastha-archaeology':['traditional-mahabharata-era','hastinapura-excavation-evidence','mahabharata-geography-pgw-network'],
'dwarka-underwater-archaeology':['traditional-mahabharata-era','krishna','heliodorus-vasudeva-inscription'],
'heliodorus-vasudeva-inscription':['krishna','dwarka-underwater-archaeology','ghosundi-nanaghat-vasudeva-evidence'],
'ghosundi-nanaghat-vasudeva-evidence':['krishna','heliodorus-vasudeva-inscription'],
'mahabharata-geography-pgw-network':['traditional-mahabharata-era','hastinapura-excavation-evidence','purana-qila-indraprastha-archaeology'],
'traditional-ramayana-era':['rama','formation-of-epic-traditions','ramayana-sites-archaeology-project','rama-setu-geography'],
'traditional-mahabharata-era':['krishna','formation-of-epic-traditions','hastinapura-excavation-evidence','dwarka-underwater-archaeology'],
}
for s,rels in relmap.items():
    if s in by_slug: by_slug[s]['relatedSlugs']=rels

# Re-run context insertion for newly added Epic Evidence if needed.
lookup={x['slug']:(x.get('titleEn') or x.get('title'),x.get('titleHi') or x.get('title')) for x in items}
for x in items:
    if x.get('category')=='Epic Evidence' and not any((s.get('titleEn')=='How to read this evidence') for s in x.get('sections',[])):
        en_t,hi_t,en_tpl,hi_tpl=category_context['Epic Evidence']
        x['sections'].insert(0,section(en_t,hi_t,en_tpl.format(title=x['titleEn'],title_hi=x['titleHi']),hi_tpl.format(title=x['titleEn'],title_hi=x['titleHi'])))

content_path.write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')

# ---------- Hindu text catalog: richer detail fields and principal-text overrides ----------
texts=json.loads(texts_path.read_text(encoding='utf-8'))

upanishad_focus={
'isha-upanishad':('Renunciation and action, the indwelling divine, unity of life and a vision that holds knowledge and action together.','त्याग और कर्म, सर्वव्यापी ईशत्व, जीवन की एकता तथा ज्ञान और कर्म को साथ रखने की दृष्टि।'),
'kena-upanishad':('Asks what power enables mind, speech, sight and hearing, leading the student toward Brahman beyond the ordinary faculties.','यह पूछता है कि मन, वाणी, दृष्टि और श्रवण को शक्ति कौन देता है, और साधक को इंद्रिय-बोध से परे ब्रह्मन् की ओर ले जाता है।'),
'katha-upanishad':('The dialogue of Nachiketa and Yama explores death, the immortal Self, disciplined choice and the path to liberation.','नचिकेता और यम का संवाद मृत्यु, अमर आत्मन्, श्रेय-प्रेय के चयन और मोक्ष के मार्ग पर केंद्रित है।'),
'prashna-upanishad':('Six students ask six structured questions on creation, prana, states of consciousness, Om and the human person.','छह जिज्ञासु सृष्टि, प्राण, चेतना की अवस्थाओं, ॐ और मानव अस्तित्व पर छह व्यवस्थित प्रश्न पूछते हैं।'),
'mundaka-upanishad':('Distinguishes higher and lower knowledge, uses the image of two birds, and teaches knowledge of Brahman as the highest goal.','परा और अपरा विद्या का भेद, दो पक्षियों का प्रसिद्ध रूपक और ब्रह्मविद्या को परम लक्ष्य के रूप में प्रस्तुत करता है।'),
'mandukya-upanishad':('A very short but influential text that interprets Om through waking, dreaming, deep sleep and the “fourth” state, turiya.','अत्यंत संक्षिप्त लेकिन प्रभावशाली उपनिषद, जो जाग्रत, स्वप्न, सुषुप्ति और तुरीय के माध्यम से ॐ की व्याख्या करता है।'),
'taittiriya-upanishad':('Includes teachings on education, ethics, Brahman, bliss and the layered understanding of the person often discussed through the five koshas.','शिक्षा, आचार, ब्रह्मन्, आनंद और पंचकोश के माध्यम से मानव अस्तित्व की परतों पर महत्वपूर्ण शिक्षाएँ देता है।'),
'aitareya-upanishad':('Reflects on creation, birth and consciousness, including the celebrated insight that consciousness is fundamental to the self.','सृष्टि, जन्म और चेतना पर विचार करता है और चेतना को आत्म-स्वरूप से जोड़ने वाली महत्वपूर्ण शिक्षा देता है।'),
'chandogya-upanishad':('A large Upanishad containing teachings on meditation, Being, Om and the celebrated mahavakya “Tat Tvam Asi”.','एक विशाल उपनिषद जिसमें उपासना, सत्, ॐ और प्रसिद्ध महावाक्य “तत्त्वमसि” सहित अनेक शिक्षाएँ हैं।'),
'brihadaranyaka-upanishad':('One of the oldest and largest Upanishads, famous for Yajnavalkya’s dialogues, Gargi and Maitreyi, “neti neti” and inquiry into Atman.','सबसे प्राचीन और विशाल उपनिषदों में से एक; याज्ञवल्क्य, गार्गी और मैत्रेयी के संवाद, “नेति नेति” और आत्मन् की खोज के लिए प्रसिद्ध।'),
'shvetashvatara-upanishad':('Brings together themes of Brahman, Ishvara/Rudra, yoga, devotion and the relation between the divine, nature and the individual self.','ब्रह्मन्, ईश्वर/रुद्र, योग, भक्ति तथा ईश्वर, प्रकृति और जीव के संबंध पर केंद्रित महत्वपूर्ण उपनिषद।'),
'kaushitaki-upanishad':('Discusses prana, consciousness, rebirth and the path of the soul in a set of philosophical dialogues.','प्राण, चेतना, पुनर्जन्म और जीव की गति पर दार्शनिक संवादों के माध्यम से विचार करता है।'),
'maitri-upanishad':('Explores mind, time, self-knowledge and yoga in a later Upanishadic synthesis.','मन, काल, आत्मज्ञान और योग को बाद की उपनिषदिक समन्वयात्मक शैली में प्रस्तुत करता है।'),
}
major_overrides={
'rigveda':('Ten mandalas containing more than a thousand hymns to deities such as Agni, Indra, Soma, Ushas and others, along with cosmological and philosophical hymns.','दस मंडलों में एक हजार से अधिक सूक्त; अग्नि, इंद्र, सोम, उषा आदि देवताओं की स्तुतियों के साथ सृष्टि और दर्शन से जुड़े प्रसिद्ध सूक्त भी।','The oldest of the four Vedas and a primary source for Vedic language, ritual poetry and early religious thought.','चार वेदों में सबसे प्राचीन; वैदिक भाषा, मंत्र-काव्य और प्रारंभिक धार्मिक चिंतन का मूल स्रोत।'),
'samaveda':('A liturgical collection in which most verses derive from the Rigveda but are arranged for melodic chanting in Soma ritual.','मुख्यतः ऋग्वैदिक मंत्रों को सोम-यज्ञ में सामगान के लिए विशेष संगीतात्मक क्रम में व्यवस्थित किया गया है।','Essential for understanding the musical and liturgical dimension of Vedic ritual.','वैदिक अनुष्ठान के संगीतात्मक और गायन-पक्ष को समझने के लिए अत्यंत महत्वपूर्ण।'),
'yajurveda':('Prose formulas and verses used by the officiating priest during sacrifice; preserved in Shukla (White) and Krishna (Black) Yajurveda traditions.','यज्ञ में अध्वर्यु पुरोहित द्वारा प्रयुक्त मंत्र और गद्यात्मक यजुष; शुक्ल और कृष्ण यजुर्वेद की प्रमुख परंपराओं में संरक्षित।','A key source for reconstructing Vedic ritual procedure and its symbolic interpretation.','वैदिक यज्ञ-विधि और उसके प्रतीकात्मक अर्थ को समझने का प्रमुख स्रोत।'),
'atharvaveda':('Hymns and rites concerning healing, protection, household life, kingship, social concerns and speculative themes.','आरोग्य, रक्षा, गृहस्थ जीवन, राजधर्म, सामाजिक विषयों और दार्शनिक चिंतन से जुड़े सूक्त और विधियाँ।','Shows the breadth of Vedic religious life beyond the large public sacrifice.','बड़े सार्वजनिक यज्ञों से परे वैदिक धार्मिक जीवन की व्यापकता को समझने में सहायक।'),
'valmiki-ramayana':('Traditionally arranged in seven kandas, narrating Rama’s life from Ayodhya through exile, the search for Sita, the war in Lanka and the return to Ayodhya.','परंपरागत रूप से सात कांडों में व्यवस्थित; अयोध्या से वनवास, सीता की खोज, लंका युद्ध और अयोध्या वापसी तक श्रीराम की कथा।','A foundational Itihasa text for Rama traditions, dharma reflection, poetry, performance and sacred geography.','राम-परंपरा, धर्म-चिंतन, काव्य, नाट्य और पवित्र भूगोल का आधारभूत इतिहास-ग्रंथ।'),
'mahabharata':('Traditionally arranged in eighteen parvas, combining the Kuru-Pandava narrative with philosophy, law, pilgrimage, political thought, legends and the Bhagavad Gita.','परंपरागत रूप से अठारह पर्वों में; कुरु-पांडव कथा के साथ दर्शन, धर्म, तीर्थ, राजनीति, आख्यान और भगवद्गीता का विशाल संग्रह।','One of the world’s largest epic traditions and a central source for Hindu reflection on dharma under difficult circumstances.','विश्व की सबसे विशाल महाकाव्य परंपराओं में से एक; जटिल परिस्थितियों में धर्म पर हिंदू चिंतन का केंद्रीय स्रोत।'),
'bhagavad-gita':('Eighteen chapters presenting Krishna’s teaching to Arjuna on action, knowledge, devotion, yoga, the Self, God and liberation.','अठारह अध्यायों में अर्जुन को श्रीकृष्ण का कर्म, ज्ञान, भक्ति, योग, आत्मन्, ईश्वर और मोक्ष पर उपदेश।','A compact synthesis of major Hindu spiritual paths and one of the most widely commented texts in Indian philosophy.','हिंदू साधना-पथों का अत्यंत प्रभावशाली समन्वय और भारतीय दर्शन में सर्वाधिक टीकित ग्रंथों में से एक।'),
'yoga-sutras':('A concise sutra text in four padas systematizing yoga, mental discipline, samadhi, obstacles, practices and liberation.','चार पादों में योग, चित्त-अनुशासन, समाधि, बाधाएँ, साधन और कैवल्य का सूत्रबद्ध विवेचन।','The classical reference text for the Yoga darshana and later commentarial traditions.','योग दर्शन और उसकी बाद की टीका-परंपरा का प्रमुख शास्त्रीय ग्रंथ।'),
'ashtadhyayi':('Eight chapters of highly compressed grammatical rules describing Sanskrit through an exceptionally systematic generative framework.','आठ अध्यायों में अत्यंत संक्षिप्त सूत्रों द्वारा संस्कृत व्याकरण का असाधारण रूप से व्यवस्थित विश्लेषण।','A landmark in the history of grammar and formal analysis.','व्याकरण और औपचारिक विश्लेषण के इतिहास की महान उपलब्धियों में से एक।'),
'arthashastra':('A systematic work on statecraft, administration, taxation, law, diplomacy, intelligence, war and economic management.','राज्य-व्यवस्था, प्रशासन, कर, कानून, कूटनीति, गुप्तचर, युद्ध और अर्थ-प्रबंधन पर व्यवस्थित ग्रंथ।','Important for studying classical Indian political thought and administrative theory.','शास्त्रीय भारतीय राजनीति और प्रशासनिक चिंतन के अध्ययन का प्रमुख स्रोत।'),
'natyashastra':('A wide-ranging treatise on drama, performance, rasa, acting, music, dance, stagecraft and aesthetics.','नाटक, अभिनय, रस, संगीत, नृत्य, रंगमंच और सौंदर्यशास्त्र का विस्तृत शास्त्र।','Foundational for the theory and vocabulary of many Indian performing arts.','भारतीय नाट्य और प्रदर्शन कलाओं के सिद्धांत और पारिभाषिक शब्दावली का आधारभूत ग्रंथ।'),
'surya-siddhanta':('A classical Sanskrit astronomical text dealing with planetary calculations, time reckoning, eclipses, trigonometric procedures and calendrical astronomy.','ग्रह-गणना, कालगणना, ग्रहण, त्रिकोणमितीय विधियों और पंचांग-खगोल पर शास्त्रीय संस्कृत ग्रंथ।','A major source for the mathematical astronomy underlying many later Indian calendrical traditions.','बाद की अनेक भारतीय पंचांग परंपराओं के गणितीय खगोल-विज्ञान का महत्वपूर्ण स्रोत।'),
'aryabhatiya':('Aryabhata’s concise mathematical-astronomical work covering arithmetic, algebraic procedures, trigonometry, time calculation and planetary astronomy.','आर्यभट का संक्षिप्त गणित-खगोल ग्रंथ; अंकगणित, गणितीय विधियाँ, त्रिकोणमिति, कालगणना और ग्रह-खगोल इसके प्रमुख विषय हैं।','Central for understanding the development of classical Indian mathematical astronomy.','शास्त्रीय भारतीय गणितीय खगोल-विज्ञान के विकास को समझने का केंद्रीय ग्रंथ।'),
'brahmasphutasiddhanta':('Brahmagupta’s major work on mathematics and astronomy, including systematic arithmetic rules for positive and negative quantities and zero.','ब्रह्मगुप्त का प्रमुख गणित-खगोल ग्रंथ, जिसमें धन-ऋण संख्याओं और शून्य से संबंधित व्यवस्थित अंकगणितीय नियम भी हैं।','A milestone in the history of Indian arithmetic, algebra and astronomy.','भारतीय अंकगणित, बीजगणित और खगोल के इतिहास का महत्वपूर्ण मील का पत्थर।'),
'sushruta-samhita':('A classical medical compendium with extensive material on surgery, anatomy, wounds, fractures, instruments, training, therapeutics and medical ethics.','शल्य-चिकित्सा, शरीररचना, घाव, अस्थिभंग, उपकरण, प्रशिक्षण, उपचार और चिकित्सकीय आचार पर विस्तृत शास्त्रीय चिकित्सा-संहिता।','A primary historical source for the surgical and medical traditions associated with Sushruta.','सुश्रुत से जुड़ी शल्य और चिकित्सा परंपरा का प्रमुख ऐतिहासिक स्रोत।'),
'charaka-samhita':('A classical Ayurvedic medical compendium emphasizing diagnosis, internal medicine, causes of disease, therapeutics, diet and physician ethics.','निदान, कायचिकित्सा, रोग-कारण, उपचार, आहार और चिकित्सक-आचार पर केंद्रित शास्त्रीय आयुर्वेदिक संहिता।','A foundational source for the history and theory of classical Ayurveda.','शास्त्रीय आयुर्वेद के इतिहास और सिद्धांत का आधारभूत स्रोत।'),
}

cat_themes={
'Veda & Vedic Corpus':('Vedic recitation, ritual, cosmology, early theology and the transition from mantra to philosophical reflection.','वैदिक मंत्र, अनुष्ठान, सृष्टि-विचार, देवता-चिंतन और मंत्र से दर्शन की ओर विकास।'),
'Upanishads':('Atman, Brahman, consciousness, meditation, death, rebirth, knowledge and liberation.','आत्मन्, ब्रह्मन्, चेतना, ध्यान, मृत्यु, पुनर्जन्म, ज्ञान और मोक्ष।'),
'Itihasa & Gita':('Dharma in action, sacred narrative, kingship, family, devotion, yoga and philosophical teaching.','जीवन में धर्म, पवित्र कथा, राजधर्म, परिवार, भक्ति, योग और दार्शनिक शिक्षा।'),
'Puranas':('Deity traditions, cosmology, genealogies, sacred geography, pilgrimage, vrata, festivals and devotional narratives.','देव-परंपराएँ, सृष्टि-विचार, वंशावलियाँ, पवित्र भूगोल, तीर्थ, व्रत, पर्व और भक्ति-कथाएँ।'),
'Dharma & Law':('Dharma, conduct, legal procedure, inheritance, penance, social norms and duties.','धर्म, आचार, न्याय-प्रक्रिया, उत्तराधिकार, प्रायश्चित्त, सामाजिक नियम और कर्तव्य।'),
'Darshana':('Logic, knowledge, metaphysics, language, causation, self, world and liberation.','तर्क, ज्ञान, तत्वमीमांसा, भाषा, कारण-कार्य, आत्मा, जगत और मोक्ष।'),
'Vedanta & Commentary':('Interpretation of Upanishads, Brahma Sutras and Gita, and debates over Brahman, self, world and devotion.','उपनिषद, ब्रह्मसूत्र और गीता की व्याख्या तथा ब्रह्मन्, जीव, जगत और भक्ति पर बहस।'),
'Agama & Tantra':('Temple ritual, mantra, initiation, deity visualization, yoga, cosmology and sacred architecture.','मंदिर-अनुष्ठान, मंत्र, दीक्षा, देव-ध्यान, योग, सृष्टि-विचार और पवित्र स्थापत्य।'),
'Yoga':('Meditation, body-breath disciplines, samadhi, liberation and different systems of yogic practice.','ध्यान, शरीर-श्वास अनुशासन, समाधि, मुक्ति और योग की विविध साधना-पद्धतियाँ।'),
'Bhakti & Regional':('Devotional poetry, vernacular theology, sacred biography, temple culture and regional retellings.','भक्ति-काव्य, लोकभाषा दर्शन, संत-चरित, मंदिर-संस्कृति और क्षेत्रीय पुनर्कथन।'),
'Knowledge Texts':('Grammar, medicine, mathematics, astronomy, arts, statecraft and other classical knowledge disciplines.','व्याकरण, चिकित्सा, गणित, खगोल, कला, राज्यशास्त्र और अन्य शास्त्रीय ज्ञान-विषय।'),
}
cat_why={
'Veda & Vedic Corpus':('Read it to understand the oldest textual layers that later Hindu traditions repeatedly reinterpret.','बाद की हिंदू परंपराओं द्वारा बार-बार पुनर्व्याख्यायित सबसे प्राचीन ग्रंथीय परतों को समझने के लिए।'),
'Upanishads':('Read it for primary philosophical reflections that became foundational to Vedanta and many modern discussions of Hindu philosophy.','वेदांत और आधुनिक हिंदू दर्शन के अनेक विमर्शों की आधारभूत दार्शनिक शिक्षाओं को मूल रूप में समझने के लिए।'),
'Itihasa & Gita':('Read it to see dharma, devotion and philosophy explored through narrative, dialogue and difficult human choices.','कथा, संवाद और कठिन मानवीय निर्णयों के माध्यम से धर्म, भक्ति और दर्शन को समझने के लिए।'),
'Puranas':('Read it to understand the narrative, ritual and pilgrimage worlds that shape much of living Hindu devotion.','जीवित हिंदू भक्ति को आकार देने वाली कथा, अनुष्ठान और तीर्थ-परंपरा को समझने के लिए।'),
'Dharma & Law':('Read it as historical normative literature and compare different texts rather than treating one work as the sole Hindu law book.','इसे ऐतिहासिक मानक-साहित्य की तरह पढ़ें और एक ग्रंथ को अकेली “हिंदू कानून-पुस्तक” मानने के बजाय विभिन्न ग्रंथों की तुलना करें।'),
'Darshana':('Read it to understand the rigor of Indian debate about knowledge, reality and liberation.','ज्ञान, वास्तविकता और मोक्ष पर भारतीय दार्शनिक बहस की गहराई को समझने के लिए।'),
'Vedanta & Commentary':('Read it to compare how major teachers interpret the same foundational scriptures differently.','एक ही आधारभूत ग्रंथों की प्रमुख आचार्य-परंपराएँ अलग-अलग व्याख्या कैसे करती हैं, यह समझने के लिए।'),
'Agama & Tantra':('Read it to understand the textual foundations of many temple, mantra and deity-centered practices.','अनेक मंदिर, मंत्र और देव-उपासना परंपराओं की ग्रंथीय पृष्ठभूमि समझने के लिए।'),
'Yoga':('Read it to distinguish classical yogic systems from modern exercise-only descriptions of yoga.','योग को केवल आधुनिक व्यायाम तक सीमित न करके उसकी शास्त्रीय साधना-पद्धतियों को समझने के लिए।'),
'Bhakti & Regional':('Read it to experience Hindu thought in regional languages, poetry, song and lived devotional communities.','क्षेत्रीय भाषाओं, कविता, भजन और जीवित भक्ति-समुदायों में हिंदू चिंतन को समझने के लिए।'),
'Knowledge Texts':('Read it to understand the breadth of classical Indian intellectual traditions beyond explicitly religious literature.','स्पष्ट धार्मिक साहित्य से आगे शास्त्रीय भारतीय बौद्धिक परंपराओं की व्यापकता समझने के लिए।'),
}

for t in texts:
    cat=t.get('category','')
    themes=cat_themes.get(cat,('Key ideas, textual structure and place in Hindu intellectual history.','मुख्य विचार, ग्रंथ-रचना और हिंदू बौद्धिक इतिहास में स्थान।'))
    why=cat_why.get(cat,('Read it to understand its place in the larger Hindu textual tradition.','विस्तृत हिंदू ग्रंथ-परंपरा में इसका स्थान समझने के लिए।'))
    t['keyThemesEn']=themes[0]; t['keyThemesHi']=themes[1]
    t['whyReadEn']=why[0]; t['whyReadHi']=why[1]
    t['structureEn']=f"{t.get('titleEn')} is a {t.get('kindEn','text').lower()} within the {t.get('category')} family. Its internal organization depends on the recension, edition or manuscript tradition used."
    t['structureHi']=f"{t.get('titleHi')} {t.get('categoryHi')} परंपरा का {t.get('kindHi','ग्रंथ')} है। इसकी आंतरिक रचना प्रयुक्त शाखा, संस्करण या पांडुलिपि-परंपरा के अनुसार कुछ भिन्न हो सकती है।"
    t['studyNoteEn']='Begin with a reliable edition or translation, keep the text’s genre in mind, and distinguish the original text from later commentary.'
    t['studyNoteHi']='विश्वसनीय संस्करण या अनुवाद से पढ़ें, ग्रंथ की विधा को ध्यान में रखें और मूल पाठ को बाद की टीका से अलग पहचानें।'
    if t['slug'] in upanishad_focus:
        en,hi=upanishad_focus[t['slug']]
        t['descriptionEn']=en; t['descriptionHi']=hi
        t['keyThemesEn']=en; t['keyThemesHi']=hi
    if t['slug'] in major_overrides:
        desc_en,desc_hi,why_en,why_hi=major_overrides[t['slug']]
        t['descriptionEn']=desc_en; t['descriptionHi']=desc_hi; t['whyReadEn']=why_en; t['whyReadHi']=why_hi

texts_path.write_text(json.dumps(texts,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Enhanced {len(items)} knowledge entries and {len(texts)} text records for v0.7')
