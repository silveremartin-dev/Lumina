"""Module de normalisation morphologique et lemmatisation tolérante pour Lumina.
Gère la désaccentuation tolérante, la lemmatisation verbale, nominale et adjectivale (Français et Anglais),
ainsi que la reconnaissance d'expressions multi-mots.
"""

import re
import unicodedata

def strip_accents(text: str) -> str:
    """Supprime les accents d'une chaîne pour la recherche tolérante."""
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Dictionnaire de formes verbales irrégulières françaises vers leur infinitif
IRREGULAR_VERBS_FR = {
    # Être
    "suis": "être", "es": "être", "est": "être", "sommes": "être", "êtes": "être", "sont": "être",
    "étais": "être", "était": "être", "étions": "être", "étiez": "être", "étaient": "être", "été": "être",
    "serai": "être", "seras": "être", "sera": "être", "serons": "être", "serez": "être", "seront": "être",
    "serais": "être", "serait": "être", "sois": "être", "soit": "être", "soient": "être",

    # Avoir
    "ai": "avoir", "as": "avoir", "a": "avoir", "avons": "avoir", "avez": "avoir", "ont": "avoir",
    "avais": "avoir", "avait": "avoir", "avions": "avoir", "aviez": "avoir", "avaient": "avoir", "eu": "avoir",
    "aurai": "avoir", "auras": "avoir", "aura": "avoir", "aurons": "avoir", "aurez": "avoir", "auront": "avoir",

    # Vouloir
    "veux": "vouloir", "veut": "vouloir", "voulons": "vouloir", "voulez": "vouloir", "veulent": "vouloir",
    "voulais": "vouloir", "voulait": "vouloir", "voulaient": "vouloir", "voulu": "vouloir",
    "voudrais": "vouloir", "voudrait": "vouloir", "voudrons": "vouloir", "voudrez": "vouloir", "voudraient": "vouloir",

    # Pouvoir
    "peux": "pouvoir", "peut": "pouvoir", "pouvons": "pouvoir", "pouvez": "pouvoir", "peuvent": "pouvoir",
    "pouvais": "pouvoir", "pouvait": "pouvoir", "pouvaient": "pouvoir", "pu": "pouvoir",
    "pourrais": "pouvoir", "pourrait": "pouvoir", "pourrons": "pouvoir", "pourrez": "pouvoir", "pourraient": "pouvoir",

    # Devoir
    "dois": "devoir", "doit": "devoir", "devons": "devoir", "devez": "devoir", "doivent": "devoir",
    "devais": "devoir", "devait": "devoir", "devaient": "devoir", "dû": "devoir", "du": "devoir",
    "devrais": "devoir", "devrait": "devoir", "devrons": "devoir", "devrez": "devoir",

    # Savoir
    "sais": "savoir", "sait": "savoir", "savons": "savoir", "savez": "savoir", "savent": "savoir",
    "savais": "savoir", "savait": "savoir", "savaient": "savoir", "su": "savoir",
    "saurai": "savoir", "saurait": "savoir",

    # Aller
    "vais": "aller", "vas": "aller", "va": "aller", "allons": "aller", "allez": "aller", "vont": "aller",
    "allais": "aller", "allait": "aller", "allaient": "aller", "allé": "aller", "allée": "aller",
    "irai": "aller", "iras": "aller", "ira": "aller", "irons": "aller", "irez": "aller", "iront": "aller",

    # Venir
    "viens": "venir", "vient": "venir", "venons": "venir", "venez": "venir", "viennent": "venir",
    "venais": "venir", "venait": "venir", "venaient": "venir", "venu": "venir", "venue": "venir",
    "viendrai": "venir", "viendra": "venir", "viendrait": "venir",

    # Prendre
    "prends": "prendre", "prend": "prendre", "prenons": "prendre", "prenez": "prendre", "prennent": "prendre",
    "prenais": "prendre", "prenait": "prendre", "prenaient": "prendre", "pris": "prendre", "prise": "prendre",
    "prendrai": "prendre", "prendra": "prendre",

    # Faire
    "fais": "faire", "fait": "faire", "faisons": "faire", "faites": "faire", "font": "faire",
    "faisais": "faire", "faisait": "faire", "faisaient": "faire",
    "ferai": "faire", "fera": "faire", "ferait": "faire",

    # Dire
    "dis": "dire", "dit": "dire", "disons": "dire", "dites": "dire", "disent": "dire",
    "disais": "dire", "disait": "dire", "disaient": "dire",
    "dirai": "dire", "dira": "dire", "dirait": "dire",

    # Voir
    "vois": "voir", "voit": "voir", "voyons": "voir", "voyez": "voir", "voient": "voir",
    "voyais": "voir", "voyait": "voir", "voyaient": "voir", "vu": "voir", "vue": "voir",
    "verrai": "voir", "verra": "voir", "verrait": "voir",

    # Mettre
    "mets": "mettre", "met": "mettre", "mettons": "mettre", "mettez": "mettre", "mettent": "mettre",
    "mettais": "mettre", "mettait": "mettre", "mettaient": "mettre", "mis": "mettre", "mise": "mettre",
    "mettrai": "mettre", "mettra": "mettre",

    # Comprendre
    "comprends": "comprendre", "comprend": "comprendre", "comprenons": "comprendre", "comprenez": "comprendre", "comprennent": "comprendre",
    "comprenais": "comprendre", "comprenait": "comprendre", "compris": "comprendre", "comprise": "comprendre",

    # Boire
    "bois": "boire", "boit": "boire", "buvons": "boire", "buvez": "boire", "boivent": "boire",
    "buvais": "boire", "buvait": "boire", "bu": "boire",

    # Connaître
    "connais": "connaître", "connaît": "connaître", "connait": "connaître", "connaissons": "connaître",
    "connaissez": "connaître", "connaissent": "connaître", "connaissais": "connaître", "connaissait": "connaître", "connu": "connaître",

    # Écrire
    "écris": "écrire", "écrit": "écrire", "écrivons": "écrire", "écrivez": "écrire", "écrivent": "écrire",
    "écrivais": "écrire", "écrivait": "écrire",
    # Lire
    "lis": "lire", "lit": "lire", "lisons": "lire", "lisez": "lire", "lisent": "lire",
    "lisais": "lire", "lisait": "lire", "lu": "lire",
    # Dormir
    "dors": "dormir", "dort": "dormir", "dormons": "dormir", "dormez": "dormir", "dorment": "dormir",
    "dormais": "dormir", "dormait": "dormir", "dormi": "dormir",
    # Courir
    "cours": "courir", "court": "courir", "courons": "courir", "courez": "courir", "courent": "courir",
    "courais": "courir", "courait": "courir", "couru": "courir",
}

# Locutions françaises et correspondances directes
MULTI_WORD_EXPRESSIONS_FR = [
    (r"\b(s'il vous plaît|s il vous plait|s'il te plaît|s il te plait)\b", "fape"),
    (r"\b(comment ça va|comment ca va|comment vas-tu|comment vas tu|comment allez-vous|comment allez vous)\b", "Ma Tina shili zelu"),
    (r"\b(je m'appelle|je m appelle|je me nomme)\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", r"Mina nomi \2"),
    (r"\b(tu t'appelles|tu t’appelles|tu te nommes)\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", r"Tina nomi \2"),
    (r"\b(il s'appelle|elle s'appelle)\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", r"Lina nomi \2"),
    (r"\b(au revoir|aurevoir|adieu|à bientôt|a bientot)\b", "fata"),
    (r"\b(merci beaucoup|merci bien|merci)\b", "fama"),
    (r"\b(s'il vous plait|s il vous plait|s il te plait)\b", "fape"),
    (r"\b(de rien|je vous en prie|je t'en prie)\b", "sulo"),
    (r"\b(tout va bien|ça va bien|ca va bien|je vais bien)\b", "Mina shili zelu"),
    (r"\b(il fait beau aujourd'hui|il fait beau aujourd hui)\b", "tana to shili suka"),
    (r"\b(il fait beau)\b", "to shili suka"),
    (r"\b(aujourd'hui|aujourd hui)\b", "tana to"),
    (r"\b(ce soir)\b", "tasi to"),
    (r"\b(ce matin)\b", "tana to"),
    (r"\b(cette nuit)\b", "tusa to"),
    (r"\b(cette année|cette annee)\b", "tara to"),
    (r"\b(cette semaine)\b", "teki to"),
    (r"\b(le long de|le long du|le long des)\b", "ko"),
    (r"\b(à travers|a travers)\b", "ko"),
    (r"\b(au milieu de|au milieu du)\b", "kiso pa"),
    (r"\b(à côté de|a cote de|pres de|près de)\b", "ko"),
    (r"\b(combien coûte|combien coute|combien de|combien)\b", "paka keli"),
    (r"\b(tout le monde)\b", "masa tota"),
    (r"\b(quelque chose)\b", "hano"),
    (r"\b(rien du tout)\b", "hno"),
    (r"\b(n'importe quoi)\b", "hano"),
    (r"\b(il y a|il y avait)\b", "shili"),
    (r"\b(c'est|c est)\b", "to shili"),
    (r"\b(ce n'est pas|ce n est pas)\b", "to ne shili"),
    (r"\b(je voudrais|j'aimerais|je souhaiterais)\b", "Mina zhivi"),
]

# Locutions anglaises
MULTI_WORD_EXPRESSIONS_EN = [
    (r"\b(how are you doing|how are you|how do you do)\b", "Ma Tina shili zelu"),
    (r"\b(my name is|i am called)\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", r"Mina nomi \2"),
    (r"\b(your name is|you are called)\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", r"Tina nomi \2"),
    (r"\b(his name is|her name is)\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", r"Lina nomi \2"),
    (r"\b(thank you very much|thank you|thanks a lot|thanks)\b", "fama"),
    (r"\b(you are welcome|you're welcome|no problem)\b", "sulo"),
    (r"\b(i am well|i am fine|i'm well|i'm fine|doing well)\b", "Mina shili zelu"),
    (r"\b(the weather is good today|weather is good)\b", "tana to shili suka"),
    (r"\b(right now|at the moment)\b", "tli"),
    (r"\b(today)\b", "tana to"),
    (r"\b(tonight)\b", "tusa to"),
    (r"\b(this morning)\b", "tana to"),
    (r"\b(this evening)\b", "tasi to"),
    (r"\b(this year)\b", "tara to"),
    (r"\b(this week)\b", "teki to"),
    (r"\b(how much|how many)\b", "paka keli"),
    (r"\b(everyone|everybody)\b", "masa tota"),
    (r"\b(there is|there are|there was|there were)\b", "shili"),
    (r"\b(i would like|i'd like)\b", "Mina zhivi"),
    (r"\b(along|alongside)\b", "ko"),
    (r"\b(across|through)\b", "ko"),
]

def lemmatize_french_word(word: str, lexicon_dict: dict) -> tuple:
    """
    Tente de trouver la forme canonique ou la racine Lumina pour un mot français.
    Retourne (lumina_root, tense_flag) ou (None, None).
    """
    w = word.lower().strip()
    if not w:
        return None, None

    w_no_acc = strip_accents(w)

    # 1. Vérification directe (avec et sans accents)
    if w in lexicon_dict:
        return lexicon_dict[w], None
    if w_no_acc in lexicon_dict:
        return lexicon_dict[w_no_acc], None

    # 2. Formes verbales irrégulières
    if w in IRREGULAR_VERBS_FR:
        inf = IRREGULAR_VERBS_FR[w]
        lum = lexicon_dict.get(inf, lexicon_dict.get(strip_accents(inf)))
        if lum:
            # Détection de temps
            tense = "na" if w in ["étais", "était", "étions", "étaient", "été", "avais", "avait", "avions", "avaient", "eu", "voulais", "voulait", "voulu", "pouvais", "pouvait", "pu", "devait", "dû", "savais", "savait", "su", "allait", "allé", "venait", "venu", "prenait", "pris", "faisait", "fait", "disait", "dit", "voyait", "vu", "mettait", "mis", "bu", "buvait", "connu", "lu", "écrit", "dormi", "couru"] else None
            if w in ["serai", "sera", "serons", "seront", "aurai", "aura", "voudra", "pourra", "devra", "saurai", "saura", "ira", "viendra", "prendra", "fera", "dira", "verra"]:
                tense = "vo"
            return lum, tense

    # 3. Lemmatisation des verbes réguliers du 1er groupe (-er)
    # Cherche si w provient d'un verbe en -er
    er_suffixes = [
        # Imparfait / Conditionnel
        ("eraient", "er", "na"), ("erait", "er", "na"), ("erais", "er", "na"),
        ("erons", "er", "vo"), ("erez", "er", "vo"), ("eront", "er", "vo"),
        ("erai", "er", "vo"), ("eras", "er", "vo"), ("era", "er", "vo"),
        ("aient", "er", "na"), ("ions", "er", "na"), ("iez", "er", "na"),
        ("ait", "er", "na"), ("ais", "er", "na"),
        # Participe passé
        ("ees", "er", "na"), ("ee", "er", "na"), ("es", "er", "na"),
        ("e", "er", None), ("ons", "er", None), ("ez", "er", None), ("ent", "er", None),
        ("ant", "er", None)
    ]
    
    # Tester avec accents : -é, -ée, -és, -ées
    if w.endswith("ées"):
        cand = w[:-3] + "er"
        if cand in lexicon_dict: return lexicon_dict[cand], "na"
    elif w.endswith("ée"):
        cand = w[:-2] + "er"
        if cand in lexicon_dict: return lexicon_dict[cand], "na"
    elif w.endswith("és"):
        cand = w[:-2] + "er"
        if cand in lexicon_dict: return lexicon_dict[cand], "na"
    elif w.endswith("é"):
        cand = w[:-1] + "er"
        if cand in lexicon_dict: return lexicon_dict[cand], "na"

    for suf, repl, tense in er_suffixes:
        if w_no_acc.endswith(suf) and len(w_no_acc) > len(suf) + 2:
            base = w_no_acc[:-len(suf)]
            cand = base + repl
            if cand in lexicon_dict:
                return lexicon_dict[cand], tense
            cand_acc = base + "er"
            # Chercher dans lexicon_dict une correspondance sans accent
            for k, val in lexicon_dict.items():
                if strip_accents(k) == cand:
                    return val, tense

    # 4. Lemmatisation des verbes en -ir (2e groupe)
    ir_suffixes = [
        ("issaient", "ir", "na"), ("issait", "ir", "na"), ("issais", "ir", "na"),
        ("issons", "ir", None), ("issez", "ir", None), ("issent", "ir", None),
        ("ira", "ir", "vo"), ("irai", "ir", "vo"),
        ("it", "ir", None), ("is", "ir", None), ("i", "ir", "na")
    ]
    for suf, repl, tense in ir_suffixes:
        if w_no_acc.endswith(suf) and len(w_no_acc) > len(suf) + 2:
            cand = w_no_acc[:-len(suf)] + repl
            if cand in lexicon_dict:
                return lexicon_dict[cand], tense
            for k, val in lexicon_dict.items():
                if strip_accents(k) == cand:
                    return val, tense

    # 5. Noms et adjectifs pluriels / féminins
    if w_no_acc.endswith("s") and len(w_no_acc) > 2:
        cand = w_no_acc[:-1]
        if cand in lexicon_dict:
            return lexicon_dict[cand], None
        for k, val in lexicon_dict.items():
            if strip_accents(k) == cand:
                return val, None
    if w_no_acc.endswith("x") and len(w_no_acc) > 2:
        cand = w_no_acc[:-1]
        if cand in lexicon_dict:
            return lexicon_dict[cand], None
        cand_al = w_no_acc[:-3] + "al" if w_no_acc.endswith("aux") else None
        if cand_al and cand_al in lexicon_dict:
            return lexicon_dict[cand_al], None

    # Féminin régulier en -e
    if w_no_acc.endswith("e") and len(w_no_acc) > 3:
        cand = w_no_acc[:-1]
        if cand in lexicon_dict:
            return lexicon_dict[cand], None
        for k, val in lexicon_dict.items():
            if strip_accents(k) == cand:
                return val, None

    return None, None

def lemmatize_english_word(word: str, lexicon_dict: dict) -> tuple:
    """
    Tente de trouver la forme canonique ou la racine Lumina pour un mot anglais.
    Retourne (lumina_root, tense_flag) ou (None, None).
    """
    w = word.lower().strip()
    if not w:
        return None, None

    # 1. Vérification directe
    if w in lexicon_dict:
        return lexicon_dict[w], None

    # 2. Verbes irréguliers fréquents anglais
    irreg_en = {
        "ran": ("run", "na"), "went": ("go", "na"), "gone": ("go", "na"),
        "came": ("come", "na"), "saw": ("see", "na"), "seen": ("see", "na"),
        "ate": ("eat", "na"), "eaten": ("eat", "na"), "drank": ("drink", "na"), "drunk": ("drink", "na"),
        "slept": ("sleep", "na"), "flew": ("fly", "na"), "flown": ("fly", "na"),
        "knew": ("know", "na"), "known": ("know", "na"), "thought": ("think", "na"),
        "bought": ("buy", "na"), "found": ("find", "na"), "met": ("meet", "na"),
        "told": ("tell", "na"), "said": ("say", "na"), "spoke": ("speak", "na"), "spoken": ("speak", "na"),
        "wrote": ("write", "na"), "written": ("write", "na"), "gave": ("give", "na"), "given": ("give", "na"),
        "took": ("take", "na"), "taken": ("take", "na"), "brought": ("bring", "na"),
        "swam": ("swim", "na"), "built": ("build", "na"), "felt": ("feel", "na"),
        "heard": ("hear", "na"), "understood": ("understand", "na"),
    }
    if w in irreg_en:
        base, tense = irreg_en[w]
        lum = lexicon_dict.get(base)
        if lum:
            return lum, tense

    # 3. Suffixes verbaux réguliers (-ing, -ed, -s, -es)
    if w.endswith("ing") and len(w) > 4:
        cand1 = w[:-3]
        cand2 = w[:-3] + "e"
        cand3 = w[:-4] if len(w) > 5 and w[-4] == w[-5] else None  # running -> run
        for cand in [cand1, cand2, cand3]:
            if cand and cand in lexicon_dict:
                return lexicon_dict[cand], None

    if w.endswith("ed") and len(w) > 3:
        cand1 = w[:-2]
        cand2 = w[:-1]  # closed -> close
        cand3 = w[:-3] + "y" if w.endswith("ied") else None
        for cand in [cand1, cand2, cand3]:
            if cand and cand in lexicon_dict:
                return lexicon_dict[cand], "na"

    # Pluriels et 3e personne du singulier (-s, -es, -ies)
    if w.endswith("ies") and len(w) > 4:
        cand = w[:-3] + "y"
        if cand in lexicon_dict:
            return lexicon_dict[cand], None

    if w.endswith("es") and len(w) > 3:
        cand = w[:-2]
        if cand in lexicon_dict:
            return lexicon_dict[cand], None

    if w.endswith("s") and len(w) > 2:
        cand = w[:-1]
        if cand in lexicon_dict:
            return lexicon_dict[cand], None

    return None, None
