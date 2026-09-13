from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'SanatanGyan' / 'Resources' / 'Raw' / 'sanatan_content.json'
CURATED_HI_SUMMARIES = json.loads((ROOT / 'tools' / 'curated_hi_summaries.json').read_text(encoding='utf-8'))

# High-quality exact translations for repeated editorial boilerplate.
EXACT_HI = {
    'Is topic ko ek single universal Hindu position samajhna sahi nahi hoga. Different texts, schools aur sampradayas nuance add karte hain. Scripture phase mein primary references directly link kiye ja sakenge.':
        'इस विषय को हिंदू धर्म की एकमात्र सार्वभौमिक मान्यता समझना उचित नहीं होगा। विभिन्न ग्रंथ, दर्शन-परंपराएँ और संप्रदाय इसमें अलग-अलग दृष्टिकोण जोड़ते हैं। ग्रंथ-पाठ चरण में प्राथमिक संदर्भ सीधे जोड़े जा सकेंगे।',
    'Agar kisi practice ke liye modern scientific claim kiya jata hai to us claim ko separately test karna chahiye. Cultural ya spiritual value ko scientific proof ki zarurat nahi hoti.':
        'यदि किसी परंपरा या अभ्यास के बारे में आधुनिक वैज्ञानिक दावा किया जाता है, तो उस दावे की अलग से जाँच होनी चाहिए। सांस्कृतिक या आध्यात्मिक महत्व को मान्य होने के लिए वैज्ञानिक प्रमाण की आवश्यकता नहीं होती।',
    'Is darshanik topic se Hindu thought ki diversity samajh aati hai. App kisi ek school ko automatically sab Hindu traditions ki final position ke roop mein present nahi karta.':
        'यह दार्शनिक विषय हिंदू चिंतन की विविधता को समझने में सहायता करता है। ऐप किसी एक दर्शन-परंपरा को सभी हिंदू परंपराओं की अंतिम या एकमात्र मान्यता के रूप में प्रस्तुत नहीं करता।',
    'Historical biography, traditional hagiography aur attributed quotations ko alag verify karna chahiye. App future releases mein primary works aur scholarly editions se direct references add karega.':
        'ऐतिहासिक जीवनी, पारंपरिक संत-चरित और किसी व्यक्ति से जोड़े गए उद्धरणों की अलग-अलग जाँच आवश्यक है। भविष्य के संस्करणों में ऐप प्राथमिक ग्रंथों और विद्वत् संस्करणों से सीधे संदर्भ जोड़ेगा।',
    'Ancient chronology should be read as a range unless evidence supports a narrow date. Traditional chronologies may use different frameworks and should be labeled separately.':
        'प्राचीन कालक्रम को सामान्यतः एक समय-सीमा के रूप में पढ़ना चाहिए, जब तक प्रमाण किसी संकीर्ण तिथि का समर्थन न करें। पारंपरिक कालक्रम अलग पद्धतियाँ अपना सकते हैं और उन्हें अलग पहचान के साथ दिखाया जाना चाहिए।',
    'Civilizational achievement ko accurately credit karna important hai. Later modern inventions ko ancient texts par retroactively impose karna documented contribution ki value ko kam karta hai.':
        'सभ्यतागत उपलब्धियों का सही और सटीक श्रेय देना महत्वपूर्ण है। बाद की आधुनिक खोजों को प्राचीन ग्रंथों पर पीछे से आरोपित करना वास्तविक, दस्तावेजीकृत योगदान का महत्व कम कर देता है।',
    'Hindu deity traditions ko sirf literal mythology ya sirf symbolism tak reduce nahi karna chahiye. Devotional, theological, philosophical, iconographic aur regional layers ek saath exist kar sakti hain.':
        'हिंदू देव-परंपराओं को केवल शाब्दिक पौराणिक कथा या केवल प्रतीकवाद तक सीमित नहीं करना चाहिए। भक्ति, धर्ममीमांसा, दर्शन, प्रतिमा-विज्ञान और क्षेत्रीय परंपराओं की अनेक परतें एक साथ मौजूद हो सकती हैं।',
    'A measurable health effect does not by itself prove every spiritual explanation, and a spiritual value does not require a biomedical mechanism to be meaningful.':
        'मापा जा सकने वाला स्वास्थ्य प्रभाव अपने-आप हर आध्यात्मिक व्याख्या को सिद्ध नहीं करता; उसी तरह किसी आध्यात्मिक मूल्य को अर्थपूर्ण होने के लिए जैव-चिकित्सीय तंत्र की आवश्यकता नहीं होती।',
    'Prefer systematic reviews, randomized trials when suitable, large observational studies for relevant questions, transparent limitations and reproducible methods.':
        'जहाँ उपयुक्त हो वहाँ व्यवस्थित समीक्षाओं, यादृच्छिक नियंत्रित परीक्षणों, बड़े अवलोकन अध्ययनों, स्पष्ट सीमाओं और दोहराए जा सकने वाले तरीकों को प्राथमिकता देनी चाहिए।',
    'Strong civilizational pride facts se aur strong hota hai. Patent, ancient text, historical technology aur modern scientific proof ko ek hi category nahi maana jana chahiye.':
        'सभ्यतागत गर्व ठोस तथ्यों से और मजबूत होता है। पेटेंट, प्राचीन ग्रंथ, ऐतिहासिक तकनीक और आधुनिक वैज्ञानिक प्रमाण को एक ही श्रेणी नहीं मानना चाहिए।',
    'Documented contribution se aage unsupported claims add karna credibility ko hurt karta hai. App evidence ke scope ko clearly state karta hai.':
        'दस्तावेजीकृत योगदान से आगे बढ़कर असमर्थित दावे जोड़ना विश्वसनीयता को नुकसान पहुँचाता है। ऐप प्रमाण की सीमा को स्पष्ट रूप से बताता है।',
    'Traditional symbolism, literary imagery, historical technology and modern scientific evidence ko alag categories mein evaluate karein.':
        'पारंपरिक प्रतीकवाद, साहित्यिक कल्पना, ऐतिहासिक तकनीक और आधुनिक वैज्ञानिक प्रमाण का अलग-अलग श्रेणियों में मूल्यांकन करना चाहिए।',
    'Unsupported': 'असमर्थित',
    'Supported': 'समर्थित',
    'Mostly Supported': 'अधिकांशतः समर्थित',
}

EXACT_EN = {
    'Is topic ko ek single universal Hindu position samajhna sahi nahi hoga. Different texts, schools aur sampradayas nuance add karte hain. Scripture phase mein primary references directly link kiye ja sakenge.':
        'This topic should not be treated as a single universal Hindu position. Different texts, philosophical schools and sampradayas add important nuance. Primary scripture references can be linked directly in the scripture phase.',
    'Agar kisi practice ke liye modern scientific claim kiya jata hai to us claim ko separately test karna chahiye. Cultural ya spiritual value ko scientific proof ki zarurat nahi hoti.':
        'If a modern scientific claim is made about a practice, that claim should be tested separately. Cultural or spiritual value does not require scientific proof to be meaningful.',
    'Is darshanik topic se Hindu thought ki diversity samajh aati hai. App kisi ek school ko automatically sab Hindu traditions ki final position ke roop mein present nahi karta.':
        'This philosophical topic illustrates the diversity of Hindu thought. The app does not present any one school as the automatic final position of all Hindu traditions.',
    'Historical biography, traditional hagiography aur attributed quotations ko alag verify karna chahiye. App future releases mein primary works aur scholarly editions se direct references add karega.':
        'Historical biography, traditional hagiography and attributed quotations should be verified separately. Future releases can add direct references to primary works and scholarly editions.',
    'Ancient chronology should be read as a range unless evidence supports a narrow date. Traditional chronologies may use different frameworks and should be labeled separately.':
        'Ancient chronology should be read as a range unless evidence supports a narrow date. Traditional chronologies may use different frameworks and should be labelled separately.',
    'Civilizational achievement ko accurately credit karna important hai. Later modern inventions ko ancient texts par retroactively impose karna documented contribution ki value ko kam karta hai.':
        'Civilizational achievements should be credited accurately. Retroactively imposing later modern inventions on ancient texts weakens the value of the genuinely documented contribution.',
    'Hindu deity traditions ko sirf literal mythology ya sirf symbolism tak reduce nahi karna chahiye. Devotional, theological, philosophical, iconographic aur regional layers ek saath exist kar sakti hain.':
        'Hindu deity traditions should not be reduced only to literal mythology or only to symbolism. Devotional, theological, philosophical, iconographic and regional layers can coexist.',
    'A measurable health effect does not by itself prove every spiritual explanation, and a spiritual value does not require a biomedical mechanism to be meaningful.':
        'A measurable health effect does not by itself prove every spiritual explanation, and a spiritual value does not require a biomedical mechanism to be meaningful.',
    'Prefer systematic reviews, randomized trials when suitable, large observational studies for relevant questions, transparent limitations and reproducible methods.':
        'Prefer systematic reviews, randomized trials where suitable, large observational studies for relevant questions, transparent limitations and reproducible methods.',
    'Strong civilizational pride facts se aur strong hota hai. Patent, ancient text, historical technology aur modern scientific proof ko ek hi category nahi maana jana chahiye.':
        'Civilizational pride becomes stronger when it rests on facts. Patents, ancient texts, historical technologies and modern scientific proof should not be treated as the same category.',
    'Documented contribution se aage unsupported claims add karna credibility ko hurt karta hai. App evidence ke scope ko clearly state karta hai.':
        'Adding unsupported claims beyond a documented contribution harms credibility. The app states the scope of evidence clearly.',
    'Traditional symbolism, literary imagery, historical technology and modern scientific evidence ko alag categories mein evaluate karein.':
        'Traditional symbolism, literary imagery, historical technology and modern scientific evidence should be evaluated as separate categories.',
}

SECTION_HI = {
    'Why it matters':'यह क्यों महत्वपूर्ण है','Simple meaning':'सरल अर्थ','Deep study':'गहन अध्ययन','Overview':'परिचय',
    'Traditional meaning':'पारंपरिक अर्थ','Scientific caution':'वैज्ञानिक सावधानी','Core idea':'मुख्य विचार',
    'Why this person matters':'इनका महत्व','Source caution':'स्रोत संबंधी सावधानी','Historical lens':'ऐतिहासिक दृष्टि',
    'What is documented':'क्या दस्तावेजीकृत है','Dating note':'तिथि संबंधी टिप्पणी','Pride with precision':'सटीक तथ्यों के साथ गर्व',
    'How to read deity traditions':'देव-परंपराओं को कैसे समझें','Verdict':'निष्कर्ष','What research can test':'अनुसंधान क्या जाँच सकता है',
    'What it cannot automatically prove':'यह अपने-आप क्या सिद्ध नहीं करता','Evidence standard':'प्रमाण का मानक',
    'The documented achievement':'दस्तावेजीकृत उपलब्धि','Common exaggeration to avoid':'किस अतिशयोक्ति से बचें','Why':'क्यों',
    'How to think about it':'इसे कैसे समझें','Historical significance':'ऐतिहासिक महत्व','Tradition':'परंपरा','Contribution':'योगदान',
    'Why important':'यह क्यों महत्वपूर्ण है','Basic idea':'मूल विचार','Samkhya view':'सांख्य दृष्टि','Comparison caution':'तुलना संबंधी सावधानी',
    'Different traditions':'विभिन्न परंपराएँ','Not one formula':'एक ही सूत्र नहीं','School differences':'दर्शन-परंपराओं में अंतर',
    'Common pramanas':'प्रमुख प्रमाण','Why it is advanced':'यह उन्नत विचार क्यों है','Core question':'मुख्य प्रश्न','Relation model':'संबंध का स्वरूप',
    'Bhakti context':'भक्ति का संदर्भ','Core perspective':'मुख्य दृष्टिकोण','Texts and thinkers':'ग्रंथ और विचारक','Moral complexity':'नैतिक जटिलता',
    'Modern reading':'आधुनिक पाठ','Practice':'अभ्यास','Psychological lens':'मनोवैज्ञानिक दृष्टि','Symbolism':'प्रतीकात्मक अर्थ','Context':'संदर्भ',
    'Traditional role':'पारंपरिक भूमिका','Evidence caution':'प्रमाण संबंधी सावधानी','Indian context':'भारतीय संदर्भ','Modern context':'आधुनिक संदर्भ',
    'Bhakti role':'भक्ति में भूमिका','Cultural diversity':'सांस्कृतिक विविधता','Ethical meaning':'नैतिक अर्थ','Modern application':'आधुनिक उपयोग',
    'Religious purpose':'धार्मिक उद्देश्य','Health caution':'स्वास्थ्य संबंधी सावधानी','Iconography':'प्रतिमा-विज्ञान','Science analogy caution':'वैज्ञानिक उपमा संबंधी सावधानी',
    'Philosophical reading':'दार्शनिक व्याख्या','Interpretive caution':'व्याख्या संबंधी सावधानी','Cultural role':'सांस्कृतिक भूमिका','Evidence boundary':'प्रमाण की सीमा',
    'Meaning':'अर्थ','Historical value':'ऐतिहासिक महत्व','Scientific comparison':'वैज्ञानिक तुलना','Not the Buddha':'बुद्ध से भिन्न',
    'Influence':'प्रभाव','Importance':'महत्व','Attribution':'लेखकत्व/श्रेय','Philosophy':'दर्शन','Dating':'काल-निर्धारण','Diversity':'विविधता',
    'Beyond worship':'पूजा से आगे','Regional variation':'क्षेत्रीय विविधता','Historical contribution':'ऐतिहासिक योगदान','Modern evidence':'आधुनिक प्रमाण',
    'Rasa':'रस','Living influence':'जीवंत प्रभाव','Knowledge crossover':'ज्ञान-परंपराओं का संगम','Caution':'सावधानी','Why impressive':'यह प्रभावशाली क्यों है',
    'Avoid exaggeration':'अतिशयोक्ति से बचें','Modern lens':'आधुनिक दृष्टि','What evidence suggests':'प्रमाण क्या संकेत देते हैं','Limitations':'सीमाएँ',
    'Evidence lens':'प्रमाण की दृष्टि','Safety':'सुरक्षा','Better way to say it':'इसे अधिक सटीक रूप से कैसे कहें'
}

SECTION_EN = {k:k for k in SECTION_HI}

# Title overrides prevent awkward machine-like Hindi in the most visible UI surface.
TITLE_HI = {
'sanatan-dharma-kya-hai':'सनातन धर्म क्या है?','hinduism-naam-kaise-aaya':'हिंदू धर्म नाम कैसे प्रचलित हुआ?','dharma':'धर्म','karma':'कर्म','atman':'आत्मन्','brahman':'ब्रह्मन्','moksha':'मोक्ष','samsara':'संसार','maya':'माया','bhakti':'भक्ति','jnana':'ज्ञान','karma-yoga':'कर्म योग','raja-yoga':'राज योग','purusharthas':'पुरुषार्थ','ashrama-system':'आश्रम व्यवस्था','shruti-aur-smriti':'श्रुति और स्मृति','vedas-overview':'वेदों का परिचय','upanishads-overview':'उपनिषदों का परिचय','itihasa':'इतिहास परंपरा','puranas-overview':'पुराणों का परिचय','agama-aur-tantra':'आगम और तंत्र','sampradaya-kya-hai':'संप्रदाय क्या है?','murti-puja-ka-idea':'मूर्ति पूजा की अवधारणा','ishta-devata':'इष्ट देवता',
'six-darshanas':'षड्दर्शन','nyaya':'न्याय दर्शन','vaisheshika':'वैशेषिक दर्शन','samkhya':'सांख्य दर्शन','classical-yoga':'शास्त्रीय योग','purva-mimamsa':'पूर्व मीमांसा','vedanta':'वेदांत','advaita-vedanta':'अद्वैत वेदांत','vishishtadvaita':'विशिष्टाद्वैत','dvaita-vedanta':'द्वैत वेदांत','achintya-bhedabheda':'अचिन्त्य भेदाभेद','consciousness-in-hindu-philosophy':'हिंदू दर्शन में चेतना','free-will-and-karma':'स्वतंत्र इच्छा और कर्म','problem-of-suffering':'दुःख की समस्या','what-is-reality':'वास्तविकता क्या है?','what-happens-after-death':'मृत्यु के बाद क्या?','bhakti-and-philosophy':'भक्ति और दर्शन','shiva-shakti-philosophy':'शिव-शक्ति दर्शन',
'namaste':'नमस्ते','pranam-and-touching-feet':'प्रणाम और चरण-स्पर्श','puja':'पूजा','aarti':'आरती','diya':'दीपक','temple-bell':'मंदिर की घंटी','tilak':'तिलक','bindi':'बिंदी','rudraksha':'रुद्राक्ष','tulsi-in-hindu-tradition':'हिंदू परंपरा में तुलसी','pradakshina':'प्रदक्षिणा','mantra':'मंत्र','japa':'जप','yajna-and-havan':'यज्ञ और हवन','fasting':'उपवास','ekadashi':'एकादशी','surya-namaskar':'सूर्य नमस्कार','samskaras':'संस्कार','pilgrimage':'तीर्थयात्रा','temple-darshan':'मंदिर दर्शन',
'shiva':'शिव','vishnu':'विष्णु','devi':'देवी','krishna':'कृष्ण','rama':'राम','ganesha':'गणेश','hanuman':'हनुमान','lakshmi':'लक्ष्मी','saraswati':'सरस्वती','durga':'दुर्गा','kali':'काली','surya':'सूर्य','skanda-kartikeya':'स्कंद कार्तिकेय',
'yajnavalkya':'याज्ञवल्क्य','gargi-vachaknavi':'गार्गी वाचक्नवी','maitreyi':'मैत्रेयी','patanjali':'पतंजलि','panini':'पाणिनि','kapila':'कपिल','adi-shankaracharya':'आदि शंकराचार्य','ramanujacharya':'रामानुजाचार्य','madhvacharya':'मध्वाचार्य','abhinavagupta':'अभिनवगुप्त','chaitanya-mahaprabhu':'चैतन्य महाप्रभु','tulsidas':'तुलसीदास','mirabai':'मीराबाई','swami-vivekananda':'स्वामी विवेकानंद','sri-aurobindo':'श्री अरविंद','ramana-maharshi':'रमण महर्षि',
'vedic-textual-traditions':'वैदिक ग्रंथ-परंपराएँ','early-upanishadic-thought':'प्रारंभिक उपनिषदिक चिंतन','formation-of-epic-traditions':'महाकाव्य परंपराओं का विकास','classical-dharmashastra-development':'शास्त्रीय धर्मशास्त्र का विकास','classical-philosophical-systems':'शास्त्रीय दार्शनिक प्रणालियाँ','puranic-and-temple-traditions-expand':'पुराण और मंदिर परंपराओं का विस्तार','bhakti-movements-diversify':'भक्ति आंदोलनों का विविध विकास','adi-shankara-and-advaita-consolidation':'आदि शंकर और अद्वैत का सुदृढ़ीकरण','ramanuja-and-sri-vaishnava-theology':'रामानुज और श्रीवैष्णव दर्शन','madhva-and-dvaita-vedanta':'मध्व और द्वैत वेदांत','early-modern-bhakti-literature':'आरंभिक आधुनिक भक्ति साहित्य','colonial-encounter-and-hindu-reform':'औपनिवेशिक काल और हिंदू सुधार आंदोलन','vivekananda-at-chicago':'शिकागो में विवेकानंद','indian-independence-and-constitutional-era':'भारतीय स्वतंत्रता और संवैधानिक युग','global-yoga-and-diaspora-hinduism':'वैश्विक योग और प्रवासी हिंदू परंपराएँ',
'panini-and-sanskrit-grammar':'पाणिनि और संस्कृत व्याकरण','indian-numeral-system':'भारतीय अंक पद्धति','zero-in-indian-mathematics':'भारतीय गणित में शून्य','aryabhata':'आर्यभट','brahmagupta':'ब्रह्मगुप्त','bhaskara-ii':'भास्कर द्वितीय','kerala-school-of-mathematics':'केरल गणित परंपरा','indian-astronomy':'भारतीय खगोल विज्ञान','ayurvedic-textual-tradition':'आयुर्वेदिक ग्रंथ-परंपरा','sushruta-tradition':'सुश्रुत परंपरा','indian-logic':'भारतीय तर्कशास्त्र','arthashastra-and-statecraft':'अर्थशास्त्र और राज्य-व्यवस्था','temple-architecture':'मंदिर वास्तुकला','traditional-water-management':'पारंपरिक जल प्रबंधन','indian-music-theory':'भारतीय संगीत सिद्धांत',
'yoga-and-stress':'योग और तनाव','yoga-and-chronic-low-back-pain':'योग और दीर्घकालिक कमर दर्द','yoga-and-sleep':'योग और नींद','meditation-and-attention':'ध्यान और एकाग्रता','pranayama-and-breathing':'प्राणायाम और श्वसन','religious-fasting-and-metabolism':'धार्मिक उपवास और चयापचय','turmeric-and-curcumin-research':'हल्दी और करक्यूमिन पर शोध','ayurveda-and-modern-evidence':'आयुर्वेद और आधुनिक प्रमाण','mantra-repetition-and-well-being':'मंत्र-जप और कल्याण','surya-namaskar-and-fitness':'सूर्य नमस्कार और शारीरिक फिटनेस',
'traditional-knowledge-digital-library':'पारंपरिक ज्ञान डिजिटल पुस्तकालय','turmeric-patent-challenge':'हल्दी पेटेंट चुनौती','panini-s-analytical-grammar':'पाणिनि का विश्लेषणात्मक व्याकरण','decimal-place-value-tradition':'दशमलव स्थान-मूल्य परंपरा','brahmagupta-and-zero':'ब्रह्मगुप्त और शून्य','classical-indian-logic':'शास्त्रीय भारतीय तर्कशास्त्र','yoga-as-a-global-indian-tradition':'वैश्विक भारतीय परंपरा के रूप में योग','upanishadic-philosophical-inquiry':'उपनिषदिक दार्शनिक जिज्ञासा','sushruta-medical-tradition':'सुश्रुत चिकित्सा परंपरा','indian-astronomical-computation':'भारतीय खगोलीय गणना',
'claim-temple-bells-kill-bacteria':'दावा: मंदिर की घंटियाँ जीवाणु मारती हैं','claim-om-has-one-scientifically-proven-universal-frequency':'दावा: ॐ की एक सार्वभौमिक वैज्ञानिक आवृत्ति सिद्ध है','claim-ancient-india-had-modern-nuclear-weapons':'दावा: प्राचीन भारत में आधुनिक परमाणु हथियार थे','claim-vedic-texts-describe-modern-airplanes-exactly':'दावा: वैदिक ग्रंथ आधुनिक विमानों का सटीक वर्णन करते हैं','claim-sanskrit-is-the-best-language-for-computer-programming':'दावा: संस्कृत कंप्यूटर प्रोग्रामिंग की सर्वोत्तम भाषा है','claim-yoga-is-only-exercise':'दावा: योग केवल व्यायाम है','claim-patent-means-a-remedy-is-scientifically-proven':'दावा: पेटेंट का अर्थ किसी उपचार का वैज्ञानिक रूप से सिद्ध होना है','claim-turmeric-patent-proved-ancient-medicine-scientifically':'दावा: हल्दी पेटेंट ने प्राचीन चिकित्सा को वैज्ञानिक रूप से सिद्ध कर दिया','claim-karma-means-fixed-destiny':'दावा: कर्म का अर्थ निश्चित भाग्य है','claim-all-hindus-believe-exactly-the-same-thing':'दावा: सभी हिंदू बिल्कुल एक ही बात मानते हैं',
'shaivism':'शैव परंपरा','vaishnavism':'वैष्णव परंपरा','shaktism':'शाक्त परंपरा','smarta-tradition':'स्मार्त परंपरा','sacred-geography':'पवित्र भूगोल','guru-shishya-tradition':'गुरु-शिष्य परंपरा','sanskrit-and-vernacular-traditions':'संस्कृत और लोकभाषा परंपराएँ','ahimsa':'अहिंसा','seva':'सेवा','rta':'ऋत','prakriti':'प्रकृति','purusha':'पुरुष','ishvara':'ईश्वर','avidya':'अविद्या',
'pramana':'प्रमाण: मान्य ज्ञान का सिद्धांत','bhedabheda':'भेदाभेद वेदांत','shuddhadvaita':'शुद्धाद्वैत','dvaitadvaita':'द्वैताद्वैत','kashmir-shaivism':'कश्मीर शैव दर्शन','dharma-ethics':'नैतिकता के रूप में धर्म','om-symbol-and-mantra':'ॐ: प्रतीक और मंत्र','japa-mala':'जप माला','kalasha':'कलश','shankha':'शंख','swastika-symbol':'हिंदू परंपरा में स्वस्तिक','kirtan-bhajan':'कीर्तन और भजन','dana':'दान','vrata':'व्रत','nataraja':'नटराज','ardhanarishvara':'अर्धनारीश्वर','dhanvantari':'धन्वंतरि','harihara':'हरिहर',
'kanada':'कणाद','akshapada-gautama':'अक्षपाद गौतम','jaimini':'जैमिनि','badarayana':'बादरायण','vallabhacharya':'वल्लभाचार्य','classical-sanskrit-knowledge-culture':'शास्त्रीय संस्कृत ज्ञान-संस्कृति','south-indian-bhakti-traditions':'दक्षिण भारतीय भक्ति परंपराएँ','temple-networks-and-pilgrimage':'मंदिर नेटवर्क और तीर्थयात्रा','charaka-tradition':'चरक चिकित्सा परंपरा','natyashastra':'नाट्यशास्त्र','pingala-and-chandas':'पिंगल और छंदशास्त्र','indian-metallurgy':'भारतीय धातुकर्म परंपराएँ','vastu-shastra':'वास्तुशास्त्र','yoga-and-balance':'योग और संतुलन','meditation-and-blood-pressure':'ध्यान और रक्तचाप','natyashastra-performing-arts':'नाट्यशास्त्र और प्रदर्शन कलाएँ','claim-vastu-is-scientifically-proven':'दावा: वास्तु वैज्ञानिक रूप से सिद्ध है'
}

# English title cleanup for the legacy Hinglish titles.
TITLE_EN = {
'sanatan-dharma-kya-hai':'What is Sanatan Dharma?','hinduism-naam-kaise-aaya':'How did the term Hinduism develop?','shruti-aur-smriti':'Shruti and Smriti','agama-aur-tantra':'Agama and Tantra','sampradaya-kya-hai':'What is a Sampradaya?','murti-puja-ka-idea':'The Idea of Murti Puja','pramana':'Pramana: Theory of Valid Knowledge','om-symbol-and-mantra':'Om: Symbol and Mantra','kirtan-bhajan':'Kirtan and Bhajan'
}

# Longest phrases first. These focus on the actual corpus vocabulary rather than pretending to be a general translator.
PHRASE_HI = [
('modern scientific evidence','आधुनिक वैज्ञानिक प्रमाण'),('modern scientific proof','आधुनिक वैज्ञानिक प्रमाण'),('modern scientific claim','आधुनिक वैज्ञानिक दावा'),
('historical evidence','ऐतिहासिक प्रमाण'),('scientific evidence','वैज्ञानिक प्रमाण'),('traditional knowledge','पारंपरिक ज्ञान'),('Indian Knowledge Systems','भारतीय ज्ञान प्रणालियाँ'),
('ultimate reality','परम वास्तविकता'),('valid knowledge','मान्य ज्ञान'),('personal relation','व्यक्तिगत संबंध'),('inner discipline','आंतरिक अनुशासन'),
('major contributions','महत्वपूर्ण योगदान'),('astronomical computation','खगोलीय गणना'),('formal arithmetic treatment','औपचारिक अंकगणितीय विवेचन'),
('zero and negative quantities','शून्य और ऋणात्मक राशियाँ'),('social, legal and ritual norms','सामाजिक, कानूनी और अनुष्ठानिक मानदंड'),
('multiple competing texts','अनेक समानांतर ग्रंथों'),('rule-based grammatical analysis','नियम-आधारित व्याकरणिक विश्लेषण'),('classical Indian achievement','शास्त्रीय भारतीय उपलब्धि'),
('place-value decimal notation','स्थान-मूल्य दशमलव पद्धति'),('world mathematics','विश्व गणित'),('mathematical treatment','गणितीय विवेचन'),
('Indian mathematical tradition','भारतीय गणितीय परंपरा'),('health claims','स्वास्थ्य संबंधी दावे'),('cultural meaning','सांस्कृतिक अर्थ'),
('spiritual value','आध्यात्मिक महत्व'),('scientific proof','वैज्ञानिक प्रमाण'),('traditional meaning','पारंपरिक अर्थ'),('cosmic order','ब्रह्मांडीय व्यवस्था'),
('divine feminine','दैवी स्त्री-तत्त्व'),('supreme reality','परम वास्तविकता'),('different schools','विभिन्न दर्शन-परंपराएँ'),('different texts','विभिन्न ग्रंथ'),
('deep reflections','गहन चिंतन'),('political-ethical reflection','राजनीतिक और नैतिक चिंतन'),('devotional narratives','भक्ति-कथाएँ'),
('broad civilizational-religious tradition','व्यापक सभ्यतागत और धार्मिक परंपरा'),('historical development','ऐतिहासिक विकास'),('umbrella term','व्यापक समावेशी नाम'),
('basic meaning','मूल अर्थ'),('action, intention and consequences','कर्म, अभिप्राय और परिणाम'),('birth, death and rebirth','जन्म, मृत्यु और पुनर्जन्म'),
('continuing cycle','निरंतर चक्र'),('cosmic power','ब्रह्मांडीय शक्ति'),('spiritual knowledge','आध्यात्मिक ज्ञान'),('human life','मानव जीवन'),
('life-stage ideal','जीवन-चरण का आदर्श'),('Vedic corpus','वैदिक साहित्य'),('highest scriptural category','सर्वोच्च शास्त्रीय श्रेणी'),
('philosophical inquiry','दार्शनिक जिज्ञासा'),('ritual reinterpretation','अनुष्ठानों की पुनर्व्याख्या'),('long period','दीर्घ काल'),('ongoing scholarship','चल रहे विद्वत् अध्ययन'),
('composition and redaction','रचना और संपादन'),('self, ultimate reality','आत्मन् और परम वास्तविकता'),('classical philosophical systems','शास्त्रीय दार्शनिक प्रणालियाँ'),
('global influence','वैश्विक प्रभाव'),('prior art','पूर्व-प्रचलित ज्ञान'),('patent examiners','पेटेंट परीक्षक'),('wrongful patents','अनुचित पेटेंट'),
('wound healing','घाव भरने'),('history of linguistics','भाषाविज्ञान के इतिहास'),('negative quantities','ऋणात्मक राशियाँ'),('chronic nonspecific low-back pain','दीर्घकालिक गैर-विशिष्ट कमर दर्द'),
('sleep quality','नींद की गुणवत्ता'),('mental/physical well-being','मानसिक और शारीरिक कल्याण'),('stress management','तनाव प्रबंधन'),
('scientifically proven','वैज्ञानिक रूप से सिद्ध'),('modern nuclear weapons','आधुनिक परमाणु हथियार'),('modern airplanes','आधुनिक विमान'),
('computer programming','कंप्यूटर प्रोग्रामिंग'),('fixed destiny','निश्चित भाग्य'),('exactly the same thing','बिल्कुल एक ही बात'),
('knowledge culture','ज्ञान-संस्कृति'),('performing arts','प्रदर्शन कलाएँ'),('blood pressure','रक्तचाप'),('water management','जल प्रबंधन'),
('music theory','संगीत सिद्धांत'),('statecraft','राज्य-व्यवस्था'),('temple architecture','मंदिर वास्तुकला'),('medical tradition','चिकित्सा परंपरा'),
('analytical grammar','विश्लेषणात्मक व्याकरण'),('astronomical computation','खगोलीय गणना'),('philosophical inquiry','दार्शनिक जिज्ञासा'),
('scientific mechanism','वैज्ञानिक तंत्र'),('biomedical mechanism','जैव-चिकित्सीय तंत्र'),('systematic attention','व्यवस्थित ध्यान'),('atomistic analysis','परमाणुवादी विश्लेषण'),
('categories of reality','वास्तविकता की श्रेणियाँ'),('religious purpose','धार्मिक उद्देश्य'),('regional layers','क्षेत्रीय परतें'),('devotional presence','भक्ति-उपस्थिति'),
('respectful greeting','सम्मानपूर्ण अभिवादन'),('respect, humility','सम्मान और विनम्रता'),('guru/elder relationship','गुरु या वरिष्ठ के साथ संबंध'),
('offering, invocation, remembrance','अर्पण, आवाहन और स्मरण'),('modern usage','आधुनिक प्रयोग'),('meditative discipline','ध्यान-साधना'),('eight-limbed framework','अष्टांग ढाँचे'),
]

PHRASE_EN = [
('kya hai','what is'),('naam kaise aaya','how the name developed'),('ke roop mein','as'),('ke through','through'),('ke liye','for'),('ke saath','with'),('ke basis par','on the basis of'),('ke hisaab se','according to'),
('se juda hai','is connected with'),('se joda jata hai','is linked with'),('alag-alag','different'),('samajh aati hai','helps explain'),('samajhna','understand'),
('mana jata hai','is regarded'),('maana jata hai','is regarded'),('kiya jata hai','is done'),('kiya jata','is done'),('jane jate hain','are known'),('joda jata hai','is linked'),
('karna chahiye','should be done'),('nahi hoti','is not required'),('zarurat nahi','is not necessary'),('sahi nahi hoga','would not be accurate'),
('par major contributions diye','made major contributions to'),('ke history mein','in the history of'),('mein hua','developed in'),('mein aata hai','appears in'),
]

WORD_HI = {
'aur':'और','and':'और','ya':'या','or':'या','ke':'के','ka':'का','ki':'की','ko':'को','se':'से','mein':'में','me':'में','par':'पर','tak':'तक','liye':'लिए','saath':'साथ','ne':'ने','bhi':'भी','hi':'ही','jo':'जो','jisme':'जिसमें','jahan':'जहाँ','lekin':'लेकिन','agar':'यदि','is':'यह','us':'उस','ek':'एक','kai':'कई','kuch':'कुछ','sab':'सभी','kisi':'किसी','alag':'अलग','tarah':'तरह','hisaab':'अनुसार','jaise':'जैसे','sirf':'केवल','aage':'आगे','baad':'बाद','beech':'बीच','andar':'अंदर','bahar':'बाहर',
'hai':'है','hain':'हैं','tha':'था','thi':'थी','the':'थे','hota':'होता','hoti':'होती','hote':'होते','hua':'हुआ','hui':'हुई','hue':'हुए','karna':'करना','karta':'करता','karti':'करती','karte':'करते','karne':'करने','kiya':'किया','kiye':'किए','karega':'करेगा','sakta':'सकता','sakti':'सकती','sakte':'सकते','chahiye':'चाहिए','jata':'जाता','jati':'जाती','jate':'जाते','maana':'माना','mana':'माना','milte':'मिलते','aati':'आती','aata':'आता','deta':'देता','deti':'देती','dete':'देते','diye':'दिए','rakhta':'रखता','rakhti':'रखती','rakhta':'रखता','samajh':'समझ','samajhna':'समझना','batata':'बताता','batati':'बताती','dikhata':'दिखाता','dikhati':'दिखाती','vary':'भिन्न होता','cover':'समाहित करता','include':'शामिल करता','includes':'शामिल करता','shamil':'शामिल',
'modern':'आधुनिक','ancient':'प्राचीन','historical':'ऐतिहासिक','history':'इतिहास','scientific':'वैज्ञानिक','science':'विज्ञान','research':'अनुसंधान','evidence':'प्रमाण','traditional':'पारंपरिक','tradition':'परंपरा','traditions':'परंपराएँ','philosophy':'दर्शन','philosophical':'दार्शनिक','darshanik':'दार्शनिक','spiritual':'आध्यात्मिक','religious':'धार्मिक','ritual':'अनुष्ठान','devotional':'भक्ति-आधारित','theological':'धर्ममीमांसात्मक','cultural':'सांस्कृतिक','regional':'क्षेत्रीय','classical':'शास्त्रीय','global':'वैश्विक','indian':'भारतीय','india':'भारत','hindu':'हिंदू','hinduism':'हिंदू धर्म','vedic':'वैदिक','upanishadic':'उपनिषदिक','vedantic':'वेदांतिक','puranic':'पौराणिक','scripture':'शास्त्र','texts':'ग्रंथ','text':'ग्रंथ','corpus':'साहित्य-संग्रह','literature':'साहित्य','schools':'दर्शन-परंपराएँ','school':'दर्शन-परंपरा','sampradayas':'संप्रदाय','sampradaya':'संप्रदाय','framework':'ढाँचा','frameworks':'ढाँचे','system':'प्रणाली','systems':'प्रणालियाँ','category':'श्रेणी','categories':'श्रेणियाँ','concept':'अवधारणा','concepts':'अवधारणाएँ','idea':'विचार','meaning':'अर्थ','meanings':'अर्थ','knowledge':'ज्ञान','gyan':'ज्ञान','vigyan':'विज्ञान','itihas':'इतिहास','darshan':'दर्शन','parampara':'परंपरा','pramaan':'प्रमाण','pramana':'प्रमाण','vichar':'विचार','samay':'समय','ganana':'गणना',
'major':'प्रमुख','important':'महत्वपूर्ण','central':'केंद्रीय','broad':'व्यापक','deep':'गहन','simple':'सरल','different':'विभिन्न','multiple':'अनेक','single':'एकमात्र','universal':'सार्वभौमिक','specific':'विशिष्ट','strong':'मज़बूत','final':'अंतिम','direct':'सीधा','directly':'सीधे','separately':'अलग से','automatically':'अपने-आप','accurately':'सटीक रूप से','clearly':'स्पष्ट रूप से','later':'बाद की','future':'भविष्य','current':'वर्तमान','common':'सामान्य','large':'बड़े','narrow':'संकीर्ण','long':'लंबे','reliable':'विश्वसनीय','literal':'शाब्दिक','real':'वास्तविक','meaningful':'अर्थपूर्ण','unsupported':'असमर्थित','supported':'समर्थित','documented':'दस्तावेजीकृत','attributed':'आरोपित/सम्बद्ध','scholarly':'विद्वत्','primary':'प्राथमिक','source':'स्रोत','sources':'स्रोत','references':'संदर्भ','reference':'संदर्भ','claim':'दावा','claims':'दावे','proof':'प्रमाण','value':'महत्व','values':'मूल्य','quality':'गुणवत्ता','limitations':'सीमाएँ','caution':'सावधानी','precision':'सटीकता','contribution':'योगदान','contributions':'योगदान','achievement':'उपलब्धि','achievements':'उपलब्धियाँ','importance':'महत्व','influence':'प्रभाव','development':'विकास','role':'भूमिका','purpose':'उद्देश्य','position':'मान्यता','thought':'चिंतन','diversity':'विविधता','nuance':'सूक्ष्मता','context':'संदर्भ','interpretation':'व्याख्या','symbolism':'प्रतीकवाद','mythology':'पौराणिक कथा','iconographic':'प्रतिमा-विज्ञान संबंधी','biography':'जीवनी','hagiography':'संत-चरित','quotations':'उद्धरण','chronology':'कालक्रम','chronologies':'कालक्रम','dating':'काल-निर्धारण','date':'तिथि','range':'समय-सीमा','editions':'संस्करण','release':'संस्करण','releases':'संस्करण',
'action':'कर्म','intention':'अभिप्राय','consequences':'परिणाम','rebirth':'पुनर्जन्म','liberation':'मोक्ष','self':'आत्म-स्वरूप','reality':'वास्तविकता','consciousness':'चेतना','death':'मृत्यु','birth':'जन्म','cycle':'चक्र','path':'मार्ग','devotion':'भक्ति','surrender':'समर्पण','remembrance':'स्मरण','seva':'सेवा','duty':'कर्तव्य','ethics':'नैतिकता','order':'व्यवस्था','conduct':'आचरण','principle':'सिद्धांत','power':'शक्ति','appearance':'प्रतीति','limitation':'सीमा','limitations':'सीमाएँ','attachment':'आसक्ति','discipline':'अनुशासन','aims':'लक्ष्य','life':'जीवन','study':'अध्ययन','inquiry':'जिज्ञासा','world':'विश्व','cosmic':'ब्रह्मांडीय','divine':'दैवी','deity':'देवता','supreme':'परम','mother':'माता','forms':'रूप','form':'रूप','worship':'उपासना','revered':'पूजित','preservation':'पालन/संरक्षण','avatar':'अवतार','ascetic':'तपस्वी','householder':'गृहस्थ','dancer':'नर्तक','transformative':'रूपांतरणकारी',
'yoga':'योग','ayurveda':'आयुर्वेद','karma':'कर्म','dharma':'धर्म','moksha':'मोक्ष','samsara':'संसार','maya':'माया','bhakti':'भक्ति','jnana':'ज्ञान','atman':'आत्मन्','brahman':'ब्रह्मन्','vedanta':'वेदांत','nyaya':'न्याय','vaisheshika':'वैशेषिक','samkhya':'सांख्य','mimamsa':'मीमांसा','advaita':'अद्वैत','dvaita':'द्वैत','shaiva':'शैव','vaishnava':'वैष्णव','shakta':'शाक्त','sanskrit':'संस्कृत','mantra':'मंत्र','meditation':'ध्यान','fasting':'उपवास','temple':'मंदिर','surya':'सूर्य','shiva':'शिव','vishnu':'विष्णु','brahmagupta':'ब्रह्मगुप्त','sushruta':'सुश्रुत','panini':'पाणिनि','aryabhata':'आर्यभट','turmeric':'हल्दी','curcumin':'करक्यूमिन','patent':'पेटेंट','technology':'तकनीक','mathematics':'गणित','mathematical':'गणितीय','arithmetic':'अंकगणित','algebra':'बीजगणित','astronomy':'खगोल विज्ञान','astronomical':'खगोलीय','medicine':'चिकित्सा','medical':'चिकित्सीय','surgery':'शल्य चिकित्सा','grammar':'व्याकरण','logic':'तर्कशास्त्र','linguistics':'भाषाविज्ञान','calendar':'पंचांग','calculation':'गणना','calculations':'गणनाएँ','planet':'ग्रह','planets':'ग्रह','earth':'पृथ्वी','sun':'सूर्य','moon':'चंद्रमा','star':'तारा','stars':'तारे','zero':'शून्य','number':'संख्या','numerals':'अंक','decimal':'दशमलव','place-value':'स्थान-मूल्य','atomistic':'परमाणुवादी','substance':'द्रव्य','motion':'गति','health':'स्वास्थ्य','effect':'प्रभाव','effects':'प्रभाव','stress':'तनाव','sleep':'नींद','pain':'दर्द','fitness':'शारीरिक क्षमता','attention':'एकाग्रता','breathing':'श्वसन','metabolism':'चयापचय','well-being':'कल्याण','acoustic':'ध्वनिक','frequency':'आवृत्ति','bacteria':'जीवाणु','pathogens':'रोगजनक','exercise':'व्यायाम','programming':'प्रोग्रामिंग','nuclear':'परमाणु','weapons':'हथियार','airplanes':'विमान','destiny':'भाग्य',
'what':'क्या','why':'क्यों','how':'कैसे','when':'कब','where':'कहाँ','can':'सकता है','cannot':'नहीं कर सकता','does':'करता है','not':'नहीं','no':'नहीं','yes':'हाँ','only':'केवल','as':'के रूप में','with':'के साथ','for':'के लिए','from':'से','through':'के माध्यम से','by':'द्वारा','on':'पर','in':'में','of':'का','the':'','a':'','an':'','it':'यह','this':'यह','every':'हर','some':'कुछ','may':'हो सकता है','should':'चाहिए','must':'अवश्य','prefer':'प्राथमिकता दें','reduce':'सीमित करना','present':'प्रस्तुत','test':'जाँच','evaluate':'मूल्यांकन','verify':'सत्यापित','prove':'सिद्ध','explain':'समझाते','describe':'वर्णित','describes':'वर्णित करता है','developed':'विकसित','exist':'मौजूद','work':'कार्य','works':'कृतियाँ','use':'प्रयोग','usage':'प्रयोग','add':'जोड़ना','link':'जोड़ना','read':'पढ़ना','credit':'श्रेय','impose':'आरोपित करना','hurt':'नुकसान पहुँचाता','state':'बताता','treatment':'विवेचन','involving':'जिसमें','quantities':'राशियाँ','norms':'मानदंड','competing':'समानांतर','social':'सामाजिक','legal':'कानूनी','ritual':'अनुष्ठानिक','formal':'औपचारिक','analysis':'विश्लेषण','analytical':'विश्लेषणात्मक','computation':'गणना','milestone':'महत्वपूर्ण पड़ाव','remarkable':'उल्लेखनीय','extraordinary':'असाधारण','foundational':'आधारभूत','systematic':'व्यवस्थित','inference':'अनुमान','debate':'वाद-विवाद','valid':'मान्य','means':'साधन','motion':'गति','quality':'गुण','treatment':'विवेचन','selected':'चयनित','population':'समूह','populations':'समूहों','intervention':'हस्तक्षेप','protocols':'प्रोटोकॉल','syntheses':'समेकित समीक्षाएँ','improvements':'सुधार','compared':'तुलना में','observational':'अवलोकनात्मक','randomized':'यादृच्छिक','trials':'परीक्षण','reviews':'समीक्षाएँ','methods':'तरीके','reproducible':'दोहराए जा सकने वाले','transparent':'स्पष्ट',
}

WORD_EN = {
'aur':'and','ke':'of','ka':'of','ki':'of','ko':'','se':'from','mein':'in','me':'in','par':'on','tak':'up to','liye':'for','saath':'with','ne':'','bhi':'also','hi':'','jo':'which','jisme':'in which','jahan':'where','lekin':'but','agar':'if','ek':'a','kai':'many','kuch':'some','sab':'all','kisi':'any','alag':'different','tarah':'way','hisaab':'according','jaise':'such as','sirf':'only','aage':'beyond','baad':'later',
'hai':'is','hain':'are','tha':'was','thi':'was','the':'were','hota':'is','hoti':'is','hote':'are','hua':'developed','hui':'developed','karna':'to do','karta':'does','karti':'does','karte':'do','karne':'to do','kiya':'did','kiye':'done','sakta':'can','sakti':'can','sakte':'can','chahiye':'should','jata':'is','jati':'is','jate':'are','maana':'regarded','mana':'regarded','milte':'are found','aati':'appears','aata':'appears','diye':'made','samajh':'understanding','samajhna':'understand','batata':'describes','batati':'describes','dikhata':'shows','dikhati':'shows','shamil':'included','darshanik':'philosophical','parampara':'tradition','pramaan':'evidence','gyan':'knowledge','vigyan':'science','itihas':'history','darshan':'philosophy','ganana':'calculation','nakshatra':'nakshatra','grah':'graha','rishi':'rishi','muni':'sage','arth':'meaning','juda':'connected','joda':'linked','jana':'known','sahi':'accurate','zarurat':'need','nahi':'not','bahut':'very','chaar':'four','anek':'many','upaasna':'worship','vichar':'idea','samay':'time','roop':'form','roop mein':'as',
}

# Common proper names / technical terms that should be transliterated, not mechanically translated.
PROPER_HI = {
'Brahmagupta':'ब्रह्मगुप्त','Aryabhata':'आर्यभट','Panini':'पाणिनि','Patanjali':'पतंजलि','Sushruta':'सुश्रुत','Charaka':'चरक','Bhaskara':'भास्कर',
'Ramanuja':'रामानुज','Madhva':'मध्व','Shankara':'शंकर','Vivekananda':'विवेकानंद','Yajnavalkya':'याज्ञवल्क्य','Gargi':'गार्गी','Maitreyi':'मैत्रेयी',
'Upanishad':'उपनिषद','Upanishads':'उपनिषद','Ramayana':'रामायण','Mahabharata':'महाभारत','Rigveda':'ऋग्वेद','Samaveda':'सामवेद','Yajurveda':'यजुर्वेद','Atharvaveda':'अथर्ववेद',
'Ashtadhyayi':'अष्टाध्यायी','Arthashastra':'अर्थशास्त्र','Natyashastra':'नाट्यशास्त्र','TKDL':'टीकेडीएल','CSIR':'सीएसआईआर','U.S.':'अमेरिकी',
}

# Approximate roman->Devanagari fallback for names/terms not covered by the corpus dictionary.
# This is deliberately a last resort; editorial content should prefer explicit translations.
VOWELS = [('ai','ै'),('au','ौ'),('aa','ा'),('ee','ी'),('ii','ी'),('oo','ू'),('uu','ू'),('a',''),('i','ि'),('u','ु'),('e','े'),('o','ो')]
CONS = [('ksh','क्ष'),('gy','ज्ञ'),('sh','श'),('chh','छ'),('ch','च'),('th','थ'),('dh','ध'),('ph','फ'),('bh','भ'),('kh','ख'),('gh','घ'),('jh','झ'),('tr','त्र'),('kr','क्र'),('pr','प्र'),('br','ब्र'),('gr','ग्र'),('dr','द्र'),('vr','व्र'),('k','क'),('g','ग'),('c','क'),('j','ज'),('t','त'),('d','द'),('n','न'),('p','प'),('b','ब'),('m','म'),('y','य'),('r','र'),('l','ल'),('v','व'),('w','व'),('s','स'),('h','ह'),('f','फ'),('q','क'),('x','क्स'),('z','ज')]

def translit_word(word:str)->str:
    if not word: return word
    # preserve simple numeric/version tokens
    if re.fullmatch(r'[A-Z]{2,6}', word):
        acronym = {'AI':'एआई','DNA':'डीएनए','API':'एपीआई','TKDL':'टीकेडीएल','CSIR':'सीएसआईआर'}
        return acronym.get(word, ' '.join(translit_word(ch.lower()) for ch in word))
    w=word.lower()
    out=''
    i=0
    # independent starting vowel
    independent={'a':'अ','aa':'आ','i':'इ','ee':'ई','ii':'ई','u':'उ','oo':'ऊ','uu':'ऊ','e':'ए','ai':'ऐ','o':'ओ','au':'औ'}
    while i<len(w):
        # leading vowel
        if i==0:
            hit=False
            for pat in sorted(independent,key=len,reverse=True):
                if w.startswith(pat,i): out+=independent[pat]; i+=len(pat); hit=True; break
            if hit: continue
        cons=None
        for pat,val in CONS:
            if w.startswith(pat,i): cons=(pat,val); break
        if cons:
            pat,val=cons; i+=len(pat); out+=val
            # attached vowel
            attached=None
            for vpat,matra in VOWELS:
                if w.startswith(vpat,i): attached=(vpat,matra); break
            if attached:
                vpat,matra=attached; i+=len(vpat)
                # i matra visually precedes but Unicode follows consonant
                out+=matra
            else:
                # no explicit vowel: virama when followed by consonant/end, else inherent a
                if i>=len(w):
                    pass
            continue
        # vowel mid-word not consumed by consonant
        hit=False
        for pat in sorted(independent,key=len,reverse=True):
            if w.startswith(pat,i): out+=independent[pat]; i+=len(pat); hit=True; break
        if hit: continue
        out+=w[i]; i+=1
    return out


def replace_phrases(text:str, pairs):
    for a,b in sorted(pairs,key=lambda x:len(x[0]),reverse=True):
        text=re.sub(re.escape(a),b,text,flags=re.I)
    return text


def hi(text:str)->str:
    if not text: return ''
    if text in EXACT_HI: return EXACT_HI[text]
    for a,b in PROPER_HI.items():
        text=re.sub(rf'(?<![A-Za-z]){re.escape(a)}(?![A-Za-z])',b,text,flags=re.I)
    text=replace_phrases(text,PHRASE_HI)
    # word-by-word replacement after phrases
    def repl(m):
        w=m.group(0)
        low=w.lower()
        if low in WORD_HI: return WORD_HI[low]
        return translit_word(w)
    text=re.sub(r"[A-Za-z][A-Za-z0-9'’.-]*",repl,text)
    text=re.sub(r'\s+([,.;:!?।])',r'\1',text)
    text=re.sub(r'\s{2,}',' ',text).strip()
    # Convert Latin punctuation sentence ending to danda where natural.
    text=text.replace('. ', '। ').rstrip('.')
    return text


def en(text:str)->str:
    if not text: return ''
    if text in EXACT_EN: return EXACT_EN[text]
    text=replace_phrases(text,PHRASE_EN)
    def repl(m):
        w=m.group(0); low=w.lower()
        return WORD_EN.get(low,w)
    text=re.sub(r"[A-Za-z][A-Za-z'’-]*",repl,text)
    # Clean predictable grammar artifacts from token replacement.
    fixes=[
        (r'\bof a\b','a'),(r'\bof the\b','the'),(r'\b in in\b',' in'),(r'\b is is\b',' is'),(r'\b and and\b',' and'),
        (r'\bof are\b','are'),(r'\bof is\b','is'),(r'\bthe a\b','the'),(r'\s+([,.;:!?])',r'\1')]
    for a,b in fixes: text=re.sub(a,b,text,flags=re.I)
    text=re.sub(r'\s{2,}',' ',text).strip()
    if text and text[0].islower(): text=text[0].upper()+text[1:]
    return text


def main():
    items=json.loads(CONTENT.read_text(encoding='utf-8'))
    changed=0
    for item in items:
        slug=item.get('slug','')
        raw_title=item.get('title','') or ''
        raw_summary=item.get('summary','') or ''
        raw_body=item.get('body','') or raw_summary

        # Titles: use reviewed overrides for legacy content, existing curated fields for newer entries.
        if not item.get('titleHi'):
            item['titleHi']=TITLE_HI.get(slug,hi(raw_title)); changed+=1
        if not item.get('titleEn'):
            item['titleEn']=TITLE_EN.get(slug,en(raw_title)); changed+=1

        # Legacy summaries have human-reviewed Hindi text. Newer articles already ship exact bilingual fields.
        if slug in CURATED_HI_SUMMARIES:
            if item.get('summaryHi') != CURATED_HI_SUMMARIES[slug]:
                item['summaryHi']=CURATED_HI_SUMMARIES[slug]; changed+=1
            if item.get('bodyHi') != CURATED_HI_SUMMARIES[slug]:
                item['bodyHi']=CURATED_HI_SUMMARIES[slug]; changed+=1
        else:
            if not item.get('summaryHi'): item['summaryHi']=hi(raw_summary); changed+=1
            if not item.get('bodyHi'): item['bodyHi']=hi(raw_body); changed+=1

        if not item.get('summaryEn'): item['summaryEn']=en(raw_summary); changed+=1
        if not item.get('bodyEn'): item['bodyEn']=en(raw_body); changed+=1
        if not item.get('subtitleEn'): item['subtitleEn']=en(item.get('subtitle','') or ''); changed+=1
        if not item.get('subtitleHi'): item['subtitleHi']=hi(item.get('subtitle','') or ''); changed+=1

        for sec in item.get('sections',[]):
            raw_sec_title=sec.get('title','') or ''
            raw_sec_content=sec.get('content','') or ''
            if not sec.get('titleEn'): sec['titleEn']=SECTION_EN.get(raw_sec_title,en(raw_sec_title)); changed+=1
            if not sec.get('titleHi'): sec['titleHi']=SECTION_HI.get(raw_sec_title,hi(raw_sec_title)); changed+=1
            if not sec.get('contentEn'): sec['contentEn']=en(raw_sec_content); changed+=1

            # When a section repeats the article summary/body, reuse the reviewed Hindi sentence.
            if slug in CURATED_HI_SUMMARIES and raw_sec_content in {raw_summary, raw_body}:
                target=CURATED_HI_SUMMARIES[slug]
            elif raw_sec_content in EXACT_HI:
                target=EXACT_HI[raw_sec_content]
            else:
                target=hi(raw_sec_content)
            if not sec.get('contentHi') or slug in CURATED_HI_SUMMARIES:
                sec['contentHi']=target; changed+=1

    CONTENT.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Localized {len(items)} entries; applied {changed} bilingual content updates.')

if __name__=='__main__':
    main()
