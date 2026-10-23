# Reddit launch post — Lumina

## Suggested subreddits

- **r/conlangs**: natural audience for an a priori "philosophical" language. ⚠️ **Read the sub's rules first.** r/conlangs is generally hostile to AI-generated languages and may restrict or ban them, and Lumina's founding document came out of a DeepSeek conversation. Disclose it up front (as below), or skip this sub if the rules forbid it.
- **r/auxlangs**: Lumina claims "universal / logical" goals, so this sub will rightly challenge it on learnability and neutrality.
- **r/Lojban** (optional): the design overlaps with Lojban and Ro on categorical roots and regularity. Frame it as a question, not an advert.
- **r/Python** (Showcase flair): the engine side (morphological analyzer, formant TTS without dependencies, single-file web studio).

---

**Title:** Lumina: an a priori conlang where each root's first consonant encodes the semantic domain and its first vowel the part of speech, with a Python analyzer/translator and formant TTS (prototype, AI-assisted origin disclosed)

---

Hi all,

I've open-sourced **Lumina**, an experimental a priori "logical" language plus the tooling around it (analyzer, French ↔ Lumina translator, TTS, and a small web studio). It's a prototype, and I'm looking for critique of the design itself.

**Disclosure up front:** the initial design came from a document generated in a conversation with the DeepSeek LLM ("Construction d'une langue universelle optimale"; the PDF is in the repo). My work was to formalize it, fix its ambiguities and typos, build the lexicon, and implement and test the tooling. I'd like to know whether the core idea survives human scrutiny.

### Core design

Every lexical root is **C1V1C2V2** (CV-CV):

- **C1 = semantic domain**: `T/D` time, `K/G` space/matter, `P/B` number/logic, `S/Z` sensation, `M/N` human/social, `F/V` speech/information, `L/R` motion, `SH/ZH` abstraction, `J/CH` tools/technique, `H` negation/void.
- **V1 = category**: `a` noun, `i` verb, `u` adjective, `o` place/collective, `e` agent/means.
- **C2V2 = specific meaning.**

Particles are CV or CVC. Grammar is strict SVO with no exceptions, stress is always penultimate, and adverbs of manner take `-fi` (`puru → purufi`). The phonology is fairly standard: 5 vowels, plus consonants including `sh`, `zh`, `ch`, `j`, `ng`. Example: `Mina sifi la kafa kabo`, analyzed word by word with IPA by the CLI.

### What's in the repo

- Bilingual (EN/FR) specification, reference grammar, lexicon, 5-lesson tutorial and phrasebook.
- Python engine: morphological/semantic analyzer with IPA, French ↔ Lumina translator, a "word forge" that builds roots from C1/V1/C2V2, a CLI and a REPL.
- TTS through Windows SAPI or a dependency-free formant WAV generator; basic STT.
- `index.html` "Lumina Studio": translator, word forge, quizzes, and a bilingual karaoke reader for chapter 1 of *Le Petit Prince*.
- 14 tests and a corpus audit script. MIT licence.

### Known weaknesses

- **Small lexicon**: about 71 roots, plus 24 particles, 6 pronouns and 11 numerals.
- **The lexicon doesn't fully obey its own rule yet.** Some examples:
  - The pronouns (`mina`, `tina`, `lina`) use `i`, which is supposed to mark verbs, and their C1 (`T`, `L`) has nothing to do with the time and motion domains.
  - Some plain nouns use `o` (`kofa` "snake", `tome` "moon").
  - Both are fixable, but they show the tension between a rigid matrix and usable vocabulary.
- **Domain-by-first-consonant creates near-minimal pairs for related concepts** (`kafa` animal / `kofa` snake / `kapa` hat / `kopa` nose). That's the classic objection to Wilkins-style languages (easy to confuse under noise) and I haven't addressed it.
- **Translation is lexicon-driven, word by word**, with no real parsing.
- **No learnability data at all.**
- There's some duplicated code between `source/` and `lumina_core/` that I still need to clean up.

### Feedback I'm looking for

- Is encoding domain in C1 and category in V1 worth the cost in confusability, or is it a dead end already explored (Ro, Wilkins, aUI)?
- How should pronouns and particles relate to the matrix: exempt, or forced into it?
- Would you keep `o` as "place/collective", or is it doing too much?
- Prior art I should read before going further?

Repo: https://github.com/silveremartin-dev/Lumina

Thanks for reading. Honest criticism is exactly what I'm after.

— Silvère Martin-Michiellot
