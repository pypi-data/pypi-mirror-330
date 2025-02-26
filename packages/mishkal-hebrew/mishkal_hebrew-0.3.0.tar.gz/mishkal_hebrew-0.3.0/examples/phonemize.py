"""
Quick Nakdan https://nakdanlive.dicta.org.il
Pro Nakdan https://nakdanpro.dicta.org.il
Manual Nakdan https://www.yo-yoo.co.il/tools/niqqud
"""
from mishkal import phonemize

sentences = [
    'הִיא אָמְרָה לִי', # Hirik with Yod vowel
    'מָה קוֹרֶה?', # Vav with Holam vowel
    'הוּא קֵרֵחַ', # Het gnuva
    "גִ'ירָפָה זַ'רְגּוֹן", # Geresh
    "שָׁלוֹם שׂוֹרֵר", # Shin Sin
    "לְבִיבָה יְלָדִים שְׁאֵלָה בְּהֵמָה זְעָקוֹת בְּרֹאשׁ גּוֹרְרִים מְצַפְצְפִים מִרְפְּאוֹתֵיהֶם", # Shva na
    "בְּרוֹשׁ סְבִיבָה בְּרָגִים שְׁפֵלָה בְּרֵכָה זְנָבוֹת גּוֹרְמִים הָלַכְתְּ וּבְרָכָה", # Shva nax
    "אַתָּה חַיָּב לִי 50 שֶׁקֶל וְהַסֵּמֶל הוּא ₪", # numbers, symbols
    "כל", # dictionary
    "ווֹלְטֶר", # double vav start
    "הֲווֹלְטֶר", # double vav middle
    "אֶלֶגַנְטִי", # lookup
    "כָּל", # match to one without niqqud
    "יִשְׂרָאֵל הוּקְמָה בִּשְׁנַת 1948",
    "₪",
    "מָחָר בְּשָׁעָה 22:00", # time to word
    "אוֹרוֹת ווֹלְטֶר ווֹלֶנְטַיְן אֻרְווֹת אוֹרְחִים אָרְבוּ הוֹוֶה וּוּבְּרִים וָו וִי וּוִיקְטוֹר", # Vavs
    "לְמַיִם אֱלֹהֵי",
    "שְׁמַע אָח שֶׁלִּי, תִּרְאֶה. נִרְאֶה לִי שֶׁזֶּה עוֹבֵד!",
    "גִ'ירָפָה",
    "יִהְיֶה",
    "בְּמָה",
]


for sentence in sentences:
    phonemes = phonemize(sentence, preserve_punctuation=True)
    print(phonemes)