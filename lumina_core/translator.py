"""Moteur de traduction bidirectionnel entre le Lumina et le Français / Anglais."""

import re
import json
from pathlib import Path
from .analyzer import LuminaAnalyzer

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class LuminaTranslator:
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = DATA_DIR
        self.analyzer = LuminaAnalyzer(data_dir / "lexique.json")
        self.fr_to_lumina = {}
        self.en_to_lumina = {}
        self._load_reverse_lexicon(data_dir / "lexique.json")

    def _load_reverse_lexicon(self, lexique_path):
        if not Path(lexique_path).exists():
            return
        with open(lexique_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Particules
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

        # Pronoms
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

        # Nombres
        for nb in data.get("numbers", []):
            word = nb["word"]
            self.fr_to_lumina[nb["fr"].lower()] = word
            self.fr_to_lumina[str(nb["value"])] = word
            self.en_to_lumina[nb["en"].lower()] = word
            self.en_to_lumina[str(nb["value"])] = word

        # Racines
        for item in data.get("roots", []):
            word = item["word"]
            for term in re.split(r'[,/]', item["fr"]):
                clean = re.sub(r'\(.*?\)', '', term).strip().lower()
                if clean:
                    self.fr_to_lumina[clean] = word
            for term in re.split(r'[,/]', item["en"]):
                clean = re.sub(r'\(.*?\)', '', term).strip().lower()
                if clean.startswith("to "):
                    clean = clean[3:].strip()
                if clean:
                    self.en_to_lumina[clean] = word

    def translate_lumina_to_fr(self, text: str) -> dict:
        """Traduit une phrase Lumina en français avec gloses mot-à-mot."""
        words_data = self.analyzer.analyze_sentence(text)
        
        # Reconstruction progressive et gloses
        glosses = []
        fr_tokens = []
        skip_next = False
        is_question = False

        for i, token in enumerate(words_data):
            if token["type"] == "punctuation":
                fr_tokens.append(token["raw"])
                continue

            clean = token["clean"]
            meaning = token["meaning_fr"] or f"[{clean}]"

            # Marqueurs spécifiques
            if clean == "ma":
                is_question = True
                glosses.append(f"{clean}: [est-ce que]")
                continue
            elif clean == "la":
                # Vérifie si le mot suivant a 'ro' plus loin pour pluriel
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
                # Marqueur pluriel déjà absorbé
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

            # Cas général
            first_meaning = meaning.split(",")[0].strip()
            fr_tokens.append(first_meaning)
            glosses.append(f"{clean}: {first_meaning}")

        raw_fr = " ".join(fr_tokens)
        # Nettoyage ponctuation et élisions
        raw_fr = re.sub(r'\s+([,?.!])', r'\1', raw_fr)
        raw_fr = re.sub(r'Je\s+a\s+manger', r"J'ai mangé", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'Tu\s+a\s+manger', r"Tu as mangé", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'Il/elle\s+a\s+manger', r"Il a mangé", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'Je\s+a\s+voir', r"J'ai vu", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'Je\s+a\s+faire', r"J'ai fait", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\[passé\]\s+(\w+)', r'a \1', raw_fr)
        raw_fr = re.sub(r'\[futur\]\s+(\w+)', r'va \1', raw_fr)
        raw_fr = re.sub(r'\[présent\]\s+', '', raw_fr)
        raw_fr = re.sub(r'\ble\s+([aeiouh])', r"l'\1", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bla\s+([aeiouh])', r"l'\1", raw_fr, flags=re.IGNORECASE)
        raw_fr = re.sub(r'\bde\s+([aeiouh])', r"d'\1", raw_fr, flags=re.IGNORECASE)

        if is_question and not raw_fr.startswith("Est-ce que"):
            raw_fr = f"Est-ce que {raw_fr}"
            if not raw_fr.endswith("?"):
                raw_fr += " ?"

        # Majuscule initiale
        if raw_fr:
            raw_fr = raw_fr[0].upper() + raw_fr[1:]

        return {
            "source": text,
            "target": raw_fr,
            "glosses": glosses,
            "tokens": words_data
        }

    def translate_fr_to_lumina(self, text: str) -> dict:
        """Traduit une phrase française simple en Lumina."""
        t = text.strip()
        is_question = t.startswith("Est-ce que") or t.endswith("?")
        t_clean = re.sub(r'^(est-ce que|est-ce-que)\s+', '', t, flags=re.IGNORECASE)
        # Séparation des élisions françaises : l'animal -> le animal, j'ai -> je ai, d'un -> de un, n'a -> ne a
        t_clean = re.sub(r"\bl'", "le ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bd'", "de ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bj'", "je ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bn'", "ne ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bc'", "ce ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r"\bs'", "se ", t_clean, flags=re.IGNORECASE)
        t_clean = re.sub(r'[?!.,;]', '', t_clean).lower()
        words = t_clean.split()

        lumina_tokens = []
        if is_question:
            lumina_tokens.append("Ma")

        tense_marker = None
        has_negation = False

        i = 0
        while i < len(words):
            w = words[i]

            # Détection de temps composé / passé
            if w in ["ai", "as", "a", "avons", "avez", "ont", "était", "étaient", "avais", "avait"]:
                tense_marker = "na"
                i += 1
                continue
            if w in ["vais", "vas", "va", "allons", "allez", "vont", "serai", "sera"]:
                tense_marker = "vo"
                i += 1
                continue
            if w in ["ne", "n'"]:
                has_negation = True
                i += 1
                continue
            if w == "pas":
                i += 1
                continue

            # Articles
            if w in ["le", "la", "l'"]:
                lumina_tokens.append("la")
                i += 1
                continue
            if w == "les":
                lumina_tokens.append("la")
                # On cherchera à mettre 'ro' après le nom
                if i + 1 < len(words):
                    next_w = words[i+1].rstrip('s')
                    next_lum = self.fr_to_lumina.get(words[i+1], self.fr_to_lumina.get(next_w))
                    if next_lum:
                        lumina_tokens.append(next_lum)
                        lumina_tokens.append("ro")
                        i += 2
                        continue
                i += 1
                continue
            if w == "des":
                if i + 1 < len(words):
                    next_w = words[i+1].rstrip('s')
                    next_lum = self.fr_to_lumina.get(words[i+1], self.fr_to_lumina.get(next_w))
                    if next_lum:
                        lumina_tokens.append(next_lum)
                        lumina_tokens.append("ro")
                        i += 2
                        continue
                i += 1
                continue
            if w in ["un", "une"]:
                # Indéfini = pas d'article
                i += 1
                continue

            # Pronoms possessifs simples
            if w in ["mon", "ma"]:
                if i + 1 < len(words):
                    nom = self.fr_to_lumina.get(words[i+1])
                    if nom:
                        lumina_tokens.extend(["la", nom, "pa", "Mina"])
                        i += 2
                        continue
            if w in ["ton", "ta"]:
                if i + 1 < len(words):
                    nom = self.fr_to_lumina.get(words[i+1])
                    if nom:
                        lumina_tokens.extend(["la", nom, "pa", "Tina"])
                        i += 2
                        continue
            if w in ["son", "sa"]:
                if i + 1 < len(words):
                    nom = self.fr_to_lumina.get(words[i+1])
                    if nom:
                        lumina_tokens.extend(["la", nom, "pa", "Lina"])
                        i += 2
                        continue

            # Insertion du marqueur de temps/négation avant un verbe
            # Recherche directe ou avec forme de base
            base_cand = w.rstrip("s")
            lum = self.fr_to_lumina.get(w, self.fr_to_lumina.get(base_cand))
            
            # Formes verbales courantes
            verb_map = {
                "suis": "shili", "es": "shili", "est": "shili", "sommes": "shili", "êtes": "shili", "sont": "shili", "été": "shili",
                "vois": "sifi", "voit": "sifi", "voyons": "sifi", "voyez": "sifi", "voient": "sifi", "vu": "sifi",
                "mange": "kidi", "manges": "kidi", "mangeons": "kidi", "mangez": "kidi", "mangent": "kidi", "mangé": "kidi",
                "fais": "kisi", "fait": "kisi", "faisons": "kisi", "faites": "kisi", "font": "kisi",
                "dit": "fidi", "dis": "fidi", "disons": "fidi", "dites": "fidi", "disent": "fidi",
                "pense": "pishi", "penses": "pishi", "pensons": "pishi", "pensez": "pishi", "pensent": "pishi", "pensé": "pishi",
                "montre": "fisi", "montres": "fisi", "montrent": "fisi", "montré": "fisi",
                "bouge": "lifi", "bouges": "lifi", "bougent": "lifi",
                "dort": "somo", "dorment": "somo"
            }
            if not lum and w in verb_map:
                lum = verb_map[w]

            if lum:
                # Si c'est un verbe et qu'on a un marqueur négation/temps en attente
                is_verb = (lum.endswith("i") and len(lum) == 4) or lum in ["shili", "sifi", "kidi", "kisi", "fidi", "fisi", "pishi", "lifi", "nomi"]
                if is_verb:
                    if has_negation:
                        lumina_tokens.append("ne")
                        has_negation = False
                    if tense_marker:
                        lumina_tokens.append(tense_marker)
                        tense_marker = None
                lumina_tokens.append(lum)
            else:
                lumina_tokens.append(f"[{w}]")

            i += 1

        result_str = " ".join(lumina_tokens)
        if result_str:
            result_str = result_str[0].upper() + result_str[1:]
        if is_question:
            result_str += "?"
        else:
            result_str += "."

        return {
            "source": text,
            "target": result_str,
            "tokens": lumina_tokens
        }
