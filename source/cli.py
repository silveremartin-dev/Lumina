"""Interface en ligne de commande (CLI) pour Lumina."""

import sys
import re
import json
import argparse
from pathlib import Path

# Assurer l'encodage UTF-8 sous Windows PowerShell / cmd
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Assurer les imports du projet
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from source.analyzer import LuminaAnalyzer
    from source.translator import LuminaTranslator
    from source.tts import LuminaTTS
except ImportError:
    try:
        from analyzer import LuminaAnalyzer
        from translator import LuminaTranslator
        from tts import LuminaTTS
    except ImportError:
        from lumina_core.analyzer import LuminaAnalyzer
        from lumina_core.translator import LuminaTranslator
        from lumina_core.tts import LuminaTTS

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def main():
    parser = argparse.ArgumentParser(
        description="Lumina CLI - Outils pour la langue logique universelle Lumina",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Commande 'analyze'
    p_analyze = subparsers.add_parser("analyze", help="Analyse morphologique et sémantique d'un mot ou d'une phrase")
    p_analyze.add_argument("text", help="Texte en Lumina à analyser")

    # Commande 'translate'
    p_trans = subparsers.add_parser("translate", help="Traduit entre Lumina, Français et Anglais")
    p_trans.add_argument("text", help="Texte source")
    p_trans.add_argument("--to", choices=["fr", "lumina", "en", "auto"], default="auto", help="Langue cible (défaut: auto-détection)")

    # Commande 'speak'
    p_speak = subparsers.add_parser("speak", help="Prononce vocalement une phrase en Lumina")
    p_speak.add_argument("text", help="Texte Lumina à prononcer")

    # Commande 'wav'
    p_wav = subparsers.add_parser("wav", help="Génère un fichier audio .WAV pour une phrase Lumina")
    p_wav.add_argument("text", help="Texte Lumina")
    p_wav.add_argument("-o", "--output", default="output.wav", help="Fichier de sortie (défaut: output.wav)")

    # Commande 'listen' (Speech-to-Text)
    p_stt = subparsers.add_parser("listen", help="Écoute au microphone (STT) et traduit automatiquement")
    p_stt.add_argument("--seconds", type=int, default=5, help="Durée d'écoute en secondes (défaut: 5)")
    p_stt.add_argument("--to", choices=["lumina", "fr", "en"], default="lumina", help="Langue de traduction cible (défaut: lumina)")

    # Commande 'wordgen'
    p_gen = subparsers.add_parser("wordgen", help="Forge un mot Lumina selon la matrice C1V1C2V2")
    p_gen.add_argument("--c1", required=True, help="Consonne de domaine (ex: K, M, T, F, S, L, J)")
    p_gen.add_argument("--v1", required=True, choices=["A", "I", "U", "O", "E", "a", "i", "u", "o", "e"], help="Voyelle de rôle grammatical")
    p_gen.add_argument("--c2v2", required=True, help="Spécification (ex: bo, fa, pa, po)")

    # Commande 'prince'
    p_prince = subparsers.add_parser("prince", help="Affiche le texte du Petit Prince bilingue aligné")
    p_prince.add_argument("--id", type=int, default=None, help="Numéro de phrase spécifique (1-22)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    analyzer = LuminaAnalyzer()
    translator = LuminaTranslator()
    tts = LuminaTTS()

    if args.command == "analyze":
        print(f"\n--- Analyse Lumina : '{args.text}' ---")
        tokens = analyzer.analyze_sentence(args.text)
        for t in tokens:
            if t["type"] == "punctuation":
                continue
            clean = t["clean"]
            t_type = t["type"]
            ipa = t["ipa"]
            fr = t.get("meaning_fr") or "inconnu"
            print(f"\n* Mot : {clean.upper()}  {ipa}")
            print(f"  Type : {t_type}")
            print(f"  Sens FR : {fr}")
            if "breakdown" in t and t["breakdown"]:
                bd = t["breakdown"]
                if "domain" in bd:
                    print(f"  Domaine (C1={bd.get('c1')}) : {bd['domain']}")
                if "role" in bd:
                    print(f"  Rôle (V1={bd.get('v1')}) : {bd['role']} - {bd.get('role_detail')}")
                if "c2v2" in bd:
                    print(f"  Radical (C2V2) : {bd['c2v2']}")

    elif args.command == "translate":
        target_lang = args.to
        lower_text = args.text.lower()
        en_indicators = ["hello", "hi", "how are you", "my name is", "the", "you", "i am", "we", "they", "is", "are", "what", "which", "where", "please", "thank you", "thanks", "goodbye"]
        fr_indicators = ["bonjour", "salut", "merci", "comment", "ça", "est-ce", "je", "tu", "il", "elle", "nous", "vous", "les", "des", "une", "m'", "t'", "j'", "l'", "d'", "s'"]
        lumina_indicators = ["mina", "tina", "miro", "tiro", "li", "na", "vo", "pe", "du", "ro", "ma", "ta", "shili", "sifi", "zelu", "fali", "fata", "fama", "nomi"]
        
        en_score = sum(1 for ind in en_indicators if re.search(r'\b' + re.escape(ind), lower_text))
        fr_score = sum(1 for ind in fr_indicators if re.search(r'\b' + re.escape(ind), lower_text))
        lumina_score = sum(1 for ind in lumina_indicators if re.search(r'\b' + re.escape(ind), lower_text))

        if target_lang == "auto":
            if en_score > fr_score and en_score > lumina_score:
                target_lang = "lumina_from_en"
            elif fr_score > lumina_score or any(k in lower_text for k in ["bonjour", "salut", "comment", "m'appelle", "je "]):
                target_lang = "lumina"
            else:
                target_lang = "fr"
        elif target_lang == "lumina":
            if en_score > fr_score:
                target_lang = "lumina_from_en"

        if target_lang == "fr":
            res = translator.translate_lumina_to_fr(args.text)
            print(f"\n[Lumina -> FR]")
            print(f"Source : {res['source']}")
            print(f"Cible  : {res['target']}")
            print(f"Gloses : {' | '.join(res['glosses'])}")
        elif target_lang == "en":
            res = translator.translate_lumina_to_en(args.text)
            print(f"\n[Lumina -> EN]")
            print(f"Source : {res['source']}")
            print(f"Cible  : {res['target']}")
            print(f"Gloses : {' | '.join(res['glosses'])}")
        elif target_lang == "lumina_from_en":
            res = translator.translate_en_to_lumina(args.text)
            print(f"\n[EN -> Lumina]")
            print(f"Source : {res['source']}")
            print(f"Cible  : {res['target']}")
            print(f"IPA    : {tts.get_ipa(res['target'])}")
        else:
            res = translator.translate_fr_to_lumina(args.text)
            print(f"\n[FR -> Lumina]")
            print(f"Source : {res['source']}")
            print(f"Cible  : {res['target']}")
            print(f"IPA    : {tts.get_ipa(res['target'])}")

    elif args.command == "speak":
        ipa = tts.get_ipa(args.text)
        print(f"\nPrononciation de : '{args.text}' {ipa}")
        tts.speak_powershell(args.text)

    elif args.command == "wav":
        out = tts.generate_formant_wav(args.text, args.output)
        print(f"\nFichier audio WAV généré avec succès : {out}")
        print(f"Transcription IPA : {tts.get_ipa(args.text)}")

    elif args.command == "listen":
        try:
            from source.stt import LuminaSTT
        except ImportError:
            from lumina_core.stt import LuminaSTT
        stt = LuminaSTT()
        print(f"\n[STT] Écoute au microphone pendant {args.seconds} secondes...")
        print("Parlez distinctement en français...")
        text = stt.listen_and_transcribe(timeout_sec=args.seconds)
        if not text:
            print("Aucune parole détectée ou périphérique microphone non configuré.")
        else:
            print(f"\n[Texte reconnu (STT)] : \"{text}\"")
            if args.to == "lumina":
                # Auto-détecter si le texte reconnu est en anglais ou en français
                is_en = any(k in text.lower().split() for k in ["the", "is", "are", "you", "hello", "what", "my"])
                if is_en:
                    res = translator.translate_en_to_lumina(text)
                else:
                    res = translator.translate_fr_to_lumina(text)
                print(f"[Traduction Lumina]   : {res['target']}")
                print(f"[Phonétique IPA]      : {tts.get_ipa(res['target'])}")
                print(f"\nPrononciation Lumina...")
                tts.speak_powershell(res['target'])
            elif args.to == "en":
                res = translator.translate_lumina_to_en(text)
                print(f"[Traduction Anglais]  : {res['target']}")
            else:
                res = translator.translate_lumina_to_fr(text)
                print(f"[Traduction Français] : {res['target']}")

    elif args.command == "wordgen":
        c1 = args.c1.upper()
        v1 = args.v1.lower()
        c2v2 = args.c2v2.lower()
        word = f"{c1.lower()}{v1}{c2v2}"
        domain = analyzer.DOMAINS.get(c1, "Inconnu")
        role_name, role_desc = analyzer.VOWEL_ROLES.get(v1, ("Inconnu", ""))
        ipa = analyzer.to_ipa(word)
        print(f"\n=== Forge de mot Lumina ===")
        print(f"Mot créé : {word.upper()}  {ipa}")
        print(f"Domaine (C1={c1}) : {domain}")
        print(f"Rôle grammatical (V1={v1}) : {role_name} ({role_desc})")
        print(f"Spécification (C2V2) : {c2v2}")

    elif args.command == "prince":
        prince_file = DATA_DIR / "petit_prince.json"
        if not prince_file.exists():
            print("Fichier petit_prince.json introuvable.")
            return
        with open(prince_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"\n=== {data['title']['lumina']} ===")
        print(f"({data['title']['fr']})\n")
        sentences = data["sentences"]
        if args.id:
            sentences = [s for s in sentences if s["id"] == args.id]
        for s in sentences:
            print(f"[{s['id']}] LUMINA : {s['lumina']}")
            print(f"    IPA    : {tts.get_ipa(s['lumina'])}")
            print(f"    FR     : {s['fr']}")
            print(f"    EN     : {s['en']}\n")

if __name__ == "__main__":
    main()
