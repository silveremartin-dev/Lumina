"""Interface en ligne de commande (CLI) pour Lumina."""

import sys
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

# Assurer que lumina_core est importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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
    p_trans = subparsers.add_parser("translate", help="Traduit entre Lumina et Français")
    p_trans.add_argument("text", help="Texte source")
    p_trans.add_argument("--to", choices=["fr", "lumina"], default="fr", help="Langue cible (défaut: fr)")

    # Commande 'speak'
    p_speak = subparsers.add_parser("speak", help="Prononce vocalement une phrase en Lumina")
    p_speak.add_argument("text", help="Texte Lumina à prononcer")

    # Commande 'wav'
    p_wav = subparsers.add_parser("wav", help="Génère un fichier audio .WAV pour une phrase Lumina")
    p_wav.add_argument("text", help="Texte Lumina")
    p_wav.add_argument("-o", "--output", default="output.wav", help="Fichier de sortie (défaut: output.wav)")

    # Commande 'wordgen'
    p_gen = subparsers.add_parser("wordgen", help="Forge un mot Lumina selon la matrice C1V1C2V2")
    p_gen.add_argument("--c1", required=True, help="Consonne de domaine (ex: K, M, T, F, S, L, J)")
    p_gen.add_argument("--v1", required=True, choices=["A", "I", "U", "O", "E", "a", "i", "u", "o", "e"], help="Voyelle de rôle grammatical")
    p_gen.add_argument("--c2v2", required=True, help="Spécification (ex: bo, fa, pa, po)")

    # Commande 'prince'
    p_prince = subparsers.add_parser("prince", help="Affiche le texte du Petit Prince bilingue aligné")
    p_prince.add_argument("--id", type=int, default=None, help="Numéro de phrase spécifique (1-13)")

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
        if args.to == "fr":
            res = translator.translate_lumina_to_fr(args.text)
            print(f"\n[Lumina -> FR]")
            print(f"Source : {res['source']}")
            print(f"Cible  : {res['target']}")
            print(f"Gloses : {' | '.join(res['glosses'])}")
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
