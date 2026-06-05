from src.features.seed.schema import SeedEntry

SEED_ENTRIES: list[SeedEntry] = [
    SeedEntry(
        text="ربنا اتنا في الدنيا حسنة وفي الاخرة حسنة وقنا عذاب النار",
        type_slug="quranic",
        category_slug="hope",
        source="سورة البقرة ٢٠١",
        quran_ref=(2, 201),
        dua_substring="ربنا اتنا في الدنيا حسنة وفي الاخرة حسنة وقنا عذاب النار",
    ),
    SeedEntry(
        text="الحمد لله رب العالمين",
        type_slug="quranic",
        category_slug="praise",
        source="سورة الفاتحة ٢",
        quran_ref=(1, 2),
    ),
    SeedEntry(
        text="ربنا افرغ علينا صبرا وثبت اقدامنا وانصرنا على القوم الكافرين",
        type_slug="quranic",
        category_slug="patience",
        source="سورة البقرة ٢٥٠",
        quran_ref=(2, 250),
        dua_substring="ربنا افرغ علينا صبرا وثبت اقدامنا وانصرنا على القوم الكافرين",
    ),
    SeedEntry(
        text="ربنا لا تؤاخذنا ان نسينا او اخطانا",
        type_slug="quranic",
        category_slug="hardship",
        source="سورة البقرة ٢٨٦",
        quran_ref=(2, 286),
        dua_substring=(
            "ربنا لا تؤاخذنا ان نسينا او اخطانا ربنا ولا تحمل علينا اصرا كما حملته "
            "على الذين من قبلنا ربنا ولا تحملنا ما لا طاقة لنا به واعف عنا واغفر لنا "
            "وارحمنا انت مولانا فانصرنا على القوم الكافرين"
        ),
    ),
    SeedEntry(
        text="ربنا لا تزغ قلوبنا بعد اذ هديتنا وهب لنا من لدنك رحمة انك انت الوهاب",
        type_slug="quranic",
        category_slug="guidance",
        source="سورة آل عمران ٨",
        quran_ref=(3, 8),
    ),
    SeedEntry(
        text="ربنا اننا امنا فاغفر لنا ذنوبنا وقنا عذاب النار",
        type_slug="quranic",
        category_slug="forgiveness",
        source="سورة آل عمران ١٦",
        quran_ref=(3, 16),
        dua_substring="ربنا اننا امنا فاغفر لنا ذنوبنا وقنا عذاب النار",
    ),
    SeedEntry(
        text="ربنا اغفر لنا ذنوبنا واسرافنا في امرنا وثبت اقدامنا وانصرنا على القوم الكافرين",
        type_slug="quranic",
        category_slug="faith",
        source="سورة آل عمران ١٤٧",
        quran_ref=(3, 147),
        dua_substring=(
            "ربنا اغفر لنا ذنوبنا واسرافنا في امرنا وثبت اقدامنا وانصرنا على القوم الكافرين"
        ),
    ),
    SeedEntry(
        text="رب هب لي من لدنك ذرية طيبة انك سميع الدعاء",
        type_slug="quranic",
        category_slug="family",
        source="سورة آل عمران ٣٨",
        quran_ref=(3, 38),
        dua_substring="رب هب لي من لدنك ذرية طيبة انك سميع الدعاء",
    ),
    SeedEntry(
        text="ربنا ظلمنا انفسنا وان لم تغفر لنا وترحمنا لنكونن من الخاسرين",
        type_slug="quranic",
        category_slug="sadness",
        source="سورة الأعراف ٢٣",
        quran_ref=(7, 23),
        dua_substring="ربنا ظلمنا انفسنا وان لم تغفر لنا وترحمنا لنكونن من الخاسرين",
    ),
    SeedEntry(
        text="رب اجعلني مقيم الصلاة ومن ذريتي ربنا وتقبل دعاء",
        type_slug="quranic",
        category_slug="work",
        source="سورة إبراهيم ٤٠",
        quran_ref=(14, 40),
        dua_substring="رب اجعلني مقيم الصلاة ومن ذريتي ربنا وتقبل دعاء",
    ),
    SeedEntry(
        text="ربنا اغفر لي ولوالدي وللمؤمنين يوم يقوم الحساب",
        type_slug="quranic",
        category_slug="parents",
        source="سورة إبراهيم ٤١",
        quran_ref=(14, 41),
    ),
    SeedEntry(
        text="رب ارحمهما كما ربياني صغيرا",
        type_slug="quranic",
        category_slug="parents",
        source="سورة الإسراء ٢٤",
        quran_ref=(17, 24),
        dua_substring="رب ارحمهما كما ربياني صغيرا",
    ),
    SeedEntry(
        text="ربنا اتنا من لدنك رحمة وهيئ لنا من امرنا رشدا",
        type_slug="quranic",
        category_slug="peace",
        source="سورة الكهف ١٠",
        quran_ref=(18, 10),
        dua_substring="ربنا اتنا من لدنك رحمة وهيئ لنا من امرنا رشدا",
    ),
    SeedEntry(
        text="رب زدني علما",
        type_slug="quranic",
        category_slug="knowledge",
        source="سورة طه ١١٤",
        quran_ref=(20, 114),
        dua_substring="رب زدني علما",
    ),
    SeedEntry(
        text="لا اله الا انت سبحانك اني كنت من الظالمين",
        type_slug="quranic",
        category_slug="anxiety",
        source="سورة الأنبياء ٨٧",
        quran_ref=(21, 87),
        dua_substring="لا اله الا انت سبحانك اني كنت من الظالمين",
    ),
    SeedEntry(
        text="رب اغفر وارحم وانت خير الراحمين",
        type_slug="quranic",
        category_slug="refuge",
        source="سورة المؤمنون ١١٨",
        quran_ref=(23, 118),
        dua_substring="رب اغفر وارحم وانت خير الراحمين",
    ),
    SeedEntry(
        text="ربنا هب لنا من ازواجنا وذرياتنا قرة اعين واجعلنا للمتقين اماما",
        type_slug="quranic",
        category_slug="marriage",
        source="سورة الفرقان ٧٤",
        quran_ref=(25, 74),
        dua_substring="ربنا هب لنا من ازواجنا وذرياتنا قرة اعين واجعلنا للمتقين اماما",
    ),
    SeedEntry(
        text="رب اوزعني ان اشكر نعمتك التي انعمت علي وعلى والدي وان اعمل صالحا ترضاه",
        type_slug="quranic",
        category_slug="gratitude",
        source="سورة النمل ١٩",
        quran_ref=(27, 19),
        dua_substring=(
            "رب اوزعني ان اشكر نعمتك التي انعمت علي وعلى والدي وان اعمل صالحا ترضاه "
            "وادخلني برحمتك في عبادك الصالحين"
        ),
    ),
    SeedEntry(
        text="رب اني لما انزلت الي من خير فقير",
        type_slug="quranic",
        category_slug="provision",
        source="سورة القصص ٢٤",
        quran_ref=(28, 24),
        dua_substring="رب اني لما انزلت الي من خير فقير",
    ),
    SeedEntry(
        text="ربنا اغفر لنا ولاخواننا الذين سبقونا بالايمان",
        type_slug="quranic",
        category_slug="deceased",
        source="سورة الحشر ١٠",
        quran_ref=(59, 10),
        dua_substring=(
            "ربنا اغفر لنا ولاخواننا الذين سبقونا بالايمان ولا تجعل في قلوبنا غلا "
            "للذين امنوا ربنا انك رءوف رحيم"
        ),
    ),
    SeedEntry(
        text="ربنا اتمم لنا نورنا واغفر لنا انك على كل شيء قدير",
        type_slug="quranic",
        category_slug="hope",
        source="سورة التحريم ٨",
        quran_ref=(66, 8),
        dua_substring="ربنا اتمم لنا نورنا واغفر لنا انك على كل شيء قدير",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، "
            "وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا "
            "صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي، "
            "فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ"
        ),
        type_slug="prophetic",
        category_slug="forgiveness",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ، وَالْعَجْزِ وَالْكَسَلِ، "
            "وَالْبُخْلِ وَالْجُبْنِ، وَضَلَعِ الدَّيْنِ، وَغَلَبَةِ الرِّجَالِ"
        ),
        type_slug="prophetic",
        category_slug="anxiety",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ رَحْمَتَكَ أَرْجُو فَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ، "
            "وَأَصْلِحْ لِي شَأْنِي كُلَّهُ، لَا إِلَهَ إِلَّا أَنْتَ"
        ),
        type_slug="prophetic",
        category_slug="sadness",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text="أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ",
        type_slug="prophetic",
        category_slug="anger",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text="اللَّهُمَّ إِنَّا نَجْعَلُكَ فِي نُحُورِهِمْ، وَنَعُوذُ بِكَ مِنْ شُرُورِهِمْ",
        type_slug="prophetic",
        category_slug="fear",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text=(
            "رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ صَلَّى اللَّهُ "
            "عَلَيْهِ وَسَلَّمَ نَبِيًّا"
        ),
        type_slug="prophetic",
        category_slug="peace",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text="اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ، وَشُكْرِكَ، وَحُسْنِ عِبَادَتِكَ",
        type_slug="prophetic",
        category_slug="gratitude",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text="يَا مُقَلِّبَ الْقُلُوبِ ثَبِّتْ قَلْبِي عَلَى دِينِكَ",
        type_slug="prophetic",
        category_slug="faith",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text=(
            "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي "
            "السَّمَاءِ، وَهُوَ السَّمِيعُ الْعَلِيمُ"
        ),
        type_slug="prophetic",
        category_slug="protection",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text=(
            "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ كُلِّ شَيْطَانٍ وَهَامَّةٍ، "
            "وَمِنْ كُلِّ عَيْنٍ لَامَّةٍ"
        ),
        type_slug="prophetic",
        category_slug="evil-eye",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، "
            "وَإِلَيْكَ النُّشُورُ"
        ),
        type_slug="prophetic",
        category_slug="morning-evening",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text="بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
        type_slug="prophetic",
        category_slug="sleep",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text="اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي",
        type_slug="prophetic",
        category_slug="ramadan",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text=(
            "ذَهَبَ الظَّمَأُ، وَابْتَلَّتِ الْعُرُوقُ، وَثَبَتَ الْأَجْرُ إِنْ شَاءَ اللَّهُ"
        ),
        type_slug="prophetic",
        category_slug="ramadan",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text=(
            "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ، إِنَّ "
            "الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيكَ لَكَ"
        ),
        type_slug="prophetic",
        category_slug="hajj",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text=(
            "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ "
            "مِنِّي وَلَا قُوَّةٍ"
        ),
        type_slug="prophetic",
        category_slug="food",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text=(
            "بِسْمِ اللَّهِ وَلَجْنَا، وَبِسْمِ اللَّهِ خَرَجْنَا، وَعَلَى اللَّهِ رَبِّنَا "
            "تَوَكَّلْنَا"
        ),
        type_slug="prophetic",
        category_slug="home",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text=(
            "أَذْهِبِ الْبَأْسَ رَبَّ النَّاسِ، اشْفِ أَنْتَ الشَّافِي، لَا شِفَاءَ إِلَّا "
            "شِفَاؤُكَ، شِفَاءً لَا يُغَادِرُ سَقَمًا"
        ),
        type_slug="prophetic",
        category_slug="healing",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا، وَرِزْقًا طَيِّبًا، وَعَمَلًا "
            "مُتَقَبَّلًا"
        ),
        type_slug="prophetic",
        category_slug="provision",
        source="سنن ابن ماجه",
    ),
    SeedEntry(
        text="اللَّهُمَّ اكْفِنِي بِحَلَالِكَ عَنْ حَرَامِكَ، وَأَغْنِنِي بِفَضْلِكَ عَمَّنْ سِوَاكَ",
        type_slug="prophetic",
        category_slug="debt",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text=(
            "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ، وَإِنَّا "
            "إِلَى رَبِّنَا لَمُنْقَلِبُونَ"
        ),
        type_slug="prophetic",
        category_slug="travel",
        source="صحيح مسلم",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ انْفَعْنِي بِمَا عَلَّمْتَنِي، وَعَلِّمْنِي مَا يَنْفَعُنِي، "
            "وَزِدْنِي عِلْمًا"
        ),
        type_slug="prophetic",
        category_slug="knowledge",
        source="سنن ابن ماجه",
    ),
    SeedEntry(
        text="بَارَكَ اللَّهُ لَكَ، وَبَارَكَ عَلَيْكَ، وَجَمَعَ بَيْنَكُمَا فِي خَيْرٍ",
        type_slug="prophetic",
        category_slug="marriage",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text="اللَّهُمَّ اغْفِرْ لَهُ وَارْحَمْهُ، وَعَافِهِ وَاعْفُ عَنْهُ",
        type_slug="prophetic",
        category_slug="deceased",
        source="صحيح مسلم",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ، كَمَا صَلَّيْتَ عَلَى "
            "إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ، إِنَّكَ حَمِيدٌ مَجِيدٌ"
        ),
        type_slug="prophetic",
        category_slug="praise",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text=(
            "لَا إِلَهَ إِلَّا اللَّهُ الْعَظِيمُ الْحَلِيمُ، لَا إِلَهَ إِلَّا اللَّهُ رَبُّ "
            "الْعَرْشِ الْعَظِيمِ، لَا إِلَهَ إِلَّا اللَّهُ رَبُّ السَّمَاوَاتِ وَرَبُّ "
            "الْأَرْضِ وَرَبُّ الْعَرْشِ الْكَرِيمِ"
        ),
        type_slug="prophetic",
        category_slug="hardship",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text="اللَّهُمَّ صَيِّبًا نَافِعًا",
        type_slug="prophetic",
        category_slug="weather",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ زَوَالِ نِعْمَتِكَ، وَتَحَوُّلِ عَافِيَتِكَ، "
            "وَفُجَاءَةِ نِقْمَتِكَ، وَجَمِيعِ سَخَطِكَ"
        ),
        type_slug="prophetic",
        category_slug="protection",
        source="صحيح مسلم",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ أَصْلِحْ لِي دِينِي الَّذِي هُوَ عِصْمَةُ أَمْرِي، وَأَصْلِحْ لِي "
            "دُنْيَايَ الَّتِي فِيهَا مَعَاشِي، وَأَصْلِحْ لِي آخِرَتِي الَّتِي فِيهَا "
            "مَعَادِي"
        ),
        type_slug="prophetic",
        category_slug="guidance",
        source="صحيح مسلم",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْهُدَى وَالتُّقَى وَالْعَفَافَ وَالْغِنَى"
        ),
        type_slug="prophetic",
        category_slug="hope",
        source="صحيح مسلم",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ آتِ نَفْسِي تَقْوَاهَا، وَزَكِّهَا أَنْتَ خَيْرُ مَنْ زَكَّاهَا، "
            "أَنْتَ وَلِيُّهَا وَمَوْلَاهَا"
        ),
        type_slug="prophetic",
        category_slug="forgiveness",
        source="صحيح مسلم",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ جَهْدِ الْبَلَاءِ، وَدَرَكِ الشَّقَاءِ، "
            "وَسُوءِ الْقَضَاءِ، وَشَمَاتَةِ الْأَعْدَاءِ"
        ),
        type_slug="prophetic",
        category_slug="fear",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text=(
            "حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ، عَلَيْهِ تَوَكَّلْتُ، وَهُوَ رَبُّ "
            "الْعَرْشِ الْعَظِيمِ"
        ),
        type_slug="prophetic",
        category_slug="hardship",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ اقْسِمْ لَنَا مِنْ خَشْيَتِكَ مَا تَحُولُ بِهِ بَيْنَنَا وَبَيْنَ "
            "مَعَاصِيكَ، وَمِنْ طَاعَتِكَ مَا تُبَلِّغُنَا بِهِ جَنَّتَكَ"
        ),
        type_slug="prophetic",
        category_slug="faith",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ أَلْهِمْنِي رُشْدِي، وَأَعِذْنِي مِنْ شَرِّ نَفْسِي"
        ),
        type_slug="prophetic",
        category_slug="istikharah",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ لَا سَهْلَ إِلَّا مَا جَعَلْتَهُ سَهْلًا، وَأَنْتَ تَجْعَلُ الْحَزْنَ "
            "إِذَا شِئْتَ سَهْلًا"
        ),
        type_slug="prophetic",
        category_slug="work",
        source="صحيح ابن حبان",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ أَنْتَ الصَّاحِبُ فِي السَّفَرِ، وَالْخَلِيفَةُ فِي الْأَهْلِ، "
            "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ وَعْثَاءِ السَّفَرِ، وَكَآبَةِ الْمَنْظَرِ"
        ),
        type_slug="prophetic",
        category_slug="loneliness",
        source="صحيح مسلم",
    ),
    SeedEntry(
        text=(
            "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ"
        ),
        type_slug="prophetic",
        category_slug="sleep",
        source="صحيح البخاري",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ بِاسْمِكَ أَمُوتُ وَأَحْيَا، اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ "
            "تَبْعَثُ عِبَادَكَ"
        ),
        type_slug="prophetic",
        category_slug="morning-evening",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ اهْدِنِي وَسَدِّدْنِي، اللَّهُمَّ إِنِّي أَسْأَلُكَ الْهُدَى "
            "وَالسَّدَادَ"
        ),
        type_slug="prophetic",
        category_slug="guidance",
        source="صحيح مسلم",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ مُصَرِّفَ الْقُلُوبِ صَرِّفْ قُلُوبَنَا عَلَى طَاعَتِكَ"
        ),
        type_slug="prophetic",
        category_slug="faith",
        source="صحيح مسلم",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْبَرَصِ، وَالْجُنُونِ، وَالْجُذَامِ، "
            "وَمِنْ سَيِّئِ الْأَسْقَامِ"
        ),
        type_slug="prophetic",
        category_slug="healing",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ وَرَحْمَتِكَ، فَإِنَّهُ لَا "
            "يَمْلِكُهَا إِلَّا أَنْتَ"
        ),
        type_slug="prophetic",
        category_slug="provision",
        source="سنن الترمذي",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْكُفْرِ، وَالْفَقْرِ، وَأَعُوذُ بِكَ مِنْ "
            "عَذَابِ الْقَبْرِ"
        ),
        type_slug="prophetic",
        category_slug="refuge",
        source="سنن أبي داود",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ اجْعَلْنِي خَيْرًا مِمَّا يَظُنُّونَ، وَاغْفِرْ لِي مَا لَا "
            "يَعْلَمُونَ، وَلَا تُؤَاخِذْنِي بِمَا يَقُولُونَ"
        ),
        type_slug="athar",
        category_slug="forgiveness",
        source="أثر أبي بكر الصديق رضي الله عنه",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ ارْزُقْنِي حُبَّكَ، وَحُبَّ مَنْ يَنْفَعُنِي حُبُّهُ عِنْدَكَ"
        ),
        type_slug="athar",
        category_slug="happiness",
        source="أثر مأثور",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ اجْعَلْ خَيْرَ عُمُرِي آخِرَهُ، وَخَيْرَ عَمَلِي خَوَاتِمَهُ، "
            "وَخَيْرَ أَيَّامِي يَوْمَ أَلْقَاكَ"
        ),
        type_slug="athar",
        category_slug="hope",
        source="أثر مأثور",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ إِنِّي أَسْأَلُكَ الرِّضَا بَعْدَ الْقَضَاءِ، وَبَرْدَ الْعَيْشِ "
            "بَعْدَ الْمَوْتِ"
        ),
        type_slug="athar",
        category_slug="peace",
        source="أثر مأثور",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ ارْزُقْنَا قُلُوبًا خَاشِعَةً، وَأَلْسِنَةً ذَاكِرَةً، وَأَعْمَالًا "
            "صَالِحَةً مُتَقَبَّلَةً"
        ),
        type_slug="custom",
        category_slug="faith",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ اشْرَحْ صَدْرِي، وَيَسِّرْ أَمْرِي، وَبَارِكْ لِي فِي عَمَلِي، "
            "وَاجْعَلْنِي مِنَ النَّاجِحِينَ"
        ),
        type_slug="custom",
        category_slug="work",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ اجْعَلْ يَوْمِي خَيْرًا مِنْ أَمْسِي، وَغَدِي خَيْرًا مِنْ يَوْمِي، "
            "وَاخْتِمْ بِالصَّالِحَاتِ أَعْمَالِي"
        ),
        type_slug="custom",
        category_slug="hope",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ آنِسْ وَحْشَتِي، وَارْحَمْ غُرْبَتِي، وَكُنْ لِي خَيْرَ مُؤْنِسٍ "
            "وَمُعِينٍ"
        ),
        type_slug="custom",
        category_slug="loneliness",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ هَوِّنْ عَلَيَّ سَكَرَاتِ الْمَوْتِ، وَثَبِّتْنِي بِالْقَوْلِ "
            "الثَّابِتِ عِنْدَ السُّؤَالِ"
        ),
        type_slug="custom",
        category_slug="fear",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ احْفَظْ أَوْلَادِي مِنْ كُلِّ سُوءٍ، وَأَنْبِتْهُمْ نَبَاتًا "
            "حَسَنًا، وَاجْعَلْهُمْ قُرَّةَ عَيْنٍ لِي"
        ),
        type_slug="custom",
        category_slug="family",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ بَارِكْ لِي فِي رِزْقِي، وَوَسِّعْ عَلَيَّ مِنْ فَضْلِكَ، وَاكْفِنِي "
            "بِحَلَالِكَ عَنْ حَرَامِكَ"
        ),
        type_slug="custom",
        category_slug="provision",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ ارْزُقْنِي شُكْرَ نِعْمَتِكَ، وَدَوَامَ عَافِيَتِكَ، وَحُسْنَ "
            "خِتَامِي عِنْدَكَ"
        ),
        type_slug="custom",
        category_slug="gratitude",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ اجْعَلْ هَذَا الْبَيْتَ عَامِرًا بِذِكْرِكَ، مَحْفُوظًا بِحِفْظِكَ، "
            "مَلِيئًا بِالْمَوَدَّةِ وَالرَّحْمَةِ"
        ),
        type_slug="custom",
        category_slug="home",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ فَرِّحْ قَلْبِي بِطَاعَتِكَ، وَامْلَأْ حَيَاتِي بِرِضَاكَ، "
            "وَاجْعَلْ سَعَادَتِي فِي قُرْبِكَ"
        ),
        type_slug="custom",
        category_slug="happiness",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ ارْفَعْ عَنَّا الْغَلَاءَ وَالْوَبَاءَ، وَأَنْزِلْ عَلَيْنَا "
            "الْغَيْثَ وَالرَّحْمَةَ"
        ),
        type_slug="custom",
        category_slug="weather",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ ارْزُقْنِي بِرَّ وَالِدَيَّ فِي حَيَاتِهِمَا، وَالدُّعَاءَ "
            "لَهُمَا بَعْدَ مَمَاتِهِمَا"
        ),
        type_slug="custom",
        category_slug="parents",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ وَفِّقْنِي فِي دِرَاسَتِي، وَافْتَحْ عَلَيَّ فُتُوحَ الْعَارِفِينَ، "
            "وَثَبِّتْ مَا تَعَلَّمْتُهُ فِي قَلْبِي"
        ),
        type_slug="custom",
        category_slug="knowledge",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ اقْضِ عَنِّي دَيْنِي، وَأَغْنِنِي مِنَ الْفَقْرِ، وَبَارِكْ لِي "
            "فِيمَا رَزَقْتَنِي"
        ),
        type_slug="custom",
        category_slug="debt",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ احْفَظْنِي فِي سَفَرِي، وَرُدَّنِي إِلَى أَهْلِي سَالِمًا "
            "غَانِمًا بِخَيْرٍ"
        ),
        type_slug="custom",
        category_slug="travel",
        source="دعاء عام",
    ),
    SeedEntry(
        text=(
            "اللَّهُمَّ ارْزُقْنِي زَوْجًا صَالِحًا، وَذُرِّيَّةً طَيِّبَةً، وَبَيْتًا "
            "تَسْكُنُ إِلَيْهِ النَّفْسُ"
        ),
        type_slug="custom",
        category_slug="marriage",
        source="دعاء عام",
    ),
]
