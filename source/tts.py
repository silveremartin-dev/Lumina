"""Module de Text-to-Speech (TTS) et transcription phonétique pour Lumina."""

import math
import wave
import struct
import subprocess
import sys
from pathlib import Path
from .analyzer import LuminaAnalyzer

class LuminaTTS:
    # Formants approximatifs (F1, F2 en Hz) pour les 5 voyelles fondamentales
    VOWEL_FORMANTS = {
        'a': (800, 1200),
        'e': (500, 1800),
        'i': (280, 2250),
        'o': (500, 850),
        'u': (320, 800)
    }

    def __init__(self):
        self.analyzer = LuminaAnalyzer()

    def get_ipa(self, text: str) -> str:
        """Génère la transcription phonétique IPA d'un texte Lumina."""
        words = text.split()
        ipa_words = [self.analyzer.to_ipa(w) for w in words]
        return " ".join(ipa_words)

    def speak_powershell(self, text: str, rate: int = 0):
        """Utilise le synthétiseur vocal intégré de Windows via PowerShell."""
        # On prépare le texte Lumina en prononciation phonétique claire
        # En configurant la voix pour articuler distinctement les voyelles ouvertes
        escaped_text = text.replace("'", "''").replace('"', '`"')
        ps_cmd = (
            f"Add-Type -AssemblyName System.Speech; "
            f"$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$synth.Rate = {rate}; "
            f"$synth.Speak('{escaped_text}');"
        )
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
            return True
        except Exception as e:
            print(f"Erreur synthèse vocale Windows : {e}", file=sys.stderr)
            return False

    def generate_formant_wav(self, text: str, output_path: str, sample_rate: int = 22050):
        """Génère un fichier audio WAV autonome par synthèse formantique harmonique pure (sans dépendance externe)."""
        clean_text = text.lower()
        samples = []
        f0_base = 125.0  # Fréquence fondamentale (pitch) en Hz

        # Durées en secondes
        vowel_duration = 0.18
        consonant_duration = 0.08
        pause_duration = 0.12

        t_global = 0.0

        for char in clean_text:
            if char in " ,.?!;:":
                # Silence
                n_samples = int(pause_duration * sample_rate)
                samples.extend([0.0] * n_samples)
                continue

            if char in self.VOWEL_FORMANTS:
                f1, f2 = self.VOWEL_FORMANTS[char]
                n_samples = int(vowel_duration * sample_rate)
                for i in range(n_samples):
                    t = i / sample_rate
                    # Source glottique (onde en dent de scie / harmonique)
                    glottal = (math.sin(2 * math.pi * f0_base * t) +
                               0.5 * math.sin(4 * math.pi * f0_base * t) +
                               0.25 * math.sin(6 * math.pi * f0_base * t))
                    
                    # Résonances formantiques F1 et F2
                    v1 = math.sin(2 * math.pi * f1 * t) * math.exp(-t * 20.0)
                    v2 = 0.6 * math.sin(2 * math.pi * f2 * t) * math.exp(-t * 25.0)
                    
                    # Enveloppe d'amplitude (attaque et chute douces)
                    env = math.sin(math.pi * (i / n_samples))
                    val = (glottal * 0.4 + (v1 + v2) * 0.6) * env * 0.7
                    samples.append(val)
            else:
                # Consonne : bruit ou burst simplifié
                n_samples = int(consonant_duration * sample_rate)
                freq = 1800.0
                if char in "sz":
                    freq = 4500.0
                elif char in "fvk":
                    freq = 2400.0
                elif char in "mn":
                    freq = 300.0

                for i in range(n_samples):
                    t = i / sample_rate
                    env = math.sin(math.pi * (i / n_samples))
                    if char in "szfv":
                        # Bruit pseudorandom / haute fréquence
                        noise = math.sin(2 * math.pi * freq * t) * (0.8 + 0.2 * math.sin(100 * t))
                        val = noise * env * 0.35
                    else:
                        tone = math.sin(2 * math.pi * freq * t)
                        val = tone * env * 0.45
                    samples.append(val)

        # Normalisation et écriture WAV 16-bit
        max_amp = max(abs(s) for s in samples) if samples else 1.0
        if max_amp == 0:
            max_amp = 1.0
        norm_factor = 30000.0 / max_amp

        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16 bits
            wf.setframerate(sample_rate)
            raw_data = bytearray()
            for s in samples:
                val_int = int(s * norm_factor)
                val_int = max(-32767, min(32767, val_int))
                raw_data.extend(struct.pack('<h', val_int))
            wf.writeframes(raw_data)

        return output_path
