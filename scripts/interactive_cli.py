"""Interactive REPL Shell for Lumina."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from source.analyzer import LuminaAnalyzer
from source.translator import LuminaTranslator
from source.tts import LuminaTTS

def print_help():
    print("""
=== Lumina Interactive REPL Shell ===
Commandes disponibles :
  <texte>               : Traduit automatiquement (FR -> Lumina ou Lumina -> FR)
  :s, :speak <texte>    : Prononce le texte Lumina à voix haute
  :a, :analyze <texte>  : Analyse morphologique et phonétique IPA
  :f, :forge <C1> <V1> <C2V2> : Forge un mot selon la matrice sémantique
  :p, :prince [id]      : Affiche une phrase du Petit Prince alignée
  :h, :help             : Affiche cette aide
  :q, :quit, exit       : Quitter la session
""")

def main():
    analyzer = LuminaAnalyzer()
    translator = LuminaTranslator()
    tts = LuminaTTS()

    print("=======================================================")
    print("  🌟 Lumina REPL — Langue Logique Universelle")
    print("  Tapez une phrase à traduire ou ':help' pour les commandes.")
    print("=======================================================\n")

    while True:
        try:
            line = input("lumina> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nÀ bientôt ! / Ta lifi sulofi!")
            break

        if not line:
            continue

        if line.lower() in [":q", ":quit", "exit", "quit"]:
            print("À bientôt ! / Ta lifi sulofi!")
            break

        if line.lower() in [":h", ":help"]:
            print_help()
            continue

        # Commande :speak
        if line.startswith(":speak ") or line.startswith(":s "):
            parts = line.split(maxsplit=1)
            if len(parts) > 1:
                target_text = parts[1]
                print(f"🔊 Prononciation de : '{target_text}' (IPA: {tts.get_ipa(target_text)})")
                tts.speak_powershell(target_text)
            continue

        # Commande :analyze
        if line.startswith(":analyze ") or line.startswith(":a "):
            parts = line.split(maxsplit=1)
            if len(parts) > 1:
                tokens = analyzer.analyze_sentence(parts[1])
                for t in tokens:
                    if t.get("type") == "punctuation":
                        continue
                    clean = t.get("clean", "")
                    fr = t.get("meaning_fr", "")
                    t_type = t.get("type", "")
                    ipa = t.get("ipa", "")
                    print(f"  * {clean.upper()} {ipa} -> [{t_type}] {fr}")
            continue

        # Commande :forge
        if line.startswith(":forge ") or line.startswith(":f "):
            parts = line.split()
            if len(parts) >= 4:
                c1, v1, c2v2 = parts[1].upper(), parts[2].lower(), parts[3].lower()
                word = f"{c1.lower()}{v1}{c2v2}"
                domain = analyzer.DOMAINS.get(c1, "Inconnu")
                role_name, role_desc = analyzer.VOWEL_ROLES.get(v1, ("Inconnu", ""))
                print(f"  ⚡ Mot forgé : {word.upper()} ({analyzer.to_ipa(word)})")
                print(f"     Domaine   : C1={c1} ({domain})")
                print(f"     Rôle      : V1={v1} ({role_name} - {role_desc})")
            else:
                print("Usage : :forge <C1> <V1> <C2V2> (ex: :forge CH A po)")
            continue

        # Commande :prince
        if line.startswith(":prince") or line.startswith(":p"):
            parts = line.split()
            p_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
            import json
            prince_f = ROOT_DIR / "data" / "petit_prince.json"
            with open(prince_f, "r", encoding="utf-8") as pf:
                p_data = json.load(pf)
            match = next((s for s in p_data["sentences"] if s["id"] == p_id), p_data["sentences"][0])
            print(f"\n[Petit Prince #{match['id']}]")
            print(f"  Lumina : {match['lumina']}")
            print(f"  IPA    : {tts.get_ipa(match['lumina'])}")
            print(f"  FR     : {match['fr']}\n")
            continue

        # Traduction automatique par détection de langue
        is_lumina = any(tok in analyzer.particles or tok in analyzer.pronouns or tok in analyzer.lexicon for tok in line.lower().split())
        if is_lumina:
            res = translator.translate_lumina_to_fr(line)
            print(f"  🇫🇷 FR  : {res['target']}")
            print(f"  📖 Glose: {' | '.join(res['glosses'])}")
        else:
            res = translator.translate_fr_to_lumina(line)
            print(f"  ✨ Lumina : {res['target']}")
            print(f"  🔊 IPA    : {tts.get_ipa(res['target'])}")

if __name__ == "__main__":
    main()
