# Spécifications Formelles de Lumina

Lumina est une langue construite (*conlang*) à visée logique et philosophique, combinant la compacité d'un système à racines modulaires catégorielles (inspiré de Wilkins, Ro et Lojban) et la simplicité grammaticale d'une langue isolante/agglutinante sans exceptions.

Ce document formalise et harmonise les spécifications issues du document fondateur (`Construction d'une langue universelle optimale - DeepSeek.pdf`) en levant les ambiguïtés et coquilles constatées.

---

## 1. Principes Fondamentaux

1. **Régularité Absolue** : Aucune exception, aucune conjugaison irrégulière, aucun accord en genre.
2. **Ordre Syntaxique Fixe** : Sujet - Verbe - Objet (SVO).
3. **Absence d'Homophones** : Chaque combinaison morphologique a un sens univoque.
4. **Système de Racines Sémantiques Prédicat-Matrice** :
   - Mots lexicaux de base : format canonique **C1V1C2V2** (4 phonèmes, 2 syllabes CV-CV).
   - Particules grammaticales : format **CV** ou **CVC**.
5. **Transparence Sémantique** :
   - **C1** définit le *Domaine sémantique principal* (ex: T = Temps, M = Humain).
   - **V1** définit la *Catégorie grammaticale ou rôle* (A = Nom, I = Verbe, U = Adjectif, O = Lieu/Collectif, E = Adverbe/Moyen).
   - **C2V2** définit la *Spécification lexicale précise*.

---

## 2. Phonologie et Orthographe Standard

### 2.1 Les Consonnes (Alphabet Lumina)
L'écriture s'effectue en alphabet latin standard sans diacritiques obligatoires :

| Graphème | IPA | Type articulatoire | Exemple |
|---|---|---|---|
| **p** | /p/ | Occlusive bilabiale sourde | *pana* (un) |
| **b** | /b/ | Occlusive bilabiale sonore | *bobo* |
| **t** | /t/ | Occlusive alvéolaire sourde | *tome* (lune) |
| **d** | /d/ | Occlusive alvéolaire sonore | *duru* (ancien) |
| **k** | /k/ | Occlusive vélaire sourde | *kafa* (animal) |
| **g** | /g/ | Occlusive vélaire sonore | *gafo* (forêt) |
| **m** | /m/ | Nasale bilabiale | *mina* (moi/je) |
| **n** | /n/ | Nasale alvéolaire | *nomi* (s'appeler) |
| **f** | /f/ | Fricative labiodentale sourde | *fapo* (livre) |
| **v** | /v/ | Fricative labiodentale sonore | *voli* (voler) |
| **s** | /s/ | Fricative alvéolaire sourde | *safo* (image) |
| **z** | /z/ | Fricative alvéolaire sonore | *zelu* (heureux) |
| **sh** | /ʃ/ | Fricative post-alvéolaire sourde | *shili* (être) |
| **zh** | /ʒ/ | Fricative post-alvéolaire sonore | *zhoro* |
| **ch** | /t͡ʃ/ | Affriquée post-alvéolaire sourde | *chapo* (machine/ordinateur) |
| **j** | /d͡ʒ/ | Affriquée post-alvéolaire sonore | *jako* (crayon) |
| **l** | /l/ | Latérale alvéolaire | *lifi* (bouger) |
| **r** | /r/ (ou /ɾ/) | Roulée ou battue alvéolaire | *razo* (raison) |
| **h** | /h/ | Fricative glottale sourde | *hano* (rien) |
| **y** | /j/ | Semi-voyelle palatale | *ya* (oui) |
| **w** | /w/ | Semi-voyelle labio-vélaire | *wa* |
| **ng** | /ŋ/ | Nasale vélaire | *konga* |

### 2.2 Les Voyelles
Les 5 voyelles fondamentales :
- **a** : /a/ (comme dans *chat*)
- **e** : /e/ (comme dans *été* ou *fête*)
- **i** : /i/ (comme dans *lit*)
- **o** : /o/ (comme dans *mot*)
- **u** : /u/ (comme dans *loup*)

> **Accent Tonique Régulier** : L'accent tonique porte toujours sur l'**avant-dernière syllabe** (pénultième), comme en espagnol ou en espéranto (*KA-fa*, *MI-na*, *sa-FO-fi*).

---

## 3. Matrice Sémantique C1V1C2V2

### 3.1 Consonne Initiale C1 (Domaines Sémantiques)
- **T- / D-** : Temps, Période, Événement, Chronologie
- **K- / G-** : Espace, Forme, Matière, Géographie, Systèmes
- **P- / B-** : Nombre, Quantité, Mesure, Logique, Calcul
- **S- / Z-** : Sensation, Perception, Émotion, Sentiment
- **M- / N-** : Être humain, Personne, Société, Relations
- **F- / V-** : Communication, Langage, Son, Information
- **L- / R-** : Mouvement, Déplacement, Trajectoire, Changement
- **SH- / ZH-** : Abstraction, Existence, Modalité, Pensée philosophique
- **J- / CH-** : Outil, Technologie, Fabrication, Utilité
- **H-** : Négation, Vide, Absence, Annulation

### 3.2 Première Voyelle V1 (Rôle Morphosyntaxique)
- **-A-** : Nom concret ou abstrait (Entité, Objet, Notion)
- **-I-** : Verbe (Action, Processus, État dynamique)
- **-U-** : Adjectif (Qualité, Propriété, Description)
- **-O-** : Lieu, Conteneur, Milieu, Collectif
- **-E-** : Agent, Moyen, Instrument, Adverbe dérivé

### 3.3 Exemple Dérivationnel
Racine **K-*-B-*** (Matière massive) :
- `KABO` : Éléphant (Nom : chose vivante massive)
- `KIBI` : Alourdir / Massifier (Verbe)
- `KABU` : Massif, énorme (Adjectif)
- `KOBO` : Habitat d'éléphant / Massif rocheux (Lieu)

Racine **F-*-P-*** (Écrit / Connaissance) :
- `FAPO` : Livre / Document (Nom)
- `FIPI` : Écrire / Consigner (Verbe)
- `FUPU` : Écrit / Documenté (Adjectif)
- `FOPO` : Bibliothèque / Librairie (Lieu)

---

## 4. Levée des Ambiguïtés du Document Source

1. **Numération (Domaine P-)** :
   Dans le PDF original, 2 et 3 étaient accidentellement notés *Panu*. Le système régularisé est :
   - 0 : `Pano`
   - 1 : `Pana`
   - 2 : `Pani`
   - 3 : `Panu`
   - 4 : `Pane`
   - 5 : `Paso`
   - 6 : `Pasa`
   - 7 : `Pasi`
   - 8 : `Pasu`
   - 9 : `Pase`
   - 10 : `Pato`
   Les ordinaux utilisent simplement la forme adjectivale `-u` ou la particule d'ordre : `safo pani` ou `safo panu-fi` ("deuxième image" au lieu de l'emprunt étranger *dua* apparu dans le brouillon original).

2. **Élimination des emprunts non conformes dans le texte du Petit Prince** :
   - *por* -> remplacé par la particule officielle **pa** (pour/vers/dans).
   - *pri* -> remplacé par **ko** (concernant/avec) ou **pa**.
   - *a* -> remplacé par **pa** (à/destiné à).
   - *kiso* / *pofo* -> formalisés en racines régulières : `kafa kofa kiso` (serpent intérieur) / `pofo` (serpent extérieur).

3. **Adverbes** :
   Formés de manière invariable avec le suffixe **-fi** greffé sur l'adjectif :
   `guru` (grand) -> `gurufi` (grandement).
   `puru` (vrai) -> `purufi` (vraiment).
