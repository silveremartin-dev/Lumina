# Lumina — Langue Logique Universelle

Projet d'ingénierie linguistique, formalisation, traduction bidirectionnelle et synthèse vocale (TTS) pour la langue construite **Lumina**.

Inspiré du document original `Construction d'une langue universelle optimale - DeepSeek.pdf`, Lumina est un langage artificiel logique basé sur une stricte matrice sémantique prédicative **C1V1C2V2** et une syntaxe **SVO** entièrement régulière (zéro exception).

---

## 🌟 Fonctionnalités du Projet

1. **Documents de Référence Formelle (`docs/`)** :
   - [**`SPECIFICATIONS.md`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/SPECIFICATIONS.md) : Spécifications et phonologie (English & [Français](file:///c:/Silvere/Encours/Developpement/Lumina/docs/SPECIFICATIONS_FR.md)).
   - [**`GRAMMAR.md`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/GRAMMAR.md) : Grammaire de référence complète (English & [Français](file:///c:/Silvere/Encours/Developpement/Lumina/docs/GRAMMAIRE_FR.md)).
   - [**`LEXICON.md`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/LEXICON.md) : Dictionnaire officiel complet (English & [Français](file:///c:/Silvere/Encours/Developpement/Lumina/docs/LEXIQUE_FR.md)).
   - [**`TUTORIAL.md`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/TUTORIAL.md) : Cours d'initiation progressif en 5 leçons (English & [Français](file:///c:/Silvere/Encours/Developpement/Lumina/docs/COURS_DEBUTANT_FR.md)).
   - [**`phrasebook_dialogues.md`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/phrasebook_dialogues.md) : Recueil de dialogues et phrases usuelles.
   - [**`ARCHITECTURE.md`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/ARCHITECTURE.md) : Architecture logicielle et synthèse formantique.

2. **Lumina Studio Web Interactif (`index.html`)** :
   - Traducteur bidirectionnel direct (Français &harr; Lumina) avec décomposition morphologique en direct.
   - Synthèse vocale intégrée (TTS) et reconnaissance vocale par microphone (STT).
   - Forge interactive de mots (Générateur sémantique C1V1C2V2).
   - Lecteur bilingue karaoké du Chapitre 1 du Petit Prince.
   - Quiz interactifs d'apprentissage.

3. **Moteur Python (`source/`) & Scripts (`scripts/`)** :
   - Analyseur morphologique et sémantique avec transcription phonétique IPA (`analyzer.py`).
   - Traducteur bidirectionnel automatique (`translator.py`).
   - Synthétiseur vocal TTS autonome & générateur audio WAV à résonance formantique (`tts.py`).
   - Module Speech-To-Text (`stt.py`).
   - Terminal interactif REPL (`scripts/interactive_cli.py`).
   - Synchronisation et export du dictionnaire (`scripts/export_dictionary.py`).
   - Audit et vérification du corpus (`scripts/verify_corpus.py`).

---

## 🚀 Démarrage Rapide

### Option A : Ouvrir Lumina Studio dans votre navigateur
Double-cliquez simplement sur [**`index.html`**](file:///c:/Silvere/Encours/Developpement/Lumina/index.html) ou lancez un serveur local :
```powershell
py -3 -m http.server 8080
```
Puis accédez à `http://localhost:8080`.

### Option B : Utiliser la CLI Python

#### 1. Traduire une phrase
```powershell
# Vers le français avec analyse mot-à-mot
py -3 lumina_core/cli.py translate "Mina na kidi la kafa kabo" --to fr

# Vers le Lumina depuis le français
py -3 lumina_core/cli.py translate "Je vois l'animal" --to lumina
```

#### 2. Analyser un mot ou une phrase (IPA, Domaine sémantique, Rôle)
```powershell
py -3 lumina_core/cli.py analyze "Mina sifi la safo sulo"
```

#### 3. Prononciation vocale (TTS Windows)
```powershell
py -3 lumina_core/cli.py speak "Mina na kisi la safo"
```

#### 4. Générer un fichier audio WAV autonome
```powershell
py -3 lumina_core/cli.py wav "Mina sifi la kafa kabo" -o parole.wav
```

#### 5. Forger un nouveau mot avec la matrice C1V1C2V2
```powershell
# Création d'une machine/ordinateur : CH (Outil) + A (Nom) + po (calcul)
py -3 lumina_core/cli.py wordgen --c1 CH --v1 A --c2v2 po
```

#### 6. Consulter le texte fondateur du Petit Prince
```powershell
py -3 lumina_core/cli.py prince --id 2
```

---

## 📐 Résumé du Système Sémantique C1V1C2V2

Chaque mot-racine canonique comporte 4 phonèmes réguliers :
- **C1 (Consonne initiale)** : Domaine conceptuel
  - `T/D` : Temps | `K/G` : Espace/Matière | `P/B` : Nombre/Logique | `S/Z` : Sensation
  - `M/N` : Humain/Social | `F/V` : Parole/Information | `L/R` : Mouvement | `SH/ZH` : Abstraction
  - `J/CH` : Outil/Technique | `H` : Négation/Vide
- **V1 (Première voyelle)** : Catégorie morphosyntaxique
  - `-A-` : Nom (Entité, Chose)
  - `-I-` : Verbe (Action, Processus)
  - `-U-` : Adjectif (Qualité, Propriété)
  - `-O-` : Lieu / Collectif
  - `-E-` : Agent / Moyen
- **C2V2** : Spécification lexicale précise.
- **Suffixe `-fi`** : Dérive un adverbe de manière à partir d'un adjectif (`puru` &rarr; `purufi`).
