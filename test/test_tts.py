"""Unit tests for Lumina phonetic transcription and formant audio synthesis."""

import wave
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from source.tts import LuminaTTS

def test_ipa_sentence_generation():
    tts = LuminaTTS()
    ipa = tts.get_ipa("Mina sifi la kafa")
    assert "/ˈmina/" in ipa
    assert "/ˈsifi/" in ipa
    assert "/ˈkafa/" in ipa

def test_wav_audio_generation(tmp_path):
    tts = LuminaTTS()
    output_wav = tmp_path / "test_speech.wav"
    out = tts.generate_formant_wav("Mina sifi", str(output_wav))
    
    assert Path(out).exists()
    assert Path(out).stat().st_size > 500  # Non-trivial audio file

    # Inspect WAV properties
    with wave.open(str(output_wav), 'rb') as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2  # 16-bit
        assert wf.getframerate() == 22050
        assert wf.getnframes() > 1000
