"""Generator for Expansion Part 4: Everyday life, actions, objects, nature, weather, commerce, food, adjectives.
Picks collision-free slots systematically.
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.baseline_data import BASELINE_DATA
import re

CONSONANTS = ['t', 'd', 'k', 'g', 'p', 'b', 's', 'z', 'm', 'n', 'f', 'v', 'l', 'r', 'sh', 'zh', 'j', 'ch', 'h']
VOWELS = ['a', 'e', 'i', 'o', 'u']

# 1. Collect all currently used keys across all family files
from scripts.families_domain_t_d import FAMILIES_T_D
from scripts.families_domain_k_g import FAMILIES_K_G
from scripts.families_domain_p_b import FAMILIES_P_B
from scripts.families_domain_s_z import FAMILIES_S_Z
from scripts.families_domain_m_n import FAMILIES_M_N
from scripts.families_domain_f_v import FAMILIES_F_V
from scripts.families_domain_l_r import FAMILIES_L_R
from scripts.families_domain_sh_zh import FAMILIES_SH_ZH
from scripts.families_domain_j_ch import FAMILIES_J_CH
from scripts.families_domain_h import FAMILIES_H
from scripts.families_expansion import FAMILIES_EXPANSION
from scripts.families_expansion_part2 import FAMILIES_EXPANSION_PART2
from scripts.families_expansion_part3 import FAMILIES_EXPANSION_PART3

used_keys = set()
for fam_list in [
    FAMILIES_T_D, FAMILIES_K_G, FAMILIES_P_B, FAMILIES_S_Z, FAMILIES_M_N,
    FAMILIES_F_V, FAMILIES_L_R, FAMILIES_SH_ZH, FAMILIES_J_CH, FAMILIES_H,
    FAMILIES_EXPANSION, FAMILIES_EXPANSION_PART2, FAMILIES_EXPANSION_PART3
]:
    for fam in fam_list:
        used_keys.add((fam[0].lower(), fam[1].lower(), fam[2].lower()))

for r in BASELINE_DATA['roots']:
    w = r['word'].lower()
    m = re.match(r'^(sh|zh|ch|[a-z])([aeiou])(sh|zh|ch|[a-z])([aeiou])$', w)
    if m:
        used_keys.add((m.group(1), m.group(3), m.group(4)))

print(f"Currently used keys: {len(used_keys)}")

def allocate_slot(c1_preferred, c1_alt=None):
    for c1 in [c1_preferred] + ([c1_alt] if c1_alt else []):
        for c2 in CONSONANTS:
            for v2 in VOWELS:
                key = (c1, c2, v2)
                if key not in used_keys:
                    used_keys.add(key)
                    return key
    raise RuntimeError(f"Exhausted slots for {c1_preferred}")

# Define semantic families to add
RAW_FAMILIES = [
    # --- ACTIONS & VERBES DU QUOTIDIEN ---
    ("m", "n", "Humain / Action & Recherche", {
        'a': ("recherche, quête, prospection, investigation", "search, quest, lookup, inquiry", "Action de chercher ce qui manque"),
        'i': ("chercher, rechercher, être en quête", "to search, to look for, to seek", "Tenter de trouver"),
        'u': ("chercheur, curieux, en quête", "searching, seeking, inquiring", "Qui cherche activement"),
        'o': ("zone de recherche, laboratoire de quête", "search area, query field", "Lieu où l'on cherche"),
        'e': ("chercheur, enquêteur, pisteur", "searcher, seeker, explorer", "Personne qui cherche"),
    }),
    ("m", "n", "Humain / Action & Découverte", {
        'a': ("trouvaille, découverte, invention, trouvée", "discovery, find, finding, invention", "Ce qui a été trouvé"),
        'i': ("trouver, découvrir, dénicher, repérer", "to find, to discover, to locate", "Parvenir à trouver"),
        'u': ("trouvé, découvert, déniché", "found, discovered, located", "Qui est trouvé"),
        'o': ("bureau des objets trouvés, gisement", "found objects office, deposit", "Lieu des trouvailles"),
        'e': ("inventeur, découvreur, trouveur", "finder, discoverer", "Personne qui trouve"),
    }),
    ("s", "z", "Sensation / Vision & Regard", {
        'a': ("regard, observation, vision attentive", "look, glance, gaze, viewing", "Action de fixer des yeux"),
        'i': ("regarder, observer, contempler, mirer", "to look at, to watch, to behold, to gaze", "Porter son regard sur"),
        'u': ("observateur, attentif des yeux, contemplatif", "watchful, gazing, looking", "Qui regarde attentivement"),
        'o': ("observatoire, mirador, point de vue", "viewpoint, lookout, vantage point", "Lieu d'où l'on regarde"),
        'e': ("spectateur, observateur, témoin visuel", "watcher, viewer, onlooker", "Personne qui regarde"),
    }),
    ("s", "z", "Sensation / Audition & Écoute", {
        'a': ("écoute, audition, attention auditive", "listening, hearing, audition", "Action de prêter l'oreille"),
        'i': ("écouter, prêter l'oreille, ouïr", "to listen, to listen to, to hearken", "Percevoir attentivement par l'ouïe"),
        'u': ("attentif, à l'écoute, tout ouïe", "attentive, listening, all ears", "Prêt à écouter"),
        'o': ("salle d'écoute, auditorium", "listening room, auditorium", "Lieu où l'on écoute"),
        'e': ("auditeur, écoutant, veilleur sonore", "listener, hearer", "Personne qui écoute"),
    }),
    ("s", "z", "Sensation / Olfaction & Odorat", {
        'a': ("odeur, senteur, effluve, parfum, arôme", "smell, scent, odor, aroma, fragrance", "Perception olfactive"),
        'i': ("sentir, humer, flairer, fleurer", "to smell, to scent, to whiff", "Percevoir une odeur"),
        'u': ("odorant, parfumé, odoriférant", "odorous, fragrant, scented", "Qui a une odeur"),
        'o': ("jardin parfumé, parfumerie", "scented garden, perfumery", "Lieu des odeurs"),
        'e': ("parfumeur, nez olfactif", "perfumer, nose", "Expert des odeurs"),
    }),
    ("s", "z", "Sensation / Gustation & Goût", {
        'a': ("goût, saveur, dégustation, sapidité", "taste, flavor, savor, relish", "Perception de la saveur"),
        'i': ("goûter, savourer, déguster, tester", "to taste, to savor, to relish", "Percevoir par le goût"),
        'u': ("savoureux, sapide, gustatif, délicieux", "tasty, flavorful, savory, delicious", "Qui a du goût"),
        'o': ("salle de dégustation, buffet", "tasting room, banquet hall", "Lieu où l'on goûte"),
        'e': ("goûteur, dégustateur, sommelier", "taster, gourmet, food critic", "Personne qui goûte"),
    }),
    ("s", "z", "Sensation / Toucher & Tact", {
        'a': ("toucher, contact tactile, caresse, palpation", "touch, contact, caress, stroke", "Perception par la peau"),
        'i': ("toucher, palper, effleurer, tâter", "to touch, to feel, to stroke, to handle", "Entrer en contact physique"),
        'u': ("tactile, palpable, au toucher", "tactile, palpable, touch-sensitive", "Accessible au toucher"),
        'o': ("surface tactile, zone de contact", "touchpad, contact surface", "Lieu du contact"),
        'e': ("masseur, palpeur, toucheur", "toucher, masseur", "Personne qui touche"),
    }),
    ("l", "r", "Mouvement / Transport & Portée", {
        'a': ("portage, fardeau, charge portée", "carrying, load, bearing", "Action de porter une charge"),
        'i': ("porter, apporter, transporter, tenir", "to carry, to bring, to bear, to wear", "Soutenir et mouvoir une charge"),
        'u': ("porteur, chargé, portant", "bearing, loaded, portable", "Qui porte"),
        'o': ("dépôt de portage, quai de chargement", "cargo bay, loading dock", "Lieu du portage"),
        'e': ("porteur, coursier, déménageur", "carrier, porter, bearer", "Personne qui porte"),
    }),
    ("l", "r", "Mouvement / Emport & Départ", {
        'a': ("emport, emménagement, enlèvement", "taking away, removal, haul", "Action d'emmener au loin"),
        'i': ("emporter, emmener, enlever au loin", "to take away, to take along, to remove", "Partir en portant avec soi"),
        'u': ("emporté, transportable au loin", "takeaway, taken away", "Qui est emporté"),
        'o': ("relais de départ, point d'emport", "pickup point, takeaway bay", "Lieu où l'on emporte"),
        'e': ("convoyeur, emmèneur", "convoyer, hauler", "Personne qui emmène"),
    }),

    # --- COMMERCE, ARGENT & ÉCONOMIE ---
    ("p", "b", "Quantité / Échange & Achat", {
        'a': ("achat, acquisition, emplette, provision", "purchase, buy, acquisition, shopping", "Action d'acheter un bien"),
        'i': ("acheter, acquérir, faire des emplettes", "to buy, to purchase, to acquire", "Obtenir contre de l'argent"),
        'u': ("acheté, payable, acquis", "purchased, bought, acquirable", "Qui a été acheté"),
        'o': ("magasin d'achat, boutique, marché", "shop, boutique, retail store", "Lieu où l'on achète"),
        'e': ("acheteur, client, chaland, consommateur", "buyer, purchaser, customer, shopper", "Personne qui achète"),
    }),
    ("p", "b", "Quantité / Échange & Vente", {
        'a': ("vente, cession, commerce, débit", "sale, selling, vending, trade", "Action de céder contre prix"),
        'i': ("vendre, céder, commercialiser, écouler", "to sell, to vend, to market", "Donner contre de l'argent"),
        'u': ("vendu, en vente, commercialisable", "sold, for sale, commercial", "Disponible à l'achat"),
        'o': ("comptoir de vente, étal, échoppe", "sales counter, stall, storefront", "Lieu de vente"),
        'e': ("vendeur, marchand, boutiquier, commerçant", "seller, vendor, merchant, shopkeeper", "Personne qui vend"),
    }),
    ("p", "b", "Quantité / Échange & Paiement", {
        'a': ("paiement, règlement, versement, solde", "payment, settlement, disbursement", "Remise d'argent dû"),
        'i': ("payer, régler, verser, solder", "to pay, to settle, to disburse", "Donner l'argent convenu"),
        'u': ("payé, réglé, soldé, acquitté", "paid, settled, discharged", "Qui a été réglé"),
        'o': ("caisse, guichet de paiement, borne", "cashier desk, checkout, payment terminal", "Lieu où l'on paie"),
        'e': ("payeur, trésorier, caissier", "payer, cashier, treasurer", "Personne qui paie ou encaisse"),
    }),
    ("p", "b", "Quantité / Valeur & Coût", {
        'a': ("coût, prix, valeur marchande, tarif", "cost, price, charge, rate, fare", "Montant exigé pour un bien"),
        'i': ("coûter, valoir, être au prix de", "to cost, to be priced at, to be worth", "Avoir un prix déterminé"),
        'u': ("cher, coûteux, onéreux, précieux", "expensive, costly, pricey", "Qui a un prix élevé"),
        'o': ("grille tarifaire, étiquette de prix", "price tag, rate board", "Affichage du coût"),
        'e': ("estimateur, évaluateur de prix", "valuer, appraiser", "Personne qui évalue le coût"),
    }),
    ("p", "b", "Quantité / Prêt & Emprunt", {
        'a': ("prêt, emprunt, crédit, créance", "loan, credit, lending, borrowing", "Cession temporaire d'un bien"),
        'i': ("prêter, accorder un prêt, avancer", "to lend, to loan, to grant credit", "Donner pour un temps"),
        'u': ("prêté, à titre de prêt, créditeur", "lent, loaned, on loan", "Faisant l'objet d'un prêt"),
        'o': ("banque de prêt, bibliothèque de prêt", "lending bank, loan desk", "Lieu où l'on prête"),
        'e': ("prêteur, créancier, banquier", "lender, creditor", "Personne qui prête"),
    }),
    ("p", "b", "Quantité / Emprunt & Dette", {
        'a': ("emprunt, dette, passif, obligation", "borrowing, debt, liability", "Ce que l'on doit rendre"),
        'i': ("emprunter, contracter une dette", "to borrow, to incur debt", "Prendre pour un temps"),
        'u': ("endetté, emprunté, débiteur", "indebted, borrowed, debtor", "Qui doit rembourser"),
        'o': ("caisse d'emprunt", "debt office", "Service de la dette"),
        'e': ("emprunteur, débiteur", "borrower, debtor", "Personne qui emprunte"),
    }),
    ("p", "b", "Quantité / Gain & Victoire", {
        'a': ("gain, bénéfice, victoire, profit", "gain, profit, win, earnings", "Ce que l'on acquiert par l'effort"),
        'i': ("gagner, remporter, vaincre, profiter", "to win, to earn, to gain, to profit", "Obtenir par la victoire"),
        'u': ("gagnant, victorieux, profitable, lucratif", "winning, victorious, profitable", "Qui a gagné"),
        'o': ("podium des vainqueurs, salle des gains", "winners podium, earnings vault", "Lieu du triomphe"),
        'e': ("gagnant, vainqueur, lauréat", "winner, victor", "Personne qui gagne"),
    }),
    ("p", "b", "Quantité / Perte & Défaite", {
        'a': ("perte, défaite, échec, manque", "loss, defeat, forfeiture, failure", "Ce que l'on a égaré ou manqué"),
        'i': ("perdre, égarer, subir une défaite", "to lose, to misplace, to forfeit", "Ne plus avoir en sa possession"),
        'u': ("perdu, défait, égaré, manqué", "lost, defeated, missing", "Qui a été égaré"),
        'o': ("fossé des pertes, zone d'oubli", "loss record, lost zone", "Lieu de l'égarement"),
        'e': ("perdant, vaincu, égaré", "loser, defeated person", "Personne qui perd"),
    }),

    # --- ACTIONS PHYSIQUES QUOTIDIENNES ---
    ("j", "ch", "Outil / Action & Ouverture", {
        'a': ("ouverture, baie, passage ouvert, fente", "opening, aperture, unlock, breach", "État ou acte d'ouvrir"),
        'i': ("ouvrir, déboucher, déverrouiller, déployer", "to open, to unlock, to unfold", "Rendre accessible"),
        'u': ("ouvert, accessible, béant, déclos", "open, unlocked, unclosed", "Qui n'est pas fermé"),
        'o': ("porte ouverte, sas d'accès", "open doorway, portal", "Lieu ouvert"),
        'e': ("ouvreur, portier d'ouverture", "opener, gate opener", "Personne qui ouvre"),
    }),
    ("j", "ch", "Outil / Action & Fermeture", {
        'a': ("fermeture, clôture, verrouillage, scellé", "closing, shutting, lock, closure", "État ou acte de fermer"),
        'i': ("fermer, clore, verrouiller, boucler", "to close, to shut, to lock", "Rendre inaccessible"),
        'u': ("fermé, clos, verrouillé, scellé", "closed, shut, locked", "Qui n'est pas ouvert"),
        'o': ("porte fermée, coffre scellé", "closed gate, locked chamber", "Lieu fermé"),
        'e': ("gardien de fermeture, serrurier", "closer, locksmith", "Personne qui ferme"),
    }),
    ("t", "d", "Temps / Début & Commencement", {
        'a': ("début, commencement, départ, aube, genèse", "beginning, start, inception, dawn", "Point initial d'un processus"),
        'i': ("commencer, débuter, initier, amorcer", "to begin, to start, to commence, to initiate", "Entrer dans un processus"),
        'u': ("initial, commençant, débutant, naissant", "initial, starting, beginner, nascent", "Au commencement"),
        'o': ("ligne de départ, case initiale", "starting line, origin point", "Lieu où l'on débute"),
        'e': ("débutant, initiateur, pionnier", "beginner, starter, initiator", "Personne qui commence"),
    }),
    ("t", "d", "Temps / Fin & Terme", {
        'a': ("fin, conclusion, terme, arrêt, épilogue", "end, finish, conclusion, epilogue", "Point final d'un processus"),
        'i': ("finir, terminer, achever, conclure, cesser", "to end, to finish, to complete, to conclude", "Parvenir au terme"),
        'u': ("final, achevé, terminé, conclu", "final, finished, complete, completed", "Qui est arrivé au bout"),
        'o': ("ligne d'arrivée, point de chute", "finish line, endpoint", "Lieu du terme"),
        'e': ("finisseur, acheveur", "finisher, completer", "Personne qui achève"),
    }),
    ("t", "d", "Temps / Attente & Patience", {
        'a': ("attente, veille, patience, expectation", "waiting, wait, expectation, patience", "Action de patienter"),
        'i': ("attendre, patienter, espérer, guetter", "to wait, to wait for, to await, to expect", "Rester en attente"),
        'u': ("attentif, patient, expectant", "waiting, patient, expectant", "Qui attend avec calme"),
        'o': ("salle d'attente, quai d'attente", "waiting room, lounge", "Lieu où l'on attend"),
        'e': ("personne en attente, guetteur", "waiter, expectant person", "Personne qui attend"),
    }),
    ("sh", "zh", "Abstraction / Espérance & Vœu", {
        'a': ("espoir, espérance, souhait, vœu, aspiration", "hope, wish, expectation, aspiration", "Attente confiante d'un bien"),
        'i': ("espérer, souhaiter, aspirer, avoir espoir", "to hope, to wish, to aspire", "Vouloir avec confiance"),
        'u': ("plein d'espoir, confiant, optimiste", "hopeful, optimistic, promising", "Animé par l'espoir"),
        'o': ("temple de l'espoir, sanctuaire des vœux", "haven of hope, wishing well", "Lieu où l'on espère"),
        'e': ("optimiste, espéreur, croyant", "hoper, optimist", "Personne qui espère"),
    }),
    ("m", "n", "Humain / Entraide & Secours", {
        'a': ("aide, assistance, secours, soutien, appui", "help, aid, assistance, support, rescue", "Action de prêter main-forte"),
        'i': ("aider, assister, secourir, soutenir", "to help, to assist, to aid, to support", "Donner de sa force à autrui"),
        'u': ("secourable, aidant, bienveillant, utile", "helpful, assisting, supportive", "Qui apporte de l'aide"),
        'o': ("poste de secours, centre d'entraide", "aid station, relief center", "Lieu de l'assistance"),
        'e': ("aidant, secouriste, sauveteur, bienfaiteur", "helper, assistant, rescuer", "Personne qui apporte son aide"),
    }),
    ("j", "ch", "Outil / Propreté & Nettoyage", {
        'a': ("lavage, nettoyage, propreté, lessive", "cleaning, washing, cleanse, laundry", "Action d'enlever la souillure"),
        'i': ("laver, nettoyer, purifier, frotter", "to wash, to clean, to cleanse, to scrub", "Rendre propre"),
        'u': ("propre, lavé, net, nettoyé, pur", "clean, washed, neat, pure", "Sans salissure"),
        'o': ("lavoir, buanderie, station de lavage", "washhouse, laundry room, carwash", "Lieu où l'on lave"),
        'e': ("laveur, nettoyeur, agent d'entretien", "cleaner, washer", "Personne qui nettoie"),
    }),
    ("j", "ch", "Outil / Réparation & Restauration", {
        'a': ("réparation, raccommodage, dépannage, remise en état", "repair, fixing, mending, restoration", "Action de remettre en état"),
        'i': ("réparer, dépanner, raccommoder, restaurer", "to repair, to fix, to mend, to restore", "Remettre en bon état"),
        'u': ("réparé, remis en état, dépanné", "repaired, fixed, mended", "Qui fonctionne à nouveau"),
        'o': ("atelier de réparation, garage de dépannage", "repair shop, workshop", "Lieu des réparations"),
        'e': ("réparateur, mécanicien, dépanneur", "repairer, fixer, mechanic", "Personne qui répare"),
    }),
    ("j", "ch", "Outil / Construction & Bâtiment", {
        'a': ("construction, bâtisse, édification, ouvrage", "construction, building, erection, structure", "Action de bâtir un ouvrage"),
        'i': ("construire, bâtir, édifier, ériger", "to build, to construct, to erect", "Assembler pour faire un édifice"),
        'u': ("construit, bâti, solide en œuvre", "built, constructed, structural", "Qui est édifié"),
        'o': ("chantier de construction, maçonnerie", "construction site, worksite", "Lieu où l'on bâtit"),
        'e': ("bâtisseur, constructeur, maçon", "builder, constructor, mason", "Personne qui bâtit"),
    }),

    # --- ÉLÉMENTS DU FOYER, MEUBLES & VAISSELLE ---
    ("k", "g", "Espace / Objet & Verre (Récipient)", {
        'a': ("verre, gobelet, calice, coupe à boire", "glass, tumbler, drinking glass, goblet", "Récipient pour boire un liquide"),
        'i': ("verser dans un verre, trinquer", "to pour into glass, to toast", "Utiliser un verre"),
        'u': ("en verre, vitreux, limpide", "glass, vitreous, glassy", "Transparent comme le verre"),
        'o': ("vaisselier à verres, buffet de verres", "glass cabinet, glassware shelf", "Lieu des verres"),
        'e': ("verrier, sommelier verseur", "glassmaker, pourer", "Spécialiste du verre"),
    }),
    ("k", "g", "Espace / Objet & Tasse / Bol", {
        'a': ("tasse, bol, mug, chope", "cup, mug, bowl, teacup", "Petit récipient chaud avec anse"),
        'i': ("servir en tasse, siroter", "to serve in a cup, to sip from cup", "Prendre en tasse"),
        'u': ("en tasse, à anse", "cup-like, cupped", "Propre à la tasse"),
        'o': ("plateau à tasses, étagère à bols", "cup tray, tea shelf", "Lieu des tasses"),
        'e': ("verseur de thé, cafetier", "tea server", "Personne qui sert les tasses"),
    }),
    ("k", "g", "Espace / Objet & Assiette / Plat", {
        'a': ("assiette, plat, écuelle, soucoupe", "plate, dish, saucer, platter", "Récipient plat pour les mets"),
        'i': ("dresser sur l'assiette, servir en plat", "to plate, to dish up, to serve on plate", "Mettre dans l'assiette"),
        'u': ("plat, en assiette, étalé", "plated, dish-shaped, flat", "Posé dans l'assiette"),
        'o': ("vaisselier d'assiettes, dressoir", "dish rack, plate cupboard", "Lieu des assiettes"),
        'e': ("dresseur de plats, plongeur d'assiettes", "plater, dishwasher", "Personne gérant les assiettes"),
    }),
    ("k", "g", "Espace / Objet & Bouteille / Flacon", {
        'a': ("bouteille, flacon, carafe, fiole", "bottle, flask, carafe, vial", "Récipient cylindrique à goulot"),
        'i': ("embouteiller, verser de la bouteille", "to bottle, to decant", "Mettre en bouteille"),
        'u': ("embouteillé, en bouteille", "bottled, flask-shaped", "En bouteille"),
        'o': ("cave à bouteilles, casier à vin", "wine cellar, bottle rack", "Lieu des bouteilles"),
        'e': ("embouteilleur, caviste", "bottler, cellar master", "Personne gérant les bouteilles"),
    }),
    ("j", "ch", "Outil / Mobilier & Chaise", {
        'a': ("chaise, siège, tabouret, fauteuil, banc", "chair, seat, stool, armchair, bench", "Meuble prévu pour s'asseoir"),
        'i': ("s'asseoir sur une chaise, installer en siège", "to sit on a chair, to seat", "Prendre place sur un siège"),
        'u': ("assis, installé, de chaise", "seated, sitting, chair-like", "En position assise"),
        'o': ("salle des chaises, rangée de sièges", "seating area, rows of chairs", "Lieu où sont les sièges"),
        'e': ("personne assise, maître de chaises", "seated person, chairmaker", "Personne assise"),
    }),
    ("j", "ch", "Outil / Mobilier & Lit / Couchette", {
        'a': ("lit, couchette, sommier, paillasse", "bed, cot, bunk, mattress", "Meuble pour dormir et reposer"),
        'i': ("border le lit, aliter, coucher", "to bed down, to tuck in, to rest in bed", "Se mettre au lit"),
        'u': ("alité, de lit, couché au lit", "bedridden, in bed, bed-bound", "Dans le lit"),
        'o': ("chambre à coucher, dortoir", "bedroom, bedchamber, dormitory", "Lieu des lits"),
        'e': ("dormeur au lit, fabricant de lits", "bedmaker, sleeper", "Personne au lit"),
    }),
    ("j", "ch", "Outil / Bâtiment & Fenêtre", {
        'a': ("fenêtre, vitre, ouverture vitrée, lucarne", "window, casement, pane, skylight", "Baie vitrée donnant jour et air"),
        'i': ("ouvrir la fenêtre, vitrer", "to glaze, to open window", "Donner du jour par la fenêtre"),
        'u': ("vitré, fenêtré, ouvrant au jour", "windowed, glazed", "Muni d'une fenêtre"),
        'o': ("rebord de fenêtre, baie vitrée", "windowsill, window bay", "Emplacement de la fenêtre"),
        'e': ("vitrier, poseur de fenêtres", "glazier, window installer", "Artisan des fenêtres"),
    }),
    ("j", "ch", "Outil / Bâtiment & Porte", {
        'a': ("porte, vantail, battant, portail, entrée", "door, gate, portal, doorway", "Panneau fermant un passage"),
        'i': ("fermer la porte, franchir la porte", "to door, to pass the doorway", "Passer la porte"),
        'u': ("portier, de porte, à battant", "doored, gated", "Relatif à la porte"),
        'o': ("encadrement de porte, sas d'entrée", "doorframe, entryway", "Lieu de la porte"),
        'e': ("portier, concierge, gardien de porte", "doorkeeper, porter, gatekeeper", "Gardien de la porte"),
    }),
    ("j", "ch", "Outil / Serrurerie & Clé", {
        'a': ("clé, clef, passe-partout, sésame", "key, master key, latchkey", "Instrument ouvrant une serrure"),
        'i': ("fermer à clé, déverrouiller à clé", "to lock with key, to unlock with key", "Actionner la serrure par clé"),
        'u': ("fermé à clé, muni de clé", "keyed, key-operated, locked", "Commandé par clé"),
        'o': ("trousseau de clés, boîte à clés", "keyring, key box", "Lieu de rangement des clés"),
        'e': ("porte-clé, serrurier", "keyholder, locksmith", "Gardien des clés"),
    }),
    ("k", "g", "Espace / Bâtiment & Mur", {
        'a': ("mur, paroi, muraille, cloison", "wall, partition, rampart, barrier", "Ouvrage vertical de maçonnerie"),
        'i': ("murer, cloisonner, dresser un mur", "to wall, to partition, to erect wall", "Élever une paroi"),
        'u': ("mural, cloisonné, de muraille", "mural, walled, partition-like", "Relatif aux murs"),
        'o': ("enceinte de murs, muraille de ville", "walled enclosure, rampart", "Espace clos de murs"),
        'e': ("maçon de murs, murailler", "wall builder, mason", "Personne dressant les murs"),
    }),
    ("k", "g", "Espace / Bâtiment & Toit", {
        'a': ("toit, toiture, comble, couverture", "roof, rooftop, ceiling cover, canopy", "Couverture supérieure d'un édifice"),
        'i': ("toiter, couvrir un toit, abriter sous toit", "to roof, to shelter under roof", "Poser la toiture"),
        'u': ("sous toit, couvert, toité", "roofed, sheltered under roof", "Abrité par le toit"),
        'o': ("grenier, comble sous le toit", "attic, loft, rooftop terrace", "Lieu sous le toit"),
        'e': ("couvreur, charpentier de toit", "roofer, rooffitter", "Artisan du toit"),
    }),
    ("k", "g", "Espace / Objet & Montre / Horloge", {
        'a': ("montre, montre-bracelet, horloge, chronomètre", "watch, wristwatch, timepiece, clock", "Appareil mesurant l'heure"),
        'i': ("donner l'heure, chronométrer, mesurer le temps", "to tell time, to clock, to time", "Indiquer l'heure exacte"),
        'u': ("horloger, ponctuel, à l'heure", "punctual, horological, on time", "Réglé comme une montre"),
        'o': ("boîtier de montre, cadran d'horloge", "watchcase, clock tower", "Lieu de l'horloge"),
        'e': ("horloger, maître du temps", "watchmaker, clockmaker", "Artisan des montres"),
    }),

    # --- VÊTEMENTS & APPARENCE ---
    ("k", "g", "Espace / Vêtement & Habit", {
        'a': ("vêtement, habit, tenue, parure, costume", "clothing, garment, attire, dress, suit", "Élément couvrant le corps humain"),
        'i': ("vêtir, habiller, porter un vêtement, parer", "to dress, to clothe, to wear, to attire", "Mettre un vêtement"),
        'u': ("vêtu, habillé, paré, costumé", "dressed, clothed, suited, clad", "Portant vêtement"),
        'o': ("penderie, garde-robe, dressing", "wardrobe, closet, clothes rack", "Lieu où l'on range les habits"),
        'e': ("habilleur, couturier, tailleur", "tailor, dressmaker, clothier", "Créateur de vêtements"),
    }),
    ("k", "g", "Espace / Vêtement & Chaussure", {
        'a': ("chaussure, soulier, botte, sandale, bottine", "shoe, boot, footwear, sandal, sneaker", "Protection du pied pour marcher"),
        'i': ("chausser, mettre des souliers, lacer", "to shoe, to put shoes on, to lace up", "Porter aux pieds"),
        'u': ("chaussé, botté, ferré aux pieds", "shod, booted, with shoes", "Portant des chaussures"),
        'o': ("meuble à chaussures, cordonnerie", "shoe rack, shoe store, cobbler shop", "Lieu des souliers"),
        'e': ("cordonnier, chausseur", "shoemaker, cobbler", "Artisan des chaussures"),
    }),
    ("k", "g", "Espace / Vêtement & Manteau", {
        'a': ("manteau, veste, pardessus, cape, anorak", "coat, jacket, overcoat, cloak, mantle", "Vêtement chaud porté par-dessus"),
        'i': ("endosser un manteau, boutonner la veste", "to coat, to put on a jacket, to wrap up", "Mettre son manteau"),
        'u': ("en manteau, emmitouflé, abrité du froid", "coated, warm-clad, wrapped up", "Protégé du froid"),
        'o': ("porte-manteau, vestiaire", "coat rack, cloakroom", "Lieu où l'on suspend le manteau"),
        'e': ("vestiaire, gardien de manteaux", "cloakroom attendant", "Gardien du vestiaire"),
    }),

    # --- GÉOGRAPHIE, EAUX & PAYSAGE ---
    ("k", "g", "Espace / Géographie & Rivière", {
        'a': ("rivière, cours d'eau, fleuve, ruisseau, flot", "river, stream, creek, brook, waterway", "Cours d'eau continu naturel"),
        'i': ("couler en rivière, serpenter, ruisseler", "to flow as river, to stream, to meander", "Suivre le lit de l'eau"),
        'u': ("fluvial, riverain, fluvialisé", "river, riverine, fluvial, riparian", "Lié à la rivière"),
        'o': ("berges de la rivière, vallée fluviale, lit", "riverbank, riverbed, stream valley", "Abords de la rivière"),
        'e': ("batelier de rivière, pêcheur d'eau douce", "riverman, freshwater fisherman", "Habitant de la rivière"),
    }),
    ("k", "g", "Espace / Géographie & Pont", {
        'a': ("pont, viaduc, passerelle, arche", "bridge, overpass, footbridge, viaduct", "Ouvrage franchissant un obstacle d'eau"),
        'i': ("enjamber, franchir par un pont, ponter", "to bridge, to span, to cross over", "Relier les deux rives"),
        'u': ("suspendu, en pont, reliant les rives", "bridged, spanned, overpass", "Franchissant l'abîme"),
        'o': ("tête de pont, arche de traversée", "bridgehead, bridge pier", "Lieu du pont"),
        'e': ("gardien de pont, bâtisseur d'arches", "bridge keeper, bridge builder", "Surveillant du pont"),
    }),
    ("k", "g", "Espace / Géographie & Mer", {
        'a': ("mer, océan, flot salé, vaste étendue marine", "sea, ocean, brine, marine expanse", "Vaste étendue d'eau salée"),
        'i': ("naviguer en mer, prendre la mer, voguer", "to take to sea, to sail the ocean", "Aller sur la mer"),
        'u': ("marin, maritime, océanique, salin", "marine, oceanic, sea, maritime", "Relatif à la mer"),
        'o': ("grand large, côte maritime, rivage salé", "open sea, ocean coast, seaside", "Domaine de la mer"),
        'e': ("marin, navigateur, loup de mer", "sailor, seaman, mariner", "Homme de mer"),
    }),
    ("k", "g", "Espace / Géographie & Montagne", {
        'a': ("montagne, mont, sommet, cime, crête", "mountain, mount, peak, summit, ridge", "Grand relief rocheux terrestre"),
        'i': ("gravir la montagne, culminer, s'élever", "to climb mountains, to peak, to scale", "S'élever vers les cimes"),
        'u': ("montagneux, alpin, escarpé, rocheux", "mountainous, alpine, craggy, steep", "Couvert de montagnes"),
        'o': ("massif montagneux, chaîne de montagnes", "mountain range, mountain realm", "Région de montagnes"),
        'e': ("alpiniste, montagnard, guide de haute cime", "mountaineer, alpine guide", "Personne de la montagne"),
    }),
    ("k", "g", "Espace / Géographie & Colline", {
        'a': ("colline, tertre, vallonnement, monticule", "hill, knoll, mound, hillock, slope", "Relief modéré et arrondi"),
        'i': ("onduler en colline, gravir le tertre", "to roll in hills, to ascend the knoll", "Former un doux relief"),
        'u': ("vallonné, de colline, ondulant", "hilly, rolling, undulating", "Semé de collines"),
        'o': ("flanc de colline, coteau", "hillslope, hillside", "Pente de la colline"),
        'e': ("gardien de coteau, vigneron de colline", "hillside dweller", "Habitant de la colline"),
    }),

    # --- MÉTÉOROLOGIE & CIEL ---
    ("g", "k", "Espace / Météo & Nuage", {
        'a': ("nuage, nuée, brume d'altitude, cumulus", "cloud, cumulus, cloud bank, overcast", "Vapeur d'eau condensée dans le ciel"),
        'i': ("s'ennuager, voiler le ciel de nuages", "to cloud over, to overcast", "Former des nuages"),
        'u': ("nuageux, couvert, voilé, brumeux", "cloudy, overcast, cloud-covered", "Rempli de nuages"),
        'o': ("mer de nuages, ciel couvert", "cloud bank, overcast sky", "Région nuageuse"),
        'e': ("observateur des nuages, songeur céleste", "cloud watcher", "Personne observant les nuages"),
    }),
    ("g", "k", "Espace / Météo & Neige", {
        'a': ("neige, flocon, poudreuse, manteau blanc", "snow, snowflake, snowfall, white blanket", "Eau cristallisée tombant du ciel"),
        'i': ("neiger, tomber en flocons, blanchir", "to snow, to blanket in white", "Tomber en neige"),
        'u': ("neigeux, enneigé, poudreux, blanc de neige", "snowy, snow-covered, powdered", "Couvert de neige"),
        'o': ("champ de neige, champ de poudreuse", "snowfield, snowdrift", "Étendue de neige"),
        'e': ("bonhomme de neige, skieur de poudreuse", "snowman, skier", "Créature des neiges"),
    }),
    ("g", "k", "Espace / Météo & Vent", {
        'a': ("vent, brise, souffle, rafale, zéphyr", "wind, breeze, gust, gale, air blast", "Mouvement d'air atmosphérique"),
        'i': ("venter, souffler, bruire en rafales", "to blow, to breeze, to gust", "Créer un souffle d'air"),
        'u': ("venteux, battu des vents, venteux", "windy, breezy, gusty", "Balayé par le vent"),
        'o': ("couloir de vent, plateau venteux", "wind tunnel, windy ridge", "Lieu exposé au vent"),
        'e': ("oiseau des tempêtes, planeur des vents", "wind flyer", "Être porté par le vent"),
    }),
    ("g", "k", "Espace / Météo & Pluie", {
        'a': ("pluie, ondée, averse, goutte d'eau", "rain, shower, downpour, raindrop", "Précipitation d'eau liquide"),
        'i': ("pleuvoir, bruiner, tomber en pluie", "to rain, to pour, to drizzle", "Tomber du ciel en liquide"),
        'u': ("pluvieux, arrosé, humide de pluie", "rainy, rainy-wet, drizzly", "Marqué par la pluie"),
        'o': ("flaque d'eau, cuvette pluviale", "rain puddle, rain gauge", "Lieu où s'accumule la pluie"),
        'e': ("amoureux de la pluie, parapluie", "rain lover, umbrella user", "Personne sous la pluie"),
    }),

    # --- NOURRITURE, BOISSON & SAVEURS ---
    ("k", "g", "Espace / Nourriture & Eau (Boisson)", {
        'a': ("eau, eau pure, onde limpide, eau potable", "water, pure water, clear drinking water", "Liquide vital incolore et inodore"),
        'i': ("abreuver, hydrater, désaltérer, boire de l'eau", "to water, to hydrate, to quench with water", "Fournir de l'eau"),
        'u': ("aqueux, hydraté, limpide comme l'eau", "watery, aqueous, hydrated, aquatic", "Fait d'eau"),
        'o': ("fontaine d'eau, puits d'eau pure, source", "water spring, drinking fountain, well", "Source d'eau potable"),
        'e': ("porteur d'eau, buveur d'eau", "water bearer, water drinker", "Personne versant l'eau"),
    }),
    ("k", "g", "Espace / Nourriture & Pain (Nourriture de base)", {
        'a': ("pain, miche, baguette, aliment de base", "bread, loaf, baguette, staple food", "Nourriture de céréale cuite au four"),
        'i': ("panifier, cuire le pain, rompre le pain", "to bake bread, to break bread", "Faire ou manger du pain"),
        'u': ("pain, boulanger, levé", "bread-like, bready, baked", "Relatif au pain"),
        'o': ("boulangerie, four à pain", "bakery, bakehouse, bread oven", "Lieu où l'on cuit le pain"),
        'e': ("boulanger, mitron, pétrisseur", "baker, breadmaker", "Artisan du pain"),
    }),
    ("k", "g", "Espace / Nourriture & Sel / Condiment", {
        'a': ("sel, sel de mer, sapidité saline", "salt, sea salt, table salt, salinity", "Minéral salé conservateur et assaisonnement"),
        'i': ("saler, assaisonner de sel, conserver au sel", "to salt, to season with salt", "Mettre du sel"),
        'u': ("salé, iodé, savoureux de sel", "salty, salted, saline, briny", "Qui a la saveur du sel"),
        'o': ("salière, marais salant", "salt shaker, salt marsh", "Lieu du sel"),
        'e': ("paludier, saunier", "salt worker, salt gatherer", "Récolteur de sel"),
    }),
    ("k", "g", "Espace / Nourriture & Sucre / Douceur", {
        'a': ("sucre, douceur, friandise, miel doux", "sugar, sweetness, candy, sweet treat", "Substance douce et sucrée"),
        'i': ("sucrer, adoucir au sucre, confire", "to sweeten, to sugar, to candy", "Mettre du sucre"),
        'u': ("sucré, doux, miellé, suave", "sweet, sugary, candied, honeyed", "Qui a la saveur sucrée"),
        'o': ("sucrier, confiserie", "sugar bowl, candy shop", "Lieu du sucre"),
        'e': ("confiseur, pâtissier", "confectioner, candymaker", "Artisan des douceurs"),
    }),

    # --- ADJECTIFS & QUALITÉS INDISPENSABLES ---
    ("s", "z", "Sensation / Esthétique & Beauté", {
        'a': ("beauté, magnificence, splendeur, charme", "beauty, magnificence, loveliness, splendor", "Qualité de ce qui plaît au regard"),
        'i': ("embellir, parer de beauté, rayonner de beauté", "to beautify, to adorn, to radiate beauty", "Rendre beau"),
        'u': ("beau, belle, magnifique, joli, splendide", "beautiful, handsome, lovely, pretty, fine", "Agréable et splendide à voir"),
        'o': ("écrin de beauté, musée des beaux-arts", "haven of beauty, art palace", "Lieu de la beauté"),
        'e': ("être de beauté, artiste de l'élégance", "beautiful soul, artist of grace", "Personne belle"),
    }),
    ("s", "z", "Sensation / Esthétique & Laideur", {
        'a': ("laideur, difformité, hideur, disgrâce", "ugliness, deformity, hideousness", "Caractère de ce qui choque le regard"),
        'i': ("enlaidir, gâcher l'aspect, défigurer", "to uglify, to disfigure, to mar", "Rendre laid"),
        'u': ("laid, laide, vilain, hideux, disgracieux", "ugly, unsightly, hideous, plain", "Désagréable au regard"),
        'o': ("cloaque hideux, terrain difforme", "ugly corner, wasteland", "Lieu sans beauté"),
        'e': ("être disgracié, monstre difforme", "ugly creature", "Être laid"),
    }),
    ("s", "z", "Sensation / Température & Chaleur", {
        'a': ("chaleur, tiédeur, ardeur, canicule", "heat, warmth, hotness, fiery heat", "Température élevée"),
        'i': ("chauffer, réchauffer, tiédir, embraser", "to heat, to warm, to heat up", "Élever la température"),
        'u': ("chaud, brûlant, ardent, caniculaire", "hot, warm, fiery, heated", "Qui a une température élevée"),
        'o': ("foyer chaud, poêle à bois, sauna", "hearth, warm room, sauna", "Lieu où il fait chaud"),
        'e': ("chauffeur, être chaleureux", "heater, warm presence", "Être qui chauffe"),
    }),
    ("s", "z", "Sensation / Température & Froid", {
        'a': ("froid, gel, froidure, frisson, glace", "cold, coldness, chill, frost, freeze", "Basse température"),
        'i': ("refroidir, glacer, grelotter de froid", "to cool, to chill, to freeze", "Abaisser la température"),
        'u': ("froid, glacial, frisquet, gelé", "cold, freezing, chilly, icy, frosty", "Qui a une basse température"),
        'o': ("glacière, chambre froide, banquise", "icebox, cold room, ice field", "Lieu où il fait froid"),
        'e': ("être frileux, bonhomme de gel", "cold dweller", "Personne exposée au froid"),
    }),
    ("l", "r", "Mouvement / Vélocité & Vitesse", {
        'a': ("vitesse, rapidité, célérité, hâte", "speed, swiftness, quickness, velocity, haste", "Grande vélocité de déplacement"),
        'i': ("accélérer, hâter, foncer, aller vite", "to speed, to hasten, to accelerate, to hurry", "Aller à grande vitesse"),
        'u': ("rapide, vite, prompt, véloce, hâtif", "fast, quick, swift, rapid, speedy", "Qui va vite"),
        'o': ("piste de vitesse, anneau de course", "speedway, race track", "Lieu où l'on va vite"),
        'e': ("sprinteur, bolide, être rapide", "sprinter, racer", "Personne rapide"),
    }),
    ("l", "r", "Mouvement / Vélocité & Lenteur", {
        'a': ("lenteur, pondération, calme, modération", "slowness, leisure, deliberation", "Faible vélocité de déplacement"),
        'i': ("ralentir, temporiser, aller lentement", "to slow down, to decelerate, to linger", "Aller avec lenteur"),
        'u': ("lent, posé, tranquille, lambin", "slow, leisurely, unhurried, calm", "Qui va lentement"),
        'o': ("zone ralentie, chemin tranquille", "slow zone, peaceful path", "Lieu où l'on va lentement"),
        'e': ("être lent, promeneur posé", "slow mover, stroller", "Personne lente"),
    }),
    ("k", "g", "Espace / Dimension & Petitesse", {
        'a': ("petitesse, miniature, menu détail, miette", "smallness, littleness, miniature, bit", "Faible dimension physique"),
        'i': ("rapetisser, amenuiser, réduire la taille", "to shrink, to lessen, to miniaturize", "Rendre plus petit"),
        'u': ("petit, menu, minuscule, ténu, bref", "small, little, tiny, minute, petty", "De faible taille"),
        'o': ("maison miniature, boîte à bijoux", "miniature home, tiny box", "Lieu tout petit"),
        'e': ("lutin, être menu, enfant en bas âge", "little one, tiny being, toddler", "Personne de petite taille"),
    }),
    ("p", "b", "Quantité / Pesanteur & Poids lourd", {
        'a': ("lourdeur, pesanteur, gravité, poids lourd", "heaviness, weightiness, ponderousness", "Grande masse matérielle"),
        'i': ("peser lourd, alourdir, charger", "to weigh heavy, to burden, to weigh down", "Avoir une masse élevée"),
        'u': ("lourd, pesant, massif, chargé", "heavy, weighty, ponderous, massive", "Qui pèse beaucoup"),
        'o': ("dépôt de fonte, quai de poids lourds", "heavy yard, freight dock", "Lieu des objets lourds"),
        'e': ("haltérophile, colosse au portage", "weightlifter, heavy lifter", "Personne robuste"),
    }),
    ("p", "b", "Quantité / Pesanteur & Légèreté", {
        'a': ("légèreté, plume, apesanteur, délicatesse", "lightness, feather, weightlessness", "Faible masse matérielle"),
        'i': ("alléger, planer sans poids, soulager", "to lighten, to unburden, to float lightly", "Avoir peu de masse"),
        'u': ("léger, aérien, plumeux, délesté", "light, lightweight, airy, featherlight", "Qui pèse peu"),
        'o': ("coussin d'air, chambre d'apesanteur", "air cushion, zero-g chamber", "Lieu de la légèreté"),
        'e': ("danseur aérien, funambule léger", "aerial dancer, tightrope walker", "Personne légère"),
    }),
    ("sh", "zh", "Abstraction / Complexité & Facilité", {
        'a': ("facilité, aisance, simplicité, évidence", "ease, facility, simplicity, effortless deed", "Ce qui s'accomplit sans effort"),
        'i': ("faciliter, rendre aisé, simplifier", "to facilitate, to ease, to simplify", "Rendre plus simple"),
        'u': ("facile, aisé, simple, sans peine", "easy, simple, effortless, smooth", "Qui s'accomplit aisément"),
        'o': ("voie facile, terrain plat", "easy path, smooth ground", "Cadre propice sans effort"),
        'e': ("praticien aisé, virtuose de la simplicité", "easy master", "Personne à qui tout réussit"),
    }),
    ("sh", "zh", "Abstraction / Complexité & Difficulté", {
        'a': ("difficulté, épreuve, ardeur, obstacle", "difficulty, hardship, trial, struggle", "Ce qui demande un rude effort"),
        'i': ("éprouver, compliquer, rendre difficile", "to complicate, to present hardship", "Demander un lourd labeur"),
        'u': ("difficile, ardu, pénible, dur, exigeant", "difficult, hard, arduous, demanding, tough", "Qui demande beaucoup d'efforts"),
        'o': ("passe difficile, champ d'épreuves", "hard pass, obstacle course", "Lieu de rude épreuve"),
        'e': ("vainqueur des épreuves, travailleur acharné", "hardship conqueror, trier", "Personne bravant l'épreuve"),
    }),
    ("t", "d", "Temps / Âge & Jeunesse", {
        'a': ("jeunesse, fraîcheur d'âge, adolescence", "youth, youthfulness, young age", "Période initiale de la vie"),
        'i': ("rajeunir, fleurir en jeunesse", "to rejuvenate, to bloom young", "Être au matin de la vie"),
        'u': ("jeune, adolescent, juvénile, frais", "young, youthful, juvenile, youthful", "Qui a peu d'années"),
        'o': ("cour des jeunes, maison de jeunesse", "youth center, young grove", "Lieu de la jeunesse"),
        'e': ("jeune homme, jeune fille, adolescent", "youth, young person, youngster", "Personne jeune"),
    }),
    ("t", "d", "Temps / Âge & Vieillesse", {
        'a': ("vieillesse, grand âge, séniorité, maturité", "old age, elderhood, senior years", "Période avancée de la vie"),
        'i': ("vieillir, prendre de l'âge, mûrir", "to age, to grow old, to mature", "Avancer en âge"),
        'u': ("vieux, vieille, âgé, ancien, chenu", "old, aged, elderly, ancient", "Qui a beaucoup d'années"),
        'o': ("foyer des anciens, maison de sagesse", "elders hall, retirement haven", "Lieu des aînés"),
        'e': ("vieillard, aîné, vétéran, ancien", "elder, old man, old woman, senior", "Personne âgée"),
    }),
    ("t", "d", "Temps / Évolution & Nouveauté", {
        'a': ("nouveauté, fraîcheur, innovation, primeur", "novelty, newness, freshness, innovation", "Ce qui vient d'apparaître"),
        'i': ("renouveler, innover, inaugurer du neuf", "to renew, to innovate, to freshen", "Produire du neuf"),
        'u': ("nouveau, nouvelle, neuf, neufve, inédit", "new, novel, fresh, brand new, unreleased", "Qui est récent"),
        'o': ("salle des nouveautés, galerie de première", "novelty gallery, premiere room", "Lieu où paraît le neuf"),
        'e': ("innovateur, créateur de renouveau", "innovator, novelty creator", "Créateur de nouveautés"),
    }),
    ("t", "d", "Temps / Histoire & Ancienneté", {
        'a': ("ancienneté, antiquité, temps révolu, mémoire", "antiquity, ancientness, olden times", "Ce qui remonte au passé lointain"),
        'i': ("remonter aux temps anciens, patiner", "to date back, to age with patina", "Avoir une longue histoire"),
        'u': ("ancien, antique, séculaire, vétuste", "ancient, antique, historic, olden", "Qui date d'antan"),
        'o': ("musée des antiquités, ruines vénérables", "antiquities museum, historic ruins", "Lieu de l'antique"),
        'e': ("historien, antiquaire, conservateur", "historian, antiquarian", "Spécialiste de l'ancien"),
    }),
]

assigned_families = []
for pref_c1, alt_c1, dom, roles in RAW_FAMILIES:
    c1, c2, v2 = allocate_slot(pref_c1, alt_c1)
    assigned_families.append((c1, c2, v2, dom, roles))
    print(f"Allocated: ({c1}, {c2}, {v2}) for {dom}")

print(f"\nSuccessfully allocated {len(assigned_families)} new families!")

# Serialize to scripts/families_expansion_part4.py
def serialize_family(fam):
    c1, c2, v2, dom, roles = fam
    lines = [f"    ('{c1}', '{c2}', '{v2}', {repr(dom)}, {{"]
    for role_v in ['a', 'i', 'u', 'o', 'e']:
        if role_v in roles:
            fr, en, sem = roles[role_v]
            lines.append(f"        '{role_v}': ({repr(fr)}, {repr(en)}, {repr(sem)}),")
    lines.append("    }),")
    return "\n".join(lines)

out_path = ROOT_DIR / "scripts" / "families_expansion_part4.py"
header = '"""Lumina Semantic Families Expansion Part 4: Everyday life, actions, objects, nature, food, adjectives.\nAuto-generated and collision-free C1-V1-C2-V2 matrix.\n"""\n\nFAMILIES_EXPANSION_PART4 = [\n'
body = "\n".join(serialize_family(fam) for fam in assigned_families)
footer = "\n]\n"
out_path.write_text(header + body + footer, encoding="utf-8")
print(f"Wrote {len(assigned_families)} families to scripts/families_expansion_part4.py.")
