# agent.md — Developer & AI Agent Collaboration Directives for Lumina

## 🎯 1. Core Project Identity & Scope

**Lumina is a deterministic, a priori constructed logical language (*conlang*) and computational linguistic suite. It replaces irregular natural language morphology with a pure, orthogonal semantic matrix ($C_1V_1C_2V_2$) and a strictly invariable Subject-Verb-Object (SVO) syntax.**

### The Problem Lumina Solves:
1. **Natural Language Ambiguity & Irregularities**: Human languages are plagued by irregular inflections, grammatical gender mismatches, and homophonic collisions.
2. **Semantic Opaqueness**: In natural tongues, word stems rarely expose their ontological hierarchy. In Lumina, every lexical root of format $C_1V_1C_2V_2$ immediately encodes its ontological domain ($C_1$), its morphosyntactic role ($V_1$), and its concrete semantic terminal ($C_2V_2$).
3. **Machine-Human Asymmetry**: While unconstrained LLMs hallucinate linguistic structures, Lumina enforces an unambiguous, algorithmic bijection between grammatical intent and surface form.

### Boundary Principles:
* **IN SCOPE**:
  1. **Formal Linguistic Specification**: Zero-exception SVO grammar, invariable particle system (`la`, `ro`, `na`, `li`, `vo`, `pe`, `du`, `ne`, `ma`, `ta`).
  2. **Deterministic Morphological Analyzer**: Parsing, decomposing, and validating $C_1V_1C_2V_2$ roots with IPA phonetic rendering.
  3. **Bidirectional Translator**: Rule-based and lexical mapping between French/English and Lumina with explicit glosses.
  4. **Phonetic & Text-To-Speech (TTS) Engine**: 100% regular penult stress, harmonic formant WAV synthesis without external binaries, and Web Speech API synthesis.
  5. **Interactive Web Studio**: Zero-dependency, client-side visual environment for translation, speech synthesis, matrix word forging, and interactive learning.
  6. **Corpus Benchmarking**: Formal alignment of canonical texts (e.g. *The Little Prince*, Chapter 1).
* **OUT OF SCOPE / STRICTLY REJECTED**:
  - Unregulated ad-hoc lexical borrowings (e.g., using French/Spanish prepositions like *por* or irregular plurals).
  - Grammatical gender or noun-class agreement.
  - Tonal or unpredictable stress variations: the penultimate vowel is always stressed.

---

## ⚡ 2. The Orthogonal Semantic Matrix ($C_1V_1C_2V_2$)

Every canonical root word consists of exactly 4 phonemes (2 open CV syllables):

$$\text{Root} = C_1 \cdot V_1 \cdot C_2 \cdot V_2$$

### 2.1 Category Classifiers ($C_1$)
- `T` / `D` : Time, Chronology, Duration, Evolution
- `K` / `G` : Space, Physical Matter, Shape, Systems
- `P` / `B` : Number, Measure, Quantity, Formal Logic
- `S` / `Z` : Sensation, Emotion, Visuals, Harmonics
- `M` / `N` : Human, Social, Agency, Relationships
- `F` / `V` : Communication, Speech, Signal, Media
- `L` / `R` : Motion, Trajectory, Kinetics, Direction
- `SH` / `ZH` : Abstraction, Ontology, Existence, Certainty
- `J` / `CH` : Tool, Mechanism, Engineering, Utility
- `H` : Negation, Void, Absence, Cancellation

### 2.2 Morphosyntactic Role ($V_1$)
- **A** : Noun (Concrete object, entity, individual)
- **I** : Verb (Dynamic action, state transition)
- **U** : Adjective (Quality, property, descriptive state)
- **O** : Locus / Container / Collective
- **E** : Agent / Instrument / Derived Adverb

### 2.3 Modifier Derivation
- Adverbs of manner are formed deterministically with suffix `-fi` appended to the adjectival stem:  
  $$\text{Adverb} = [C_1 U C_2 V_2]\text{-fi}$$  
  *Example:* `guru` (large) $\to$ `gurufi` (greatly); `puru` (true) $\to$ `purufi` (truly).

---

## 🔄 3. Multi-Tier System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                   TIER 1 : Lexical & Semantic Core                     │
│  `data/lexique.json` & `source/analyzer.py`                           │
│  - Orthogonal Root Matrix Parser ($C_1V_1C_2V_2$)                      │
│  - Penultimate Stress IPA Phonetic Transcriber                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│ TIER 2: Engine  │        │ TIER 3: Audio   │        │ TIER 4: Studio  │
│ `translator.py` │        │ `tts.py` (WAV)  │        │ `index.html`    │
│ - FR/EN <-> Lum │        │ - Formants      │        │ - Web TTS       │
│ - Tense & SVO   │        │ - Windows SAPI  │        │ - Matrix Forge  │
└─────────────────┘        └─────────────────┘        └─────────────────┘
```

---

## 🛠️ 4. Code Standards & Testing Policy

1. **Standard Library First**: Core computational linguistics routines must run on pure Python standard library (`re`, `json`, `wave`, `math`, `struct`, `argparse`).
2. **Reproducibility**: All unit tests in `test/` must pass cleanly without external network access:
   ```powershell
   py -3 -m pytest test/
   ```
3. **Phonetic Determinism**: IPA output must strictly adhere to the IPA standards defined in `docs/SPECIFICATIONS.md`.
4. **Bilingual Corpus**: Any modification to lexical items must update both `data/lexique.json` and English/French documentation in `docs/`.
