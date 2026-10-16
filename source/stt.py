"""Module de Speech-To-Text (STT) et reconnaissance vocale pour Lumina."""

import sys
import subprocess
from pathlib import Path

class LuminaSTT:
    def __init__(self):
        pass

    def listen_and_transcribe(self, timeout_sec: int = 6) -> str:
        """Écoute le microphone par défaut sous Windows et transcrit la voix en texte."""
        ps_script = f"""
        Add-Type -AssemblyName System.Speech
        $engine = New-Object System.Speech.Recognition.SpeechRecognitionEngine
        $grammar = New-Object System.Speech.Recognition.DictationGrammar
        $engine.LoadGrammar($grammar)
        $engine.SetInputToDefaultAudioDevice()
        $res = $engine.Recognize([TimeSpan]::FromSeconds({timeout_sec}))
        if ($res) {{
            Write-Output $res.Text
        }} else {{
            Write-Output ""
        }}
        """
        try:
            p = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_sec + 4
            )
            return p.stdout.strip()
        except Exception as e:
            print(f"Erreur STT microphone : {e}", file=sys.stderr)
            return ""

    def transcribe_wav(self, wav_path: str) -> str:
        """Transcrit un fichier audio .WAV sous Windows."""
        abs_path = str(Path(wav_path).resolve()).replace("'", "''")
        ps_script = f"""
        Add-Type -AssemblyName System.Speech
        $engine = New-Object System.Speech.Recognition.SpeechRecognitionEngine
        $grammar = New-Object System.Speech.Recognition.DictationGrammar
        $engine.LoadGrammar($grammar)
        $engine.SetInputToWaveFile('{abs_path}')
        $res = $engine.Recognize()
        if ($res) {{
            Write-Output $res.Text
        }} else {{
            Write-Output ""
        }}
        """
        try:
            p = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            return p.stdout.strip()
        except Exception as e:
            print(f"Erreur STT fichier WAV : {e}", file=sys.stderr)
            return ""
