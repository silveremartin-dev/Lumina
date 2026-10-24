"""Moteur de traduction bidirectionnel entre le Lumina et le Français / Anglais."""

import re
import json
from pathlib import Path
from .analyzer import LuminaAnalyzer
from .lemmatizer import (
    lemmatize_french_word, lemmatize_english_word,
    MULTI_WORD_EXPRESSIONS_FR, MULTI_WORD_EXPRESSIONS_EN,
    strip_accents
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class LuminaTranslator:
    # Formes verbales françaises courantes mappées vers leur infinitif ou racine Lumina
    COMMON_VERBS = {
        # Être (shili)
        "suis": ("shili", None), "es": ("shili", None), "est": ("shili", None),
        "sommes": ("shili", None), "êtes": ("shili", None), "sont": ("shili", None),
        "étais": ("shili", "na"), "était": ("shili", "na"), "étions": ("shili", "na"),
        "étiez": ("shili", "na"), "étaient": ("shili", "na"), "été": ("shili", "na"),
        "serai": ("shili", "vo"), "seras": ("shili", "vo"), "sera": ("shili", "vo"),
        "serons": ("shili", "vo"), "serez": ("shili", "vo"), "seront": ("shili", "vo"),
        "être": ("shili", None),

        # Avoir (possession / passé)
        "ai": ("shili", "na"), "as": ("shili", "na"), "a": ("shili", "na"),
        "avons": ("shili", "na"), "avez": ("shili", "na"), "ont": ("shili", "na"),
        "avais": ("shili", "na"), "avait": ("shili", "na"), "avions": ("shili", "na"),
        "aviez": ("shili", "na"), "avaient": ("shili", "na"), "eu": ("shili", "na"),
        "aurai": ("shili", "vo"), "auras": ("shili", "vo"), "aura": ("shili", "vo"),

        # S'appeler / Nommer (nomi)
        "appelle": ("nomi", None), "appelles": ("nomi", None), "appelons": ("nomi", None),
        "appelez": ("nomi", None), "appellent": ("nomi", None), "appelé": ("nomi", "na"),
        "appeler": ("nomi", None),

        # Voir (sifi)
        "vois": ("sifi", None), "voit": ("sifi", None), "voyons": ("sifi", None),
        "voyez": ("sifi", None), "voient": ("sifi", None), "voyais": ("sifi", "na"),
        "voyait": ("sifi", "na"), "vu": ("sifi", "na"), "verrai": ("sifi", "vo"),
        "verra": ("sifi", "vo"), "voir": ("sifi", None),

        # Manger (kidi)
        "mange": ("kidi", None), "manges": ("kidi", None), "mangeons": ("kidi", None),
        "mangez": ("kidi", None), "mangent": ("kidi", None), "mangeais": ("kidi", "na"),
        "mangeait": ("kidi", "na"), "mangé": ("kidi", "na"), "mangera": ("kidi", "vo"),
        "manger": ("kidi", None),

        # Faire / Créer (kisi)
        "fais": ("kisi", None), "fait": ("kisi", None), "faisons": ("kisi", None),
        "faites": ("kisi", None), "font": ("kisi", None), "faisais": ("kisi", "na"),
        "faisait": ("kisi", "na"), "fera": ("kisi", "vo"), "ferai": ("kisi", "vo"),
        "faire": ("kisi", None),

        # Dire / Parler (fidi)
        "dis": ("fidi", None), "dit": ("fidi", None), "disons": ("fidi", None),
        "dites": ("fidi", None), "disent": ("fidi", None), "disais": ("fidi", "na"),
        "disait": ("fidi", "na"), "dira": ("fidi", "vo"), "dire": ("fidi", None),
        "parle": ("fidi", None), "parles": ("fidi", None), "parlons": ("fidi", None),
        "parlez": ("fidi", None), "parlent": ("fidi", None), "parlé": ("fidi", "na"),
        "parler": ("fidi", None),

        # Penser (pishi)
        "pense": ("pishi", None), "penses": ("pishi", None), "pensons": ("pishi", None),
        "pensez": ("pishi", None), "pensent": ("pishi", None), "pensé": ("pishi", "na"),
        "pensait": ("pishi", "na"), "penser": ("pishi", None),

        # Montrer (fisi)
        "montre": ("fisi", None), "montres": ("fisi", None), "montrons": ("fisi", None),
        "montrez": ("fisi", None), "montrent": ("fisi", None), "montré": ("fisi", "na"),
        "montrait": ("fisi", "na"), "montrer": ("fisi", None),

        # Bouger / Se mouvoir (lifi)
        "bouge": ("lifi", None), "bouges": ("lifi", None), "bougeons": ("lifi", None),
        "bougez": ("lifi", None), "bougent": ("lifi", None), "bougé": ("lifi", "na"),
        "bouger": ("lifi", None),

        # Dormir (somo)
        "dors": ("somo", None), "dort": ("somo", None), "dormons": ("somo", None),
        "dormez": ("somo", None), "dorment": ("somo", None), "dormi": ("somo", "na"),
        "dormait": ("somo", "na"), "dormir": ("somo", None),

        # Voler dans l'air (voli)
        "vole": ("voli", None), "voles": ("voli", None), "volons": ("voli", None),
        "volez": ("voli", None), "volent": ("voli", None), "volé": ("voli", "na"),
        "volait": ("voli", "na"), "volera": ("voli", "vo"), "voler": ("voli", None),

        # Piloter / Conduire (miva)
        "pilote": ("miva", None), "pilotes": ("miva", None), "pilotons": ("miva", None),
        "pilotez": ("miva", None), "pilotent": ("miva", None), "piloté": ("miva", "na"),
        "pilotait": ("miva", "na"), "piloter": ("miva", None),

        # Savoir / Connaître (shaki)
        "sais": ("shaki", None), "sait": ("shaki", None), "savons": ("shaki", None),
        "savez": ("shaki", None), "savent": ("shaki", None), "savais": ("shaki", "na"),
        "savait": ("shaki", "na"), "su": ("shaki", "na"), "savoir": ("shaki", None),
        "connais": ("shaki", None), "connaît": ("shaki", None), "connait": ("shaki", None),
        "connaissons": ("shaki", None), "connaissez": ("shaki", None), "connaissent": ("shaki", None),
        "connu": ("shaki", "na"), "connaître": ("shaki", None),

        # Pouvoir (zhipi)
        "peux": ("zhipi", None), "peut": ("zhipi", None), "pouvons": ("zhipi", None),
        "pouvez": ("zhipi", None), "peuvent": ("zhipi", None), "pouvais": ("zhipi", "na"),
        "pouvait": ("zhipi", "na"), "pu": ("zhipi", "na"), "pourra": ("zhipi", "vo"),
        "pourrais": ("zhipi", None), "pourrait": ("zhipi", None), "pouvoir": ("zhipi", None),

        # Vouloir (zhivi)
        "veux": ("zhivi", None), "veut": ("zhivi", None), "voulons": ("zhivi", None),
        "voulez": ("zhivi", None), "veulent": ("zhivi", None), "voulais": ("zhivi", "na"),
        "voulait": ("zhivi", "na"), "voulu": ("zhivi", "na"), "voudra": ("zhivi", "vo"),
        "voudrais": ("zhivi", None), "voudrait": ("zhivi", None), "vouloir": ("zhivi", None),

        # Chercher (mita)
        "cherche": ("mita", None), "cherches": ("mita", None), "cherchons": ("mita", None),
        "cherchez": ("mita", None), "cherchent": ("mita", None), "cherchait": ("mita", "na"),
        "cherché": ("mita", "na"), "chercher": ("mita", None),

        # Marcher (kivi)
        "marche": ("kivi", None), "marches": ("kivi", None), "marchons": ("kivi", None),
        "marchez": ("kivi", None), "marchent": ("kivi", None), "marchait": ("kivi", "na"),
        "marché": ("kivi", "na"), "marcher": ("kivi", None),

        # Devoir (debi)
        "dois": ("debi", None), "doit": ("debi", None), "devons": ("debi", None),
        "devez": ("debi", None), "doivent": ("debi", None), "devait": ("debi", "na"),
        "dû": ("debi", "na"), "devra": ("debi", "vo"), "devoir": ("debi", None),

        # Trouver (tovi)
        "trouve": ("tovi", None), "trouves": ("tovi", None), "trouvons": ("tovi", None),
        "trouvez": ("tovi", None), "trouvent": ("tovi", None), "trouvé": ("tovi", "na"),
        "trouvait": ("tovi", "na"), "trouver": ("tovi", None),

        # Comprendre (piko)
        "comprends": ("piko", None), "comprend": ("piko", None), "comprenons": ("piko", None),
        "comprenez": ("piko", None), "comprennent": ("piko", None), "compris": ("piko", "na"),
        "comprenait": ("piko", "na"), "comprendre": ("piko", None),

        # Aimer (zimo)
        "aime": ("zimo", None), "aimes": ("zimo", None), "aimons": ("zimo", None),
        "aimez": ("zimo", None), "aiment": ("zimo", None), "aimé": ("zimo", "na"),
        "aimer": ("zimo", None),

        # Aller / Partir (lika)
        "vais": ("lika", None), "vas": ("lika", None), "va": ("lika", None),
        "allons": ("lika", None), "allez": ("lika", None), "vont": ("lika", None),
        "allais": ("lika", "na"), "allait": ("lika", "na"), "allé": ("lika", "na"),
        "ira": ("lika", "vo"), "irai": ("lika", "vo"), "aller": ("lika", None),
    }

    COMMON_VERBS_EN = {
        "am": ("shili", None), "is": ("shili", None), "are": ("shili", None),
        "was": ("shili", "na"), "were": ("shili", "na"), "been": ("shili", "na"), "be": ("shili", None),
        "have": ("shili", None), "has": ("shili", None), "had": ("shili", "na"),
        "do": ("kisi", None), "does": ("kisi", None), "did": ("kisi", "na"), "done": ("kisi", "na"),
        "make": ("kisi", None), "makes": ("kisi", None), "made": ("kisi", "na"),
        "see": ("sifi", None), "sees": ("sifi", None), "saw": ("sifi", "na"), "seen": ("sifi", "na"),
        "look": ("sifi", None), "looks": ("sifi", None), "looked": ("sifi", "na"),
        "eat": ("kidi", None), "eats": ("kidi", None), "ate": ("kidi", "na"), "eaten": ("kidi", "na"),
        "say": ("fidi", None), "says": ("fidi", None), "said": ("fidi", "na"),
        "speak": ("fidi", None), "speaks": ("fidi", None), "spoke": ("fidi", "na"), "spoken": ("fidi", "na"),
        "talk": ("fidi", None), "talks": ("fidi", None), "talked": ("fidi", "na"),
        "tell": ("fidi", None), "tells": ("fidi", None), "told": ("fidi", "na"),
        "think": ("pishi", None), "thinks": ("pishi", None), "thought": ("pishi", "na"),
        "show": ("fisi", None), "shows": ("fisi", None), "showed": ("fisi", "na"), "shown": ("fisi", "na"),
        "move": ("lifi", None), "moves": ("lifi", None), "moved": ("lifi", "na"),
        "sleep": ("somo", None), "sleeps": ("somo", None), "slept": ("somo", "na"),
        "fly": ("voli", None), "flies": ("voli", None), "flew": ("voli", "na"), "flown": ("voli", "na"),
        "know": ("shaki", None), "knows": ("shaki", None), "knew": ("shaki", "na"), "known": ("shaki", "na"),
        "understand": ("piko", None), "understands": ("piko", None), "understood": ("piko", "na"),
        "want": ("zhivi", None), "wants": ("zhivi", None), "wanted": ("zhivi", "na"),
        "can": ("zhipi", None), "could": ("zhipi", "na"),
        "must": ("debi", None), "should": ("debi", None),
        "find": ("tovi", None), "finds": ("tovi", None), "found": ("tovi", "na"),
        "meet": ("timo", None), "meets": ("timo", None), "met": ("timo", "na"),
        "answer": ("fiko", None), "answers": ("fiko", None), "answered": ("fiko", "na"),
        "love": ("zimo", None), "loves": ("zimo", None), "loved": ("zimo", "na"),
        "go": ("lika", None), "goes": ("lika", None), "went": ("lika", "na"), "gone": ("lika", "na"),
        "walk": ("kivi", None), "walks": ("kivi", None), "walking": ("kivi", None), "walked": ("kivi", "na"),
        "search": ("mita", None), "searches": ("mita", None), "searching": ("mita", None), "searched": ("mita", "na"),
        "cost": ("paki", None), "costs": ("paki", None), "costed": ("paki", "na"),
        "name": ("nomi", None), "names": ("nomi", None), "named": ("nomi", "na"),
        "call": ("nomi", None), "calls": ("nomi", None), "called": ("nomi", "na")
    }

    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = DATA_DIR
        self.data_dir = data_dir
        self.analyzer = LuminaAnalyzer(data_dir / "lexique.json")
        self.fr_to_lumina = {}
        self.en_to_lumina = {}
        self._load_reverse_lexicon(data_dir / "lexique.json")

    def _load_reverse_lexicon(self, lexique_path):
        if not Path(lexique_path).exists():
            return
        with open(lexique_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1. Particules prioritaires
        for p in data.get("particles", []):
            word = p["word"]
            for term in re.split(r'[,/]', p["fr"]):
                clean = term.strip().lower()
                if clean and not clean.startswith("["):
                    self.fr_to_lumina[clean] = word
            for term in re.split(r'[,/]', p["en"]):
                clean = term.strip().lower()
                if clean and not clean.startswith("["):
                    self.en_to_lumina[clean] = word

        # 2. Pronoms
        for pr in data.get("pronouns", []):
            word = pr["word"]
            for term in re.split(r'[,/]', pr["fr"]):
                clean = re.sub(r'\(.*?\)', '', term).strip().lower()
                if clean:
                    self.fr_to_lumina[clean] = word
            for term in re.split(r'[,/]', pr["en"]):
                clean = re.sub(r'\(.*?\)', '', term).strip().lower()
                if clean:
                    self.en_to_lumina[clean] = word

        # 3. Nombres
        for nb in data.get("numbers", []):
            word = nb["word"]
            self.fr_to_lumina[nb["fr"].lower()] = word
            self.fr_to_lumina[str(nb["value"])] = word
            self.en_to_lumina[nb["en"].lower()] = word
            self.en_to_lumina[str(nb["value"])] = word

        # 4. Racines avec priorité : les noms ('noun') et verbes ('verb') ne sont pas écrasés par les adjectifs
        for item in data.get("roots", []):
            word = item["word"]
            pos = item.get("pos", "")
            for term in re.split(r'[,/]', item["fr"]):
                clean = re.sub(r'\(.*?\)', '', term).strip().lower()
                if clean:
                    # Ne pas écraser un nom existant par un adjectif homographe (ex: animal)
                    if clean not in self.fr_to_lumina or pos == "noun":
                        self.fr_to_lumina[clean] = word
                    no_acc = strip_accents(clean)
                    if no_acc not in self.fr_to_lumina or pos == "noun":
                        self.fr_to_lumina[no_acc] = word
            for term in re.split(r'[,/]', item["en"]):
                clean = re.sub(r'\(.*?\)', '', term).strip().lower()
                if clean.startswith("to "):
                    clean = clean[3:].strip()
                if clean:
                    if clean not in self.en_to_lumina or pos == "noun":
                        self.en_to_lumina[clean] = word

        # 5. Adverbes dérivés
        for adv in data.get("adverbs", []):
            word = adv["word"]
            for term in re.split(r'[,/]', adv["fr"]):
                clean = re.sub(r'\(.*?\)', '', term).strip().lower()
                if clean and clean not in self.fr_to_lumina:
                    self.fr_to_lumina[clean] = word
                    no_acc = strip_accents(clean)
                    if no_acc not in self.fr_to_lumina:
                        self.fr_to_lumina[no_acc] = word

        # 6. Démonstratifs invariables
        for dem in ["ce", "cette", "cet", "ces", "ceci"]:
            self.fr_to_lumina[dem] = "to"
        for dem in ["cela", "ça"]:
            self.fr_to_lumina[dem] = "ta"
        for dem in ["this", "these"]:
            self.en_to_lumina[dem] = "to"
        for dem in ["that", "those"]:
            self.en_to_lumina[dem] = "ta"

    def translate_lumina_to_fr(self, text: str) -> dict:
        """Traduit une phrase Lumina en français avec gloses mot-à-mot."""
        words_data = self.analyzer.analyze_sentence(text)
        
        glosses = []
        fr_tokens = []
        is_question = False

        for i, token in enumerate(words_data):
            if token["type"] == "punctuation":
                fr_tokens.append(token["raw"])
                continue

            clean = token["clean"]
            raw_w = token["raw"]

            # Si c'est un nom propre étranger (préservé avec majuscule)
            if raw_w[0].isupper() and token["type"] == "unknown":
                fr_tokens.append(raw_w)
                glosses.append(f"{raw_w}: [Nom propre]")
                continue

            # Formules et particules spécifiques
            if clean == "ma":
                is_question = True
                glosses.append(f"{clean}: [est-ce que]")
                continue
            elif clean == "la":
                has_plural = False
                for j in range(i + 1, min(i + 4, len(words_data))):
                    if words_data[j].get("clean") == "ro":
                        has_plural = True
                        break
                fr_art = "les" if has_plural else "le/la"
                fr_tokens.append(fr_art)
                glosses.append(f"{clean}: {fr_art}")
                continue
            elif clean == "ro":
                glosses.append(f"{clean}: [pluriel]")
                continue
            elif clean == "na":
                fr_tokens.append("[passé]")
                glosses.append(f"{clean}: [passé]")
                continue
            elif clean == "li":
                fr_tokens.append("[présent]")
                glosses.append(f"{clean}: [présent]")
                continue
            elif clean == "vo":
                fr_tokens.append("[futur]")
                glosses.append(f"{clean}: [futur]")
                continue
            elif clean == "ne":
                fr_tokens.append("ne pas")
                glosses.append(f"{clean}: ne pas")
                continue

            meaning = token["meaning_fr"] or f"[{clean}]"
            first_meaning = meaning.split(",")[0].strip()
            # Nettoyer parenthèses de description
            first_meaning = re.sub(r'\(.*?\)', '', first_meaning).strip()

            # Traduction contextuelle de verbes courants
            if clean == "nomi":
                first_meaning = "s'appeler"
            elif clean == "fali":
                first_meaning = "bonjour"

            fr_tokens.append(first_meaning)
            glosses.append(f"{clean}: {first_meaning}")

        raw_fr = " ".join(fr_tokens)
        raw_fr = re.sub(r'\s+([,?.!])', r'\1', raw_fr)
        
        # Reconnaissance d'expressions courantes en sortie
        raw_fr = re.sub(r'\bMina\s+s\'appeler\s+(\w+)', r"Je m'appelle \1", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bTina\s+s\'appeler\s+(\w+)', r"Tu t'appelles \1", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bLina\s+s\'appeler\s+(\w+)', r"Il s'appelle \1", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bJe\s+s\'appeler\s+(\w+)', r"Je m'appelle \1", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bTu\s+s\'appeler\s+(\w+)', r"Tu t'appelles \1", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bTu\s+être\s+heureux\b', r"tu vas bien", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bJe\s+être\s+heureux\b', r"je vais bien", raw_fr, flags=re.IGNORECASE)

        # Gestion des temps composés passés
        raw_fr = re.sub(r'Je\s+\[passé\]\s+voir', r"J'ai vu", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'Je\s+\[passé\]\s+manger', r"J'ai mangé", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'Je\s+\[passé\]\s+faire', r"J'ai fait", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\[passé\]\s+(\w+)', r'a \1', raw_fr)
        raw_fr = re.sub(r'\[futur\]\s+(\w+)', r'va \1', raw_fr)
        raw_fr = re.sub(r'\[présent\]\s*', '', raw_fr)

        # Ajustement des articles élidés en français : le/la animal -> l'animal
        raw_fr = re.sub(r'\ble/la\s+([aeiouh][\w-]+)', r"l'\1", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bde\s+le/la\b', 'du', raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bde\s+les\b', 'des', raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bà\s+le/la\b', 'au', raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bà\s+les\b', 'aux', raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\ble/la\b', 'le', raw_fr)

        if is_question and not raw_fr.strip().endswith("?"):
            if not raw_fr.lower().startswith("est-ce que"):
                raw_fr = "Est-ce que " + raw_fr[0].lower() + raw_fr[1:]
            raw_fr += " ?"

        if raw_fr:
            raw_fr = raw_fr[0].upper() + raw_fr[1:]

        return {
            "source": text,
            "target": raw_fr,
            "glosses": glosses,
            "tokens": words_data
        }

    def _translate_single_clause_fr_to_lumina(self, clause_text: str) -> list:
        """Traduit une proposition ou clause simple du français vers Lumina."""
        t = clause_text.strip()
        if not t:
            return []

        # 1. Expressions idiomatiques multi-mots directes
        for pat, repl in MULTI_WORD_EXPRESSIONS_FR:
            t = re.sub(pat, repl, t, flags=re.IGNORECASE)

        # 2. Salutations et politesses isolées
        t_lower = t.lower().strip("?!.,; ")
        if t_lower in ["bonjour", "salut", "coucou", "salutations"]:
            return ["Fali"]
        if t_lower in ["au revoir", "adieu", "à bientôt"]:
            return ["Fata"]
        if t_lower in ["merci", "merci beaucoup"]:
            return ["Fama"]
        if t_lower in ["s'il vous plaît", "s'il te plaît", "s'il-vous-plaît", "s'il-te-plaît", "fape"]:
            return ["Fape"]
        if t_lower in ["pardon", "excusez-moi", "excuse-moi", "désolé"]:
            return ["Fase"]
        if t_lower in ["oui", "ouais", "d'accord"]:
            return ["Ya"]
        if t_lower in ["non"]:
            return ["No"]
        if t_lower in ["comment ça va", "comment vas-tu", "comment allez-vous", "ça va"]:
            return ["Ma", "Tina", "shili", "zelu"]
        if t_lower in ["je vais bien", "ça va bien", "tout va bien"]:
            return ["Mina", "shili", "zelu"]

        # Détection de question
        is_question = t.startswith("Est-ce que") or t.startswith("est-ce que") or t.endswith("?")
        t_clean = re.sub(r'^(est-ce que|est-ce-que)\s+', '', t, flags=re.IGNORECASE)
        
        # Reconnaissance de "je m'appelle <Nom>", "tu t'appelles <Nom>"
        m_name = re.match(r"^(?:je\s+(?:m'appelle|m’appelle|me\s+nomme))\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", t_clean, re.IGNORECASE)
        if m_name:
            nom_propre = m_name.group(1).capitalize()
            return ["Mina", "nomi", nom_propre]

        m_name_tu = re.match(r"^(?:tu\s+(?:t'appelles|t’appelles|te\s+nommes))\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", t_clean, re.IGNORECASE)
        if m_name_tu:
            nom_propre = m_name_tu.group(1).capitalize()
            return ["Tina", "nomi", nom_propre]

        # Séparation des élisions françaises
        t_clean = re.sub(r"\bl['’]", "le ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bd['’]", "de ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bj['’]", "je ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bm['’]", "me ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bt['’]", "te ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bs['’]", "se ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bc['’]", "ce ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bn['’]", "ne ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bqu['’]", "que ", t_clean, flags=re.IGNORECASE)

        # Nettoyage ponctuation pour tokenisation
        raw_words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9'-]+", t_clean)
        
        lumina_tokens = []
        if is_question:
            lumina_tokens.append("Ma")

        tense_marker = None
        has_negation = False

        def resolve_fr_noun(tok: str):
            tok_low = tok.lower()
            if tok_low in self.fr_to_lumina:
                return self.fr_to_lumina[tok_low]
            tok_no_acc = strip_accents(tok_low)
            if tok_no_acc in self.fr_to_lumina:
                return self.fr_to_lumina[tok_no_acc]
            if tok_low.endswith("s") and len(tok_low) > 2:
                cand = tok_low.rstrip("s")
                if cand in self.fr_to_lumina:
                    return self.fr_to_lumina[cand]
                if strip_accents(cand) in self.fr_to_lumina:
                    return self.fr_to_lumina[strip_accents(cand)]
            lum_cand, _ = lemmatize_french_word(tok_low, self.fr_to_lumina)
            return lum_cand

        i = 0
        while i < len(raw_words):
            raw_w = raw_words[i]
            w = raw_w.lower()

            # Après 'nomi', le mot suivant est obligatoirement un nom propre préservé
            if i > 0 and raw_words[i-1].lower() == "nomi":
                lumina_tokens.append(raw_w.capitalize())
                i += 1
                continue

            # Désambiguïsation contextuelle : 'montre' précédé d'un déterminant/démonstratif est un nom
            if w == "montre" and i > 0 and raw_words[i-1].lower() in ["ce", "cette", "cet", "ces", "la", "une", "sa", "ma", "ta", "to"]:
                lum_montre = self.fr_to_lumina.get("montre-bracelet", self.fr_to_lumina.get("montre", "gake"))
                lumina_tokens.append(lum_montre)
                i += 1
                continue

            # Déjà un mot Lumina (issu des remplacements d'expressions comme Fali, nomi, shili, etc.)
            if w in self.analyzer.lexicon or w in self.analyzer.particles or w in self.analyzer.pronouns or w in self.analyzer.numbers or (w.endswith("fi") and w[:-2] in self.analyzer.lexicon):
                lumina_tokens.append(raw_w if raw_w[0].isupper() else w)
                i += 1
                continue

            # Détection de négation
            if w in ["ne"]:
                has_negation = True
                i += 1
                continue
            if w == "pas":
                i += 1
                continue

            # Détection de temps composé / auxiliaires
            if w in ["ai", "as", "a", "avons", "avez", "ont", "était", "étaient", "avais", "avait"]:
                tense_marker = "na"
                i += 1
                continue
            if w in ["vais", "vas", "va", "allons", "allez", "vont", "serai", "sera"]:
                tense_marker = "vo"
                i += 1
                continue

            # Articles définis
            if w in ["le", "la"]:
                lumina_tokens.append("la")
                i += 1
                continue
            if w in ["les", "des"]:
                lumina_tokens.append("la")
                if i + 1 < len(raw_words):
                    next_raw = raw_words[i+1]
                    next_lum = resolve_fr_noun(next_raw)
                    if next_lum:
                        lumina_tokens.append(next_lum)
                        lumina_tokens.append("ro")
                        i += 2
                        continue
                i += 1
                continue
            if w in ["un", "une"]:
                # Indéfini en Lumina = pas d'article
                i += 1
                continue

            # Pronoms possessifs complets
            possessive_map = {
                "mon": ("Mina", False), "ma": ("Mina", False), "mes": ("Mina", True),
                "ton": ("Tina", False), "ta": ("Tina", False), "tes": ("Tina", True),
                "son": ("Lina", False), "sa": ("Lina", False), "ses": ("Lina", True),
                "notre": ("Miro", False), "nos": ("Miro", True),
                "votre": ("Tiro", False), "vos": ("Tiro", True),
                "leur": ("Liro", False), "leurs": ("Liro", True)
            }
            if w in possessive_map:
                pron, is_plur = possessive_map[w]
                if i + 1 < len(raw_words):
                    nom = resolve_fr_noun(raw_words[i+1])
                    if nom:
                        lumina_tokens.append("la")
                        lumina_tokens.append(nom)
                        if is_plur:
                            lumina_tokens.append("ro")
                        lumina_tokens.extend(["pa", pron])
                        i += 2
                        continue

            # Formes verbales courantes
            if w in self.COMMON_VERBS:
                lum_verb, auto_tense = self.COMMON_VERBS[w]
                if auto_tense and not tense_marker:
                    tense_marker = auto_tense
                if has_negation:
                    lumina_tokens.append("ne")
                    has_negation = False
                if tense_marker:
                    lumina_tokens.append(tense_marker)
                    tense_marker = None
                lumina_tokens.append(lum_verb)
                i += 1
                continue

            # Recherche directe ou lemmatisée dans le lexique inversé
            base_cand = w.rstrip("s")
            lum = self.fr_to_lumina.get(w, self.fr_to_lumina.get(strip_accents(w), self.fr_to_lumina.get(base_cand)))
            lem_tense = None
            if not lum:
                lum, lem_tense = lemmatize_french_word(w, self.fr_to_lumina)

            if lum:
                if lem_tense and not tense_marker:
                    tense_marker = lem_tense
                is_verb = (len(lum) == 4 and lum.endswith("i")) or lum in ["shili", "sifi", "kidi", "kisi", "fidi", "fisi", "pishi", "lifi", "nomi", "mido", "gari"]
                if is_verb:
                    if has_negation:
                        lumina_tokens.append("ne")
                        has_negation = False
                    if tense_marker:
                        lumina_tokens.append(tense_marker)
                        tense_marker = None
                lumina_tokens.append(lum)
            elif raw_w[0].isupper() and i > 0:
                # Nom propre préservé tel quel sans crochets
                lumina_tokens.append(raw_w)
            else:
                lumina_tokens.append(f"[{w}]")

            i += 1

        return lumina_tokens

        return lumina_tokens

    def translate_fr_to_lumina(self, text: str) -> dict:
        """Traduit une phrase ou un ensemble de propositions françaises en Lumina."""
        t = text.strip()
        if not t:
            return {"source": text, "target": "", "tokens": []}

        # Découpage par propositions selon la ponctuation majeure (virgules, points-virgules, points d'interrogation)
        clause_parts = re.split(r'([,;?!])', t)
        
        result_clauses = []
        all_tokens = []
        
        clause_buffer = ""
        for part in clause_parts:
            if part in [",", ";", "?", "!"]:
                if clause_buffer.strip():
                    tokens = self._translate_single_clause_fr_to_lumina(clause_buffer)
                    if tokens:
                        all_tokens.extend(tokens)
                        clause_str = " ".join(tokens)
                        result_clauses.append((clause_str, part))
                    clause_buffer = ""
            else:
                clause_buffer += part

        if clause_buffer.strip():
            tokens = self._translate_single_clause_fr_to_lumina(clause_buffer)
            if tokens:
                all_tokens.extend(tokens)
                clause_str = " ".join(tokens)
                punct = "?" if t.endswith("?") else "."
                result_clauses.append((clause_str, punct))

        if not result_clauses:
            tokens = self._translate_single_clause_fr_to_lumina(t)
            all_tokens = tokens
            punct = "?" if t.endswith("?") else "."
            result_clauses = [(" ".join(tokens), punct)]

        # Assemblage final
        final_pieces = []
        for i, (clause_str, punct) in enumerate(result_clauses):
            if clause_str:
                if i == 0:
                    clause_str = clause_str[0].upper() + clause_str[1:]
                else:
                    # Traiter majuscule après ponctuation forte
                    clause_str = clause_str[0].upper() + clause_str[1:]
                final_pieces.append(f"{clause_str}{punct}")

        final_str = " ".join(final_pieces)
        final_str = re.sub(r'\s+([,;])\s*', r'\1 ', final_str)

        return {
            "source": text,
            "target": final_str,
            "tokens": all_tokens
        }

    def _translate_single_clause_en_to_lumina(self, clause_text: str) -> list:
        """Translates a simple English clause to Lumina."""
        t = clause_text.strip()
        if not t:
            return []

        # 1. Multi-word idiomatic expressions
        for pat, repl in MULTI_WORD_EXPRESSIONS_EN:
            t = re.sub(pat, repl, t, flags=re.IGNORECASE)

        t_lower = t.lower().strip("?!.,; ")
        if t_lower in ["hello", "hi", "hey", "greetings"]:
            return ["Fali"]
        if t_lower in ["goodbye", "bye", "farewell", "see you"]:
            return ["Fata"]
        if t_lower in ["thank you", "thanks", "many thanks"]:
            return ["Fama"]
        if t_lower in ["please", "fape"]:
            return ["Fape"]
        if t_lower in ["sorry", "excuse me", "pardon"]:
            return ["Fase"]
        if t_lower in ["yes", "yeah", "yep", "sure"]:
            return ["Ya"]
        if t_lower in ["no", "nope"]:
            return ["No"]
        if t_lower in ["how are you", "how are you doing", "how do you do"]:
            return ["Ma", "Tina", "shili", "zelu"]
        if t_lower in ["i am fine", "i am well", "i'm fine", "i'm well", "i am good", "i'm good"]:
            return ["Mina", "shili", "zelu"]

        # Question detection
        is_question = t.endswith("?") or bool(re.match(r'^(do|does|did|is|are|was|were|can|will|shall|have|has)\s+', t, re.IGNORECASE))
        t_clean = re.sub(r'^(do|does|did)\s+', '', t, flags=re.IGNORECASE)

        # "My name is <Name>" / "I am called <Name>"
        m_name = re.match(r"^(?:my\s+name\s+is|i\s+am\s+called)\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", t_clean, re.IGNORECASE)
        if m_name:
            proper = m_name.group(1).capitalize()
            return ["Mina", "nomi", proper]

        m_name_you = re.match(r"^(?:your\s+name\s+is|you\s+are\s+called)\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", t_clean, re.IGNORECASE)
        if m_name_you:
            proper = m_name_you.group(1).capitalize()
            return ["Tina", "nomi", proper]

        # English contractions
        t_clean = re.sub(r"\bi'm\b", "i am", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\byou're\b", "you are", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bhe's\b", "he is", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bshe's\b", "she is", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bit's\b", "it is", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bwe're\b", "we are", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bthey're\b", "they are", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bdon't\b", "do not", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bdoesn't\b", "does not", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bdidn't\b", "did not", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bcan't\b|\bcannot\b", "can not", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bwon't\b", "will not", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bi'll\b", "i will", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bi've\b", "i have", t_clean, flags=re.IGNORECASE)

        raw_words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9'-]+", t_clean)

        lumina_tokens = []
        if is_question:
            lumina_tokens.append("Ma")

        tense_marker = None
        has_negation = False

        def resolve_en_noun(tok: str):
            tok_low = tok.lower()
            if tok_low in self.en_to_lumina:
                return self.en_to_lumina[tok_low]
            if tok_low.endswith("s") and len(tok_low) > 2:
                cand = tok_low.rstrip("s")
                if cand in self.en_to_lumina:
                    return self.en_to_lumina[cand]
            lum_cand, _ = lemmatize_english_word(tok_low, self.en_to_lumina)
            return lum_cand

        i = 0
        while i < len(raw_words):
            raw_w = raw_words[i]
            w = raw_w.lower()

            # After 'nomi', the next token is strictly a preserved proper name
            if i > 0 and raw_words[i-1].lower() == "nomi":
                lumina_tokens.append(raw_w.capitalize())
                i += 1
                continue

            # Recognized Lumina tokens
            if w in self.analyzer.lexicon or w in self.analyzer.particles or w in self.analyzer.pronouns or w in self.analyzer.numbers or (w.endswith("fi") and w[:-2] in self.analyzer.lexicon):
                lumina_tokens.append(raw_w if raw_w[0].isupper() else w)
                i += 1
                continue

            if w in ["not", "never"]:
                has_negation = True
                i += 1
                continue

            if w in ["will", "shall"]:
                tense_marker = "vo"
                i += 1
                continue

            # Articles
            if w == "the":
                lumina_tokens.append("la")
                if i + 1 < len(raw_words):
                    next_raw = raw_words[i+1]
                    next_w = next_raw.lower()
                    next_lum = resolve_en_noun(next_raw)
                    if next_w.endswith('s') and next_lum:
                        lumina_tokens.append(next_lum)
                        lumina_tokens.append("ro")
                        i += 2
                        continue
                i += 1
                continue

            if w in ["a", "an"]:
                i += 1
                continue

            # Possessives
            possessive_map_en = {
                "my": "Mina", "your": "Tina", "his": "Lina", "her": "Lina", "its": "Lina",
                "our": "Miro", "their": "Liro"
            }
            if w in possessive_map_en:
                pron = possessive_map_en[w]
                if i + 1 < len(raw_words):
                    next_raw = raw_words[i+1]
                    nom = resolve_en_noun(next_raw)
                    if nom:
                        lumina_tokens.append("la")
                        lumina_tokens.append(nom)
                        if next_raw.lower().endswith('s') and not next_raw.lower().endswith('ss'):
                            lumina_tokens.append("ro")
                        lumina_tokens.extend(["pa", pron])
                        i += 2
                        continue

            # English common verbs
            if w in self.COMMON_VERBS_EN:
                lum_verb, auto_tense = self.COMMON_VERBS_EN[w]
                if auto_tense and not tense_marker:
                    tense_marker = auto_tense
                if has_negation:
                    lumina_tokens.append("ne")
                    has_negation = False
                if tense_marker:
                    lumina_tokens.append(tense_marker)
                    tense_marker = None
                lumina_tokens.append(lum_verb)
                i += 1
                continue

            # Dictionary lookup and lemmatization
            base_cand = w.rstrip('s')
            lum = self.en_to_lumina.get(w, self.en_to_lumina.get(base_cand))
            lem_tense = None
            if not lum:
                lum, lem_tense = lemmatize_english_word(w, self.en_to_lumina)

            if lum:
                if lem_tense and not tense_marker:
                    tense_marker = lem_tense
                is_verb = (len(lum) == 4 and lum.endswith("i")) or lum in ["shili", "sifi", "kidi", "kisi", "fidi", "fisi", "pishi", "lifi", "nomi", "mido", "gari"]
                if is_verb:
                    if has_negation:
                        lumina_tokens.append("ne")
                        has_negation = False
                    if tense_marker:
                        lumina_tokens.append(tense_marker)
                        tense_marker = None
                lumina_tokens.append(lum)
            elif raw_w[0].isupper() and i > 0:
                lumina_tokens.append(raw_w)
            else:
                lumina_tokens.append(f"[{w}]")

            i += 1

        return lumina_tokens

        return lumina_tokens

    def translate_en_to_lumina(self, text: str) -> dict:
        """Translates an English sentence or compound clauses to Lumina."""
        t = text.strip()
        if not t:
            return {"source": text, "target": "", "tokens": []}

        clause_parts = re.split(r'([,;?!])', t)
        result_clauses = []
        all_tokens = []
        clause_buffer = ""

        for part in clause_parts:
            if part in [",", ";", "?", "!"]:
                if clause_buffer.strip():
                    tokens = self._translate_single_clause_en_to_lumina(clause_buffer)
                    if tokens:
                        all_tokens.extend(tokens)
                        clause_str = " ".join(tokens)
                        result_clauses.append((clause_str, part))
                    clause_buffer = ""
            else:
                clause_buffer += part

        if clause_buffer.strip():
            tokens = self._translate_single_clause_en_to_lumina(clause_buffer)
            if tokens:
                all_tokens.extend(tokens)
                clause_str = " ".join(tokens)
                punct = "?" if t.endswith("?") else "."
                result_clauses.append((clause_str, punct))

        if not result_clauses:
            tokens = self._translate_single_clause_en_to_lumina(t)
            all_tokens = tokens
            punct = "?" if t.endswith("?") else "."
            result_clauses = [(" ".join(tokens), punct)]

        final_pieces = []
        for i, (clause_str, punct) in enumerate(result_clauses):
            if clause_str:
                clause_str = clause_str[0].upper() + clause_str[1:]
                final_pieces.append(f"{clause_str}{punct}")

        final_str = " ".join(final_pieces)
        final_str = re.sub(r'\s+([,;])\s*', r'\1 ', final_str)

        return {
            "source": text,
            "target": final_str,
            "tokens": all_tokens
        }

    def translate_lumina_to_en(self, text: str) -> dict:
        """Translates a Lumina sentence to English with glosses."""
        words_data = self.analyzer.analyze_sentence(text)
        glosses = []
        en_tokens = []
        is_question = False

        for i, token in enumerate(words_data):
            if token["type"] == "punctuation":
                en_tokens.append(token["raw"])
                continue

            clean = token["clean"]
            raw_w = token["raw"]

            if raw_w[0].isupper() and token["type"] == "unknown":
                en_tokens.append(raw_w)
                glosses.append(f"{raw_w}: [Proper Name]")
                continue

            if clean == "ma":
                is_question = True
                glosses.append(f"{clean}: [question]")
                continue
            elif clean == "la":
                en_tokens.append("the")
                glosses.append(f"{clean}: the")
                continue
            elif clean == "ro":
                glosses.append(f"{clean}: [plural]")
                continue
            elif clean == "na":
                en_tokens.append("[past]")
                glosses.append(f"{clean}: [past]")
                continue
            elif clean == "li":
                en_tokens.append("[present]")
                glosses.append(f"{clean}: [present]")
                continue
            elif clean == "vo":
                en_tokens.append("will")
                glosses.append(f"{clean}: will")
                continue
            elif clean == "ne":
                en_tokens.append("not")
                glosses.append(f"{clean}: not")
                continue

            meaning = token["meaning_en"] or f"[{clean}]"
            first_meaning = meaning.split(",")[0].strip()
            first_meaning = re.sub(r'\(.*?\)', '', first_meaning).strip()

            if clean == "nomi":
                first_meaning = "be called"
            elif clean == "fali":
                first_meaning = "hello"

            en_tokens.append(first_meaning)
            glosses.append(f"{clean}: {first_meaning}")

        raw_en = " ".join(en_tokens)
        raw_en = re.sub(r'\s+([,?.!])', r'\1', raw_en)

        # Contextual idiomatic fixes
        raw_en = re.sub(r'\bMina\s+(?:to\s+)?be\s+called\s+(\w+)', r"my name is \1", raw_en, flags=re.IGNORECASE)
        raw_en = re.sub(r'\bTina\s+(?:to\s+)?be\s+called\s+(\w+)', r"your name is \1", raw_en, flags=re.IGNORECASE)
        raw_en = re.sub(r'\bI\s+(?:to\s+)?be\s+called\s+(\w+)', r"my name is \1", raw_en, flags=re.IGNORECASE)
        raw_en = re.sub(r'\byou\s+(?:to\s+)?be\s+happy\b', r"are you well", raw_en, flags=re.IGNORECASE)
        raw_en = re.sub(r'\bI\s+(?:to\s+)?be\s+happy\b', r"I am well", raw_en, flags=re.IGNORECASE)
        raw_en = re.sub(r'\[present\]\s*', '', raw_en)
        raw_en = re.sub(r'\[past\]\s+(\w+)', r'did \1', raw_en)

        if is_question and not raw_en.strip().endswith("?"):
            raw_en = raw_en.rstrip(".") + "?"

        if raw_en:
            raw_en = raw_en[0].upper() + raw_en[1:]

        return {
            "source": text,
            "target": raw_en,
            "glosses": glosses,
            "tokens": words_data
        }
