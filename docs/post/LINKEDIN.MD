Une langue où chaque mot annonce son domaine de sens et sa catégorie grammaticale dès ses deux premières lettres : c'est possible ?
Je publie Lumina, une langue construite logique, avec son moteur de traduction et de synthèse vocale. 🌐

Le point de départ : un document de conception (« Construction d'une langue universelle optimale ») issu d'un échange avec le LLM DeepSeek. J'ai voulu vérifier si ses idées tenaient une fois formalisées et implémentées pour de vrai.

Le principe : chaque racine suit le gabarit C1V1C2V2 (deux syllabes CV-CV).
• C1 donne le domaine : T/D = temps, K/G = espace et matière, M/N = humain et social, L/R = mouvement…
• V1 donne la catégorie : a = nom, i = verbe, u = adjectif, o = lieu ou collectif, e = agent ou moyen
• C2V2 précise le sens. Ordre SVO, zéro exception, accent toujours sur l'avant-dernière syllabe.

Ce que contient le dépôt :
📘 Spécifications, grammaire, lexique et cours en 5 leçons, en français et en anglais
🐍 Un moteur Python : analyse morphologique avec IPA, traduction français ↔ Lumina, « forge » de mots C1V1C2V2
🔊 Synthèse vocale (Windows SAPI ou générateur WAV par formants, sans dépendance) et reconnaissance vocale
🖥️ « Lumina Studio », une page web autonome : traducteur, forge, quiz, et lecture karaoké bilingue du chapitre 1 du Petit Prince
✅ 14 tests et un script d'audit du corpus

⚠️ Soyons clairs : c'est une expérience. Le lexique compte environ 70 racines (plus de 110 entrées en comptant particules, pronoms et nombres), la traduction se fait mot à mot, et certaines entrées ne respectent pas encore la règle voyelle = catégorie. Aucune étude d'apprentissage n'a été menée.

Linguistes, conlangers, curieux : critiques et contributions bienvenues 👇
https://github.com/silveremartin-dev/Lumina

#Conlang #Linguistique #LangueConstruite #OpenSource #Python #TAL #SyntheseVocale
