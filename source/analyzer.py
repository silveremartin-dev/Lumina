"""Analyseur morphologique, sémantique et phonologique pour Lumina."""

import re
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class LuminaAnalyzer:
    DOMAINS = {
        "T": "Temps / Chronologie",
        "D": "Temps / Durée & Devenir",
        "K": "Espace / Matière & Forme",
        "G": "Espace / Système & Organisation",
        "P": "Quantité / Mesure & Logique",
        "B": "Quantité / Totalité & Calcul",
        "S": "Sensation / Émotion & Perception",
        "Z": "Sensation / Ambiance & Harmonie",
        "M": "Humain / Individu & Société",
        "N": "Humain / Altruisme & Relation",
        "F": "Communication / Parole & Information",
        "V": "Communication / Son & Diffusion",
        "L": "Mouvement / Trajectoire & Déplacement",
        "R": "Mouvement / Vitesse & Direction",
        "SH": "Abstraction / Idée & Existence",
        "ZH": "Abstraction / Certitude & Monde",
        "J": "Outil / Industrie & Machine",
        "CH": "Outil / Technique & Utilisation",
        "H": "Négation / Vide & Absence"
    }

    VOWEL_ROLES = {
        "a": ("Nom", "Entité, objet concret, personne ou notion"),
        "i": ("Verbe", "Action, processus ou devenir"),
        "u": ("Adjectif", "Propriété, qualité ou état"),
        "o": ("Lieu / Collectif", "Conteneur, milieu, ensemble"),
        "e": ("Agent / Instrument", "Moyen d'action ou agent dérivé")
    }

    def __init__(self, lexique_path=None):
        if lexique_path is None:
            lexique_path = DATA_DIR / "lexique.json"
        
        self.lexicon = {}
        self.particles = {}
        self.pronouns = {}
        self.numbers = {}
        
        if Path(lexique_path).exists():
            with open(lexique_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("particles", []):
                    self.particles[item["word"].lower()] = item
                for item in data.get("pronouns", []):
                    self.pronouns[item["word"].lower()] = item
                for item in data.get("numbers", []):
                    self.numbers[item["word"].lower()] = item
                for item in data.get("roots", []):
                    self.lexicon[item["word"].lower()] = item

    def to_ipa(self, word: str) -> str:
        """Convertit un mot Lumina en transcription phonétique IPA avec accent tonique."""
        w = word.lower().strip(",.?!:;\"'")
        if not w:
            return ""

        # Découpage syllabique approximatif (CV ou CVC)
        # Remplacement des digraphes
        res = w
        res = re.sub(r'sh', 'ʃ', res)
        res = re.sub(r'zh', 'ʒ', res)
        res = re.sub(r'ch', 't͡ʃ', res)
        res = re.sub(r'ng', 'ŋ', res)
        res = re.sub(r'j', 'd͡ʒ', res)
        res = re.sub(r'y', 'j', res)
        res = re.sub(r'r', 'r', res)
        res = re.sub(r'u', 'u', res)
        
        # Trouver les voyelles pour poser l'accent sur l'avant-dernière syllabe
        vowels = list(re.finditer(r'[aeiou]', res))
        if len(vowels) >= 2:
            # Pénultième voyelle
            target_vowel_idx = vowels[-2].start()
            # Chercher le début de la syllabe (consonne précédente)
            syllable_start = target_vowel_idx
            while syllable_start > 0 and res[syllable_start - 1] not in "aeiou/ ˈ":
                syllable_start -= 1
            res = res[:syllable_start] + "ˈ" + res[syllable_start:]
        elif len(vowels) == 1:
            res = "ˈ" + res

        return f"/{res}/"

    def analyze_word(self, word: str) -> dict:
        """Analyse morphologique et sémantique complète d'un mot Lumina."""
        clean_word = word.lower().strip(",.?!:;\"'()")
        result = {
            "raw": word,
            "clean": clean_word,
            "type": "unknown",
            "meaning_fr": None,
            "meaning_en": None,
            "ipa": self.to_ipa(clean_word),
            "breakdown": {}
        }

        # 1. Vérification particule grammaticale
        if clean_word in self.particles:
            p = self.particles[clean_word]
            result["type"] = f"particle ({p['type']})"
            result["meaning_fr"] = p["fr"]
            result["meaning_en"] = p["en"]
            result["breakdown"]["description"] = p.get("desc")
            return result

        # 2. Vérification pronom
        if clean_word in self.pronouns:
            pr = self.pronouns[clean_word]
            result["type"] = "pronoun"
            result["meaning_fr"] = pr["fr"]
            result["meaning_en"] = pr["en"]
            result["breakdown"]["person"] = pr.get("desc")
            return result

        # 3. Vérification nombre
        if clean_word in self.numbers:
            nb = self.numbers[clean_word]
            result["type"] = "number"
            result["meaning_fr"] = f"{nb['fr']} ({nb['value']})"
            result["meaning_en"] = f"{nb['en']} ({nb['value']})"
            return result

        # 4. Vérification adverbe en -fi
        is_adverb = False
        base_word = clean_word
        if clean_word.endswith("fi") and len(clean_word) > 4:
            is_adverb = True
            base_word = clean_word[:-2]

        # 5. Recherche dans le lexique des racines
        if base_word in self.lexicon:
            item = self.lexicon[base_word]
            result["type"] = "adverb" if is_adverb else item.get("pos", "root")
            if is_adverb:
                result["meaning_fr"] = f"adverbe de '{item['fr']}'"
                result["meaning_en"] = f"adverbially ({item['en']})"
            else:
                result["meaning_fr"] = item["fr"]
                result["meaning_en"] = item["en"]
            result["breakdown"]["domain"] = item.get("domain")
            result["breakdown"]["semantic"] = item.get("semantic")

        # 6. Décomposition structurelle C1V1C2V2
        m = re.match(r'^(sh|zh|ch|ng|[a-z])([aeiou])(sh|zh|ch|ng|[a-z])([aeiou])(fi)?$', clean_word)
        if m:
            c1, v1, c2, v2, suffix = m.groups()
            c1_upper = c1.upper()
            result["breakdown"]["c1"] = c1_upper
            result["breakdown"]["domain"] = self.DOMAINS.get(c1_upper, "Catégorie spécifique")
            
            role_name, role_desc = self.VOWEL_ROLES.get(v1, ("Inconnu", "Inconnu"))
            result["breakdown"]["v1"] = v1
            result["breakdown"]["role"] = role_name
            result["breakdown"]["role_detail"] = role_desc
            result["breakdown"]["c2v2"] = f"{c2}{v2}"
            if suffix:
                result["breakdown"]["suffix"] = "-fi (adverbe de manière)"
                if result["type"] == "unknown":
                    result["type"] = "derived_adverb"
            elif result["type"] == "unknown":
                result["type"] = f"canonical_root ({role_name})"

        return result

    def analyze_sentence(self, sentence: str) -> list:
        """Analyse chaque mot d'une phrase Lumina."""
        tokens = re.findall(r"[\w'-]+|[^\w\s]", sentence)
        analysis = []
        for token in tokens:
            if re.match(r'^\w', token):
                analysis.append(self.analyze_word(token))
            else:
                analysis.append({"raw": token, "type": "punctuation"})
        return analysis
