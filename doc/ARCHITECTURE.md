# Lumina — System Architecture & Technical Specifications

This document outlines the software architecture of the Lumina computational linguistics platform, encompassing parsing, bidirectional translation, acoustic speech synthesis, and verification.

---

## 1. Architectural Overview

```
                                  Lumina Input
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │    Morphological Analyzer (AST)       │
                   │  - Canonical C1V1C2V2 Dissector       │
                   │  - Invariable Particle Extractor      │
                   │  - Penultimate Stress IPA Engine      │
                   └───────────────────┬───────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────────┐                         ┌───────────────────────┐
│  Bidirectional Translator │                         │    Acoustic Engine    │
│  - Lumina -> EN/FR SVO    │                         │  - Glottal Oscillator │
│  - EN/FR -> Lumina Normal │                         │  - Formant Resonators │
│  - Morphological Glossing │                         │  - Standard 16-bit WAV│
└───────────────────────────┘                         └───────────────────────┘
            │                                                     │
            └──────────────────────────┬──────────────────────────┘
                                       ▼
                         Client Application Layer
                       ┌───────────────────────────┐
                       │   CLI Tool (`cli.py`)     │
                       │   Web Studio (`index.html`)│
                       └───────────────────────────┘
```

---

## 2. Component Design

### 2.1 Morphological & Semantic Analyzer (`source/analyzer.py`)
- **RegEx Tokenizer**: Splits on word boundaries while retaining syntactic punctuation.
- **Root Dissection**: Decomposes four-phoneme words into:
  $$\text{Root} = C_1 + V_1 + C_2V_2$$
  Matches against category tables in constant time $\mathcal{O}(1)$.
- **IPA Transcription Engine**: Replaces post-alveolar digraphs (`sh` $\to$ /ʃ/, `ch` $\to$ /t͡ʃ/, `j` $\to$ /d͡ʒ/) and applies penultimate vocalic stress markers (/ˈ/).

### 2.2 Bidirectional Translator (`source/translator.py`)
- **Direct & Inverted Indices**: Pre-loads bidirectional lookup tables from `data/lexique.json`.
- **Preposition & Tense Resolvers**: Converts French and English past/present/future auxiliaries into Lumina preverbal particles (`na`, `li`, `vo`) and maps contractions (`l'animal` $\to$ `la kafa`).
- **Glosses Generation**: Generates per-token semantic glosses for educational transparency.

### 2.3 Acoustic Synthesis Engine (`source/tts.py`)
- **Harmonic Glottal Source**: Implements sawtooth wave summation:
  $$S(t) = \sum_{k=1}^{3} \frac{1}{k} \sin(2\pi \cdot k \cdot f_0 \cdot t)$$
  with fundamental frequency $f_0 = 125\text{ Hz}$.
- **Formant Resonant Filters**: Applies dual-formant resonance pairs $(F_1, F_2)$ tailored to pure Lumina vowels:
  - `/a/`: $(800\text{ Hz}, 1200\text{ Hz})$
  - `/e/`: $(500\text{ Hz}, 1800\text{ Hz})$
  - `/i/`: $(280\text{ Hz}, 2250\text{ Hz})$
  - `/o/`: $(500\text{ Hz}, 850\text{ Hz})$
  - `/u/`: $(320\text{ Hz}, 800\text{ Hz})$
- **Zero External Dependencies**: Writes standard uncompressed linear PCM RIFF WAV headers using Python's native `wave` and `struct` libraries.

---

## 3. Directory Layout Standards

| Directory | Purpose |
|---|---|
| `doc/` | Comprehensive technical and linguistic documentation in English |
| `docs/` | French documentation & pedagogical resources |
| `data/` | Authoritative JSON corpora (`lexique.json`, `petit_prince.json`) |
| `source/` | Production-grade Python package |
| `scripts/` | Tooling, corpus auditing, and execution scripts |
| `test/` | Automated unit tests verified by `pytest` |
| `scratch/` | Git-ignored sandbox for transient audio and scratch files |
