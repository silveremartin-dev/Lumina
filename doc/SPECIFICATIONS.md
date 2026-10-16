# Lumina — Formal Language Specifications

Lumina is an *a priori* constructed logical language (*conlang*) designed for semantic transparency, mathematical predictability, and unambiguous morphological parsing.

---

## 1. Foundational Axioms

1. **Zero Morphological Exceptions**: Every grammatical rule, tense marker, and affix operates universally without irregular stems or suppletive forms.
2. **Fixed Syntax**: Strict Subject-Verb-Object (SVO) word order for declarative clauses.
3. **No Gender Inflexion**: Complete absence of grammatical gender or arbitrary agreement categories.
4. **Orthogonal Semantic Matrix ($C_1V_1C_2V_2$)**: Every primary lexical stem consists of exactly four phonemes across two open syllables.
5. **No Intentional Homophones**: Distinct phonetic forms map to distinct semantic vectors.

---

## 2. Phonology & Orthography

### 2.1 Consonants
The inventory consists of 22 phonemes represented in standard Latin orthography:

| Grapheme | IPA | Description | Example |
|---|---|---|---|
| `p` | /p/ | Voiceless bilabial plosive | *pana* (one) |
| `b` | /b/ | Voiced bilabial plosive | *bobo* |
| `t` | /t/ | Voiceless alveolar plosive | *tome* (moon) |
| `d` | /d/ | Voiced alveolar plosive | *duru* (old) |
| `k` | /k/ | Voiceless velar plosive | *kafa* (animal) |
| `g` | /g/ | Voiced velar plosive | *gafo* (forest) |
| `m` | /m/ | Bilabial nasal | *mina* (I, me) |
| `n` | /n/ | Alveolar nasal | *nomi* (to be named) |
| `f` | /f/ | Voiceless labiodental fricative | *fapo* (book) |
| `v` | /v/ | Voiced labiodental fricative | *voli* (to fly) |
| `s` | /s/ | Voiceless alveolar fricative | *safo* (picture) |
| `z` | /z/ | Voiced alveolar fricative | *zelu* (happy) |
| `sh` | /ʃ/ | Voiceless postalveolar fricative | *shili* (to be) |
| `zh` | /ʒ/ | Voiced postalveolar fricative | *zhoro* |
| `ch` | /t͡ʃ/ | Voiceless postalveolar affricate | *chapo* (computer) |
| `j` | /d͡ʒ/ | Voiced postalveolar affricate | *jako* (pencil) |
| `l` | /l/ | Alveolar lateral approximant | *lifi* (to move) |
| `r` | /r/ | Alveolar trill or tap | *razo* (reason) |
| `h` | /h/ | Voiceless glottal fricative | *hano* (nothing) |
| `y` | /j/ | Palatal approximant | *ya* (yes) |
| `w` | /w/ | Labial-velar approximant | *wa* |
| `ng` | /ŋ/ | Velar nasal | *konga* |

### 2.2 Vowels
Five cardinal pure vowels:
- `a` : /a/ (open front unrounded, as in *father*)
- `e` : /e/ (close-mid front unrounded, as in *cafe*)
- `i` : /i/ (close front unrounded, as in *machine*)
- `o` : /o/ (close-mid back rounded, as in *force*)
- `u` : /u/ (close back rounded, as in *flute*)

### 2.3 Suprasegmentals & Stress
Stress is strictly invariant: it always falls on the **penultimate syllable** (the second-to-last vowel):
- *KA-fa* /ˈkafa/
- *MI-na* /ˈmina/
- *pu-RU-fi* /puˈrufi/

---

## 3. The $C_1V_1C_2V_2$ Semantic Matrix

```
       [C1 : Semantic Domain]
                 │
                 ▼
       [V1 : Morphosyntactic Role]
                 │
                 ▼
       [C2V2 : Lexical Specification]
```

### 3.1 Initial Consonant $C_1$ (Ontological Domain)
- **T- / D-** : Time, Duration, Chronology, Process
- **K- / G-** : Space, Matter, Shape, Systems, Geography
- **P- / B-** : Number, Quantity, Measure, Formal Logic
- **S- / Z-** : Sensation, Perception, Emotion, Harmonics
- **M- / N-** : Human, Individual, Society, Social Bond
- **F- / V-** : Communication, Language, Sound, Media
- **L- / R-** : Motion, Vector, Velocity, Trajectory
- **SH- / ZH-** : Abstraction, Ontology, Existence, Certainty
- **J- / CH-** : Tool, Engineering, Craft, Utility
- **H-** : Negation, Zero, Void, Cancellation

### 3.2 First Vowel $V_1$ (Part of Speech)
- **-A-** : Noun (Entity, concrete object, person, concept)
- **-I-** : Verb (Dynamic action, state transition, occurrence)
- **-U-** : Adjective (Attribute, qualitative state)
- **-O-** : Locus / Container / Collective
- **-E-** : Agent / Instrument / Derived Modifier

### 3.3 Derivational Example
Using base root **F-*-P-*** (Documentation / Epigraphy):
- `fapo` = book, document (Noun)
- `fipi` = to write, record (Verb)
- `fupu` = written, documented (Adjective)
- `fopo` = library, archive (Locus)

---

## 4. Decimal Number System (Domain P-)

| Digit | Word | Digit | Word |
|---|---|---|---|
| 0 | `Pano` | 5 | `Paso` |
| 1 | `Pana` | 6 | `Pasa` |
| 2 | `Pani` | 7 | `Pasi` |
| 3 | `Panu` | 8 | `Pasu` |
| 4 | `Pane` | 9 | `Pase` |
| 10 | `Pato` | 100 | `Pato-pato` |

Composite numerals follow left-to-right positional compounding:
- 12 = `Pato-pani` (ten-two)
- 40 = `Pane-pato` (four-ten)
- 56 = `Paso-pato-pasa` (five-ten-six)
