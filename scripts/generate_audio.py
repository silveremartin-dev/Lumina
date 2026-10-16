"""Script to synthesize complete speech audio WAV files into scratch/."""

import json
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

from source.tts import LuminaTTS

def main():
    tts = LuminaTTS()
    scratch_dir = ROOT_DIR / "scratch"
    scratch_dir.mkdir(exist_ok=True)

    prince_file = ROOT_DIR / "data" / "petit_prince.json"
    with open(prince_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Generating audio files for Petit Prince sentences...")
    for s in data["sentences"][:3]:  # Generate first 3 sentences as showcase
        out_file = scratch_dir / f"prince_sentence_{s['id']}.wav"
        tts.generate_formant_wav(s["lumina"], str(out_file))
        print(f"Generated #{s['id']}: {out_file} (IPA: {tts.get_ipa(s['lumina'])})")

    print("\n✅ Audio generation finished!")

if __name__ == "__main__":
    main()
