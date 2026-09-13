from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'SanatanGyan'/'Resources'/'Raw'
content_path=RAW/'sanatan_content.json'
texts_path=RAW/'sanatan_texts.json'
items=json.loads(content_path.read_text(encoding='utf-8'))
by={x['slug']:x for x in items}

# Add two more source-grounded epic-context entries.
new_items=[
{
'id':'epic-ayodhya-archaeology','slug':'ayodhya-long-settlement-archaeology','title':'Ayodhya: Archaeology of a Long-Lived Sacred City','titleEn':'Ayodhya: Archaeology of a Long-Lived Sacred City','titleHi':'अयोध्या: दीर्घकालीन पवित्र नगर का पुरातत्त्व','subtitleEn':'Settlement history and Ramayana sacred geography','subtitleHi':'बसावट-इतिहास और रामायण का पवित्र भूगोल','category':'Epic Evidence','level':'Advanced',
'summaryEn':'Archaeological work in Ayodhya has documented a long sequence of human occupation and material culture. Ayodhya is simultaneously one of the most important sacred places in the Rama tradition, so the app presents the excavated settlement history and the living Ramayana association together with clear labels.',
'summaryHi':'अयोध्या में हुए पुरातात्त्विक अध्ययनों ने दीर्घकालीन मानवीय बसावट और भौतिक संस्कृति की अनेक परतें दर्ज की हैं। साथ ही अयोध्या श्रीराम-परंपरा के सबसे महत्वपूर्ण पवित्र स्थलों में है; इसलिए ऐप उत्खनित बसावट-इतिहास और जीवित रामायण-संबंध को स्पष्ट लेबल के साथ साथ रखता है।',
'bodyEn':'','bodyHi':'','evidenceLevel':'Strong Evidence','claimVerdict':'Supported','dateLabel':'Archaeological studies of Ayodhya','evidenceTypeEn':'Archaeology / sacred geography','evidenceTypeHi':'पुरातत्त्व / पवित्र भूगोल','evidenceScopeEn':'Verified long-term archaeological occupation at Ayodhya and its documented place in Ramayana sacred geography.','evidenceScopeHi':'अयोध्या की सत्यापित दीर्घकालीन पुरातात्त्विक बसावट और रामायण के पवित्र भूगोल में उसका दस्तावेजीकृत स्थान।','featured':True,
'tags':['ramayana','rama','ayodhya','archaeology','sacred geography'],'aliases':['Ayodhya archaeology','अयोध्या पुरातत्त्व'],'relatedSlugs':['traditional-ramayana-era','ramayana-sites-archaeology-project','sringaverapura-archaeology','rama-setu-geography'],
'sections':[
{'titleEn':'What archaeology directly records','titleHi':'पुरातत्त्व सीधे क्या दर्ज करता है','contentEn':'Excavated deposits, ceramics, structural remains and other material evidence show that Ayodhya has a deep and complex settlement history. Archaeology is especially useful for reconstructing how the city developed across different periods.','contentHi':'उत्खनित परतें, मृद्भांड, संरचनात्मक अवशेष और अन्य भौतिक सामग्री बताती है कि अयोध्या का बसावट-इतिहास दीर्घ और जटिल है। पुरातत्त्व अलग-अलग कालों में नगर के विकास को समझने का प्रत्यक्ष साधन देता है।'},
{'titleEn':'Place in the Rama tradition','titleHi':'श्रीराम परंपरा में स्थान','contentEn':'Across Hindu sacred geography, Ayodhya is revered as the city of Shri Rama and is central to Ramayana memory, pilgrimage and worship. This cultural continuity is a distinct historical fact about the place, alongside the archaeological sequence.','contentHi':'हिंदू पवित्र भूगोल में अयोध्या श्रीराम की नगरी के रूप में पूजित है और रामायण-स्मृति, तीर्थ तथा उपासना का केंद्रीय स्थल है। यह दीर्घ सांस्कृतिक निरंतरता उस स्थान का एक अलग ऐतिहासिक तथ्य है, जिसे पुरातात्त्विक क्रम के साथ समझा जा सकता है।'}],
'sources':[{'title':'Archaeology of Ramayana Sites — Ayodhya','publisher':'Archaeological Survey of India / IGNCA archive','url':'https://ignca.gov.in/Asi_data/74144.pdf','note':'ASI archaeological study concerning Ayodhya in the Ramayana-sites research programme.'}]
},
{
'id':'epic-mora-vrishni','slug':'mora-well-vrishni-evidence','title':'Mora Well Inscription and Early Vrishni Worship','titleEn':'Mora Well Inscription and Early Vrishni Worship','titleHi':'मोरा कुआँ अभिलेख और प्रारंभिक वृष्णि उपासना','subtitleEn':'Early Mathura epigraphy connected with the Vrishni heroes','subtitleHi':'वृष्णि वीरों से जुड़ा प्रारंभिक मथुरा अभिलेख','category':'Epic Evidence','level':'Advanced',
'summaryEn':'The Mora Well inscription from the Mathura region belongs to the early historical epigraphic record of Vrishni hero worship. It is important material evidence for the antiquity of the religious tradition surrounding the Vrishnis in the Mathura cultural region associated with Krishna traditions.',
'summaryHi':'मथुरा क्षेत्र का मोरा कुआँ अभिलेख वृष्णि वीरों की उपासना से जुड़े प्रारंभिक ऐतिहासिक अभिलेखीय प्रमाणों में गिना जाता है। यह कृष्ण-परंपरा से जुड़े मथुरा सांस्कृतिक क्षेत्र में वृष्णि धार्मिक परंपरा की प्राचीनता के लिए महत्वपूर्ण भौतिक प्रमाण है।',
'bodyEn':'','bodyHi':'','evidenceLevel':'Strong Evidence','claimVerdict':'Supported','dateLabel':'Early historic Mathura epigraphy','evidenceTypeEn':'Epigraphy / religious history','evidenceTypeHi':'अभिलेख / धार्मिक इतिहास','evidenceScopeEn':'Verified inscriptional evidence for early Vrishni cultic traditions in the Mathura region.','evidenceScopeHi':'मथुरा क्षेत्र में प्रारंभिक वृष्णि उपासना-परंपरा का सत्यापित अभिलेखीय प्रमाण।','featured':True,
'tags':['mahabharata','krishna','vrishni','mathura','inscription'],'aliases':['Mora inscription','मोरा अभिलेख'],'relatedSlugs':['traditional-mahabharata-era','heliodorus-vasudeva-inscription','ghosundi-nanaghat-vasudeva-evidence','dwarka-underwater-archaeology'],
'sections':[
{'titleEn':'Why the inscription matters','titleHi':'यह अभिलेख क्यों महत्वपूर्ण है','contentEn':'Unlike a later literary retelling, an inscription is a material record fixed to a historical place and epigraphic context. The Mora evidence therefore helps historians trace the early public and cultic presence of Vrishni traditions in the Mathura region.','contentHi':'बाद की साहित्यिक पुनर्कथा से अलग, अभिलेख किसी ऐतिहासिक स्थान और अभिलेखीय संदर्भ में स्थित भौतिक दस्तावेज होता है। इसलिए मोरा का प्रमाण इतिहासकारों को मथुरा क्षेत्र में वृष्णि परंपरा की प्रारंभिक सार्वजनिक और उपासना-संबंधी उपस्थिति समझने में सहायता करता है।'},
{'titleEn':'Connection with Krishna traditions','titleHi':'कृष्ण-परंपरा से संबंध','contentEn':'Mathura and the Vrishni lineage are deeply connected with Krishna traditions. The inscription is best used as direct evidence for an early Vrishni religious setting, while the larger sacred narrative remains available in the Itihasa and later devotional traditions.','contentHi':'मथुरा और वृष्णि वंश का कृष्ण-परंपरा से गहरा संबंध है। यह अभिलेख प्रारंभिक वृष्णि धार्मिक परिवेश का प्रत्यक्ष प्रमाण है; व्यापक पवित्र कथा इतिहास-ग्रंथों और बाद की भक्ति-परंपराओं में संरक्षित है।'}],
'sources':[{'title':'Early Inscriptions of Mathura','publisher':'Archaeological Survey of India / IGNCA archive','url':'https://ignca.gov.in/Asi_data/66430.pdf','note':'Epigraphic corpus for early Mathura, including records relevant to Vrishni traditions.'}]
}
]
for x in new_items:
    if x['slug'] not in by:
        items.append(x); by[x['slug']]=x

# Strong verified-fact details: replace generic boilerplate with topic-specific explanation.
fact_sections={
'fact-aryabhata-earth-rotation':[
('Textual statement','ग्रंथीय कथन','Aryabhata explains the apparent westward movement of the stars through the rotation of the Earth, using the familiar analogy of a person in a moving boat who sees stationary objects appear to move in the opposite direction.','आर्यभट तारों की पश्चिम की ओर दिखाई देने वाली गति को पृथ्वी के घूर्णन से समझाते हैं और चलती नाव में बैठे व्यक्ति को स्थिर वस्तुओं के विपरीत दिशा में चलते दिखाई देने की प्रसिद्ध उपमा देते हैं।'),
('Historical significance','ऐतिहासिक महत्व','This is a documented example of rotational reasoning in classical Indian mathematical astronomy. The app keeps this specific textual achievement distinct from broader claims about a complete modern heliocentric system.','यह शास्त्रीय भारतीय गणितीय खगोल-विज्ञान में घूर्णन संबंधी तर्क का दस्तावेजीकृत उदाहरण है। ऐप इस विशिष्ट ग्रंथीय उपलब्धि को अन्य व्यापक आधुनिक खगोलीय दावों से अलग रखता है।')],
'fact-aryabhata-eclipses':[
('How the explanation works','व्याख्या कैसे काम करती है','Aryabhata treated eclipses as astronomical shadow phenomena: a lunar eclipse involves the Moon entering the Earth’s shadow, while a solar eclipse occurs when the Moon comes between the observer and the Sun.','आर्यभट ने ग्रहणों को खगोलीय छाया-घटना के रूप में समझाया: चंद्र ग्रहण में चंद्रमा पृथ्वी की छाया में प्रवेश करता है, जबकि सूर्य ग्रहण में चंद्रमा पर्यवेक्षक और सूर्य के बीच आता है।'),
('Why it matters','यह क्यों महत्वपूर्ण है','The approach placed eclipse prediction inside mathematical astronomy, where geometry, relative positions and calculation could be used instead of treating the event only as an omen.','इस दृष्टिकोण ने ग्रहण-गणना को गणितीय खगोल-विज्ञान के भीतर रखा, जहाँ ज्यामिति, सापेक्ष स्थितियों और गणना का उपयोग किया जा सकता था।')],
'fact-sushruta-surgery':[
('Breadth of surgical material','शल्य-विषयों की व्यापकता','The Sushruta Samhita discusses surgical operations alongside wounds, fractures and dislocations, instruments, anatomy, bandaging, training methods and post-operative care.','सुश्रुत संहिता शल्य-क्रियाओं के साथ घाव, अस्थिभंग और संधि-च्युतियाँ, उपकरण, शरीररचना, पट्टियाँ, प्रशिक्षण-पद्धतियाँ और शल्योत्तर देखभाल जैसे विषयों पर चर्चा करती है।'),
('Why historians study it','चिकित्सा-इतिहास में महत्व','Because the material is embedded in a systematic medical compendium, it is a major primary source for reconstructing the history of surgery and medical education in South Asia.','क्योंकि यह सामग्री एक व्यवस्थित चिकित्सा-संहिता में संरक्षित है, दक्षिण एशिया में शल्य-चिकित्सा और चिकित्सकीय शिक्षा के इतिहास को समझने के लिए यह प्रमुख प्राथमिक स्रोत है।')],
'fact-sushruta-rhinoplasty':[
('Reconstructive principle','पुनर्निर्माण का सिद्धांत','The Sushruta surgical tradition includes a method for reconstructing a damaged nose using living tissue fashioned into a flap and repositioned to restore form.','सुश्रुत की शल्य-परंपरा में क्षतिग्रस्त नाक के पुनर्निर्माण के लिए जीवित ऊतक की पट्टी तैयार कर उसे पुनः स्थापित करने की विधि का वर्णन मिलता है।'),
('Place in surgical history','शल्य-इतिहास में स्थान','Histories of plastic and reconstructive surgery repeatedly discuss this Indian tradition because tissue-flap reconstruction became an important principle in later reconstructive practice.','प्लास्टिक और पुनर्निर्माण शल्य-चिकित्सा के इतिहास में इस भारतीय परंपरा की बार-बार चर्चा होती है, क्योंकि जीवित ऊतक की फ्लैप-पद्धति बाद की पुनर्निर्माण तकनीकों का महत्वपूर्ण सिद्धांत बनी।')],
'fact-brahmagupta-zero':[
('Rules in the Brahmasphutasiddhanta','ब्रह्मस्फुटसिद्धांत के नियम','Brahmagupta gave explicit arithmetic rules involving zero as well as positive and negative quantities. This is an important milestone in the history of treating zero within written arithmetic procedures.','ब्रह्मगुप्त ने शून्य के साथ-साथ धन और ऋण राशियों के लिए स्पष्ट अंकगणितीय नियम दिए। लिखित अंकगणित में शून्य को व्यवस्थित रूप से扱ने के इतिहास में यह महत्वपूर्ण पड़ाव है।'.replace('扱','व्यवहार कर')),
('Mathematical context','गणितीय संदर्भ','His work belongs to a wider Indian place-value and computational tradition and also contains substantial material on algebra and astronomy.','उनका ग्रंथ व्यापक भारतीय स्थान-मूल्य और गणना-परंपरा का भाग है तथा उसमें बीजगणित और खगोल पर भी महत्वपूर्ण सामग्री है।')],
'fact-panini-ashtadhyayi':[
('Rule-based architecture','नियम-आधारित रचना','The Ashtadhyayi organizes Sanskrit grammar into eight chapters of highly compressed sutras. Its rules, technical markers and ordered operations form an unusually systematic description of language.','अष्टाध्यायी संस्कृत व्याकरण को आठ अध्यायों के अत्यंत संक्षिप्त सूत्रों में व्यवस्थित करती है। इसके नियम, तकनीकी संकेत और क्रमबद्ध प्रक्रियाएँ भाषा का असाधारण रूप से व्यवस्थित वर्णन प्रस्तुत करती हैं।'),
('Long intellectual legacy','दीर्घ बौद्धिक परंपरा','Panini’s grammar generated a major commentarial tradition and became a foundational reference for later Sanskrit grammatical scholarship.','पाणिनि के व्याकरण पर विशाल टीका-परंपरा विकसित हुई और यह बाद के संस्कृत व्याकरण-अध्ययन का आधारभूत संदर्भ बना।')],
'fact-tkdl':[
('What TKDL does','टीकेडीएल क्या करता है','The Traditional Knowledge Digital Library translates and structures knowledge from classical Indian systems into formats that patent examiners can search as prior art.','पारंपरिक ज्ञान डिजिटल पुस्तकालय शास्त्रीय भारतीय ज्ञान-प्रणालियों की सामग्री को अनुवादित और संरचित करके ऐसे रूप में उपलब्ध कराता है जिसे पेटेंट परीक्षक पूर्व-कला के रूप में खोज सकें।'),
('Why it is important','यह क्यों महत्वपूर्ण है','Its purpose is defensive protection: already-known traditional knowledge can be identified during patent examination so that novelty is assessed against documented prior knowledge.','इसका उद्देश्य रक्षात्मक संरक्षण है: पहले से ज्ञात पारंपरिक ज्ञान को पेटेंट जाँच के समय पहचाना जा सके और नवीनता का मूल्यांकन दस्तावेजीकृत पूर्व-ज्ञान के आधार पर हो।')],
'fact-turmeric-patent':[
('The challenge','चुनौती','CSIR submitted documentary prior-art evidence against U.S. patent claims concerning the use of turmeric for wound healing.','सीएसआईआर ने घाव-उपचार में हल्दी के उपयोग से संबंधित अमेरिकी पेटेंट दावों के विरुद्ध दस्तावेजीकृत पूर्व-कला प्रमाण प्रस्तुत किए।'),
('Outcome','परिणाम','The challenged claims were cancelled after re-examination. The episode became a widely cited example of why traditional knowledge must be visible to patent examiners.','पुनः परीक्षण के बाद चुनौती दिए गए दावे निरस्त हुए। यह घटना इस बात का प्रसिद्ध उदाहरण बनी कि पारंपरिक ज्ञान पेटेंट परीक्षकों के लिए खोज योग्य होना क्यों आवश्यक है।')],
'fact-yoga-unesco':[
('UNESCO recognition','यूनेस्को मान्यता','In 2016 UNESCO inscribed Yoga on the Representative List of the Intangible Cultural Heritage of Humanity, recognizing it as a living cultural tradition transmitted through practice and teaching.','2016 में यूनेस्को ने योग को मानवता की अमूर्त सांस्कृतिक विरासत की प्रतिनिधि सूची में अंकित किया और इसे अभ्यास तथा शिक्षण से आगे बढ़ने वाली जीवित सांस्कृतिक परंपरा के रूप में मान्यता दी।'),
('What the listing means','इस सूची का अर्थ','The listing recognizes cultural heritage and continuity; it is distinct from clinical evidence about any particular health claim, which must be evaluated through medical research.','यह सूची सांस्कृतिक विरासत और निरंतरता को मान्यता देती है; किसी विशेष स्वास्थ्य-दावे के चिकित्सकीय प्रमाण का मूल्यांकन अलग शोध-पद्धति से किया जाता है।')],
'fact-vedic-chanting-unesco':[
('UNESCO recognition','यूनेस्को मान्यता','The Tradition of Vedic Chanting is on UNESCO’s Representative List of the Intangible Cultural Heritage of Humanity. The recognition highlights a sophisticated oral system used to preserve pronunciation, accent and recitational form.','वैदिक मंत्रोच्चार की परंपरा यूनेस्को की मानवता की अमूर्त सांस्कृतिक विरासत की प्रतिनिधि सूची में है। यह मान्यता उच्चारण, स्वर और पाठ-रूप को सुरक्षित रखने वाली विकसित मौखिक प्रणाली को रेखांकित करती है।'),
('Why oral preservation matters','मौखिक संरक्षण का महत्व','Multiple recitation techniques and teacher-student transmission helped preserve Vedic texts with exceptional attention to sound and sequence.','अनेक पाठ-पद्धतियों और गुरु-शिष्य परंपरा ने ध्वनि और क्रम पर असाधारण ध्यान के साथ वैदिक पाठों को सुरक्षित रखने में सहायता की।')],
'fact-international-yoga-day':[
('United Nations decision','संयुक्त राष्ट्र का निर्णय','The UN General Assembly adopted resolution 69/131 in 2014 and proclaimed 21 June as the International Day of Yoga.','संयुक्त राष्ट्र महासभा ने 2014 में प्रस्ताव 69/131 स्वीकार कर 21 जून को अंतरराष्ट्रीय योग दिवस घोषित किया।'),
('Global observance','वैश्विक आयोजन','The observance created a recurring international platform for public awareness of yoga and its Indian cultural roots.','इस वार्षिक आयोजन ने योग और उसकी भारतीय सांस्कृतिक जड़ों के प्रति वैश्विक जन-जागरूकता का एक स्थायी मंच बनाया।')],
'fact-panchanga-five-limbs':[
('The five limbs','पाँच अंग','The word Panchanga refers to five calendrical elements: vara (weekday), tithi (lunar day), nakshatra (lunar mansion), yoga and karana.','पंचांग के पाँच पारंपरिक अंग हैं—वार, तिथि, नक्षत्र, योग और करण।'),
('How they are used','इनका उपयोग','Together these elements describe different solar, lunar and calendrical relationships used in traditional Indian time-reckoning and festival calculation.','ये पाँचों अंग सूर्य, चंद्रमा और कालगणना के अलग-अलग संबंधों को व्यक्त करते हैं और पारंपरिक भारतीय समय-निर्धारण तथा पर्व-गणना में उपयोग होते हैं।')],
'fact-tithi-12-degrees':[
('Astronomical definition','खगोलीय परिभाषा','A tithi advances whenever the angular separation of the Moon from the Sun increases by 12 degrees. Thirty such divisions make one synodic lunar month.','चंद्रमा और सूर्य के बीच दीर्घांशीय कोणीय अंतर में प्रत्येक 12 अंश की वृद्धि पर अगली तिथि आरंभ होती है। ऐसे 30 भाग एक चांद्र सिनोडिक मास बनाते हैं।'),
('Why tithi can change at any clock time','तिथि किसी भी घड़ी-समय पर क्यों बदल सकती है','Because tithi is defined by a continuously changing Sun–Moon angle rather than by midnight, its ending time can fall at different hours of the civil day.','क्योंकि तिथि मध्यरात्रि से नहीं बल्कि लगातार बदलते सूर्य–चंद्र कोण से निर्धारित होती है, इसलिए उसका समाप्ति-समय नागरिक दिन के किसी भी घंटे में आ सकता है।')],
'fact-nakshatra-27':[
('Astronomical division','खगोलीय विभाजन','In the standard 27-nakshatra system, the sidereal ecliptic is divided into 27 equal segments. Each segment spans 13 degrees 20 arcminutes.','मानक 27-नक्षत्र प्रणाली में निरयन क्रांतिवृत्त को 27 समान भागों में बाँटा जाता है। प्रत्येक भाग 13 अंश 20 कला का होता है।'),
('Daily Panchanga use','दैनिक पंचांग में उपयोग','The Moon’s sidereal longitude determines which nakshatra segment it occupies at a given time, which is why nakshatra changes independently of the civil date.','किसी समय चंद्रमा का निरयन दीर्घांश यह निर्धारित करता है कि वह किस नक्षत्र-खंड में है; इसी कारण नक्षत्र का परिवर्तन नागरिक तारीख से स्वतंत्र समय पर हो सकता है।')],
'fact-indian-astronomical-ephemeris':[
('Official astronomical publication','आधिकारिक खगोलीय प्रकाशन','India’s Positional Astronomy Centre publishes astronomical ephemeris data used for precise positions and calendrical calculations.','भारत का स्थितीय खगोल विज्ञान केंद्र सटीक खगोलीय स्थितियों और कालगणना के लिए प्रयुक्त पंचांग-सारणी प्रकाशित करता है।'),
('Connection with Panchanga calculation','पंचांग-गणना से संबंध','Modern official ephemerides provide calculated solar, lunar and planetary positions that support precise astronomical and calendar work.','आधुनिक आधिकारिक एपhemeris सूर्य, चंद्रमा और ग्रहों की गणितीय स्थितियाँ प्रदान करती है, जो सटीक खगोलीय और कैलेंडर-गणना का आधार बनती हैं।'.replace('एपhemeris','खगोलीय सारणी'))]
}
for slug, secs in fact_sections.items():
    if slug in by:
        by[slug]['sections']=[{'titleEn':a,'titleHi':b,'contentEn':c,'contentHi':d} for a,b,c,d in secs]

# Remove generic boilerplate section bodies that occur repeatedly across the corpus.
def repeated_values(lang_key:str):
    c=Counter()
    for x in items:
        for s in x.get('sections',[]):
            v=' '.join((s.get(lang_key) or '').split()).strip()
            if v: c[v]+=1
    return {v for v,n in c.items() if n>=3}
rep_en=repeated_values('contentEn'); rep_hi=repeated_values('contentHi')
for x in items:
    kept=[]
    for s in x.get('sections',[]):
        en=' '.join((s.get('contentEn') or '').split()).strip()
        hi=' '.join((s.get('contentHi') or '').split()).strip()
        # Keep verified fact curated sections and any genuinely unique section.
        if x['slug'] not in fact_sections and (en in rep_en or hi in rep_hi):
            continue
        kept.append(s)
    x['sections']=kept

# Add a unique, useful second section to thin articles without repeating the summary.
category_frame={
'Sanatan Basics':('Place in the wider framework','व्यापक सनातन संदर्भ',
                  '{title} is best understood together with the connected ideas shown in this app. Its meaning can vary by philosophical school, text and living tradition; reading those contexts side by side gives a fuller picture.',
                  '{title} को ऐप में दिखाए गए संबंधित विचारों के साथ समझना अधिक उपयोगी है। अलग दर्शन, ग्रंथ और जीवित परंपरा में इसके अर्थ पर अलग बल हो सकता है; इन संदर्भों को साथ पढ़ने से अधिक समग्र समझ बनती है।'),
'Philosophy':('Questions to compare','किन प्रश्नों पर तुलना करें',
              'While studying {title}, compare how it explains valid knowledge, self, world, causation, the divine and liberation. These comparison points make its distinctive philosophical position easier to see.',
              '{title} का अध्ययन करते समय प्रमाण, आत्मा, जगत, कारण-कार्य, ईश्वर और मोक्ष पर उसके उत्तरों की तुलना करें। इससे उसकी विशिष्ट दार्शनिक स्थिति अधिक स्पष्ट दिखाई देती है।'),
'Practices & Symbols':('Living practice','जीवित परंपरा',
                       '{title} is practiced or interpreted in more than one regional and family context. The most useful approach is to understand its devotional meaning, ritual setting and local custom together.',
                       '{title} अलग-अलग क्षेत्रीय और पारिवारिक संदर्भों में भिन्न रूप से किया या समझा जा सकता है। इसके भक्ति-भाव, अनुष्ठानिक संदर्भ और स्थानीय रीति को साथ समझना सबसे उपयोगी है।'),
'Deities':('Many layers of meaning','अर्थ की अनेक परतें',
           'The tradition of {title} can be approached through devotion, theology, iconography, sacred narrative, temple practice and philosophy. These layers complement one another rather than reducing the deity to a single interpretation.',
           '{title} की परंपरा को भक्ति, दर्शन, मूर्तिशास्त्र, पवित्र कथा, मंदिर-उपासना और धर्ममीमांसा—इन अनेक स्तरों पर समझा जा सकता है। ये परतें एक-दूसरे को पूरक बनाती हैं।'),
'Thinkers & Acharyas':('How to study the legacy','विरासत का अध्ययन कैसे करें',
                       'For {title}, separate works securely associated with the thinker, later commentarial traditions, institutional lineages and popular memory. Doing so makes both historical study and traditional reverence clearer.',
                       '{title} के अध्ययन में उनसे निश्चित रूप से जुड़े ग्रंथ, बाद की टीका-परंपरा, संस्थागत गुरु-परंपरा और लोक-स्मृति को अलग पहचानना उपयोगी है। इससे ऐतिहासिक अध्ययन और पारंपरिक श्रद्धा दोनों अधिक स्पष्ट होते हैं।'),
'Indian Knowledge Systems':('Knowledge tradition in context','ज्ञान-परंपरा का संदर्भ',
                            '{title} belongs to a larger Indian intellectual ecosystem in which texts, calculation, observation, commentary and teacher-student transmission interacted over centuries.',
                            '{title} एक व्यापक भारतीय बौद्धिक संसार का हिस्सा है, जहाँ ग्रंथ, गणना, अवलोकन, टीका और गुरु-शिष्य परंपरा सदियों तक एक-दूसरे से जुड़ी रहीं।'),
'History':('Why this phase matters','यह चरण क्यों महत्वपूर्ण है',
           '{title} helps connect textual, institutional and cultural developments across time. Reading it in sequence with the neighbouring timeline entries shows continuity as well as change within Hindu traditions.',
           '{title} अलग-अलग कालों के ग्रंथीय, संस्थागत और सांस्कृतिक विकास को जोड़कर समझने में सहायता करता है। समयरेखा की आसपास की प्रविष्टियों के साथ पढ़ने पर हिंदू परंपराओं की निरंतरता और परिवर्तन दोनों स्पष्ट होते हैं।'),
'Garv with Proof':('Why this documented achievement matters','यह दस्तावेजीकृत उपलब्धि क्यों महत्वपूर्ण है',
                   '{title} is valuable because its central contribution can be traced to documentary or institutional sources. The achievement is strong enough to appreciate on its own, without adding claims beyond the source.',
                   '{title} का महत्व इस बात में है कि इसकी मुख्य उपलब्धि को दस्तावेज़ी या संस्थागत स्रोतों से जाँचा जा सकता है। स्रोत से आगे अतिरिक्त दावा जोड़े बिना भी यह उपलब्धि अपने आप में गौरवपूर्ण है।'),
'Epic Evidence':('What this directly establishes','यह प्रत्यक्ष रूप से क्या स्थापित करता है',
                 'For {title}, the verified core is the material, inscriptional, geographical or documentary evidence described above. Its place in Ramayana or Mahabharata sacred memory is shown alongside that evidence with its own clear label.',
                 '{title} में सत्यापित केंद्र वही भौतिक, अभिलेखीय, भौगोलिक या दस्तावेज़ी प्रमाण है जिसका ऊपर वर्णन है। रामायण या महाभारत की पवित्र स्मृति में उसका स्थान उसी प्रमाण के साथ, अपने स्पष्ट लेबल में दिखाया गया है।')
}
for x in items:
    if len(x.get('sections',[]))>=2 or x['category']=='Verified Facts':
        continue
    frame=category_frame.get(x.get('category'))
    if not frame: continue
    en_title,hi_title,en_tpl,hi_tpl=frame
    title_en=x.get('titleEn') or x.get('title') or x['slug']
    title_hi=x.get('titleHi') or title_en
    x.setdefault('sections',[]).append({'titleEn':en_title,'titleHi':hi_title,'contentEn':en_tpl.format(title=title_en),'contentHi':hi_tpl.format(title=title_hi)})

# Remove any exact summary/body duplication and duplicate section bodies inside a single article.
for x in items:
    for lang in ('En','Hi'):
        if ' '.join((x.get('body'+lang) or '').split()).lower()== ' '.join((x.get('summary'+lang) or '').split()).lower():
            x['body'+lang]=''
    seen_en=set(); seen_hi=set(); unique=[]
    for s in x.get('sections',[]):
        en=' '.join((s.get('contentEn') or '').split()).strip().lower(); hi=' '.join((s.get('contentHi') or '').split()).strip().lower()
        if (en and en in seen_en) or (hi and hi in seen_hi): continue
        if en: seen_en.add(en)
        if hi: seen_hi.add(hi)
        unique.append(s)
    x['sections']=unique

content_path.write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')

# Text catalog: remove repeated generic copy by making each entry title-specific and more useful.
texts=json.loads(texts_path.read_text(encoding='utf-8'))
# Correct specific Natyashastra override in case earlier script used the wrong slug.
specific={
'natyashastra':(
    'A foundational Sanskrit treatise on drama and performance, discussing rasa, acting, gesture, stagecraft, music, dance and aesthetics.',
    'नाटक और प्रदर्शन-कला का आधारभूत संस्कृत ग्रंथ, जिसमें रस, अभिनय, अंग-संचार, रंगमंच, संगीत, नृत्य और सौंदर्यशास्त्र का विस्तृत विवेचन है।',
    'Drama, rasa theory, acting, gesture, stage design, music, dance and aesthetics.',
    'नाटक, रस-सिद्धांत, अभिनय, अंग-संचार, रंगमंच, संगीत, नृत्य और सौंदर्यशास्त्र।',
    'Read it to understand the classical vocabulary behind a large part of Indian theatre, dance and aesthetic theory.',
    'भारतीय नाट्य, नृत्य और सौंदर्यशास्त्र की शास्त्रीय शब्दावली और सिद्धांत समझने के लिए।')
}
for t in texts:
    title_en=t.get('titleEn','').strip(); title_hi=t.get('titleHi','').strip(); cat_en=t.get('category',''); cat_hi=t.get('categoryHi','')
    if t['slug'] in specific:
        de,dh,ke,kh,we,wh=specific[t['slug']]
        t['descriptionEn']=de;t['descriptionHi']=dh;t['keyThemesEn']=ke;t['keyThemesHi']=kh;t['whyReadEn']=we;t['whyReadHi']=wh
    # Make generic descriptions precise to this named work.
    if t.get('descriptionEn','').startswith(('One of the eighteen traditionally enumerated Mahapuranas','A widely known devotional or regional classic','A Dharmashastra text','An early Dharma text')):
        t['descriptionEn']=f"{title_en} is {t['descriptionEn'][0].lower()+t['descriptionEn'][1:]}"
        t['descriptionHi']=f"{title_hi}: {t['descriptionHi']}"
    # Title-specific themes and reading rationale avoid 100 identical blocks while retaining category guidance.
    themes_en=t.get('keyThemesEn','').strip(); themes_hi=t.get('keyThemesHi','').strip()
    if themes_en and title_en.lower() not in themes_en.lower():
        t['keyThemesEn']=f"In {title_en}, focus on: {themes_en[0].lower()+themes_en[1:]}"
    if themes_hi and title_hi not in themes_hi:
        t['keyThemesHi']=f"{title_hi} में मुख्य अध्ययन-विषय: {themes_hi}"
    why_en=t.get('whyReadEn','').strip(); why_hi=t.get('whyReadHi','').strip()
    if why_en and title_en.lower() not in why_en.lower():
        t['whyReadEn']=f"Read {title_en} to place its teachings in context. {why_en}"
    if why_hi and title_hi not in why_hi:
        t['whyReadHi']=f"{title_hi} को उसके ग्रंथीय संदर्भ में पढ़ें। {why_hi}"
    t['studyNoteEn']=f"For {title_en}, begin with a reliable edition or translation, note its genre ({t.get('kindEn','text')}), and keep the base text distinct from later commentary and regional interpretation."
    t['studyNoteHi']=f"{title_hi} का अध्ययन विश्वसनीय संस्करण या अनुवाद से शुरू करें। इसकी विधा ({t.get('kindHi','ग्रंथ')}) को ध्यान में रखें और मूल पाठ को बाद की टीका तथा क्षेत्रीय व्याख्या से अलग पहचानें।"

texts_path.write_text(json.dumps(texts,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Polished {len(items)} knowledge entries and {len(texts)} text records.')
