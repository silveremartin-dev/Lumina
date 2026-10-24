# Lumina — Langue Logique Universelle

[![Tests](https://img.shields.io/badge/tests-23%20passed-brightgreen.svg)](file:///c:/Silvere/Encours/Developpement/Lumina/test)
[![Interface](https://img.shields.io/badge/Interface-FR%20%7C%20EN-blue.svg)](file:///c:/Silvere/Encours/Developpement/Lumina/index.html)
[![Syntaxe](https://img.shields.io/badge/Syntaxe-SVO%20Régulière-purple.svg)](file:///c:/Silvere/Encours/Developpement/Lumina/docs/GRAMMAIRE_FR.MD)

Projet d'ingénierie linguistique, formalisation, traduction multilingue, phonologie et synthèse vocale (TTS) pour la langue construite **Lumina**.

Inspiré du document original *« Construction d'une langue universelle optimale »*, Lumina est un langage artificiel logique basé sur une stricte matrice sémantique prédicative **C1V1C2V2** et une syntaxe **SVO** entièrement régulière (zéro exception).

---

## 🌟 Fonctionnalités Principales

### 1. Lumina Web Studio Interactif (`index.html`)
- **Bilingue Intégral (FR / EN)** : Bouton d'en-tête `🇫🇷 FR / 🇬🇧 EN` basculant instantanément l'ensemble de l'interface (titres, onglets, boutons, cartes de phonèmes, 5 cours interactifs, quiz, forge sémantique, karaoké du Petit Prince et référence grammaticale).
- **Traduction Multidirectionnelle (4 modes)** :
  - 🇫🇷 Français &rarr; Lumina
  - 🌐 Lumina &rarr; Français
  - 🇬🇧 English &rarr; Lumina
  - 🌐 Lumina &rarr; English
- **Reconnaissance & Synthèse Vocale (STT / TTS)** : Dictée vocale par microphone (Web Speech Recognition) et prononciation automatique instantanée (Web Speech Synthesis).
- **Forge Sémantique C1V1C2V2** : Sélecteur matriciel interactif de racines et dérivation de mots nouveaux avec validation phonotactique en temps réel.
- **Lecteur Bilingue Karaoké** : Le Petit Prince (Chapitre 1) en texte synchronisé mot-à-mot avec lecture audio continue, pause et reprise.
- **5 Leçons Progressives avec Quiz** : De l'alphabet phonétique jusqu'aux structures propositionnelles complexes avec score immédiat.

### 2. Moteur Python (`source/`) & Scripts (`scripts/`)
- **`source/analyzer.py`** : Analyseur morphologique et sémantique avec transcription phonétique IPA.
- **`source/translator.py`** : Moteur de traduction automatique bidirectionnel.
- **`source/tts.py`** : Synthétiseur vocal TTS autonome & générateur audio WAV à résonance formantique.
- **`scripts/interactive_cli.py`** : Terminal interactif REPL.
- **`scripts/validate_web_studio.py`** : Script d'assurance qualité vérifiant l'intégrité UTF-8, la validité des déclarations JavaScript et des gestionnaires d'événements `onclick`.

### 3. Documentation Complète (`docs/`)
- [**`SPECIFICATIONS.MD`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/SPECIFICATIONS.MD) & [**`SPECIFICATIONS_FR.MD`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/SPECIFICATIONS_FR.MD) : Spécifications et phonologie formelle.
- [**`GRAMMAR.MD`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/GRAMMAR.MD) & [**`GRAMMAIRE_FR.MD`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/GRAMMAIRE_FR.MD) : Grammaire de référence complète (SVO, modaux, aspects, particules).
- [**`LEXICON.MD`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/LEXICON.MD) & [**`LEXIQUE_FR.MD`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/LEXIQUE_FR.MD) : Dictionnaire officiel complet.
- [**`TUTORIAL.MD`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/TUTORIAL.MD) & [**`COURS_DEBUTANT_FR.MD`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/COURS_DEBUTANT_FR.MD) : Manuel d'apprentissage en 5 leçons.
- [**`PHRASEBOOK_DIALOGUES.MD`**](file:///c:/Silvere/Encours/Developpement/Lumina/docs/PHRASEBOOK_DIALOGUES.MD) : Recueil de dialogues et expressions courantes.

---

## 🚀 Démarrage Rapide

### Option A : Lanceur 1-clic (Le plus simple)
Double-cliquez simplement sur **`LANCER_STUDIO.bat`** à la racine du projet ou ouvrez directement [**`index.html`**](file:///c:/Silvere/Encours/Developpement/Lumina/index.html) dans votre navigateur web favori (aucune installation requise).

### Option B : Suite de Tests Python
```powershell
py -3 -m pytest test
py -3 scripts/validate_web_studio.py
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
