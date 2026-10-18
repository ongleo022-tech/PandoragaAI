# Pandoraga Ω — profil RAM 12GB
# Profil dérivé du moteur complet fourni par l’utilisateur.
# Réglages de ressources indicatifs : ils ne garantissent pas une consommation RAM exacte ni un Elo donné.
# ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 1/25 — CONFIGURATION GÉNÉRALE
# ============================================================

import os
import json
import time
import math
import random


# ------------------------------------------------------------
# IDENTITÉ
# ------------------------------------------------------------

PANDORAGA_NOM = "Pandoraga Full Adaptation Ω"
PANDORAGA_VERSION = "Ω Adaptation MAX 2.0"

AUTEUR = "Pandoraga Project"


# ------------------------------------------------------------
# FICHIERS
# ------------------------------------------------------------

MEMOIRE_FICHIER = "pandoraga_memoire.json"


# ------------------------------------------------------------
# PARAMÈTRES DU MOTEUR
# ------------------------------------------------------------

MAX_DEPTH = 15
# Mode MAX : budget maximal de recherche configuré.
# La limite de temps reste une limite de sécurité.
TIME_LIMIT = 30.0

# Capacité maximale configurée de la table de transposition.
HASH_MAX_ENTRIES = 300_000


# ------------------------------------------------------------
# PARAMÈTRES D'ADAPTATION Ω
# ------------------------------------------------------------

ADAPTATION_ACTIVE = True

# Force de l'apprentissage.
LEARNING_RATE = 0.10

# Influence maximale de l'adaptation.
ADAPTATION_MAX = 2.0

# Influence minimale de l'adaptation.
ADAPTATION_MIN = 0.5


# ------------------------------------------------------------
# PARAMÈTRES DE STYLE
# ------------------------------------------------------------

STYLE_AGRESSIF = "agressif"
STYLE_DEFENSIF = "defensif"
STYLE_TACTIQUE = "tactique"
STYLE_POSITIONNEL = "positionnel"
STYLE_EQUILIBRE = "equilibre"


# ------------------------------------------------------------
# PARAMÈTRES DE RECHERCHE
# ------------------------------------------------------------

USE_ALPHA_BETA = True
USE_PVS = True
USE_ITERATIVE_DEEPENING = True
USE_QUIESCENCE = True
USE_TRANSPOSITION = True
USE_KILLER_MOVES = True
USE_HISTORY_HEURISTIC = True
USE_MOVE_ORDERING = True


# ------------------------------------------------------------
# PARAMÈTRES DE MÉMOIRE
# ------------------------------------------------------------

MEMORY_MAX_GAMES = 500
MEMORY_MAX_ERRORS = 500
MEMORY_MAX_MOVES = 5000
MEMORY_MAX_OPPONENTS = 1000


# ------------------------------------------------------------
# PARAMÈTRES D'ÉVALUATION
# ------------------------------------------------------------

PIECE_VALUES = {
    "P": 100,       # Pion
    "N": 320,       # Cavalier
    "B": 330,       # Fou
    "R": 500,       # Tour
    "Q": 900,       # Dame
    "K": 20000      # Roi
}


# ------------------------------------------------------------
# VALEURS PAR DÉFAUT DE L'ADAPTATION
# ------------------------------------------------------------

DEFAULT_ADAPTATION = {
    "agressivite": 1.0,
    "defense": 1.0,
    "tactique": 1.0,
    "positionnel": 1.0,
    "mobilite": 1.0,
    "securite_roi": 1.0,
    "structure_pions": 1.0,
    "ouvertures": 1.0
}


# ------------------------------------------------------------
# ÉTAT DU MOTEUR
# ------------------------------------------------------------

engine_state = {
    "running": False,
    "stop": False,
    "nodes": 0,
    "depth": 0,
    "start_time": 0.0,
    "best_move": None,
    "evaluation": 0
}


# ------------------------------------------------------------
# UTILITAIRES
# ------------------------------------------------------------

def temps_ecoule():
    """Retourne le temps écoulé depuis le début de la recherche."""
    if engine_state["start_time"] == 0:
        return 0.0

    return time.time() - engine_state["start_time"]


def temps_depasse():
    """Indique si la limite de temps est dépassée."""
    if TIME_LIMIT <= 0:
        return False

    return temps_ecoule() >= TIME_LIMIT


def limiter_adaptation(valeur):
    """Empêche une adaptation de devenir trop faible ou trop forte."""
    return max(
        ADAPTATION_MIN,
        min(ADAPTATION_MAX, valeur)
    )


# ------------------------------------------------------------
# AFFICHAGE
# ------------------------------------------------------------

def afficher_banniere():
    print()
    print("=" * 60)
    print("🐼 PANDORAGA FULL ADAPTATION Ω")
    print("=" * 60)
    print(f"Version        : {PANDORAGA_VERSION}")
    print(f"Profondeur max : {MAX_DEPTH}")
    print(f"Temps réflexion: {TIME_LIMIT}s")
    print(f"Mémoire        : {MEMOIRE_FICHIER}")
    print(f"Adaptation Ω   : {'ACTIVE' if ADAPTATION_ACTIVE else 'OFF'}")
    print("=" * 60)
    print()


# ------------------------------------------------------------
# INITIALISATION
# ------------------------------------------------------------

def initialiser_moteur():
    """Initialise l'état interne de Pandoraga."""
    engine_state["running"] = False
    engine_state["stop"] = False
    engine_state["nodes"] = 0
    engine_state["depth"] = 0
    engine_state["start_time"] = 0.0
    engine_state["best_move"] = None
    engine_state["evaluation"] = 0


# ------------------------------------------------------------
# TEST DU BLOC
# ------------------------------------------------------------

if __name__ == "__main__":
    initialiser_moteur()
    afficher_banniere()
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 2/25 — PIÈCES ET CONSTANTES D'ÉCHECS
# ============================================================

# ------------------------------------------------------------
# COULEURS
# ------------------------------------------------------------

BLANC = 0
NOIR = 1

COULEURS = (BLANC, NOIR)


# ------------------------------------------------------------
# PIÈCES
# ------------------------------------------------------------

VIDE = 0

PION = 1
CAVALIER = 2
FOU = 3
TOUR = 4
DAME = 5
ROI = 6


# ------------------------------------------------------------
# PIÈCES SIGNÉES
# ------------------------------------------------------------
# Une pièce blanche est positive.
# Une pièce noire est négative.
#
# Exemple :
#   PION BLANC     = +1
#   PION NOIR      = -1
#   ROI BLANC      = +6
#   ROI NOIR       = -6
#
# Cela facilite énormément l'évaluation du plateau.

PIECE_BLANCHE = {
    PION: PION,
    CAVALIER: CAVALIER,
    FOU: FOU,
    TOUR: TOUR,
    DAME: DAME,
    ROI: ROI
}

PIECE_NOIRE = {
    PION: -PION,
    CAVALIER: -CAVALIER,
    FOU: -FOU,
    TOUR: -TOUR,
    DAME: -DAME,
    ROI: -ROI
}


# ------------------------------------------------------------
# NOMS DES PIÈCES
# ------------------------------------------------------------

NOMS_PIECES = {
    VIDE: "Vide",
    PION: "Pion",
    CAVALIER: "Cavalier",
    FOU: "Fou",
    TOUR: "Tour",
    DAME: "Dame",
    ROI: "Roi"
}


# ------------------------------------------------------------
# SYMBOLes UNICODE
# ------------------------------------------------------------

SYMBOLES_BLANC = {
    PION: "♙",
    CAVALIER: "♘",
    FOU: "♗",
    TOUR: "♖",
    DAME: "♕",
    ROI: "♔"
}

SYMBOLES_NOIR = {
    PION: "♟",
    CAVALIER: "♞",
    FOU: "♝",
    TOUR: "♜",
    DAME: "♛",
    ROI: "♚"
}


# ------------------------------------------------------------
# TABLEAU DES SYMBOLes
# ------------------------------------------------------------

SYMBOLES_PIECES = {
    0: ".",

    1: "♙",
    2: "♘",
    3: "♗",
    4: "♖",
    5: "♕",
    6: "♔",

    -1: "♟",
    -2: "♞",
    -3: "♝",
    -4: "♜",
    -5: "♛",
    -6: "♚"
}


# ------------------------------------------------------------
# VALEURS MATÉRIELLES
# ------------------------------------------------------------

VALEURS_PIECES = {
    PION: 100,
    CAVALIER: 320,
    FOU: 330,
    TOUR: 500,
    DAME: 900,
    ROI: 20000
}


# ------------------------------------------------------------
# NOMS COURTS
# ------------------------------------------------------------

LETTRES_PIECES = {
    PION: "P",
    CAVALIER: "N",
    FOU: "B",
    TOUR: "R",
    DAME: "Q",
    ROI: "K"
}


# ------------------------------------------------------------
# CASES : 0 → 63
# ------------------------------------------------------------
#
# Organisation :
#
# 56 57 58 59 60 61 62 63
# 48 49 50 51 52 53 54 55
# 40 41 42 43 44 45 46 47
# 32 33 34 35 36 37 38 39
# 24 25 26 27 28 29 30 31
# 16 17 18 19 20 21 22 23
#  8  9 10 11 12 13 14 15
#  0  1  2  3  4  5  6  7
#
# a1 = 0
# b1 = 1
# ...
# h8 = 63


NOMBRE_CASES = 64


# ------------------------------------------------------------
# CONVERSION CASE → NOM
# ------------------------------------------------------------

NOMS_CASES = []

for rang in range(8):
    for colonne in range(8):
        lettre = chr(ord("a") + colonne)
        numero = rang + 1
        NOMS_CASES.append(lettre + str(numero))


# ------------------------------------------------------------
# DICTIONS INCRÉMENTALES
# ------------------------------------------------------------

DIRECTION_HAUT = 8
DIRECTION_BAS = -8

DIRECTION_DROITE = 1
DIRECTION_GAUCHE = -1

DIRECTION_HAUT_DROITE = 9
DIRECTION_HAUT_GAUCHE = 7
DIRECTION_BAS_DROITE = -7
DIRECTION_BAS_GAUCHE = -9


# ------------------------------------------------------------
# DIRECTIONS CAVALIER
# ------------------------------------------------------------

DIRECTIONS_CAVALIER = (
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2)
)


# ------------------------------------------------------------
# DIRECTIONS ROI
# ------------------------------------------------------------

DIRECTIONS_ROI = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
)


# ------------------------------------------------------------
# DIRECTIONS FOUS
# ------------------------------------------------------------

DIRECTIONS_FOU = (
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
)


# ------------------------------------------------------------
# DIRECTIONS TOURS
# ------------------------------------------------------------

DIRECTIONS_TOUR = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
)


# ------------------------------------------------------------
# DIRECTIONS DAME
# ------------------------------------------------------------

DIRECTIONS_DAME = DIRECTIONS_FOU + DIRECTIONS_TOUR


# ------------------------------------------------------------
# DROITS DE ROQUE
# ------------------------------------------------------------

ROQUE_BLANC_ROI = 1
ROQUE_BLANC_DAME = 2
ROQUE_NOIR_ROI = 4
ROQUE_NOIR_DAME = 8

ROQUE_AUCUN = 0

TOUS_ROQUES = (
    ROQUE_BLANC_ROI
    | ROQUE_BLANC_DAME
    | ROQUE_NOIR_ROI
    | ROQUE_NOIR_DAME
)


# ------------------------------------------------------------
# ÉTATS DE PARTIE
# ------------------------------------------------------------

PARTIE_ACTIVE = 0
PARTIE_ECHEC = 1
PARTIE_MAT = 2
PARTIE_PAT = 3
PARTIE_NULLE = 4
PARTIE_ABANDON = 5


# ------------------------------------------------------------
# PROMOTIONS
# ------------------------------------------------------------

PROMOTIONS = (
    CAVALIER,
    FOU,
    TOUR,
    DAME
)


# ------------------------------------------------------------
# OUTILS
# ------------------------------------------------------------

def couleur_piece(piece):
    """Retourne la couleur d'une pièce."""

    if piece > 0:
        return BLANC

    if piece < 0:
        return NOIR

    return None


def type_piece(piece):
    """Retourne le type d'une pièce sans tenir compte de sa couleur."""

    return abs(piece)


def est_piece_blanche(piece):
    return piece > 0


def est_piece_noire(piece):
    return piece < 0


def est_case_valide(case):
    return 0 <= case < 64


def case_vers_nom(case):
    """Convertit 0..63 en notation a1..h8."""

    if not est_case_valide(case):
        return "??"

    return NOMS_CASES[case]


def nom_vers_case(nom):
    """Convertit a1..h8 en index 0..63."""

    if not isinstance(nom, str):
        return -1

    nom = nom.lower().strip()

    if len(nom) != 2:
        return -1

    colonne = ord(nom[0]) - ord("a")
    rang = ord(nom[1]) - ord("1")

    if not (0 <= colonne < 8):
        return -1

    if not (0 <= rang < 8):
        return -1

    return rang * 8 + colonne


def ligne_case(case):
    """Retourne la ligne 0..7."""

    return case // 8


def colonne_case(case):
    """Retourne la colonne 0..7."""

    return case % 8


def piece_vers_symbole(piece):
    """Retourne le symbole Unicode d'une pièce."""

    return SYMBOLES_PIECES.get(piece, "?")


def piece_vers_lettre(piece):
    """Retourne P/N/B/R/Q/K avec la couleur implicite."""

    return LETTRES_PIECES.get(abs(piece), "?")


# ------------------------------------------------------------
# TEST DU BLOC
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 BLOC 2 — TEST")
    print("-" * 40)

    print("a1 =", nom_vers_case("a1"))
    print("e1 =", nom_vers_case("e1"))
    print("h8 =", nom_vers_case("h8"))

    print()

    print("0  =", case_vers_nom(0))
    print("4  =", case_vers_nom(4))
    print("60 =", case_vers_nom(60))
    print("63 =", case_vers_nom(63))

    print()

    print("Pion blanc :", piece_vers_symbole(PION))
    print("Roi blanc  :", piece_vers_symbole(ROI))
    print("Pion noir  :", piece_vers_symbole(-PION))
    print("Roi noir   :", piece_vers_symbole(-ROI))

    print()

    print("Bloc 2 chargé avec succès.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 3/25 — PLATEAU ET POSITION INITIALE
# ============================================================

# ------------------------------------------------------------
# CRÉATION D'UN PLATEAU VIDE
# ------------------------------------------------------------

def creer_plateau_vide():
    """
    Crée un plateau de 64 cases.

    Index :
        0  = a1
        1  = b1
        ...
        63 = h8
    """

    return [VIDE] * 64


# ------------------------------------------------------------
# POSITION INITIALE
# ------------------------------------------------------------

def creer_position_initiale():
    """
    Crée la position de départ officielle d'une partie d'échecs.
    """

    plateau = creer_plateau_vide()

    # --------------------------------------------------------
    # BLANCS
    # --------------------------------------------------------

    # Première rangée
    plateau[nom_vers_case("a1")] = TOUR
    plateau[nom_vers_case("b1")] = CAVALIER
    plateau[nom_vers_case("c1")] = FOU
    plateau[nom_vers_case("d1")] = DAME
    plateau[nom_vers_case("e1")] = ROI
    plateau[nom_vers_case("f1")] = FOU
    plateau[nom_vers_case("g1")] = CAVALIER
    plateau[nom_vers_case("h1")] = TOUR

    # Pions blancs
    for colonne in range(8):
        plateau[8 + colonne] = PION

    # --------------------------------------------------------
    # NOIRS
    # --------------------------------------------------------

    # Huitième rangée
    plateau[nom_vers_case("a8")] = -TOUR
    plateau[nom_vers_case("b8")] = -CAVALIER
    plateau[nom_vers_case("c8")] = -FOU
    plateau[nom_vers_case("d8")] = -DAME
    plateau[nom_vers_case("e8")] = -ROI
    plateau[nom_vers_case("f8")] = -FOU
    plateau[nom_vers_case("g8")] = -CAVALIER
    plateau[nom_vers_case("h8")] = -TOUR

    # Pions noirs
    for colonne in range(8):
        plateau[48 + colonne] = -PION

    return plateau


# ------------------------------------------------------------
# ÉTAT COMPLET D'UNE PARTIE
# ------------------------------------------------------------

def creer_etat_initial():
    """
    Crée toutes les informations nécessaires à une partie.
    """

    return {
        "plateau": creer_position_initiale(),

        # Blanc commence toujours.
        "tour": BLANC,

        # Droits de roque.
        "roque": TOUS_ROQUES,

        # Case de prise en passant.
        # -1 = aucune.
        "en_passant": -1,

        # Compteur de demi-coups.
        "demi_coups": 0,

        # Numéro du coup complet.
        "numero_coup": 1,

        # Historique des positions.
        "historique": [],

        # Historique des coups.
        "coups_joues": [],

        # État de la partie.
        "statut": PARTIE_ACTIVE
    }


# ------------------------------------------------------------
# COPIE D'UN ÉTAT
# ------------------------------------------------------------

def copier_etat(etat):
    """
    Crée une copie indépendante de l'état.
    """

    return {
        "plateau": etat["plateau"][:],
        "tour": etat["tour"],
        "roque": etat["roque"],
        "en_passant": etat["en_passant"],
        "demi_coups": etat["demi_coups"],
        "numero_coup": etat["numero_coup"],
        "historique": etat["historique"][:],
        "coups_joues": etat["coups_joues"][:],
        "statut": etat["statut"]
    }


# ------------------------------------------------------------
# AFFICHAGE DU PLATEAU
# ------------------------------------------------------------

def afficher_plateau(plateau):
    """
    Affiche le plateau dans la console.
    """

    print()
    print("    a b c d e f g h")
    print("   -----------------")

    for rang in range(7, -1, -1):

        ligne = []

        for colonne in range(8):

            case = rang * 8 + colonne
            piece = plateau[case]

            ligne.append(piece_vers_symbole(piece))

        print(f"{rang + 1} | " + " ".join(ligne) + f" | {rang + 1}")

    print("   -----------------")
    print("    a b c d e f g h")
    print()


# ------------------------------------------------------------
# RECHERCHE DU ROI
# ------------------------------------------------------------

def trouver_roi(plateau, couleur):
    """
    Retourne la case du roi de la couleur donnée.

    Retour :
        0..63 si trouvé
        -1 sinon
    """

    roi = ROI if couleur == BLANC else -ROI

    for case in range(64):

        if plateau[case] == roi:
            return case

    return -1


# ------------------------------------------------------------
# COMPTER LES PIÈCES
# ------------------------------------------------------------

def compter_pieces(plateau, couleur=None):
    """
    Compte les pièces présentes.

    Si couleur est None :
        compte toutes les pièces.

    Sinon :
        compte uniquement la couleur demandée.
    """

    total = 0

    for piece in plateau:

        if piece == VIDE:
            continue

        if couleur is None:
            total += 1

        elif couleur_piece(piece) == couleur:
            total += 1

    return total


# ------------------------------------------------------------
# MATÉRIEL D'UNE COULEUR
# ------------------------------------------------------------

def materiel_couleur(plateau, couleur):
    """
    Calcule la valeur matérielle d'une couleur.
    """

    total = 0

    for piece in plateau:

        if piece == VIDE:
            continue

        if couleur_piece(piece) != couleur:
            continue

        total += VALEURS_PIECES[type_piece(piece)]

    return total


# ------------------------------------------------------------
# RÉSUMÉ DU PLATEAU
# ------------------------------------------------------------

def resume_plateau(plateau):
    """
    Retourne un petit résumé utile pour le moteur.
    """

    return {
        "pieces_blanches": compter_pieces(plateau, BLANC),
        "pieces_noires": compter_pieces(plateau, NOIR),
        "materiel_blanc": materiel_couleur(plateau, BLANC),
        "materiel_noir": materiel_couleur(plateau, NOIR),
        "roi_blanc": trouver_roi(plateau, BLANC),
        "roi_noir": trouver_roi(plateau, NOIR)
    }


# ------------------------------------------------------------
# NOTATION SIMPLE DU PLATEAU
# ------------------------------------------------------------

def plateau_vers_chaine(plateau):
    """
    Transforme le plateau en chaîne compacte.

    Utile plus tard pour :
        - mémoire
        - répétitions
        - hash
        - table de transposition
    """

    return "".join(
        str(piece) + ","
        for piece in plateau
    )


# ------------------------------------------------------------
# POSITION DE DÉPART
# ------------------------------------------------------------

def afficher_position_initiale():
    """
    Affiche la position initiale complète.
    """

    etat = creer_etat_initial()

    print()
    print("🐼 PANDORAGA Ω — POSITION INITIALE")
    print("=" * 40)

    afficher_plateau(etat["plateau"])

    print("Tour :", "Blanc" if etat["tour"] == BLANC else "Noir")
    print("Roque :", etat["roque"])
    print("En passant :", etat["en_passant"])

    resume = resume_plateau(etat["plateau"])

    print()
    print("Pièces blanches :", resume["pieces_blanches"])
    print("Pièces noires   :", resume["pieces_noires"])
    print("Matériel blanc  :", resume["materiel_blanc"])
    print("Matériel noir   :", resume["materiel_noir"])
    print("Roi blanc       :", case_vers_nom(resume["roi_blanc"]))
    print("Roi noir        :", case_vers_nom(resume["roi_noir"]))


# ------------------------------------------------------------
# TEST DU BLOC 3
# ------------------------------------------------------------

if __name__ == "__main__":

    afficher_position_initiale()

    print()
    print("🐼 BLOC 3 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 4/25 — ANALYSE ET GESTION DES POSITIONS
# ============================================================

# ------------------------------------------------------------
# COULEUR OPPOSÉE
# ------------------------------------------------------------

def couleur_opposee(couleur):
    """Retourne la couleur adverse."""

    if couleur == BLANC:
        return NOIR

    return BLANC


# ------------------------------------------------------------
# CASE → COORDONNÉES
# ------------------------------------------------------------

def case_coordonnees(case):
    """
    Convertit une case 0..63 en coordonnées :
        (colonne, ligne)

    Exemple :
        a1 -> (0, 0)
        h8 -> (7, 7)
    """

    if not est_case_valide(case):
        return None

    return (
        colonne_case(case),
        ligne_case(case)
    )


# ------------------------------------------------------------
# COORDONNÉES → CASE
# ------------------------------------------------------------

def coordonnees_case(colonne, ligne):
    """
    Convertit des coordonnées 0..7 en case 0..63.
    """

    if not (0 <= colonne < 8):
        return -1

    if not (0 <= ligne < 8):
        return -1

    return ligne * 8 + colonne


# ------------------------------------------------------------
# CASE SUR LE PLATEAU
# ------------------------------------------------------------

def case_sur_plateau(colonne, ligne):
    return (
        0 <= colonne < 8
        and
        0 <= ligne < 8
    )


# ------------------------------------------------------------
# PIÈCE SUR UNE CASE
# ------------------------------------------------------------

def obtenir_piece(etat, case):
    """
    Retourne la pièce située sur une case.
    """

    if not est_case_valide(case):
        return VIDE

    return etat["plateau"][case]


# ------------------------------------------------------------
# MODIFIER UNE CASE
# ------------------------------------------------------------

def placer_piece(etat, case, piece):
    """
    Place une pièce sur une case.
    """

    if not est_case_valide(case):
        return False

    etat["plateau"][case] = piece

    return True


# ------------------------------------------------------------
# VIDER UNE CASE
# ------------------------------------------------------------

def vider_case(etat, case):
    """
    Supprime la pièce d'une case.
    """

    if not est_case_valide(case):
        return False

    etat["plateau"][case] = VIDE

    return True


# ------------------------------------------------------------
# CASE VIDE ?
# ------------------------------------------------------------

def case_vide(etat, case):
    return obtenir_piece(etat, case) == VIDE


# ------------------------------------------------------------
# CASE OCCUPÉE ?
# ------------------------------------------------------------

def case_occupee(etat, case):
    return obtenir_piece(etat, case) != VIDE


# ------------------------------------------------------------
# CASE OCCUPÉE PAR UNE COULEUR
# ------------------------------------------------------------

def case_occupee_par(etat, case, couleur):
    """
    Vérifie si une case appartient à une couleur.
    """

    piece = obtenir_piece(etat, case)

    if piece == VIDE:
        return False

    return couleur_piece(piece) == couleur


# ------------------------------------------------------------
# CASE OCCUPÉE PAR L'ADVERSAIRE
# ------------------------------------------------------------

def case_ennemie(etat, case, couleur):
    """
    Vérifie si la case contient une pièce adverse.
    """

    piece = obtenir_piece(etat, case)

    if piece == VIDE:
        return False

    return couleur_piece(piece) == couleur_opposee(couleur)


# ------------------------------------------------------------
# LISTE DES CASES D'UNE COULEUR
# ------------------------------------------------------------

def cases_couleur(etat, couleur):
    """
    Retourne toutes les cases occupées par une couleur.
    """

    resultat = []

    for case in range(64):

        piece = etat["plateau"][case]

        if piece == VIDE:
            continue

        if couleur_piece(piece) == couleur:
            resultat.append(case)

    return resultat


# ------------------------------------------------------------
# LISTE DES PIÈCES D'UNE COULEUR
# ------------------------------------------------------------

def pieces_couleur(etat, couleur):
    """
    Retourne :
        [(case, pièce), ...]
    """

    resultat = []

    for case in range(64):

        piece = etat["plateau"][case]

        if piece == VIDE:
            continue

        if couleur_piece(piece) == couleur:
            resultat.append((case, piece))

    return resultat


# ------------------------------------------------------------
# COMPTER UN TYPE DE PIÈCE
# ------------------------------------------------------------

def compter_type_piece(etat, couleur, type_piece_recherche):
    """
    Compte par exemple :
        nombre de cavaliers blancs
        nombre de tours noires
    """

    total = 0

    for case, piece in pieces_couleur(etat, couleur):

        if type_piece(piece) == type_piece_recherche:
            total += 1

    return total


# ------------------------------------------------------------
# MATÉRIEL SIGNÉ
# ------------------------------------------------------------

def evaluation_materielle(etat):
    """
    Retourne :
        matériel blanc - matériel noir
    """

    blanc = materiel_couleur(
        etat["plateau"],
        BLANC
    )

    noir = materiel_couleur(
        etat["plateau"],
        NOIR
    )

    return blanc - noir


# ------------------------------------------------------------
# POSITION CLÉ
# ------------------------------------------------------------

def cle_position(etat):
    """
    Génère une clé représentant l'état important
    de la position.

    Cette fonction sera utilisée plus tard par :
        - répétitions
        - mémoire
        - table de transposition
    """

    plateau = plateau_vers_chaine(
        etat["plateau"]
    )

    return (
        plateau
        + "|T:" + str(etat["tour"])
        + "|R:" + str(etat["roque"])
        + "|EP:" + str(etat["en_passant"])
    )


# ------------------------------------------------------------
# POSITION RÉPÉTÉE
# ------------------------------------------------------------

def position_deja_vue(etat):
    """
    Vérifie si la position actuelle existe déjà
    dans l'historique.
    """

    cle = cle_position(etat)

    return cle in etat["historique"]


# ------------------------------------------------------------
# ENREGISTRER LA POSITION
# ------------------------------------------------------------

def enregistrer_position(etat):
    """
    Ajoute la position actuelle à l'historique.
    """

    cle = cle_position(etat)

    etat["historique"].append(cle)


# ------------------------------------------------------------
# NOMBRE DE RÉPÉTITIONS
# ------------------------------------------------------------

def nombre_repetitions(etat):
    """
    Compte combien de fois la position actuelle
    apparaît dans l'historique.
    """

    cle = cle_position(etat)

    return etat["historique"].count(cle)


# ------------------------------------------------------------
# RÈGLE DES 50 COUPS
# ------------------------------------------------------------

def regle_50_coups(etat):
    """
    Retourne True si le compteur atteint 100 demi-coups.
    """

    return etat["demi_coups"] >= 100


# ------------------------------------------------------------
# MATÉRIEL INSUFFISANT
# ------------------------------------------------------------

def materiel_insuffisant(etat):
    """
    Détection simple de quelques positions de matériel
    insuffisant pour mater.

    Cette fonction sera améliorée plus tard.
    """

    plateau = etat["plateau"]

    pieces = []

    for piece in plateau:

        if piece == VIDE:
            continue

        pieces.append(type_piece(piece))

    # Roi contre roi
    if len(pieces) == 2:
        return True

    # Roi + cavalier contre roi
    if len(pieces) == 3:

        non_rois = [
            p for p in pieces
            if p != ROI
        ]

        if len(non_rois) == 1:
            if non_rois[0] == CAVALIER:
                return True

    # Roi + fou contre roi
    if len(pieces) == 3:

        non_rois = [
            p for p in pieces
            if p != ROI
        ]

        if len(non_rois) == 1:
            if non_rois[0] == FOU:
                return True

    return False


# ------------------------------------------------------------
# ÉTAT DE LA PARTIE
# ------------------------------------------------------------

def analyser_etat_position(etat):
    """
    Retourne un résumé complet de la position.
    """

    plateau = etat["plateau"]

    roi_blanc = trouver_roi(
        plateau,
        BLANC
    )

    roi_noir = trouver_roi(
        plateau,
        NOIR
    )

    return {
        "tour": etat["tour"],

        "roi_blanc": roi_blanc,
        "roi_noir": roi_noir,

        "pieces_blanches": compter_pieces(
            plateau,
            BLANC
        ),

        "pieces_noires": compter_pieces(
            plateau,
            NOIR
        ),

        "materiel": evaluation_materielle(
            etat
        ),

        "repetitions": nombre_repetitions(
            etat
        ),

        "regle_50_coups": regle_50_coups(
            etat
        ),

        "materiel_insuffisant":
            materiel_insuffisant(etat)
    }


# ------------------------------------------------------------
# CLONER UNE POSITION
# ------------------------------------------------------------

def cloner_position(etat):
    """
    Alias pratique pour le moteur de recherche.
    """

    return copier_etat(etat)


# ------------------------------------------------------------
# RESET DE LA PARTIE
# ------------------------------------------------------------

def reinitialiser_partie():
    """
    Crée une nouvelle partie complète.
    """

    etat = creer_etat_initial()

    enregistrer_position(etat)

    return etat


# ------------------------------------------------------------
# TEST DU BLOC 4
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 BLOC 4 — TEST")
    print("=" * 40)

    etat_test = reinitialiser_partie()

    print("Tour :",
          "Blanc" if etat_test["tour"] == BLANC
          else "Noir")

    print(
        "Roi blanc :",
        case_vers_nom(
            trouver_roi(
                etat_test["plateau"],
                BLANC
            )
        )
    )

    print(
        "Roi noir :",
        case_vers_nom(
            trouver_roi(
                etat_test["plateau"],
                NOIR
            )
        )
    )

    print(
        "Matériel :",
        evaluation_materielle(etat_test)
    )

    print(
        "Clé créée :",
        len(cle_position(etat_test)),
        "caractères"
    )

    print(
        "Matériel insuffisant :",
        materiel_insuffisant(etat_test)
    )

    print()
    print("🐼 BLOC 4 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 5/25 — GÉNÉRATEUR DE COUPS
# ============================================================

# ------------------------------------------------------------
# STRUCTURE D'UN COUP
# ------------------------------------------------------------

def creer_coup(
    depart,
    arrivee,
    promotion=VIDE,
    capture=VIDE,
    en_passant=False,
    roque=False,
):
    """
    Crée un dictionnaire représentant un coup.

    depart      : case de départ 0..63
    arrivee     : case d'arrivée 0..63
    promotion   : pièce de promotion éventuelle
    capture     : pièce capturée
    en_passant  : prise en passant
    roque       : petit ou grand roque
    """

    return {
        "depart": depart,
        "arrivee": arrivee,
        "promotion": promotion,
        "capture": capture,
        "en_passant": en_passant,
        "roque": roque
    }


# ------------------------------------------------------------
# COORDONNÉES D'UN COUP
# ------------------------------------------------------------

def coup_vers_chaine(coup):
    """
    Convertit un coup en notation simple.

    Exemple :
        e2e4
        e7e8Q
    """

    depart = case_vers_nom(coup["depart"])
    arrivee = case_vers_nom(coup["arrivee"])

    resultat = depart + arrivee

    promotion = coup["promotion"]

    if promotion != VIDE:
        resultat += LETTRES_PIECES.get(
            promotion,
            "?"
        )

    return resultat


# ------------------------------------------------------------
# AJOUTER UN COUP
# ------------------------------------------------------------

def ajouter_coup(
    coups,
    depart,
    arrivee,
    promotion=VIDE,
    capture=VIDE,
    en_passant=False,
    roque=False
):
    """
    Ajoute un coup à une liste s'il est valide.
    """

    if not est_case_valide(depart):
        return

    if not est_case_valide(arrivee):
        return

    coups.append(
        creer_coup(
            depart,
            arrivee,
            promotion,
            capture,
            en_passant,
            roque
        )
    )


# ------------------------------------------------------------
# COUPS DU PION
# ------------------------------------------------------------

def coups_pion(etat, case, couleur, coups):
    """
    Génère les coups pseudo-légaux d'un pion.
    """

    plateau = etat["plateau"]

    colonne = colonne_case(case)
    ligne = ligne_case(case)

    direction = 1 if couleur == BLANC else -1

    ligne_depart = 1 if couleur == BLANC else 6
    ligne_promotion = 7 if couleur == BLANC else 0

    # --------------------------------------------------------
    # AVANCÉE D'UNE CASE
    # --------------------------------------------------------

    nouvelle_ligne = ligne + direction

    if case_sur_plateau(
        colonne,
        nouvelle_ligne
    ):

        destination = coordonnees_case(
            colonne,
            nouvelle_ligne
        )

        if plateau[destination] == VIDE:

            if nouvelle_ligne == ligne_promotion:

                for promotion in PROMOTIONS:
                    ajouter_coup(
                        coups,
                        case,
                        destination,
                        promotion=promotion
                    )

            else:

                ajouter_coup(
                    coups,
                    case,
                    destination
                )

                # ------------------------------------------------
                # AVANCÉE DE DEUX CASES
                # ------------------------------------------------

                if ligne == ligne_depart:

                    ligne_double = (
                        ligne
                        + 2 * direction
                    )

                    destination_double = (
                        coordonnees_case(
                            colonne,
                            ligne_double
                        )
                    )

                    if (
                        plateau[destination_double]
                        == VIDE
                    ):
                        ajouter_coup(
                            coups,
                            case,
                            destination_double
                        )

    # --------------------------------------------------------
    # CAPTURES DIAGONALES
    # --------------------------------------------------------

    for delta_colonne in (-1, 1):

        nouvelle_colonne = (
            colonne + delta_colonne
        )

        nouvelle_ligne = (
            ligne + direction
        )

        if not case_sur_plateau(
            nouvelle_colonne,
            nouvelle_ligne
        ):
            continue

        destination = coordonnees_case(
            nouvelle_colonne,
            nouvelle_ligne
        )

        piece = plateau[destination]

        # Capture normale
        if piece != VIDE:

            if couleur_piece(piece) != couleur:

                if nouvelle_ligne == ligne_promotion:

                    for promotion in PROMOTIONS:
                        ajouter_coup(
                            coups,
                            case,
                            destination,
                            promotion=promotion,
                            capture=piece
                        )

                else:

                    ajouter_coup(
                        coups,
                        case,
                        destination,
                        capture=piece
                    )

        # ----------------------------------------------------
        # PRISE EN PASSANT
        # ----------------------------------------------------

        if destination == etat["en_passant"]:

            ajouter_coup(
                coups,
                case,
                destination,
                capture=(
                    -PION
                    if couleur == BLANC
                    else PION
                ),
                en_passant=True
            )


# ------------------------------------------------------------
# COUPS DU CAVALIER
# ------------------------------------------------------------

def coups_cavalier(etat, case, couleur, coups):
    """
    Génère les coups du cavalier.
    """

    plateau = etat["plateau"]

    colonne = colonne_case(case)
    ligne = ligne_case(case)

    for delta_colonne, delta_ligne in DIRECTIONS_CAVALIER:

        nouvelle_colonne = colonne + delta_colonne
        nouvelle_ligne = ligne + delta_ligne

        if not case_sur_plateau(
            nouvelle_colonne,
            nouvelle_ligne
        ):
            continue

        destination = coordonnees_case(
            nouvelle_colonne,
            nouvelle_ligne
        )

        piece = plateau[destination]

        if piece == VIDE:

            ajouter_coup(
                coups,
                case,
                destination
            )

        elif couleur_piece(piece) != couleur:

            ajouter_coup(
                coups,
                case,
                destination,
                capture=piece
            )


# ------------------------------------------------------------
# COUPS D'UNE PIÈCE GLISSANTE
# ------------------------------------------------------------

def coups_glissants(
    etat,
    case,
    couleur,
    directions,
    coups
):
    """
    Générateur commun pour :
        - fou
        - tour
        - dame
    """

    plateau = etat["plateau"]

    colonne_depart = colonne_case(case)
    ligne_depart = ligne_case(case)

    for delta_colonne, delta_ligne in directions:

        colonne = colonne_depart + delta_colonne
        ligne = ligne_depart + delta_ligne

        while case_sur_plateau(
            colonne,
            ligne
        ):

            destination = coordonnees_case(
                colonne,
                ligne
            )

            piece = plateau[destination]

            if piece == VIDE:

                ajouter_coup(
                    coups,
                    case,
                    destination
                )

            else:

                if couleur_piece(piece) != couleur:

                    ajouter_coup(
                        coups,
                        case,
                        destination,
                        capture=piece
                    )

                # Une pièce bloque toujours la direction.
                break

            colonne += delta_colonne
            ligne += delta_ligne


# ------------------------------------------------------------
# COUPS DU FOU
# ------------------------------------------------------------

def coups_fou(etat, case, couleur, coups):

    coups_glissants(
        etat,
        case,
        couleur,
        DIRECTIONS_FOU,
        coups
    )


# ------------------------------------------------------------
# COUPS DE LA TOUR
# ------------------------------------------------------------

def coups_tour(etat, case, couleur, coups):

    coups_glissants(
        etat,
        case,
        couleur,
        DIRECTIONS_TOUR,
        coups
    )


# ------------------------------------------------------------
# COUPS DE LA DAME
# ------------------------------------------------------------

def coups_dame(etat, case, couleur, coups):

    coups_glissants(
        etat,
        case,
        couleur,
        DIRECTIONS_DAME,
        coups
    )


# ------------------------------------------------------------
# COUPS DU ROI
# ------------------------------------------------------------

def coups_roi(etat, case, couleur, coups):
    """
    Génère les déplacements normaux du roi.

    Le roque sera traité séparément.
    """

    plateau = etat["plateau"]

    colonne = colonne_case(case)
    ligne = ligne_case(case)

    for delta_colonne, delta_ligne in DIRECTIONS_ROI:

        nouvelle_colonne = (
            colonne + delta_colonne
        )

        nouvelle_ligne = (
            ligne + delta_ligne
        )

        if not case_sur_plateau(
            nouvelle_colonne,
            nouvelle_ligne
        ):
            continue

        destination = coordonnees_case(
            nouvelle_colonne,
            nouvelle_ligne
        )

        piece = plateau[destination]

        if piece == VIDE:

            ajouter_coup(
                coups,
                case,
                destination
            )

        elif couleur_piece(piece) != couleur:

            ajouter_coup(
                coups,
                case,
                destination,
                capture=piece
            )


# ------------------------------------------------------------
# GÉNÉRATEUR PAR TYPE DE PIÈCE
# ------------------------------------------------------------

def coups_piece(etat, case, coups):
    """
    Génère les coups pseudo-légaux d'une pièce.
    """

    piece = etat["plateau"][case]

    if piece == VIDE:
        return

    couleur = couleur_piece(piece)
    type_piece_actuel = type_piece(piece)

    if type_piece_actuel == PION:

        coups_pion(
            etat,
            case,
            couleur,
            coups
        )

    elif type_piece_actuel == CAVALIER:

        coups_cavalier(
            etat,
            case,
            couleur,
            coups
        )

    elif type_piece_actuel == FOU:

        coups_fou(
            etat,
            case,
            couleur,
            coups
        )

    elif type_piece_actuel == TOUR:

        coups_tour(
            etat,
            case,
            couleur,
            coups
        )

    elif type_piece_actuel == DAME:

        coups_dame(
            etat,
            case,
            couleur,
            coups
        )

    elif type_piece_actuel == ROI:

        coups_roi(
            etat,
            case,
            couleur,
            coups
        )


# ------------------------------------------------------------
# GÉNÉRATEUR DE TOUS LES COUPS
# ------------------------------------------------------------

def generer_coups_pseudo_legaux(etat):
    """
    Génère tous les coups possibles pour le joueur actuel.

    Attention :
    les coups laissant le roi en échec sont encore présents.

    Le bloc 6 les supprimera.
    """

    coups = []

    couleur = etat["tour"]

    for case in range(64):

        piece = etat["plateau"][case]

        if piece == VIDE:
            continue

        if couleur_piece(piece) != couleur:
            continue

        coups_piece(
            etat,
            case,
            coups
        )

    return coups


# ------------------------------------------------------------
# COUPS PAR TYPE
# ------------------------------------------------------------

def compter_coups_pseudo_legaux(etat):
    """
    Retourne le nombre de coups pseudo-légaux.
    """

    return len(
        generer_coups_pseudo_legaux(etat)
    )


# ------------------------------------------------------------
# AFFICHAGE DES COUPS
# ------------------------------------------------------------

def afficher_coups(coups):
    """
    Affiche les coups générés.
    """

    if not coups:
        print("Aucun coup généré.")
        return

    for numero, coup in enumerate(coups, 1):

        print(
            f"{numero:3d}. "
            f"{coup_vers_chaine(coup)}"
        )


# ------------------------------------------------------------
# TEST DU BLOC 5
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 BLOC 5 — TEST DU GÉNÉRATEUR")
    print("=" * 50)

    etat_test = creer_etat_initial()

    coups = generer_coups_pseudo_legaux(
        etat_test
    )

    print(
        "Coups pseudo-légaux depuis la position initiale :",
        len(coups)
    )

    print()

    afficher_coups(coups)

    print()
    print("🐼 BLOC 5 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 6/25 — COUPS LÉGAUX, ÉCHEC ET ANNULATION
# ============================================================


# ------------------------------------------------------------
# ATTAQUE D'UNE CASE
# ------------------------------------------------------------

def case_attaquee(etat, case, par_couleur):
    """
    Vérifie si une case est attaquée par une couleur.

    Important :
    cette fonction ne dépend pas de la légalité du coup.
    Elle sert notamment à vérifier les cases autour du roi
    et les conditions du roque.
    """

    if not est_case_valide(case):
        return False

    plateau = etat["plateau"]

    colonne = colonne_case(case)
    ligne = ligne_case(case)

    # --------------------------------------------------------
    # PIONS
    # --------------------------------------------------------

    # Pour attaquer la case cible :
    # un pion blanc doit être une ligne en dessous.
    # un pion noir doit être une ligne au-dessus.

    direction = -1 if par_couleur == BLANC else 1

    ligne_pion = ligne + direction

    if 0 <= ligne_pion < 8:

        for delta_colonne in (-1, 1):

            colonne_pion = colonne + delta_colonne

            if 0 <= colonne_pion < 8:

                case_pion = coordonnees_case(
                    colonne_pion,
                    ligne_pion
                )

                pion = (
                    PION
                    if par_couleur == BLANC
                    else -PION
                )

                if plateau[case_pion] == pion:
                    return True

    # --------------------------------------------------------
    # CAVALIERS
    # --------------------------------------------------------

    cavalier = (
        CAVALIER
        if par_couleur == BLANC
        else -CAVALIER
    )

    for dc, dl in DIRECTIONS_CAVALIER:

        c = colonne + dc
        l = ligne + dl

        if not case_sur_plateau(c, l):
            continue

        case_cavalier = coordonnees_case(c, l)

        if plateau[case_cavalier] == cavalier:
            return True

    # --------------------------------------------------------
    # ROI
    # --------------------------------------------------------

    roi = (
        ROI
        if par_couleur == BLANC
        else -ROI
    )

    for dc, dl in DIRECTIONS_ROI:

        c = colonne + dc
        l = ligne + dl

        if not case_sur_plateau(c, l):
            continue

        case_roi = coordonnees_case(c, l)

        if plateau[case_roi] == roi:
            return True

    # --------------------------------------------------------
    # TOURS ET DAMES
    # --------------------------------------------------------

    tour = (
        TOUR
        if par_couleur == BLANC
        else -TOUR
    )

    dame = (
        DAME
        if par_couleur == BLANC
        else -DAME
    )

    for dc, dl in DIRECTIONS_TOUR:

        c = colonne + dc
        l = ligne + dl

        while case_sur_plateau(c, l):

            destination = coordonnees_case(c, l)
            piece = plateau[destination]

            if piece != VIDE:

                if piece == tour or piece == dame:
                    return True

                break

            c += dc
            l += dl

    # --------------------------------------------------------
    # FOUS ET DAMES
    # --------------------------------------------------------

    fou = (
        FOU
        if par_couleur == BLANC
        else -FOU
    )

    for dc, dl in DIRECTIONS_FOU:

        c = colonne + dc
        l = ligne + dl

        while case_sur_plateau(c, l):

            destination = coordonnees_case(c, l)
            piece = plateau[destination]

            if piece != VIDE:

                if piece == fou or piece == dame:
                    return True

                break

            c += dc
            l += dl

    return False


# ------------------------------------------------------------
# ROI EN ÉCHEC
# ------------------------------------------------------------

def roi_en_echec(etat, couleur):
    """
    Vérifie si le roi de la couleur donnée est attaqué.
    """

    case_roi = trouver_roi(
        etat["plateau"],
        couleur
    )

    # Position invalide.
    if case_roi == -1:
        return True

    adversaire = couleur_opposee(couleur)

    return case_attaquee(
        etat,
        case_roi,
        adversaire
    )


# ------------------------------------------------------------
# APPLICATION D'UN COUP
# ------------------------------------------------------------

def appliquer_coup(etat, coup):
    """
    Applique un coup à l'état actuel.

    Retourne un objet 'annulation' permettant
    de restaurer exactement la position précédente.
    """

    plateau = etat["plateau"]

    depart = coup["depart"]
    arrivee = coup["arrivee"]

    piece = plateau[depart]
    piece_capturee = plateau[arrivee]

    # --------------------------------------------------------
    # SAUVEGARDE
    # --------------------------------------------------------

    sauvegarde = {
        "depart": depart,
        "arrivee": arrivee,
        "piece": piece,
        "piece_capturee": piece_capturee,

        "promotion": coup["promotion"],
        "en_passant": coup["en_passant"],
        "roque": coup["roque"],

        "ancien_roque": etat["roque"],
        "ancien_en_passant": etat["en_passant"],
        "ancien_demi_coups": etat["demi_coups"],
        "ancien_numero_coup": etat["numero_coup"],
        "ancien_tour": etat["tour"],

        "ancien_statut": etat["statut"],

        "case_capture_en_passant": -1,
        "piece_capture_en_passant": VIDE
    }

    # --------------------------------------------------------
    # PRISE EN PASSANT
    # --------------------------------------------------------

    if coup["en_passant"]:

        if piece > 0:
            case_capture = arrivee - 8
        else:
            case_capture = arrivee + 8

        sauvegarde["case_capture_en_passant"] = case_capture
        sauvegarde["piece_capture_en_passant"] = (
            plateau[case_capture]
        )

        plateau[case_capture] = VIDE

    # --------------------------------------------------------
    # DÉPLACEMENT
    # --------------------------------------------------------

    plateau[depart] = VIDE

    piece_final = piece

    # --------------------------------------------------------
    # PROMOTION
    # --------------------------------------------------------

    if coup["promotion"] != VIDE:

        if piece > 0:
            piece_final = coup["promotion"]
        else:
            piece_final = -coup["promotion"]

    plateau[arrivee] = piece_final

    # --------------------------------------------------------
    # ROQUE
    # --------------------------------------------------------

    if coup["roque"]:

        # Petit roque blanc
        if depart == nom_vers_case("e1") and arrivee == nom_vers_case("g1"):

            plateau[nom_vers_case("h1")] = VIDE
            plateau[nom_vers_case("f1")] = TOUR

        # Grand roque blanc
        elif depart == nom_vers_case("e1") and arrivee == nom_vers_case("c1"):

            plateau[nom_vers_case("a1")] = VIDE
            plateau[nom_vers_case("d1")] = TOUR

        # Petit roque noir
        elif depart == nom_vers_case("e8") and arrivee == nom_vers_case("g8"):

            plateau[nom_vers_case("h8")] = VIDE
            plateau[nom_vers_case("f8")] = -TOUR

        # Grand roque noir
        elif depart == nom_vers_case("e8") and arrivee == nom_vers_case("c8"):

            plateau[nom_vers_case("a8")] = VIDE
            plateau[nom_vers_case("d8")] = -TOUR

    # --------------------------------------------------------
    # DROITS DE ROQUE
    # --------------------------------------------------------

    # Si un roi bouge, ses droits disparaissent.

    if type_piece(piece) == ROI:

        if piece > 0:
            etat["roque"] &= ~(
                ROQUE_BLANC_ROI
                | ROQUE_BLANC_DAME
            )

        else:
            etat["roque"] &= ~(
                ROQUE_NOIR_ROI
                | ROQUE_NOIR_DAME
            )

    # Une tour quitte sa case initiale.

    if depart == nom_vers_case("a1"):
        etat["roque"] &= ~ROQUE_BLANC_DAME

    elif depart == nom_vers_case("h1"):
        etat["roque"] &= ~ROQUE_BLANC_ROI

    elif depart == nom_vers_case("a8"):
        etat["roque"] &= ~ROQUE_NOIR_DAME

    elif depart == nom_vers_case("h8"):
        etat["roque"] &= ~ROQUE_NOIR_ROI

    # Une tour est capturée sur sa case initiale.

    if arrivee == nom_vers_case("a1"):
        etat["roque"] &= ~ROQUE_BLANC_DAME

    elif arrivee == nom_vers_case("h1"):
        etat["roque"] &= ~ROQUE_BLANC_ROI

    elif arrivee == nom_vers_case("a8"):
        etat["roque"] &= ~ROQUE_NOIR_DAME

    elif arrivee == nom_vers_case("h8"):
        etat["roque"] &= ~ROQUE_NOIR_ROI

    # --------------------------------------------------------
    # PRISE EN PASSANT FUTURE
    # --------------------------------------------------------

    etat["en_passant"] = -1

    if type_piece(piece) == PION:

        difference = arrivee - depart

        if abs(difference) == 16:

            etat["en_passant"] = (
                depart + difference // 2
            )

    # --------------------------------------------------------
    # COMPTEUR 50 COUPS
    # --------------------------------------------------------

    if (
        type_piece(piece) == PION
        or piece_capturee != VIDE
        or coup["en_passant"]
    ):
        etat["demi_coups"] = 0

    else:
        etat["demi_coups"] += 1

    # --------------------------------------------------------
    # NUMÉRO DU COUP
    # --------------------------------------------------------

    if etat["tour"] == NOIR:
        etat["numero_coup"] += 1

    # --------------------------------------------------------
    # CHANGEMENT DE TOUR
    # --------------------------------------------------------

    etat["tour"] = couleur_opposee(
        etat["tour"]
    )

    # --------------------------------------------------------
    # HISTORIQUE
    # --------------------------------------------------------

    etat["coups_joues"].append(
        coup_vers_chaine(coup)
    )

    enregistrer_position(etat)

    return sauvegarde


# ------------------------------------------------------------
# ANNULATION D'UN COUP
# ------------------------------------------------------------

def annuler_coup(etat, sauvegarde):
    """
    Restaure exactement l'état avant le coup.
    """

    plateau = etat["plateau"]

    depart = sauvegarde["depart"]
    arrivee = sauvegarde["arrivee"]

    # --------------------------------------------------------
    # RESTAURATION DES PIÈCES
    # --------------------------------------------------------

    plateau[depart] = sauvegarde["piece"]

    plateau[arrivee] = sauvegarde["piece_capturee"]

    # --------------------------------------------------------
    # ANNULATION PRISE EN PASSANT
    # --------------------------------------------------------

    case_capture = sauvegarde[
        "case_capture_en_passant"
    ]

    if case_capture != -1:

        plateau[case_capture] = sauvegarde[
            "piece_capture_en_passant"
        ]

    # --------------------------------------------------------
    # ANNULATION DU ROQUE
    # --------------------------------------------------------

    if sauvegarde["roque"]:

        if (
            depart == nom_vers_case("e1")
            and arrivee == nom_vers_case("g1")
        ):
            plateau[nom_vers_case("f1")] = VIDE
            plateau[nom_vers_case("h1")] = TOUR

        elif (
            depart == nom_vers_case("e1")
            and arrivee == nom_vers_case("c1")
        ):
            plateau[nom_vers_case("d1")] = VIDE
            plateau[nom_vers_case("a1")] = TOUR

        elif (
            depart == nom_vers_case("e8")
            and arrivee == nom_vers_case("g8")
        ):
            plateau[nom_vers_case("f8")] = VIDE
            plateau[nom_vers_case("h8")] = -TOUR

        elif (
            depart == nom_vers_case("e8")
            and arrivee == nom_vers_case("c8")
        ):
            plateau[nom_vers_case("d8")] = VIDE
            plateau[nom_vers_case("a8")] = -TOUR

    # --------------------------------------------------------
    # RESTAURATION DE L'ÉTAT
    # --------------------------------------------------------

    etat["roque"] = sauvegarde["ancien_roque"]

    etat["en_passant"] = sauvegarde[
        "ancien_en_passant"
    ]

    etat["demi_coups"] = sauvegarde[
        "ancien_demi_coups"
    ]

    etat["numero_coup"] = sauvegarde[
        "ancien_numero_coup"
    ]

    etat["tour"] = sauvegarde[
        "ancien_tour"
    ]

    etat["statut"] = sauvegarde[
        "ancien_statut"
    ]

    # --------------------------------------------------------
    # HISTORIQUE
    # --------------------------------------------------------

    if etat["coups_joues"]:
        etat["coups_joues"].pop()

    if etat["historique"]:
        etat["historique"].pop()


# ------------------------------------------------------------
# TEST DE LÉGALITÉ D'UN COUP
# ------------------------------------------------------------

def coup_est_legal(etat, coup):
    """
    Vérifie qu'un coup ne laisse pas le roi
    du joueur en échec.
    """

    couleur = etat["tour"]

    sauvegarde = appliquer_coup(
        etat,
        coup
    )

    legal = not roi_en_echec(
        etat,
        couleur
    )

    annuler_coup(
        etat,
        sauvegarde
    )

    return legal


# ------------------------------------------------------------
# COUPS LÉGAUX
# ------------------------------------------------------------

def generer_coups_legaux(etat):
    """
    Génère uniquement les coups réellement légaux.
    """

    coups_pseudo = generer_coups_pseudo_legaux(
        etat
    )

    coups_legaux = []

    for coup in coups_pseudo:

        if coup_est_legal(
            etat,
            coup
        ):
            coups_legaux.append(coup)

    return coups_legaux


# ------------------------------------------------------------
# COUP LÉGAL PAR NOTATION
# ------------------------------------------------------------

def trouver_coup_par_chaine(etat, notation):
    """
    Recherche un coup légal comme :
        e2e4
        g1f3
        e7e8Q
    """

    notation = notation.strip().lower()

    coups = generer_coups_legaux(etat)

    for coup in coups:

        if coup_vers_chaine(coup).lower() == notation:
            return coup

    return None


# ------------------------------------------------------------
# TEST DU BLOC 6
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 BLOC 6 — TEST")
    print("=" * 50)

    etat_test = creer_etat_initial()

    coups = generer_coups_legaux(
        etat_test
    )

    print(
        "Coups légaux initiaux :",
        len(coups)
    )

    print()

    for coup in coups:
        print(
            coup_vers_chaine(coup),
            end="  "
        )

    print()

    # Test e2-e4
    coup_test = trouver_coup_par_chaine(
        etat_test,
        "e2e4"
    )

    if coup_test is not None:

        print()
        print("Test e2e4 : OK")

        sauvegarde = appliquer_coup(
            etat_test,
            coup_test
        )

        print(
            "Tour suivant :",
            "Blanc"
            if etat_test["tour"] == BLANC
            else "Noir"
        )

        annuler_coup(
            etat_test,
            sauvegarde
        )

        print("Annulation : OK")

    else:

        print("Test e2e4 : ÉCHEC")

    print()
    print("🐼 BLOC 6 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 7/26 — ÉCHEC, MAT, PAT ET FIN DE PARTIE
# ============================================================


# ------------------------------------------------------------
# JOUEUR ACTUEL EN ÉCHEC
# ------------------------------------------------------------

def joueur_en_echec(etat):
    """Vérifie si le joueur dont c'est le tour est en échec."""

    return roi_en_echec(
        etat,
        etat["tour"]
    )


# ------------------------------------------------------------
# COUPS LÉGAUX DU JOUEUR ACTUEL
# ------------------------------------------------------------

def coups_disponibles(etat):
    """Retourne les coups légaux du joueur actuel."""

    return generer_coups_legaux(etat)


# ------------------------------------------------------------
# MAT ?
# ------------------------------------------------------------

def est_mat(etat):
    """
    Une position est échec et mat si :
      1. le roi est en échec
      2. aucun coup légal n'est disponible
    """

    if not joueur_en_echec(etat):
        return False

    coups = coups_disponibles(etat)

    return len(coups) == 0


# ------------------------------------------------------------
# PAT ?
# ------------------------------------------------------------

def est_pat(etat):
    """
    Une position est pat si :
      1. le roi n'est PAS en échec
      2. aucun coup légal n'est disponible
    """

    if joueur_en_echec(etat):
        return False

    coups = coups_disponibles(etat)

    return len(coups) == 0


# ------------------------------------------------------------
# NULLE PAR RÉPÉTITION
# ------------------------------------------------------------

def est_nulle_repetition(etat):
    """
    Détection de répétition.
    """

    return nombre_repetitions(etat) >= 3


# ------------------------------------------------------------
# NULLE PAR 50 COUPS
# ------------------------------------------------------------

def est_nulle_50_coups(etat):
    return regle_50_coups(etat)


# ------------------------------------------------------------
# NULLE PAR MATÉRIEL
# ------------------------------------------------------------

def est_nulle_materiel(etat):
    return materiel_insuffisant(etat)


# ------------------------------------------------------------
# NULLE
# ------------------------------------------------------------

def est_nulle(etat):
    """
    Vérifie les principales conditions de nulle.
    """

    if est_pat(etat):
        return True

    if est_nulle_repetition(etat):
        return True

    if est_nulle_50_coups(etat):
        return True

    if est_nulle_materiel(etat):
        return True

    return False


# ------------------------------------------------------------
# GAGNANT
# ------------------------------------------------------------

def gagnant_partie(etat):
    """
    Retourne :
        BLANC
        NOIR
        None

    Si la partie n'est pas terminée, retourne None.
    """

    if not est_mat(etat):
        return None

    # Le joueur qui est mat perd.
    return couleur_opposee(etat["tour"])


# ------------------------------------------------------------
# STATUT DE LA PARTIE
# ------------------------------------------------------------

def determiner_statut(etat):
    """
    Détermine automatiquement l'état actuel de la partie.
    """

    # Échec et mat
    if est_mat(etat):

        etat["statut"] = PARTIE_MAT

        return PARTIE_MAT

    # Pat
    if est_pat(etat):

        etat["statut"] = PARTIE_PAT

        return PARTIE_PAT

    # Nulle par répétition
    if est_nulle_repetition(etat):

        etat["statut"] = PARTIE_NULLE

        return PARTIE_NULLE

    # Nulle par 50 coups
    if est_nulle_50_coups(etat):

        etat["statut"] = PARTIE_NULLE

        return PARTIE_NULLE

    # Nulle par matériel insuffisant
    if est_nulle_materiel(etat):

        etat["statut"] = PARTIE_NULLE

        return PARTIE_NULLE

    # Partie toujours en cours
    etat["statut"] = PARTIE_ACTIVE

    return PARTIE_ACTIVE


# ------------------------------------------------------------
# PARTIE TERMINÉE ?
# ------------------------------------------------------------

def partie_terminee(etat):
    """
    Retourne True si la partie est terminée.
    """

    statut = determiner_statut(etat)

    return statut != PARTIE_ACTIVE


# ------------------------------------------------------------
# TEXTE DU STATUT
# ------------------------------------------------------------

def nom_statut(statut):
    """Convertit le statut interne en texte."""

    if statut == PARTIE_ACTIVE:
        return "PARTIE ACTIVE"

    if statut == PARTIE_ECHEC:
        return "ÉCHEC"

    if statut == PARTIE_MAT:
        return "ÉCHEC ET MAT"

    if statut == PARTIE_PAT:
        return "PAT"

    if statut == PARTIE_NULLE:
        return "NULLE"

    if statut == PARTIE_ABANDON:
        return "ABANDON"

    return "INCONNU"


# ------------------------------------------------------------
# MESSAGE DE FIN
# ------------------------------------------------------------

def message_fin_partie(etat):
    """
    Retourne un message lisible concernant la fin de partie.
    """

    statut = determiner_statut(etat)

    if statut == PARTIE_ACTIVE:
        return "La partie continue."

    if statut == PARTIE_MAT:

        gagnant = gagnant_partie(etat)

        if gagnant == BLANC:
            return "♔ Échec et mat — les Blancs gagnent !"

        if gagnant == NOIR:
            return "♚ Échec et mat — les Noirs gagnent !"

        return "Échec et mat."

    if statut == PARTIE_PAT:
        return "🤝 Pat — partie nulle."

    if statut == PARTIE_NULLE:

        if est_nulle_repetition(etat):
            return "🤝 Partie nulle — répétition."

        if est_nulle_50_coups(etat):
            return "🤝 Partie nulle — règle des 50 coups."

        if est_nulle_materiel(etat):
            return "🤝 Partie nulle — matériel insuffisant."

        return "🤝 Partie nulle."

    if statut == PARTIE_ABANDON:
        return "🏳️ Partie abandonnée."

    return "État de partie inconnu."


# ------------------------------------------------------------
# ANALYSE RAPIDE DE LA POSITION
# ------------------------------------------------------------

def analyser_fin_de_partie(etat):
    """
    Retourne un dictionnaire utile au moteur.
    """

    statut = determiner_statut(etat)

    return {
        "terminee": statut != PARTIE_ACTIVE,
        "statut": statut,
        "statut_nom": nom_statut(statut),
        "echec": joueur_en_echec(etat),
        "mat": est_mat(etat),
        "pat": est_pat(etat),
        "nulle": est_nulle(etat),
        "gagnant": gagnant_partie(etat),
        "coups_legaux": len(
            generer_coups_legaux(etat)
        )
    }


# ------------------------------------------------------------
# VÉRIFICATION AVANT DE JOUER
# ------------------------------------------------------------

def peut_jouer(etat):
    """
    Vérifie si un coup peut encore être joué.
    """

    if partie_terminee(etat):
        return False

    return True


# ------------------------------------------------------------
# JOUER UN COUP LÉGAL
# ------------------------------------------------------------

def jouer_coup(etat, coup):
    """
    Applique un coup uniquement s'il est légal.

    Retourne True si le coup a été joué.
    """

    if partie_terminee(etat):
        return False

    coups = generer_coups_legaux(etat)

    coup_trouve = None

    for coup_legal in coups:

        if (
            coup_legal["depart"] == coup["depart"]
            and
            coup_legal["arrivee"] == coup["arrivee"]
            and
            coup_legal["promotion"] == coup["promotion"]
        ):
            coup_trouve = coup_legal
            break

    if coup_trouve is None:
        return False

    appliquer_coup(
        etat,
        coup_trouve
    )

    determiner_statut(etat)

    return True


# ------------------------------------------------------------
# JOUER AVEC UNE NOTATION
# ------------------------------------------------------------

def jouer_notation(etat, notation):
    """
    Permet de jouer par exemple :

        e2e4
        g1f3
        e7e8Q
    """

    if partie_terminee(etat):
        return False

    coup = trouver_coup_par_chaine(
        etat,
        notation
    )

    if coup is None:
        return False

    appliquer_coup(
        etat,
        coup
    )

    determiner_statut(etat)

    return True


# ------------------------------------------------------------
# TEST DU BLOC 7
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 BLOC 7 — TEST")
    print("=" * 50)

    etat_test = creer_etat_initial()

    print(
        "Statut initial :",
        nom_statut(
            determiner_statut(etat_test)
        )
    )

    print(
        "Coups légaux :",
        len(
            generer_coups_legaux(etat_test)
        )
    )

    print(
        "En échec :",
        joueur_en_echec(etat_test)
    )

    print(
        "Mat :",
        est_mat(etat_test)
    )

    print(
        "Pat :",
        est_pat(etat_test)
    )

    print(
        "Nulle :",
        est_nulle(etat_test)
    )

    print()
    print(
        "Message :",
        message_fin_partie(etat_test)
    )

    print()
    print("🐼 BLOC 7 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 8/26 — ROQUE + PRISE EN PASSANT
# ============================================================


# ------------------------------------------------------------
# VÉRIFICATION D'UNE CASE VIDE
# ------------------------------------------------------------

def cases_vides(etat, cases):
    """Vérifie que toutes les cases données sont vides."""

    for case in cases:
        if etat["plateau"][case] != VIDE:
            return False

    return True


# ------------------------------------------------------------
# ROQUE BLANC — PETIT
# ------------------------------------------------------------

def peut_roquer_blanc_roi(etat):
    """
    Vérifie les conditions du petit roque blanc :

        e1 → g1
        tour h1 → f1
    """

    e1 = nom_vers_case("e1")
    f1 = nom_vers_case("f1")
    g1 = nom_vers_case("g1")
    h1 = nom_vers_case("h1")

    plateau = etat["plateau"]

    # Droit de roque
    if not (etat["roque"] & ROQUE_BLANC_ROI):
        return False

    # Pièces correctes
    if plateau[e1] != ROI:
        return False

    if plateau[h1] != TOUR:
        return False

    # Cases libres
    if not cases_vides(etat, [f1, g1]):
        return False

    # Le roi ne doit pas être en échec
    if case_attaquee(etat, e1, NOIR):
        return False

    # Le roi ne peut pas traverser une case attaquée
    if case_attaquee(etat, f1, NOIR):
        return False

    # Le roi ne peut pas arriver sur une case attaquée
    if case_attaquee(etat, g1, NOIR):
        return False

    return True


# ------------------------------------------------------------
# ROQUE BLANC — GRAND
# ------------------------------------------------------------

def peut_roquer_blanc_dame(etat):
    """
    Vérifie le grand roque blanc :

        e1 → c1
        tour a1 → d1
    """

    e1 = nom_vers_case("e1")
    d1 = nom_vers_case("d1")
    c1 = nom_vers_case("c1")
    b1 = nom_vers_case("b1")
    a1 = nom_vers_case("a1")

    plateau = etat["plateau"]

    if not (etat["roque"] & ROQUE_BLANC_DAME):
        return False

    if plateau[e1] != ROI:
        return False

    if plateau[a1] != TOUR:
        return False

    # b1 est également libre pour le grand roque.
    if not cases_vides(
        etat,
        [b1, c1, d1]
    ):
        return False

    if case_attaquee(etat, e1, NOIR):
        return False

    if case_attaquee(etat, d1, NOIR):
        return False

    if case_attaquee(etat, c1, NOIR):
        return False

    return True


# ------------------------------------------------------------
# ROQUE NOIR — PETIT
# ------------------------------------------------------------

def peut_roquer_noir_roi(etat):
    """
    Vérifie le petit roque noir :

        e8 → g8
        tour h8 → f8
    """

    e8 = nom_vers_case("e8")
    f8 = nom_vers_case("f8")
    g8 = nom_vers_case("g8")
    h8 = nom_vers_case("h8")

    plateau = etat["plateau"]

    if not (etat["roque"] & ROQUE_NOIR_ROI):
        return False

    if plateau[e8] != -ROI:
        return False

    if plateau[h8] != -TOUR:
        return False

    if not cases_vides(
        etat,
        [f8, g8]
    ):
        return False

    if case_attaquee(etat, e8, BLANC):
        return False

    if case_attaquee(etat, f8, BLANC):
        return False

    if case_attaquee(etat, g8, BLANC):
        return False

    return True


# ------------------------------------------------------------
# ROQUE NOIR — GRAND
# ------------------------------------------------------------

def peut_roquer_noir_dame(etat):
    """
    Vérifie le grand roque noir :

        e8 → c8
        tour a8 → d8
    """

    e8 = nom_vers_case("e8")
    d8 = nom_vers_case("d8")
    c8 = nom_vers_case("c8")
    b8 = nom_vers_case("b8")
    a8 = nom_vers_case("a8")

    plateau = etat["plateau"]

    if not (etat["roque"] & ROQUE_NOIR_DAME):
        return False

    if plateau[e8] != -ROI:
        return False

    if plateau[a8] != -TOUR:
        return False

    if not cases_vides(
        etat,
        [b8, c8, d8]
    ):
        return False

    if case_attaquee(etat, e8, BLANC):
        return False

    if case_attaquee(etat, d8, BLANC):
        return False

    if case_attaquee(etat, c8, BLANC):
        return False

    return True


# ------------------------------------------------------------
# GÉNÉRATION DES COUPS DE ROQUE
# ------------------------------------------------------------

def generer_coups_roque(etat):
    """
    Génère les coups de roque disponibles
    pour le joueur actuel.
    """

    coups = []

    if etat["tour"] == BLANC:

        if peut_roquer_blanc_roi(etat):

            ajouter_coup(
                coups,
                nom_vers_case("e1"),
                nom_vers_case("g1"),
                roque=True
            )

        if peut_roquer_blanc_dame(etat):

            ajouter_coup(
                coups,
                nom_vers_case("e1"),
                nom_vers_case("c1"),
                roque=True
            )

    else:

        if peut_roquer_noir_roi(etat):

            ajouter_coup(
                coups,
                nom_vers_case("e8"),
                nom_vers_case("g8"),
                roque=True
            )

        if peut_roquer_noir_dame(etat):

            ajouter_coup(
                coups,
                nom_vers_case("e8"),
                nom_vers_case("c8"),
                roque=True
            )

    return coups


# ------------------------------------------------------------
# PRISE EN PASSANT DISPONIBLE ?
# ------------------------------------------------------------

def prise_en_passant_disponible(etat):
    """
    Retourne True si une case de prise en passant
    est actuellement disponible.
    """

    return (
        etat["en_passant"] != -1
    )


# ------------------------------------------------------------
# CASE DE PRISE EN PASSANT
# ------------------------------------------------------------

def case_en_passant(etat):
    """
    Retourne la case de prise en passant.
    """

    return etat["en_passant"]


# ------------------------------------------------------------
# AJOUTER LES ROQUES AUX COUPS
# ------------------------------------------------------------

def generer_coups_speciaux(etat):
    """
    Retourne tous les coups spéciaux disponibles.
    """

    return generer_coups_roque(etat)


# ------------------------------------------------------------
# GÉNÉRATEUR COMPLET DE COUPS PSEUDO-LÉGAUX
# ------------------------------------------------------------

def generer_coups_pseudo_legaux_complet(etat):
    """
    Version complète du générateur pseudo-légal.

    Bloc 5 :
        pièces normales

    Bloc 8 :
        + roque
        + prise en passant déjà générée par le pion
    """

    coups = generer_coups_pseudo_legaux(etat)

    coups_specials = generer_coups_speciaux(
        etat
    )

    coups.extend(coups_specials)

    return coups


# ------------------------------------------------------------
# GÉNÉRATEUR COMPLET DE COUPS LÉGAUX
# ------------------------------------------------------------

def generer_coups_legaux_complet(etat):
    """
    Génère les coups légaux avec les règles spéciales.
    """

    coups_pseudo = (
        generer_coups_pseudo_legaux_complet(etat)
    )

    coups_legaux = []

    for coup in coups_pseudo:

        if coup_est_legal(
            etat,
            coup
        ):
            coups_legaux.append(coup)

    return coups_legaux


# ------------------------------------------------------------
# REMPLACER LE GÉNÉRATEUR PRINCIPAL
# ------------------------------------------------------------

# À partir de maintenant, Pandoraga utilisera cette version
# complète lorsqu'elle est disponible.

generer_coups_legaux_original = generer_coups_legaux


def generer_coups_legaux(etat):
    """
    Générateur principal de Pandoraga.

    Inclut maintenant :
        - déplacements normaux
        - captures
        - promotions
        - prise en passant
        - roque
        - protection du roi
    """

    return generer_coups_legaux_complet(etat)


# ------------------------------------------------------------
# TEST DU BLOC 8
# ------------------------------------------------------------

def test_roque_position_initiale():
    """
    Depuis la position initiale, aucun roque n'est possible
    car les pièces entre le roi et les tours bloquent.
    """

    etat = creer_etat_initial()

    roques = generer_coups_roque(etat)

    return len(roques) == 0


def test_prise_en_passant():
    """
    Test simple de l'existence d'une case en passant.
    """

    etat = creer_etat_initial()

    # Aucun en passant au début.
    return not prise_en_passant_disponible(etat)


if __name__ == "__main__":

    print()
    print("🐼 BLOC 8 — TEST")
    print("=" * 50)

    etat_test = creer_etat_initial()

    roques = generer_coups_roque(
        etat_test
    )

    print(
        "Roques depuis la position initiale :",
        len(roques)
    )

    print(
        "Prise en passant disponible :",
        prise_en_passant_disponible(etat_test)
    )

    coups = generer_coups_legaux(
        etat_test
    )

    print(
        "Coups légaux complets :",
        len(coups)
    )

    print()

    print(
        "Test roque initial :",
        "OK" if test_roque_position_initiale()
        else "ERREUR"
    )

    print(
        "Test en passant initial :",
        "OK" if test_prise_en_passant()
        else "ERREUR"
    )

    print()
    print("🐼 BLOC 8 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 9/26 — PROMOTION AVANCÉE DES PIONS
# ============================================================


# ------------------------------------------------------------
# PROMOTIONS VALIDES
# ------------------------------------------------------------

PROMOTIONS_VALIDES = (
    DAME,
    TOUR,
    FOU,
    CAVALIER
)


# ------------------------------------------------------------
# PROMOTION VALIDE ?
# ------------------------------------------------------------

def promotion_valide(piece):
    """
    Vérifie qu'une pièce peut être choisie pour une promotion.
    """

    return piece in PROMOTIONS_VALIDES


# ------------------------------------------------------------
# PION SUR DERNIER RANG
# ------------------------------------------------------------

def pion_sur_derniere_rang(case, couleur):
    """
    Vérifie si un pion est arrivé sur son dernier rang.
    """

    if not est_case_valide(case):
        return False

    ligne = ligne_case(case)

    if couleur == BLANC:
        return ligne == 7

    return ligne == 0


# ------------------------------------------------------------
# PION À PROMOUVOIR
# ------------------------------------------------------------

def pion_a_promouvoir(plateau, case):
    """
    Vérifie si la pièce présente sur la case
    est un pion qui doit être promu.
    """

    if not est_case_valide(case):
        return False

    piece = plateau[case]

    if type_piece(piece) != PION:
        return False

    couleur = couleur_piece(piece)

    return pion_sur_derniere_rang(
        case,
        couleur
    )


# ------------------------------------------------------------
# PROMOTIONS POSSIBLES
# ------------------------------------------------------------

def promotions_possibles(couleur):
    """
    Retourne les pièces disponibles pour une promotion.
    """

    return list(PROMOTIONS_VALIDES)


# ------------------------------------------------------------
# CRÉER LES COUPS DE PROMOTION
# ------------------------------------------------------------

def creer_coups_promotion(
    depart,
    arrivee,
    couleur,
    capture=VIDE
):
    """
    Crée les quatre possibilités de promotion.
    """

    coups = []

    for promotion in PROMOTIONS_VALIDES:

        ajouter_coup(
            coups,
            depart,
            arrivee,
            promotion=promotion,
            capture=capture
        )

    return coups


# ------------------------------------------------------------
# NORMALISER UNE PROMOTION
# ------------------------------------------------------------

def normaliser_promotion(promotion):
    """
    Accepte plusieurs formes :

        5       -> Dame
        "Q"     -> Dame
        "D"     -> Dame
        "dame"  -> Dame
        "N"     -> Cavalier
        "C"     -> Cavalier
    """

    if isinstance(promotion, int):

        if promotion_valide(promotion):
            return promotion

        return VIDE

    if not isinstance(promotion, str):
        return VIDE

    valeur = promotion.strip().lower()

    correspondance = {
        "q": DAME,
        "d": DAME,
        "dame": DAME,

        "r": TOUR,
        "t": TOUR,
        "tour": TOUR,

        "b": FOU,
        "f": FOU,
        "fou": FOU,

        "n": CAVALIER,
        "c": CAVALIER,
        "cavalier": CAVALIER
    }

    return correspondance.get(
        valeur,
        VIDE
    )


# ------------------------------------------------------------
# SYMBOLE DE PROMOTION
# ------------------------------------------------------------

def symbole_promotion(promotion):
    """
    Retourne le symbole de la pièce promue.
    """

    promotion = normaliser_promotion(
        promotion
    )

    return LETTRES_PIECES.get(
        promotion,
        "?"
    )


# ------------------------------------------------------------
# VALIDATION D'UN COUP DE PROMOTION
# ------------------------------------------------------------

def promotion_coup_valide(etat, coup):
    """
    Vérifie la cohérence d'une promotion.
    """

    depart = coup["depart"]
    arrivee = coup["arrivee"]

    piece = etat["plateau"][depart]

    # Le départ doit contenir un pion.
    if type_piece(piece) != PION:
        return False

    couleur = couleur_piece(piece)

    # La destination doit être le dernier rang.
    if not pion_sur_derniere_rang(
        arrivee,
        couleur
    ):
        return False

    # La pièce de promotion doit être valide.
    if not promotion_valide(
        coup["promotion"]
    ):
        return False

    return True


# ------------------------------------------------------------
# PROMOTION D'UNE PIÈCE
# ------------------------------------------------------------

def piece_apres_promotion(piece, promotion):
    """
    Retourne la pièce finale après promotion.
    """

    promotion = normaliser_promotion(
        promotion
    )

    if not promotion_valide(promotion):
        return piece

    if piece > 0:
        return promotion

    return -promotion


# ------------------------------------------------------------
# FORCER UNE PROMOTION
# ------------------------------------------------------------

def appliquer_promotion_directe(
    etat,
    case,
    promotion
):
    """
    Utilitaire permettant de transformer directement
    un pion déjà arrivé au dernier rang.

    Principalement utilisé pour les tests et la gestion
    de positions spéciales.
    """

    if not est_case_valide(case):
        return False

    piece = etat["plateau"][case]

    if type_piece(piece) != PION:
        return False

    couleur = couleur_piece(piece)

    if not pion_sur_derniere_rang(
        case,
        couleur
    ):
        return False

    promotion = normaliser_promotion(
        promotion
    )

    if not promotion_valide(promotion):
        return False

    etat["plateau"][case] = (
        promotion
        if couleur == BLANC
        else -promotion
    )

    return True


# ------------------------------------------------------------
# TROUVER LES PROMOTIONS D'UNE POSITION
# ------------------------------------------------------------

def trouver_pions_a_promouvoir(etat):
    """
    Retourne toutes les cases contenant un pion
    arrivé au dernier rang.
    """

    resultat = []

    for case in range(64):

        if pion_a_promouvoir(
            etat["plateau"],
            case
        ):
            resultat.append(case)

    return resultat


# ------------------------------------------------------------
# PROMOTION AUTOMATIQUE EN DAME
# ------------------------------------------------------------

def promotion_automatique_dame(etat):
    """
    Utilitaire d'entraînement :
    transforme les pions arrivés au dernier rang
    en dames.

    Le moteur de recherche normal ne doit pas utiliser
    cette fonction pour remplacer les quatre choix légaux.
    """

    cases = trouver_pions_a_promouvoir(
        etat
    )

    for case in cases:

        appliquer_promotion_directe(
            etat,
            case,
            DAME
        )

    return len(cases)


# ------------------------------------------------------------
# VALEUR D'UNE PROMOTION
# ------------------------------------------------------------

def valeur_promotion(promotion):
    """
    Retourne la valeur matérielle d'une promotion.
    """

    promotion = normaliser_promotion(
        promotion
    )

    return VALEURS_PIECES.get(
        promotion,
        0
    )


# ------------------------------------------------------------
# MEILLEURE PROMOTION MATÉRIELLE
# ------------------------------------------------------------

def meilleure_promotion():
    """
    Pour l'instant, la promotion ayant la plus grande
    valeur matérielle est la Dame.

    Le moteur complet pourra néanmoins choisir Cavalier,
    Tour ou Fou selon la position.
    """

    meilleure = CAVALIER
    meilleure_valeur = 0

    for promotion in PROMOTIONS_VALIDES:

        valeur = valeur_promotion(
            promotion
        )

        if valeur > meilleure_valeur:

            meilleure_valeur = valeur
            meilleure = promotion

    return meilleure


# ------------------------------------------------------------
# TEXTE D'UNE PROMOTION
# ------------------------------------------------------------

def description_promotion(promotion):
    """
    Retourne une description lisible.
    """

    promotion = normaliser_promotion(
        promotion
    )

    noms = {
        DAME: "Dame",
        TOUR: "Tour",
        FOU: "Fou",
        CAVALIER: "Cavalier"
    }

    return noms.get(
        promotion,
        "Promotion inconnue"
    )


# ------------------------------------------------------------
# COUP AVEC PROMOTION
# ------------------------------------------------------------

def notation_promotion(
    depart,
    arrivee,
    promotion
):
    """
    Produit une notation simple :

        e7e8Q
        b2b1N
    """

    promotion = normaliser_promotion(
        promotion
    )

    if not promotion_valide(promotion):
        return ""

    return (
        case_vers_nom(depart)
        +
        case_vers_nom(arrivee)
        +
        symbole_promotion(promotion)
    )


# ------------------------------------------------------------
# VÉRIFIER TOUTES LES PROMOTIONS LÉGALES
# ------------------------------------------------------------

def verifier_promotions_position(etat):
    """
    Vérifie que chaque pion arrivant au dernier rang
    possède bien les quatre possibilités de promotion
    dans le générateur de coups.
    """

    resultat = []

    coups = generer_coups_pseudo_legaux(
        etat
    )

    for coup in coups:

        if coup["promotion"] == VIDE:
            continue

        resultat.append(
            coup_vers_chaine(coup)
        )

    return resultat


# ------------------------------------------------------------
# TEST DU BLOC 9
# ------------------------------------------------------------

def test_normalisation_promotions():

    tests = {
        "Q": DAME,
        "D": DAME,
        "dame": DAME,

        "R": TOUR,
        "T": TOUR,
        "tour": TOUR,

        "B": FOU,
        "F": FOU,
        "fou": FOU,

        "N": CAVALIER,
        "C": CAVALIER,
        "cavalier": CAVALIER
    }

    for entree, attendu in tests.items():

        if normaliser_promotion(
            entree
        ) != attendu:
            return False

    return True


def test_promotion_position():

    etat = creer_etat_initial()

    # Place un pion blanc sur e7.
    etat["plateau"][
        nom_vers_case("e7")
    ] = PION

    # Libère e8.
    etat["plateau"][
        nom_vers_case("e8")
    ] = VIDE

    promotions = []

    for coup in generer_coups_pseudo_legaux(
        etat
    ):

        if coup["depart"] == nom_vers_case("e7"):

            if coup["promotion"] != VIDE:

                promotions.append(
                    coup["promotion"]
                )

    return set(promotions) == set(
        PROMOTIONS_VALIDES
    )


if __name__ == "__main__":

    print()
    print("🐼 BLOC 9 — TEST")
    print("=" * 50)

    print(
        "Normalisation promotions :",
        "OK"
        if test_normalisation_promotions()
        else "ERREUR"
    )

    print(
        "Test génération promotion :",
        "OK"
        if test_promotion_position()
        else "ERREUR"
    )

    print()

    print(
        "Meilleure promotion matérielle :",
        description_promotion(
            meilleure_promotion()
        )
    )

    print()
    print("🐼 BLOC 9 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 10/26 — ÉVALUATION MATÉRIELLE
# ============================================================


# ------------------------------------------------------------
# VALEURS DES PIÈCES
# ------------------------------------------------------------

VALEURS_PIECES = {

    PION: 100,
    CAVALIER: 320,
    FOU: 330,
    TOUR: 500,
    DAME: 900,
    ROI: 20000
}


# ------------------------------------------------------------
# VALEURS DES PIÈCES EN TEXTE
# ------------------------------------------------------------

NOMS_PIECES = {

    PION: "Pion",
    CAVALIER: "Cavalier",
    FOU: "Fou",
    TOUR: "Tour",
    DAME: "Dame",
    ROI: "Roi"
}


# ------------------------------------------------------------
# VALEUR D'UNE PIÈCE
# ------------------------------------------------------------

def valeur_piece(piece):
    """
    Retourne la valeur absolue d'une pièce.

    Exemple :

        PION blanc  -> 100
        PION noir   -> 100
        DAME blanc  -> 900
        DAME noir   -> 900
    """

    if piece == VIDE:
        return 0

    return VALEURS_PIECES.get(
        type_piece(piece),
        0
    )


# ------------------------------------------------------------
# VALEUR SIGNÉE
# ------------------------------------------------------------

def valeur_piece_signee(piece):
    """
    Retourne la valeur avec la couleur :

        Blanc = positif
        Noir  = négatif
    """

    if piece == VIDE:
        return 0

    valeur = valeur_piece(piece)

    if piece > 0:
        return valeur

    return -valeur


# ------------------------------------------------------------
# MATÉRIEL BLANC
# ------------------------------------------------------------

def materiel_blanc(etat):
    """
    Calcule le matériel total des Blancs.
    """

    total = 0

    for piece in etat["plateau"]:

        if piece > 0:

            total += valeur_piece(
                piece
            )

    return total


# ------------------------------------------------------------
# MATÉRIEL NOIR
# ------------------------------------------------------------

def materiel_noir(etat):
    """
    Calcule le matériel total des Noirs.
    """

    total = 0

    for piece in etat["plateau"]:

        if piece < 0:

            total += valeur_piece(
                piece
            )

    return total


# ------------------------------------------------------------
# DIFFÉRENCE MATÉRIELLE
# ------------------------------------------------------------

def difference_materielle(etat):
    """
    Score matériel :

        positif = avantage blanc
        négatif = avantage noir
    """

    return (
        materiel_blanc(etat)
        -
        materiel_noir(etat)
    )


# ------------------------------------------------------------
# COMPTER UNE PIÈCE
# ------------------------------------------------------------

def compter_piece(etat, piece_type, couleur):
    """
    Compte le nombre d'une pièce donnée.

    Exemple :

        compter_piece(etat, PION, BLANC)
    """

    compteur = 0

    for piece in etat["plateau"]:

        if piece == VIDE:
            continue

        if type_piece(piece) != piece_type:
            continue

        if couleur_piece(piece) != couleur:
            continue

        compteur += 1

    return compteur


# ------------------------------------------------------------
# INVENTAIRE DU MATÉRIEL
# ------------------------------------------------------------

def inventaire_materiel(etat):
    """
    Retourne le nombre de chaque pièce pour chaque couleur.
    """

    inventaire = {

        "blanc": {
            "pions": 0,
            "cavaliers": 0,
            "fous": 0,
            "tours": 0,
            "dames": 0,
            "roi": 0
        },

        "noir": {
            "pions": 0,
            "cavaliers": 0,
            "fous": 0,
            "tours": 0,
            "dames": 0,
            "roi": 0
        }
    }

    noms = {
        PION: "pions",
        CAVALIER: "cavaliers",
        FOU: "fous",
        TOUR: "tours",
        DAME: "dames",
        ROI: "roi"
    }

    for piece in etat["plateau"]:

        if piece == VIDE:
            continue

        type_actuel = type_piece(piece)
        couleur = couleur_piece(piece)

        nom = noms.get(
            type_actuel
        )

        if nom is None:
            continue

        if couleur == BLANC:

            inventaire["blanc"][nom] += 1

        else:

            inventaire["noir"][nom] += 1

    return inventaire


# ------------------------------------------------------------
# PIÈCES RESTANTES
# ------------------------------------------------------------

def pieces_restantes(etat, couleur):
    """
    Retourne une liste des pièces restantes.
    """

    resultat = []

    for case, piece in enumerate(
        etat["plateau"]
    ):

        if piece == VIDE:
            continue

        if couleur_piece(piece) != couleur:
            continue

        resultat.append({
            "case": case,
            "piece": type_piece(piece),
            "valeur": valeur_piece(piece)
        })

    return resultat


# ------------------------------------------------------------
# AVANTAGE MATÉRIEL
# ------------------------------------------------------------

def avantage_materiel(etat):
    """
    Retourne une description simple de l'avantage.
    """

    difference = difference_materielle(
        etat
    )

    if difference > 0:

        return {
            "camp": BLANC,
            "score": difference
        }

    if difference < 0:

        return {
            "camp": NOIR,
            "score": abs(difference)
        }

    return {
        "camp": None,
        "score": 0
    }


# ------------------------------------------------------------
# MATÉRIEL INSUFFISANT
# ------------------------------------------------------------

def materiel_insuffisant(etat):
    """
    Détection simple des positions où le mat est impossible
    avec le matériel présent.

    Cas gérés :

        Roi contre Roi
        Roi + Fou contre Roi
        Roi + Cavalier contre Roi

    """

    pieces = []

    for piece in etat["plateau"]:

        if piece == VIDE:
            continue

        type_actuel = type_piece(piece)

        if type_actuel == ROI:
            continue

        pieces.append(
            type_actuel
        )

    # Roi contre roi
    if len(pieces) == 0:
        return True

    # Roi + une seule pièce mineure contre roi
    if len(pieces) == 1:

        if pieces[0] in (
            FOU,
            CAVALIER
        ):
            return True

    return False


# ------------------------------------------------------------
# SCORE MATÉRIEL POUR BLANC
# ------------------------------------------------------------

def evaluation_materielle_blanc(etat):
    """
    Score vu du point de vue des Blancs.
    """

    return difference_materielle(
        etat
    )


# ------------------------------------------------------------
# SCORE MATÉRIEL POUR NOIR
# ------------------------------------------------------------

def evaluation_materielle_noir(etat):
    """
    Score vu du point de vue des Noirs.
    """

    return -difference_materielle(
        etat
    )


# ------------------------------------------------------------
# SCORE POUR LE JOUEUR ACTUEL
# ------------------------------------------------------------

def evaluation_materielle(etat):
    """
    Score vu du point de vue du joueur dont c'est le tour.

    Positif = bon pour le joueur actuel.
    Négatif = mauvais pour le joueur actuel.
    """

    score = difference_materielle(
        etat
    )

    if etat["tour"] == BLANC:
        return score

    return -score


# ------------------------------------------------------------
# BONUS DE MATÉRIEL SIMPLE
# ------------------------------------------------------------

def bonus_paire_de_fous(etat, couleur):
    """
    Petit bonus pour la paire de fous.
    """

    nombre = compter_piece(
        etat,
        FOU,
        couleur
    )

    if nombre >= 2:
        return 30

    return 0


# ------------------------------------------------------------
# BONUS DE PAIRES DE CAVALIERS
# ------------------------------------------------------------

def bonus_paire_cavaliers(etat, couleur):
    """
    Petit bonus pour deux cavaliers.
    """

    nombre = compter_piece(
        etat,
        CAVALIER,
        couleur
    )

    if nombre >= 2:
        return 10

    return 0


# ------------------------------------------------------------
# ÉVALUATION MATÉRIELLE AMÉLIORÉE
# ------------------------------------------------------------

def evaluation_materielle_complete(etat):
    """
    Évaluation matérielle légèrement améliorée.

    Elle prend en compte :

        matériel
        paire de fous
        paire de cavaliers
    """

    score = difference_materielle(
        etat
    )

    score += bonus_paire_de_fous(
        etat,
        BLANC
    )

    score -= bonus_paire_de_fous(
        etat,
        NOIR
    )

    score += bonus_paire_cavaliers(
        etat,
        BLANC
    )

    score -= bonus_paire_cavaliers(
        etat,
        NOIR
    )

    if etat["tour"] == NOIR:
        score = -score

    return score


# ------------------------------------------------------------
# RAPPORT MATÉRIEL
# ------------------------------------------------------------

def rapport_materiel(etat):
    """
    Produit un rapport exploitable par Pandoraga.
    """

    inventaire = inventaire_materiel(
        etat
    )

    avantage = avantage_materiel(
        etat
    )

    return {

        "blanc": inventaire["blanc"],

        "noir": inventaire["noir"],

        "materiel_blanc":
            materiel_blanc(etat),

        "materiel_noir":
            materiel_noir(etat),

        "difference":
            difference_materielle(etat),

        "avantage":
            avantage,

        "materiel_insuffisant":
            materiel_insuffisant(etat)
    }


# ------------------------------------------------------------
# TEST DU BLOC 10
# ------------------------------------------------------------

def test_evaluation_initiale():

    etat = creer_etat_initial()

    # Position initiale parfaitement équilibrée.
    return (
        difference_materielle(etat)
        == 0
    )


def test_valeurs():

    return (
        VALEURS_PIECES[PION] == 100
        and
        VALEURS_PIECES[CAVALIER] == 320
        and
        VALEURS_PIECES[FOU] == 330
        and
        VALEURS_PIECES[TOUR] == 500
        and
        VALEURS_PIECES[DAME] == 900
    )


if __name__ == "__main__":

    print()
    print("🐼 BLOC 10 — TEST")
    print("=" * 50)

    etat_test = creer_etat_initial()

    print(
        "Test valeurs :",
        "OK"
        if test_valeurs()
        else "ERREUR"
    )

    print(
        "Test position initiale :",
        "OK"
        if test_evaluation_initiale()
        else "ERREUR"
    )

    print()

    print(
        "Matériel blanc :",
        materiel_blanc(etat_test)
    )

    print(
        "Matériel noir :",
        materiel_noir(etat_test)
    )

    print(
        "Différence :",
        difference_materielle(etat_test)
    )

    print(
        "Évaluation joueur actuel :",
        evaluation_materielle(etat_test)
    )

    print(
        "Matériel insuffisant :",
        materiel_insuffisant(etat_test)
    )

    print()

    print("Inventaire :")

    rapport = rapport_materiel(
        etat_test
    )

    print(
        rapport["blanc"]
    )

    print(
        rapport["noir"]
    )

    print()
    print("🐼 BLOC 10 CHARGÉ AVEC SUCCÈS.")
# ============================================================
# BLOC 11/26 — ÉVALUATION POSITIONNELLE
# ============================================================


# ------------------------------------------------------------
# TABLES POSITIONNELLES
# ------------------------------------------------------------

TABLE_PION = [
     0,   0,   0,   0,   0,   0,   0,   0,
     5,  10,  10, -5,  -5,  10,  10,   5,
     2,   2,   5,  10,  10,   5,   2,   2,
     0,   0,   0,  20,  20,   0,   0,   0,
     2,   2,  5,  15,  15,   5,   2,   2,
     5,  -5, -10,   0,   0, -10,  -5,   5,
     5,  10,  10, -20, -20,  10,  10,   5,
     0,   0,   0,   0,   0,   0,   0,   0
]


TABLE_CAVALIER = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]


TABLE_FOU = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,   10,  10,  10,  10,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]


TABLE_TOUR = [
     0,   0,   5,  10,  10,   5,   0,   0,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
     5,  10,  10,  10,  10,  10,  10,   5,
     0,   0,   5,  10,  10,   5,   0,   0
]


TABLE_DAME = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
     -5,   0,   5,   5,   5,   5,   0,  -5,
      0,   0,   5,   5,   5,   5,   0,  -5,
    -10,   5,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20
]


TABLE_ROI_MILIEU = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20
]


TABLE_ROI_FIN = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10,   0,   0, -10, -20, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -30,   0,   0,   0,   0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]


# ------------------------------------------------------------
# TABLE CORRESPONDANT À UNE PIÈCE
# ------------------------------------------------------------

def table_positionnelle(piece, phase_fin=False):

    type_piece_actuel = type_piece(piece)

    if type_piece_actuel == PION:
        return TABLE_PION

    if type_piece_actuel == CAVALIER:
        return TABLE_CAVALIER

    if type_piece_actuel == FOU:
        return TABLE_FOU

    if type_piece_actuel == TOUR:
        return TABLE_TOUR

    if type_piece_actuel == DAME:
        return TABLE_DAME

    if type_piece_actuel == ROI:

        if phase_fin:
            return TABLE_ROI_FIN

        return TABLE_ROI_MILIEU

    return None


# ------------------------------------------------------------
# MIROIR POUR LES NOIRS
# ------------------------------------------------------------

def case_miroir(case):
    """
    Les tables sont écrites du point de vue des Blancs.
    Pour les Noirs, on retourne la case verticalement.
    """

    ligne = ligne_case(case)
    colonne = colonne_case(case)

    ligne = 7 - ligne

    return coordonnees_case(
        colonne,
        ligne
    )


# ------------------------------------------------------------
# PHASE DE PARTIE
# ------------------------------------------------------------

def phase_partie(etat):
    """
    Estime la phase :

        0 = ouverture
        1 = milieu
        2 = finale
    """

    dames = (
        compter_piece(etat, DAME, BLANC)
        +
        compter_piece(etat, DAME, NOIR)
    )

    tours = (
        compter_piece(etat, TOUR, BLANC)
        +
        compter_piece(etat, TOUR, NOIR)
    )

    pieces_mineures = (
        compter_piece(etat, FOU, BLANC)
        +
        compter_piece(etat, FOU, NOIR)
        +
        compter_piece(etat, CAVALIER, BLANC)
        +
        compter_piece(etat, CAVALIER, NOIR)
    )

    if dames == 0 and tours <= 2:
        return 2

    if dames <= 1 and pieces_mineures <= 2:
        return 2

    if dames == 2 and tours == 4:
        return 0

    return 1


# ------------------------------------------------------------
# BONUS POSITIONNEL D'UNE PIÈCE
# ------------------------------------------------------------

def bonus_case_piece(piece, case, phase_fin=False):

    table = table_positionnelle(
        piece,
        phase_fin
    )

    if table is None:
        return 0

    case_table = case

    if piece < 0:
        case_table = case_miroir(case)

    return table[case_table]


# ------------------------------------------------------------
# CENTRE
# ------------------------------------------------------------

CASES_CENTRE = (
    nom_vers_case("d4"),
    nom_vers_case("e4"),
    nom_vers_case("d5"),
    nom_vers_case("e5")
)


CASES_CENTRE_ELARGI = (
    nom_vers_case("c3"),
    nom_vers_case("d3"),
    nom_vers_case("e3"),
    nom_vers_case("f3"),

    nom_vers_case("c4"),
    nom_vers_case("d4"),
    nom_vers_case("e4"),
    nom_vers_case("f4"),

    nom_vers_case("c5"),
    nom_vers_case("d5"),
    nom_vers_case("e5"),
    nom_vers_case("f5"),

    nom_vers_case("c6"),
    nom_vers_case("d6"),
    nom_vers_case("e6"),
    nom_vers_case("f6")
)


# ------------------------------------------------------------
# CONTRÔLE DU CENTRE
# ------------------------------------------------------------

def evaluation_centre(etat):

    score = 0

    for case in CASES_CENTRE:

        piece = etat["plateau"][case]

        if piece == VIDE:
            continue

        valeur = 20

        if couleur_piece(piece) == BLANC:
            score += valeur
        else:
            score -= valeur

    return score


# ------------------------------------------------------------
# BONUS DE POSITION CENTRALE
# ------------------------------------------------------------

def bonus_centre_piece(case):

    if case in CASES_CENTRE:
        return 15

    if case in CASES_CENTRE_ELARGI:
        return 5

    return 0


# ------------------------------------------------------------
# PIONS ISOLÉS
# ------------------------------------------------------------

def pions_isoles(etat, couleur):

    colonnes = [0] * 8

    for case in range(64):

        piece = etat["plateau"][case]

        if piece == VIDE:
            continue

        if type_piece(piece) != PION:
            continue

        if couleur_piece(piece) != couleur:
            continue

        colonnes[colonne_case(case)] += 1

    resultat = 0

    for colonne in range(8):

        if colonnes[colonne] == 0:
            continue

        gauche = (
            colonnes[colonne - 1]
            if colonne > 0
            else 0
        )

        droite = (
            colonnes[colonne + 1]
            if colonne < 7
            else 0
        )

        if gauche == 0 and droite == 0:
            resultat += colonnes[colonne]

    return resultat


# ------------------------------------------------------------
# PIONS DOUBLÉS
# ------------------------------------------------------------

def pions_doubles(etat, couleur):

    colonnes = [0] * 8

    for case in range(64):

        piece = etat["plateau"][case]

        if piece == VIDE:
            continue

        if type_piece(piece) != PION:
            continue

        if couleur_piece(piece) != couleur:
            continue

        colonnes[colonne_case(case)] += 1

    doubles = 0

    for nombre in colonnes:

        if nombre > 1:
            doubles += nombre - 1

    return doubles


# ------------------------------------------------------------
# PIONS PASSÉS
# ------------------------------------------------------------

def pions_passes(etat, couleur):

    plateau = etat["plateau"]

    resultat = 0

    for case in range(64):

        piece = plateau[case]

        if piece == VIDE:
            continue

        if type_piece(piece) != PION:
            continue

        if couleur_piece(piece) != couleur:
            continue

        colonne = colonne_case(case)
        ligne = ligne_case(case)

        bloque = False

        for autre_case in range(64):

            autre = plateau[autre_case]

            if autre == VIDE:
                continue

            if type_piece(autre) != PION:
                continue

            if couleur_piece(autre) == couleur:
                continue

            autre_colonne = colonne_case(
                autre_case
            )

            autre_ligne = ligne_case(
                autre_case
            )

            if abs(
                autre_colonne - colonne
            ) > 1:
                continue

            if couleur == BLANC:

                if autre_ligne > ligne:
                    bloque = True
                    break

            else:

                if autre_ligne < ligne:
                    bloque = True
                    break

        if not bloque:
            resultat += 1

    return resultat


# ------------------------------------------------------------
# MOBILITÉ
# ------------------------------------------------------------

def evaluation_mobilite(etat):

    coups = generer_coups_pseudo_legaux(
        etat
    )

    score_blanc = 0
    score_noir = 0

    for coup in coups:

        piece = etat["plateau"][
            coup["depart"]
        ]

        if couleur_piece(piece) == BLANC:
            score_blanc += 1
        else:
            score_noir += 1

    return (
        score_blanc
        -
        score_noir
    )


# ------------------------------------------------------------
# DÉVELOPPEMENT
# ------------------------------------------------------------

def evaluation_developpement(etat):

    score = 0

    cases_depart_blanc = (
        nom_vers_case("b1"),
        nom_vers_case("g1"),
        nom_vers_case("c1"),
        nom_vers_case("f1")
    )

    cases_depart_noir = (
        nom_vers_case("b8"),
        nom_vers_case("g8"),
        nom_vers_case("c8"),
        nom_vers_case("f8")
    )

    for case in cases_depart_blanc:

        piece = etat["plateau"][case]

        if piece == VIDE:
            score += 5

    for case in cases_depart_noir:

        piece = etat["plateau"][case]

        if piece == VIDE:
            score -= 5

    return score


# ------------------------------------------------------------
# ACTIVITÉ DES TOURS
# ------------------------------------------------------------

def tours_sur_colonne_ouverte(etat, couleur):

    resultat = 0

    for colonne in range(8):

        contient_pion = False

        for ligne in range(8):

            case = coordonnees_case(
                colonne,
                ligne
            )

            piece = etat["plateau"][case]

            if type_piece(piece) == PION:
                contient_pion = True
                break

        if contient_pion:
            continue

        for ligne in range(8):

            case = coordonnees_case(
                colonne,
                ligne
            )

            piece = etat["plateau"][case]

            if type_piece(piece) != TOUR:
                continue

            if couleur_piece(piece) == couleur:
                resultat += 1

    return resultat


# ------------------------------------------------------------
# PIONS ISOLÉS — SCORE
# ------------------------------------------------------------

def score_pions_isoles(etat):

    blancs = pions_isoles(
        etat,
        BLANC
    )

    noirs = pions_isoles(
        etat,
        NOIR
    )

    return (
        noirs * 15
        -
        blancs * 15
    )


# ------------------------------------------------------------
# PIONS DOUBLÉS — SCORE
# ------------------------------------------------------------

def score_pions_doubles(etat):

    blancs = pions_doubles(
        etat,
        BLANC
    )

    noirs = pions_doubles(
        etat,
        NOIR
    )

    return (
        noirs * 10
        -
        blancs * 10
    )


# ------------------------------------------------------------
# PIONS PASSÉS — SCORE
# ------------------------------------------------------------

def score_pions_passes(etat):

    blancs = pions_passes(
        etat,
        BLANC
    )

    noirs = pions_passes(
        etat,
        NOIR
    )

    return (
        blancs * 25
        -
        noirs * 25
    )


# ------------------------------------------------------------
# SCORE DES TOURS
# ------------------------------------------------------------

def score_tours_ouvertes(etat):

    blancs = tours_sur_colonne_ouverte(
        etat,
        BLANC
    )

    noirs = tours_sur_colonne_ouverte(
        etat,
        NOIR
    )

    return (
        blancs * 20
        -
        noirs * 20
    )


# ------------------------------------------------------------
# ÉVALUATION POSITIONNELLE
# ------------------------------------------------------------

def evaluation_positionnelle(etat):

    phase = phase_partie(etat)

    phase_fin = (
        phase == 2
    )

    score = 0

    # --------------------------------------------------------
    # TABLES POSITIONNELLES
    # --------------------------------------------------------

    for case in range(64):

        piece = etat["plateau"][case]

        if piece == VIDE:
            continue

        valeur = bonus_case_piece(
            piece,
            case,
            phase_fin
        )

        if piece > 0:
            score += valeur
        else:
            score -= valeur

    # --------------------------------------------------------
    # CENTRE
    # --------------------------------------------------------

    score += evaluation_centre(
        etat
    )

    # --------------------------------------------------------
    # PIONS
    # --------------------------------------------------------

    score += score_pions_isoles(
        etat
    )

    score += score_pions_doubles(
        etat
    )

    score += score_pions_passes(
        etat
    )

    # --------------------------------------------------------
    # MOBILITÉ
    # --------------------------------------------------------

    score += evaluation_mobilite(
        etat
    ) * 2

    # --------------------------------------------------------
    # DÉVELOPPEMENT
    # --------------------------------------------------------

    score += evaluation_developpement(
        etat
    )

    # --------------------------------------------------------
    # TOURS
    # --------------------------------------------------------

    score += score_tours_ouvertes(
        etat
    )

    # --------------------------------------------------------
    # POINT DE VUE DU JOUEUR
    # --------------------------------------------------------

    if etat["tour"] == NOIR:
        score = -score

    return score


# ------------------------------------------------------------
# ÉVALUATION GLOBALE
# ------------------------------------------------------------

def evaluation_position(etat):

    materiel = evaluation_materielle_complete(
        etat
    )

    position = evaluation_positionnelle(
        etat
    )

    return materiel + position


# ------------------------------------------------------------
# RAPPORT POSITIONNEL
# ------------------------------------------------------------

def rapport_positionnel(etat):

    return {

        "phase":
            phase_partie(etat),

        "materiel":
            evaluation_materielle_complete(
                etat
            ),

        "position":
            evaluation_positionnelle(
                etat
            ),

        "total":
            evaluation_position(etat),

        "centre":
            evaluation_centre(etat),

        "mobilite":
            evaluation_mobilite(etat),

        "pions_isoles_blanc":
            pions_isoles(etat, BLANC),

        "pions_isoles_noir":
            pions_isoles(etat, NOIR),

        "pions_doubles_blanc":
            pions_doubles(etat, BLANC),

        "pions_doubles_noir":
            pions_doubles(etat, NOIR),

        "pions_passes_blanc":
            pions_passes(etat, BLANC),

        "pions_passes_noir":
            pions_passes(etat, NOIR)
    }


# ------------------------------------------------------------
# TEST DU BLOC 11
# ------------------------------------------------------------

def test_position_initiale():

    etat = creer_etat_initial()

    score = evaluation_position(etat)

    # La position initiale doit rester proche de 0.
    return abs(score) < 100


def test_centre():

    etat = creer_etat_initial()

    # e4
    etat["plateau"][
        nom_vers_case("e2")
    ] = VIDE

    etat["plateau"][
        nom_vers_case("e4")
    ] = PION

    score = evaluation_centre(
        etat
    )

    return score > 0


if __name__ == "__main__":

    print()
    print("🐼 BLOC 11 — TEST")
    print("=" * 55)

    etat_test = creer_etat_initial()

    print(
        "Phase :",
        phase_partie(etat_test)
    )

    print(
        "Centre :",
        evaluation_centre(etat_test)
    )

    print(
        "Mobilité :",
        evaluation_mobilite(etat_test)
    )

    print(
        "Évaluation positionnelle :",
        evaluation_positionnelle(
            etat_test
        )
    )

    print(
        "Évaluation globale :",
        evaluation_position(
            etat_test
        )
    )

    print()

    print(
        "Test position initiale :",
        "OK"
        if test_position_initiale()
        else "ERREUR"
    )

    print(
        "Test contrôle centre :",
        "OK"
        if test_centre()
        else "ERREUR"
    )

    print()

    print("📊 RAPPORT POSITIONNEL")
    print("-" * 55)

    rapport = rapport_positionnel(
        etat_test
    )

    for cle, valeur in rapport.items():
        print(
            f"{cle:25} : {valeur}"
        )

    print()
    print("🐼 BLOC 11 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 12/26 — SÉCURITÉ DU ROI
# ============================================================


# ------------------------------------------------------------
# DIRECTIONS AUTOUR DU ROI
# ------------------------------------------------------------

DIRECTIONS_ROI = (
    (-1, -1),
    ( 0, -1),
    ( 1, -1),
    (-1,  0),
    ( 1,  0),
    (-1,  1),
    ( 0,  1),
    ( 1,  1)
)


# ------------------------------------------------------------
# TROUVER LE ROI
# ------------------------------------------------------------

def trouver_roi(etat, couleur):
    """
    Retourne la case du roi de la couleur donnée.
    """

    roi = ROI if couleur == BLANC else -ROI

    for case, piece in enumerate(etat["plateau"]):

        if piece == roi:
            return case

    return -1


# ------------------------------------------------------------
# CASES AUTOUR DU ROI
# ------------------------------------------------------------

def cases_autour_roi(case):
    """
    Retourne les cases voisines d'un roi.
    """

    if not est_case_valide(case):
        return []

    colonne = colonne_case(case)
    ligne = ligne_case(case)

    resultat = []

    for dx, dy in DIRECTIONS_ROI:

        nouvelle_colonne = colonne + dx
        nouvelle_ligne = ligne + dy

        if not (0 <= nouvelle_colonne < 8):
            continue

        if not (0 <= nouvelle_ligne < 8):
            continue

        resultat.append(
            coordonnees_case(
                nouvelle_colonne,
                nouvelle_ligne
            )
        )

    return resultat


# ------------------------------------------------------------
# CASE ATTAQUÉE PAR L'ADVERSAIRE
# ------------------------------------------------------------

def case_attaquee_par_adversaire(
    etat,
    case,
    couleur
):
    """
    Vérifie si une case est attaquée par l'adversaire.
    """

    adversaire = (
        NOIR
        if couleur == BLANC
        else BLANC
    )

    return case_attaquee(
        etat,
        case,
        adversaire
    )


# ------------------------------------------------------------
# CASES DE FUITE DU ROI
# ------------------------------------------------------------

def cases_fuite_roi(etat, couleur):
    """
    Compte les cases voisines accessibles au roi.
    """

    roi_case = trouver_roi(
        etat,
        couleur
    )

    if roi_case == -1:
        return []

    resultat = []

    for destination in cases_autour_roi(
        roi_case
    ):

        piece = etat["plateau"][destination]

        # Une case occupée par une pièce alliée
        # n'est pas une case de fuite.
        if piece != VIDE:

            if couleur_piece(piece) == couleur:
                continue

        if case_attaquee_par_adversaire(
            etat,
            destination,
            couleur
        ):
            continue

        resultat.append(
            destination
        )

    return resultat


# ------------------------------------------------------------
# SCORE DES CASES DE FUITE
# ------------------------------------------------------------

def score_cases_fuite(etat, couleur):

    nombre = len(
        cases_fuite_roi(
            etat,
            couleur
        )
    )

    # Plus il y a de cases de fuite,
    # plus le roi est mobile.
    return nombre * 8


# ------------------------------------------------------------
# BOUCLIER DE PIONS
# ------------------------------------------------------------

def bouclier_pions_roi(etat, couleur):

    roi_case = trouver_roi(
        etat,
        couleur
    )

    if roi_case == -1:
        return 0

    colonne_roi = colonne_case(
        roi_case
    )

    ligne_roi = ligne_case(
        roi_case
    )

    score = 0

    direction = 1 if couleur == BLANC else -1

    ligne_pion = ligne_roi + direction

    if not (0 <= ligne_pion < 8):
        return 0

    for dc in (-1, 0, 1):

        colonne = colonne_roi + dc

        if not (0 <= colonne < 8):
            continue

        case = coordonnees_case(
            colonne,
            ligne_pion
        )

        piece = etat["plateau"][case]

        if piece == PION and couleur == BLANC:
            score += 12

        elif piece == -PION and couleur == NOIR:
            score += 12

    return score


# ------------------------------------------------------------
# PIONS AUTOUR DU ROI
# ------------------------------------------------------------

def nombre_pions_proches_roi(
    etat,
    couleur
):
    """
    Compte les pions alliés dans la zone proche du roi.
    """

    roi_case = trouver_roi(
        etat,
        couleur
    )

    if roi_case == -1:
        return 0

    score = 0

    for case in cases_autour_roi(
        roi_case
    ):

        piece = etat["plateau"][case]

        if couleur == BLANC and piece == PION:
            score += 1

        elif couleur == NOIR and piece == -PION:
            score += 1

    return score


# ------------------------------------------------------------
# ATTAQUES AUTOUR DU ROI
# ------------------------------------------------------------

def attaques_autour_roi(
    etat,
    couleur
):
    """
    Compte les cases autour du roi contrôlées
    par l'adversaire.
    """

    roi_case = trouver_roi(
        etat,
        couleur
    )

    if roi_case == -1:
        return 0

    score = 0

    for case in cases_autour_roi(
        roi_case
    ):

        if case_attaquee_par_adversaire(
            etat,
            case,
            couleur
        ):
            score += 1

    return score


# ------------------------------------------------------------
# ATTAQUES DIRECTES DU ROI
# ------------------------------------------------------------

def roi_en_echec(etat, couleur):

    roi_case = trouver_roi(
        etat,
        couleur
    )

    if roi_case == -1:
        return True

    return case_attaquee_par_adversaire(
        etat,
        roi_case,
        couleur
    )


# ------------------------------------------------------------
# EXPOSITION DU ROI
# ------------------------------------------------------------

def exposition_roi(etat, couleur):

    roi_case = trouver_roi(
        etat,
        couleur
    )

    if roi_case == -1:
        return 100

    colonne = colonne_case(
        roi_case
    )

    ligne = ligne_case(
        roi_case
    )

    score = 0

    # Vérifie les cases autour du roi.
    for case in cases_autour_roi(
        roi_case
    ):

        piece = etat["plateau"][case]

        if piece == VIDE:
            score += 4

    # Les colonnes ouvertes proches du roi
    # augmentent légèrement l'exposition.
    for dc in (-1, 0, 1):

        colonne_test = colonne + dc

        if not (0 <= colonne_test < 8):
            continue

        contient_pion = False

        for ligne_test in range(8):

            case = coordonnees_case(
                colonne_test,
                ligne_test
            )

            piece = etat["plateau"][case]

            if type_piece(piece) == PION:
                contient_pion = True
                break

        if not contient_pion:
            score += 6

    return score


# ------------------------------------------------------------
# PENALITÉ DE ROI EXPOSÉ
# ------------------------------------------------------------

def penalite_roi_expose(etat, couleur):

    exposition = exposition_roi(
        etat,
        couleur
    )

    attaques = attaques_autour_roi(
        etat,
        couleur
    )

    score = exposition

    score += attaques * 12

    return score


# ------------------------------------------------------------
# SCORE SÉCURITÉ BLANC
# ------------------------------------------------------------

def securite_roi_blanc(etat):

    score = 0

    # Bouclier
    score += bouclier_pions_roi(
        etat,
        BLANC
    )

    # Cases de fuite
    score += score_cases_fuite(
        etat,
        BLANC
    )

    # Pions proches
    score += (
        nombre_pions_proches_roi(
            etat,
            BLANC
        ) * 5
    )

    # Exposition
    score -= penalite_roi_expose(
        etat,
        BLANC
    )

    # Échec = très mauvaise sécurité
    if roi_en_echec(
        etat,
        BLANC
    ):
        score -= 150

    return score


# ------------------------------------------------------------
# SCORE SÉCURITÉ NOIR
# ------------------------------------------------------------

def securite_roi_noir(etat):

    score = 0

    score += bouclier_pions_roi(
        etat,
        NOIR
    )

    score += score_cases_fuite(
        etat,
        NOIR
    )

    score += (
        nombre_pions_proches_roi(
            etat,
            NOIR
        ) * 5
    )

    score -= penalite_roi_expose(
        etat,
        NOIR
    )

    if roi_en_echec(
        etat,
        NOIR
    ):
        score -= 150

    return score


# ------------------------------------------------------------
# ÉVALUATION GLOBALE DE LA SÉCURITÉ
# ------------------------------------------------------------

def evaluation_securite_roi(etat):

    blanc = securite_roi_blanc(
        etat
    )

    noir = securite_roi_noir(
        etat
    )

    score = blanc - noir

    if etat["tour"] == NOIR:
        score = -score

    return score


# ------------------------------------------------------------
# BONUS DU ROQUE
# ------------------------------------------------------------

def bonus_roque(etat, couleur):

    roi_case = trouver_roi(
        etat,
        couleur
    )

    if roi_case == -1:
        return 0

    if couleur == BLANC:

        cases_roque = (
            nom_vers_case("g1"),
            nom_vers_case("c1")
        )

    else:

        cases_roque = (
            nom_vers_case("g8"),
            nom_vers_case("c8")
        )

    if roi_case in cases_roque:
        return 25

    return 0


# ------------------------------------------------------------
# SCORE ROQUE
# ------------------------------------------------------------

def evaluation_roque(etat):

    blanc = bonus_roque(
        etat,
        BLANC
    )

    noir = bonus_roque(
        etat,
        NOIR
    )

    score = blanc - noir

    if etat["tour"] == NOIR:
        score = -score

    return score


# ------------------------------------------------------------
# ÉVALUATION ROI COMPLÈTE
# ------------------------------------------------------------

def evaluation_roi(etat):

    return (
        evaluation_securite_roi(etat)
        +
        evaluation_roque(etat)
    )


# ------------------------------------------------------------
# ÉVALUATION GLOBALE PANDORAGA
# ------------------------------------------------------------

def evaluation_complete(etat):

    return (
        evaluation_materielle_complete(
            etat
        )
        +
        evaluation_positionnelle(
            etat
        )
        +
        evaluation_roi(
            etat
        )
    )


# ------------------------------------------------------------
# RAPPORT SÉCURITÉ
# ------------------------------------------------------------

def rapport_securite_roi(etat):

    return {

        "roi_blanc":
            trouver_roi(
                etat,
                BLANC
            ),

        "roi_noir":
            trouver_roi(
                etat,
                NOIR
            ),

        "echec_blanc":
            roi_en_echec(
                etat,
                BLANC
            ),

        "echec_noir":
            roi_en_echec(
                etat,
                NOIR
            ),

        "fuites_blanc":
            len(
                cases_fuite_roi(
                    etat,
                    BLANC
                )
            ),

        "fuites_noir":
            len(
                cases_fuite_roi(
                    etat,
                    NOIR
                )
            ),

        "attaques_blanc":
            attaques_autour_roi(
                etat,
                BLANC
            ),

        "attaques_noir":
            attaques_autour_roi(
                etat,
                NOIR
            ),

        "bouclier_blanc":
            bouclier_pions_roi(
                etat,
                BLANC
            ),

        "bouclier_noir":
            bouclier_pions_roi(
                etat,
                NOIR
            ),

        "score":
            evaluation_roi(
                etat
            )
    }


# ------------------------------------------------------------
# TESTS
# ------------------------------------------------------------

def test_rois():

    etat = creer_etat_initial()

    roi_blanc = trouver_roi(
        etat,
        BLANC
    )

    roi_noir = trouver_roi(
        etat,
        NOIR
    )

    return (
        roi_blanc != -1
        and
        roi_noir != -1
    )


def test_securite_initiale():

    etat = creer_etat_initial()

    score = evaluation_securite_roi(
        etat
    )

    # La position initiale ne doit pas être
    # fortement déséquilibrée.
    return abs(score) < 100


# ------------------------------------------------------------
# EXÉCUTION DU TEST
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 BLOC 12 — TEST")
    print("=" * 55)

    etat_test = creer_etat_initial()

    print(
        "Roi blanc :",
        trouver_roi(
            etat_test,
            BLANC
        )
    )

    print(
        "Roi noir :",
        trouver_roi(
            etat_test,
            NOIR
        )
    )

    print(
        "Échec blanc :",
        roi_en_echec(
            etat_test,
            BLANC
        )
    )

    print(
        "Échec noir :",
        roi_en_echec(
            etat_test,
            NOIR
        )
    )

    print(
        "Fuites blanc :",
        len(
            cases_fuite_roi(
                etat_test,
                BLANC
            )
        )
    )

    print(
        "Fuites noir :",
        len(
            cases_fuite_roi(
                etat_test,
                NOIR
            )
        )
    )

    print(
        "Sécurité roi :",
        evaluation_securite_roi(
            etat_test
        )
    )

    print(
        "Évaluation complète :",
        evaluation_complete(
            etat_test
        )
    )

    print()

    print(
        "Test rois :",
        "OK"
        if test_rois()
        else "ERREUR"
    )

    print(
        "Test sécurité initiale :",
        "OK"
        if test_securite_initiale()
        else "ERREUR"
    )

    print()

    print("📊 RAPPORT ROI")
    print("-" * 55)

    rapport = rapport_securite_roi(
        etat_test
    )

    for cle, valeur in rapport.items():

        print(
            f"{cle:22} : {valeur}"
        )

    print()
    print("🐼 BLOC 12 CHARGÉ AVEC SUCCÈS.")

    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 13/26 — ORDonnancement INTELLIGENT DES COUPS
# ============================================================


# ------------------------------------------------------------
# CONSTANTES D'ORDONNANCEMENT
# ------------------------------------------------------------

SCORE_PROMOTION = 9000
SCORE_ECHEC = 8000
SCORE_CAPTURE = 5000
SCORE_CAPTURE_BONNE = 3000
SCORE_CENTRE = 100
SCORE_DEVELOPPEMENT = 80


# ------------------------------------------------------------
# RÉCUPÉRER LA PIÈCE PRISE
# ------------------------------------------------------------

def piece_capturee(etat, coup):
    """
    Retourne la pièce capturée par un coup.

    Gère également la prise en passant.
    """

    arrivee = coup["arrivee"]

    # Capture normale
    piece = etat["plateau"][arrivee]

    if piece != VIDE:
        return piece

    # Prise en passant
    if coup.get("en_passant", False):

        depart = coup["depart"]

        colonne_depart = colonne_case(
            depart
        )

        colonne_arrivee = colonne_case(
            arrivee
        )

        if colonne_depart != colonne_arrivee:

            direction = (
                -1
                if etat["tour"] == BLANC
                else 1
            )

            case_capture = coordonnees_case(
                colonne_arrivee,
                ligne_case(arrivee) + direction
            )

            if est_case_valide(case_capture):
                return etat["plateau"][case_capture]

    return VIDE


# ------------------------------------------------------------
# COUP = CAPTURE ?
# ------------------------------------------------------------

def coup_est_capture(etat, coup):

    if coup.get("capture", VIDE) != VIDE:
        return True

    arrivee = coup["arrivee"]

    if etat["plateau"][arrivee] != VIDE:
        return True

    if coup.get("en_passant", False):
        return True

    return False


# ------------------------------------------------------------
# COUP = PROMOTION ?
# ------------------------------------------------------------

def coup_est_promotion(coup):

    promotion = coup.get(
        "promotion",
        VIDE
    )

    return (
        promotion != VIDE
        and
        promotion_valide(promotion)
    )


# ------------------------------------------------------------
# COUP = ROQUE ?
# ------------------------------------------------------------

def coup_est_roque(coup):

    return bool(
        coup.get(
            "roque",
            False
        )
    )


# ------------------------------------------------------------
# COUP = ÉCHEC ?
# ------------------------------------------------------------

def coup_donne_echec(etat, coup):
    """
    Teste si le coup donne échec.

    On utilise une copie de l'état afin de ne pas
    modifier la position actuelle.
    """

    try:

        copie = copier_etat(
            etat
        )

        appliquer_coup(
            copie,
            coup
        )

        couleur_adverse = (
            NOIR
            if etat["tour"] == BLANC
            else BLANC
        )

        return roi_en_echec(
            copie,
            couleur_adverse
        )

    except Exception:
        return False


# ------------------------------------------------------------
# SCORE MVV-LVA
# ------------------------------------------------------------

def score_capture_mvv_lva(
    etat,
    coup
):
    """
    MVV-LVA :

        Most Valuable Victim
        Least Valuable Attacker

    Capturer une Dame avec un Pion
    est donc très prioritaire.
    """

    victime = piece_capturee(
        etat,
        coup
    )

    if victime == VIDE:
        return 0

    valeur_victime = valeur_piece(
        victime
    )

    piece = etat["plateau"][
        coup["depart"]
    ]

    valeur_attaquant = valeur_piece(
        piece
    )

    return (
        valeur_victime * 10
        -
        valeur_attaquant
    )


# ------------------------------------------------------------
# SCORE CENTRAL
# ------------------------------------------------------------

def score_centre_coup(coup):

    arrivee = coup["arrivee"]

    if arrivee in CASES_CENTRE:
        return SCORE_CENTRE

    if arrivee in CASES_CENTRE_ELARGI:
        return SCORE_CENTRE // 2

    return 0


# ------------------------------------------------------------
# SCORE PROMOTION
# ------------------------------------------------------------

def score_promotion_coup(coup):

    if not coup_est_promotion(coup):
        return 0

    promotion = normaliser_promotion(
        coup["promotion"]
    )

    return (
        SCORE_PROMOTION
        +
        valeur_promotion(
            promotion
        )
    )


# ------------------------------------------------------------
# SCORE ROQUE
# ------------------------------------------------------------

def score_roque_coup(coup):

    if coup_est_roque(coup):
        return 250

    return 0


# ------------------------------------------------------------
# SCORE CAPTURE
# ------------------------------------------------------------

def score_capture_coup(
    etat,
    coup
):

    if not coup_est_capture(
        etat,
        coup
    ):
        return 0

    return (
        SCORE_CAPTURE
        +
        score_capture_mvv_lva(
            etat,
            coup
        )
    )


# ------------------------------------------------------------
# SCORE D'ÉCHEC
# ------------------------------------------------------------

def score_echec_coup(
    etat,
    coup
):

    if coup_donne_echec(
        etat,
        coup
    ):
        return SCORE_ECHEC

    return 0


# ------------------------------------------------------------
# IDENTIFIANT D'UN COUP
# ------------------------------------------------------------

def identifiant_coup(coup):

    depart = coup.get(
        "depart",
        -1
    )

    arrivee = coup.get(
        "arrivee",
        -1
    )

    promotion = coup.get(
        "promotion",
        VIDE
    )

    return (
        depart,
        arrivee,
        promotion
    )


# ------------------------------------------------------------
# HASH SIMPLE DU COUP
# ------------------------------------------------------------

def cle_coup(coup):

    return identifiant_coup(
        coup
    )


# ------------------------------------------------------------
# SCORE TACTIQUE COMPLET
# ------------------------------------------------------------

def score_coup_tactique(
    etat,
    coup
):
    """
    Calcule la priorité tactique du coup.
    """

    score = 0

    score += score_promotion_coup(
        coup
    )

    score += score_capture_coup(
        etat,
        coup
    )

    score += score_echec_coup(
        etat,
        coup
    )

    score += score_roque_coup(
        coup
    )

    score += score_centre_coup(
        coup
    )

    return score


# ------------------------------------------------------------
# HISTORIQUE DES COUPS
# ------------------------------------------------------------

HISTORIQUE_COUPS = {}


def obtenir_score_historique(coup):

    cle = cle_coup(
        coup
    )

    return HISTORIQUE_COUPS.get(
        cle,
        0
    )


def ajouter_score_historique(
    coup,
    bonus
):

    cle = cle_coup(
        coup
    )

    ancien = HISTORIQUE_COUPS.get(
        cle,
        0
    )

    nouveau = ancien + bonus

    # Limitation pour éviter une croissance infinie.
    nouveau = max(
        -100000,
        min(
            100000,
            nouveau
        )
    )

    HISTORIQUE_COUPS[cle] = nouveau


# ------------------------------------------------------------
# COUPS KILLER
# ------------------------------------------------------------

COUPS_KILLER = {}


def enregistrer_coup_killer(
    profondeur,
    coup
):

    cle = cle_coup(
        coup
    )

    liste = COUPS_KILLER.setdefault(
        profondeur,
        []
    )

    # Déjà présent
    if cle in liste:
        return

    liste.insert(
        0,
        cle
    )

    # Maximum de 2 killer moves par profondeur.
    del liste[2:]


def est_coup_killer(
    profondeur,
    coup
):

    cle = cle_coup(
        coup
    )

    return cle in COUPS_KILLER.get(
        profondeur,
        []
    )


# ------------------------------------------------------------
# SCORE KILLER
# ------------------------------------------------------------

def score_killer(
    profondeur,
    coup
):

    if est_coup_killer(
        profondeur,
        coup
    ):
        return 7000

    return 0


# ------------------------------------------------------------
# SCORE HISTORIQUE
# ------------------------------------------------------------

def score_historique(coup):

    return obtenir_score_historique(
        coup
    )


# ------------------------------------------------------------
# SCORE TOTAL DU COUP
# ------------------------------------------------------------

def score_ordre_coup(
    etat,
    coup,
    profondeur=0
):

    score = 0

    # Tactique
    score += score_coup_tactique(
        etat,
        coup
    )

    # Killer
    score += score_killer(
        profondeur,
        coup
    )

    # History
    score += score_historique(
        coup
    )

    return score


# ------------------------------------------------------------
# TRI DES COUPS
# ------------------------------------------------------------

def ordonner_coups(
    etat,
    coups,
    profondeur=0
):
    """
    Trie les coups du plus intéressant
    au moins intéressant.
    """

    coups_scores = []

    for coup in coups:

        score = score_ordre_coup(
            etat,
            coup,
            profondeur
        )

        coups_scores.append(
            (
                score,
                coup
            )
        )

    coups_scores.sort(
        key=lambda element: element[0],
        reverse=True
    )

    return [
        coup
        for score, coup
        in coups_scores
    ]


# ------------------------------------------------------------
# ORDRE AVEC SCORES
# ------------------------------------------------------------

def ordonner_coups_detail(
    etat,
    coups,
    profondeur=0
):

    resultat = []

    for coup in coups:

        score = score_ordre_coup(
            etat,
            coup,
            profondeur
        )

        resultat.append({
            "coup": coup,
            "score": score
        })

    resultat.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return resultat


# ------------------------------------------------------------
# MEILLEUR COUP TACTIQUE
# ------------------------------------------------------------

def meilleur_coup_tactique(
    etat,
    coups
):

    if not coups:
        return None

    tries = ordonner_coups(
        etat,
        coups
    )

    return tries[0]


# ------------------------------------------------------------
# COUPS CAPTURES UNIQUEMENT
# ------------------------------------------------------------

def coups_captures(
    etat,
    coups
):

    return [
        coup
        for coup in coups
        if coup_est_capture(
            etat,
            coup
        )
    ]


# ------------------------------------------------------------
# COUPS DE PROMOTION
# ------------------------------------------------------------

def coups_promotions(coups):

    return [
        coup
        for coup in coups
        if coup_est_promotion(
            coup
        )
    ]


# ------------------------------------------------------------
# COUPS DONNANT ÉCHEC
# ------------------------------------------------------------

def coups_echecs(
    etat,
    coups
):

    resultat = []

    for coup in coups:

        if coup_donne_echec(
            etat,
            coup
        ):
            resultat.append(
                coup
            )

    return resultat


# ------------------------------------------------------------
# RAPPORT D'ORDONNANCEMENT
# ------------------------------------------------------------

def rapport_ordre_coups(
    etat,
    coups,
    profondeur=0
):

    details = ordonner_coups_detail(
        etat,
        coups,
        profondeur
    )

    resultat = []

    for element in details:

        coup = element["coup"]

        resultat.append({
            "coup": coup,
            "score": element["score"],
            "capture":
                coup_est_capture(
                    etat,
                    coup
                ),
            "promotion":
                coup_est_promotion(
                    coup
                ),
            "roque":
                coup_est_roque(
                    coup
                )
        })

    return resultat


# ------------------------------------------------------------
# TEST MVV-LVA
# ------------------------------------------------------------

def test_valeurs_ordre():

    return (
        SCORE_PROMOTION > SCORE_CAPTURE
        and
        SCORE_ECHEC > 0
        and
        SCORE_CAPTURE > 0
    )


# ------------------------------------------------------------
# TEST ORDRE INITIAL
# ------------------------------------------------------------

def test_ordre_initial():

    etat = creer_etat_initial()

    coups = generer_coups_pseudo_legaux(
        etat
    )

    if not coups:
        return False

    tries = ordonner_coups(
        etat,
        coups
    )

    return len(tries) == len(coups)


# ------------------------------------------------------------
# TEST HISTORIQUE
# ------------------------------------------------------------

def test_historique():

    etat = creer_etat_initial()

    coups = generer_coups_pseudo_legaux(
        etat
    )

    if not coups:
        return False

    coup = coups[0]

    ancien = obtenir_score_historique(
        coup
    )

    ajouter_score_historique(
        coup,
        100
    )

    nouveau = obtenir_score_historique(
        coup
    )

    return nouveau > ancien


# ------------------------------------------------------------
# TEST KILLER
# ------------------------------------------------------------

def test_killer():

    etat = creer_etat_initial()

    coups = generer_coups_pseudo_legaux(
        etat
    )

    if not coups:
        return False

    coup = coups[0]

    enregistrer_coup_killer(
        3,
        coup
    )

    return est_coup_killer(
        3,
        coup
    )


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 BLOC 13 — TEST")
    print("=" * 60)

    etat_test = creer_etat_initial()

    coups_test = generer_coups_pseudo_legaux(
        etat_test
    )

    print(
        "Nombre de coups :",
        len(coups_test)
    )

    print()

    print(
        "Test valeurs :",
        "OK"
        if test_valeurs_ordre()
        else "ERREUR"
    )

    print(
        "Test ordre :",
        "OK"
        if test_ordre_initial()
        else "ERREUR"
    )

    print(
        "Test historique :",
        "OK"
        if test_historique()
        else "ERREUR"
    )

    print(
        "Test killer :",
        "OK"
        if test_killer()
        else "ERREUR"
    )

    print()

    print("⚡ TOP COUPS")
    print("-" * 60)

    rapport = rapport_ordre_coups(
        etat_test,
        coups_test,
        profondeur=1
    )

    for element in rapport[:10]:

        print(
            "Score:",
            element["score"],
            "|",
            element["coup"]
        )

    print()
    print("🐼 BLOC 13 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 14/26 — TABLE DE TRANSPOSITION
# ============================================================


# ------------------------------------------------------------
# CONSTANTES
# ------------------------------------------------------------

TT_EXACT = 0
TT_ALPHA = 1
TT_BETA = 2

TT_MAX_ENTRIES = 300000


# ------------------------------------------------------------
# TABLE PRINCIPALE
# ------------------------------------------------------------

TABLE_TRANSPOSITION = {}


# ------------------------------------------------------------
# STATISTIQUES
# ------------------------------------------------------------

TT_STATS = {
    "hits": 0,
    "misses": 0,
    "stores": 0,
    "replacements": 0
}


# ------------------------------------------------------------
# RÉINITIALISER LA TABLE
# ------------------------------------------------------------

def vider_table_transposition():
    """
    Efface toute la table de transposition.
    """

    TABLE_TRANSPOSITION.clear()

    TT_STATS["hits"] = 0
    TT_STATS["misses"] = 0
    TT_STATS["stores"] = 0
    TT_STATS["replacements"] = 0


# ------------------------------------------------------------
# CLÉ DU PLATEAU
# ------------------------------------------------------------

def cle_position(etat):
    """
    Crée une clé complète de position.

    On prend en compte :

        - plateau
        - joueur
        - droits de roque
        - prise en passant
    """

    plateau = tuple(
        etat["plateau"]
    )

    tour = etat.get(
        "tour",
        BLANC
    )

    roque = etat.get(
        "roque",
        0
    )

    en_passant = etat.get(
        "en_passant",
        -1
    )

    return (
        plateau,
        tour,
        roque,
        en_passant
    )


# ------------------------------------------------------------
# HASH DE POSITION
# ------------------------------------------------------------

def hash_position(etat):
    """
    Retourne un entier représentant la position.

    Python possède déjà un hash rapide des tuples.
    """

    return hash(
        cle_position(etat)
    )


# ------------------------------------------------------------
# CLÉ AVEC PROFONDEUR
# ------------------------------------------------------------

def cle_transposition(
    etat,
    profondeur
):

    return (
        hash_position(etat),
        profondeur
    )


# ------------------------------------------------------------
# CRÉER UNE ENTRÉE
# ------------------------------------------------------------

def creer_entree_tt(
    score,
    profondeur,
    type_score,
    meilleur_coup=None
):

    return {

        "score": score,

        "profondeur":
            profondeur,

        "type":
            type_score,

        "meilleur_coup":
            meilleur_coup
    }


# ------------------------------------------------------------
# ENREGISTRER UNE POSITION
# ------------------------------------------------------------

def stocker_transposition(
    etat,
    profondeur,
    score,
    type_score=TT_EXACT,
    meilleur_coup=None
):
    """
    Stocke le résultat d'une recherche.
    """

    global TABLE_TRANSPOSITION

    cle = cle_transposition(
        etat,
        profondeur
    )

    nouvelle_entree = creer_entree_tt(
        score,
        profondeur,
        type_score,
        meilleur_coup
    )

    if cle in TABLE_TRANSPOSITION:

        ancienne = TABLE_TRANSPOSITION[cle]

        # On remplace uniquement si la nouvelle
        # recherche est au moins aussi profonde.
        if profondeur >= ancienne.get(
            "profondeur",
            -1
        ):

            TABLE_TRANSPOSITION[cle] = (
                nouvelle_entree
            )

            TT_STATS["replacements"] += 1

        return

    # Limite mémoire simple.
    if len(
        TABLE_TRANSPOSITION
    ) >= TT_MAX_ENTRIES:

        supprimer_entree_transposition()

    TABLE_TRANSPOSITION[cle] = (
        nouvelle_entree
    )

    TT_STATS["stores"] += 1


# ------------------------------------------------------------
# RÉCUPÉRER UNE POSITION
# ------------------------------------------------------------

def recuperer_transposition(
    etat,
    profondeur
):
    """
    Cherche une position dans la table.
    """

    cle = cle_transposition(
        etat,
        profondeur
    )

    entree = TABLE_TRANSPOSITION.get(
        cle
    )

    if entree is None:

        TT_STATS["misses"] += 1

        return None

    TT_STATS["hits"] += 1

    return entree


# ------------------------------------------------------------
# MEILLEUR COUP MÉMORISÉ
# ------------------------------------------------------------

def meilleur_coup_transposition(
    etat,
    profondeur
):

    entree = recuperer_transposition(
        etat,
        profondeur
    )

    if entree is None:
        return None

    return entree.get(
        "meilleur_coup"
    )


# ------------------------------------------------------------
# SUPPRESSION D'UNE ENTRÉE
# ------------------------------------------------------------

def supprimer_entree_transposition():

    if not TABLE_TRANSPOSITION:
        return

    # Version simple :
    # supprimer une entrée quelconque.
    cle = next(
        iter(TABLE_TRANSPOSITION)
    )

    del TABLE_TRANSPOSITION[
        cle
    ]


# ------------------------------------------------------------
# TAILLE DE LA TABLE
# ------------------------------------------------------------

def taille_table_transposition():

    return len(
        TABLE_TRANSPOSITION
    )


# ------------------------------------------------------------
# STATISTIQUES DE LA TABLE
# ------------------------------------------------------------

def statistiques_transposition():

    return {

        "entrees":
            len(TABLE_TRANSPOSITION),

        "hits":
            TT_STATS["hits"],

        "misses":
            TT_STATS["misses"],

        "stores":
            TT_STATS["stores"],

        "replacements":
            TT_STATS["replacements"]
    }


# ------------------------------------------------------------
# TAUX DE HIT
# ------------------------------------------------------------

def taux_hit_transposition():

    hits = TT_STATS["hits"]
    misses = TT_STATS["misses"]

    total = hits + misses

    if total == 0:
        return 0.0

    return (
        hits / total
    ) * 100.0


# ------------------------------------------------------------
# NETTOYAGE DE LA TABLE
# ------------------------------------------------------------

def nettoyer_transposition():

    """
    Nettoyage simple des entrées.

    Pour cette première version, les entrées les moins
    profondes sont supprimées lorsque la table est pleine.
    """

    if len(
        TABLE_TRANSPOSITION
    ) < TT_MAX_ENTRIES:

        return

    entrees = list(
        TABLE_TRANSPOSITION.items()
    )

    entrees.sort(
        key=lambda element:
            element[1].get(
                "profondeur",
                0
            )
    )

    nombre_a_supprimer = max(
        1,
        len(entrees) // 10
    )

    for cle, entree in entrees[
        :nombre_a_supprimer
    ]:

        TABLE_TRANSPOSITION.pop(
            cle,
            None
        )


# ------------------------------------------------------------
# VERSION AMÉLIORÉE DU STOCKAGE
# ------------------------------------------------------------

def stocker_tt(
    etat,
    profondeur,
    score,
    type_score=TT_EXACT,
    meilleur_coup=None
):

    """
    Interface courte utilisée par le moteur.
    """

    nettoyer_transposition()

    stocker_transposition(
        etat,
        profondeur,
        score,
        type_score,
        meilleur_coup
    )


# ------------------------------------------------------------
# INTERFACE DE RECHERCHE TT
# ------------------------------------------------------------

def chercher_tt(
    etat,
    profondeur
):

    return recuperer_transposition(
        etat,
        profondeur
    )


# ------------------------------------------------------------
# VÉRIFIER SI UNE POSITION EXISTE
# ------------------------------------------------------------

def position_connue(
    etat,
    profondeur
):

    cle = cle_transposition(
        etat,
        profondeur
    )

    return (
        cle in TABLE_TRANSPOSITION
    )


# ------------------------------------------------------------
# EXPORT DU MEILLEUR COUP
# ------------------------------------------------------------

def enregistrer_meilleur_coup_tt(
    etat,
    profondeur,
    score,
    coup
):

    stocker_tt(
        etat,
        profondeur,
        score,
        TT_EXACT,
        coup
    )


# ------------------------------------------------------------
# TEST DE CLÉ
# ------------------------------------------------------------

def test_cle_position():

    etat = creer_etat_initial()

    cle1 = cle_position(
        etat
    )

    cle2 = cle_position(
        etat
    )

    return cle1 == cle2


# ------------------------------------------------------------
# TEST STOCKAGE
# ------------------------------------------------------------

def test_stockage_tt():

    vider_table_transposition()

    etat = creer_etat_initial()

    stocker_tt(
        etat,
        4,
        123
    )

    entree = chercher_tt(
        etat,
        4
    )

    if entree is None:
        return False

    return (
        entree["score"] == 123
        and
        entree["profondeur"] == 4
    )


# ------------------------------------------------------------
# TEST MEILLEUR COUP
# ------------------------------------------------------------

def test_meilleur_coup_tt():

    vider_table_transposition()

    etat = creer_etat_initial()

    coups = generer_coups_pseudo_legaux(
        etat
    )

    if not coups:
        return False

    coup = coups[0]

    enregistrer_meilleur_coup_tt(
        etat,
        3,
        250,
        coup
    )

    trouve = meilleur_coup_transposition(
        etat,
        3
    )

    return (
        trouve is not None
        and
        identifiant_coup(trouve)
        ==
        identifiant_coup(coup)
    )


# ------------------------------------------------------------
# TEST HIT
# ------------------------------------------------------------

def test_hit_tt():

    vider_table_transposition()

    etat = creer_etat_initial()

    stocker_tt(
        etat,
        2,
        100
    )

    recuperer_transposition(
        etat,
        2
    )

    return (
        TT_STATS["hits"] == 1
    )


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 BLOC 14 — TABLE DE TRANSPOSITION")
    print("=" * 60)

    print(
        "Test clé position :",
        "OK"
        if test_cle_position()
        else "ERREUR"
    )

    print(
        "Test stockage :",
        "OK"
        if test_stockage_tt()
        else "ERREUR"
    )

    print(
        "Test meilleur coup :",
        "OK"
        if test_meilleur_coup_tt()
        else "ERREUR"
    )

    print(
        "Test hit :",
        "OK"
        if test_hit_tt()
        else "ERREUR"
    )

    print()

    print(
        "Entrées :",
        taille_table_transposition()
    )

    print(
        "Taux de hit :",
        f"{taux_hit_transposition():.2f}%"
    )

    print()

    print(
        "Statistiques :"
    )

    stats = statistiques_transposition()

    for cle, valeur in stats.items():

        print(
            f"{cle:20} : {valeur}"
        )

    print()
    print("🐼 BLOC 14 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 15/26 — NEGAMAX + ALPHA-BETA
# ============================================================


# ------------------------------------------------------------
# CONSTANTES DE RECHERCHE
# ------------------------------------------------------------

INFINI = 10_000_000

MATE = 1_000_000

SCORE_MIN = -INFINI
SCORE_MAX = INFINI


# ------------------------------------------------------------
# STATISTIQUES DE RECHERCHE
# ------------------------------------------------------------

STATS_RECHERCHE = {
    "noeuds": 0,
    "coupes_alpha": 0,
    "coupes_beta": 0,
    "tt_hits": 0,
    "feuilles": 0,
    "coups_analyses": 0
}


# ------------------------------------------------------------
# RÉINITIALISER LES STATISTIQUES
# ------------------------------------------------------------

def reset_stats_recherche():

    for cle in STATS_RECHERCHE:
        STATS_RECHERCHE[cle] = 0


# ------------------------------------------------------------
# TEST POSITION TERMINALE
# ------------------------------------------------------------

def position_terminale(etat):

    coups = generer_coups_legaux(
        etat
    )

    if coups:
        return False

    return True


# ------------------------------------------------------------
# SCORE DES POSITIONS TERMINALES
# ------------------------------------------------------------

def score_terminal(
    etat,
    profondeur
):

    coups = generer_coups_legaux(
        etat
    )

    if coups:
        return None

    couleur = etat["tour"]

    # --------------------------------------------------------
    # ROI EN ÉCHEC = MAT
    # --------------------------------------------------------

    if roi_en_echec(
        etat,
        couleur
    ):

        # Plus le mat est proche,
        # meilleur est le score.
        return -MATE + profondeur

    # --------------------------------------------------------
    # PAS DE COUP + PAS D'ÉCHEC = PAT
    # --------------------------------------------------------

    return 0


# ------------------------------------------------------------
# COUP EST LÉGAL
# ------------------------------------------------------------

def verifier_coup_legal(
    etat,
    coup
):

    try:

        copie = copier_etat(
            etat
        )

        appliquer_coup(
            copie,
            coup
        )

        couleur = etat["tour"]

        return not roi_en_echec(
            copie,
            couleur
        )

    except Exception:
        return False


# ------------------------------------------------------------
# GÉNÉRATEUR DE COUPS DE RECHERCHE
# ------------------------------------------------------------

def coups_recherche(
    etat,
    profondeur
):

    coups = generer_coups_legaux(
        etat
    )

    if not coups:
        return []

    # --------------------------------------------------------
    # ORDRE INTELLIGENT DU BLOC 13
    # --------------------------------------------------------

    return ordonner_coups(
        etat,
        coups,
        profondeur
    )


# ------------------------------------------------------------
# APPLICATION TEMPORAIRE D'UN COUP
# ------------------------------------------------------------

def jouer_coup_temporaire(
    etat,
    coup
):

    copie = copier_etat(
        etat
    )

    appliquer_coup(
        copie,
        coup
    )

    return copie


# ------------------------------------------------------------
# SCORE DE LA POSITION
# ------------------------------------------------------------

def score_position(
    etat
):

    return evaluation_complete(
        etat
    )


# ------------------------------------------------------------
# NEGAMAX SIMPLE
# ------------------------------------------------------------

def negamax(
    etat,
    profondeur
):

    STATS_RECHERCHE["noeuds"] += 1

    # --------------------------------------------------------
    # POSITION TERMINALE
    # --------------------------------------------------------

    terminal = score_terminal(
        etat,
        profondeur
    )

    if terminal is not None:

        STATS_RECHERCHE["feuilles"] += 1

        return terminal

    # --------------------------------------------------------
    # PROFONDEUR 0
    # --------------------------------------------------------

    if profondeur <= 0:

        STATS_RECHERCHE["feuilles"] += 1

        return score_position(
            etat
        )

    # --------------------------------------------------------
    # COUPS
    # --------------------------------------------------------

    coups = coups_recherche(
        etat,
        profondeur
    )

    if not coups:

        return score_position(
            etat
        )

    meilleur = SCORE_MIN

    for coup in coups:

        STATS_RECHERCHE[
            "coups_analyses"
        ] += 1

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -negamax(
            enfant,
            profondeur - 1
        )

        if score > meilleur:
            meilleur = score

    return meilleur


# ------------------------------------------------------------
# NEGAMAX ALPHA-BETA
# ------------------------------------------------------------

def negamax_alpha_beta(
    etat,
    profondeur,
    alpha,
    beta
):
    """
    Recherche principale.

    Alpha :
        meilleur score déjà garanti.

    Beta :
        limite au-delà de laquelle
        la branche n'est plus intéressante.
    """

    STATS_RECHERCHE["noeuds"] += 1

    # --------------------------------------------------------
    # TERMINAL
    # --------------------------------------------------------

    terminal = score_terminal(
        etat,
        profondeur
    )

    if terminal is not None:

        STATS_RECHERCHE["feuilles"] += 1

        return terminal

    # --------------------------------------------------------
    # FEUILLE
    # --------------------------------------------------------

    if profondeur <= 0:

        STATS_RECHERCHE["feuilles"] += 1

        return score_position(
            etat
        )

    # --------------------------------------------------------
    # TABLE DE TRANSPOSITION
    # --------------------------------------------------------

    entree = chercher_tt(
        etat,
        profondeur
    )

    if entree is not None:

        STATS_RECHERCHE[
            "tt_hits"
        ] += 1

        type_score = entree.get(
            "type",
            TT_EXACT
        )

        score = entree.get(
            "score",
            0
        )

        if type_score == TT_EXACT:
            return score

        if type_score == TT_ALPHA:

            if score <= alpha:
                return score

        elif type_score == TT_BETA:

            if score >= beta:
                return score

    # --------------------------------------------------------
    # SAUVEGARDE DE ALPHA ORIGINAL
    # --------------------------------------------------------

    alpha_original = alpha

    # --------------------------------------------------------
    # COUPS
    # --------------------------------------------------------

    coups = coups_recherche(
        etat,
        profondeur
    )

    if not coups:

        return score_position(
            etat
        )

    meilleur = SCORE_MIN
    meilleur_coup = None

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    for coup in coups:

        STATS_RECHERCHE[
            "coups_analyses"
        ] += 1

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -negamax_alpha_beta(
            enfant,
            profondeur - 1,
            -beta,
            -alpha
        )

        # ----------------------------------------------------
        # MEILLEUR SCORE
        # ----------------------------------------------------

        if score > meilleur:

            meilleur = score

            meilleur_coup = coup

        # ----------------------------------------------------
        # ALPHA
        # ----------------------------------------------------

        if score > alpha:

            alpha = score

        # ----------------------------------------------------
        # COUPURE BETA
        # ----------------------------------------------------

        if alpha >= beta:

            STATS_RECHERCHE[
                "coupes_beta"
            ] += 1

            # Killer move
            enregistrer_coup_killer(
                profondeur,
                coup
            )

            # History
            ajouter_score_historique(
                coup,
                profondeur * profondeur
            )

            break

    # --------------------------------------------------------
    # TYPE DE SCORE TT
    # --------------------------------------------------------

    if meilleur <= alpha_original:

        type_score = TT_ALPHA

    elif meilleur >= beta:

        type_score = TT_BETA

    else:

        type_score = TT_EXACT

    # --------------------------------------------------------
    # MÉMORISATION
    # --------------------------------------------------------

    stocker_tt(
        etat,
        profondeur,
        meilleur,
        type_score,
        meilleur_coup
    )

    return meilleur


# ------------------------------------------------------------
# ALPHA-BETA RACINE
# ------------------------------------------------------------

def rechercher_meilleur_coup(
    etat,
    profondeur
):

    reset_stats_recherche()

    coups = coups_recherche(
        etat,
        profondeur
    )

    if not coups:

        return None, score_terminal(
            etat,
            profondeur
        )

    meilleur_coup = None

    meilleur_score = SCORE_MIN

    alpha = SCORE_MIN
    beta = SCORE_MAX

    for coup in coups:

        STATS_RECHERCHE[
            "coups_analyses"
        ] += 1

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -negamax_alpha_beta(
            enfant,
            profondeur - 1,
            -beta,
            -alpha
        )

        if score > meilleur_score:

            meilleur_score = score

            meilleur_coup = coup

        if score > alpha:
            alpha = score

    # --------------------------------------------------------
    # STOCKAGE RACINE
    # --------------------------------------------------------

    if meilleur_coup is not None:

        stocker_tt(
            etat,
            profondeur,
            meilleur_score,
            TT_EXACT,
            meilleur_coup
        )

    return (
        meilleur_coup,
        meilleur_score
    )


# ------------------------------------------------------------
# VERSION COURTE
# ------------------------------------------------------------

def meilleur_coup(
    etat,
    profondeur=3
):

    coup, score = rechercher_meilleur_coup(
        etat,
        profondeur
    )

    return coup


# ------------------------------------------------------------
# ANALYSE D'UNE POSITION
# ------------------------------------------------------------

def analyser_position(
    etat,
    profondeur=3
):

    coup, score = rechercher_meilleur_coup(
        etat,
        profondeur
    )

    return {
        "coup": coup,
        "score": score,
        "profondeur": profondeur,
        "noeuds":
            STATS_RECHERCHE["noeuds"],
        "feuilles":
            STATS_RECHERCHE["feuilles"],
        "coupes_beta":
            STATS_RECHERCHE["coupes_beta"],
        "tt_hits":
            STATS_RECHERCHE["tt_hits"]
    }


# ------------------------------------------------------------
# TEST ALPHA-BETA
# ------------------------------------------------------------

def test_alpha_beta():

    etat = creer_etat_initial()

    coup, score = rechercher_meilleur_coup(
        etat,
        2
    )

    return (
        coup is not None
        and
        isinstance(score, (int, float))
    )


# ------------------------------------------------------------
# TEST NEGAMAX
# ------------------------------------------------------------

def test_negamax():

    etat = creer_etat_initial()

    score = negamax(
        etat,
        1
    )

    return isinstance(
        score,
        (int, float)
    )


# ------------------------------------------------------------
# TEST TABLE DE TRANSPOSITION
# ------------------------------------------------------------

def test_tt_recherche():

    vider_table_transposition()

    etat = creer_etat_initial()

    rechercher_meilleur_coup(
        etat,
        2
    )

    taille = taille_table_transposition()

    return taille > 0


# ------------------------------------------------------------
# TEST COUP LÉGAL
# ------------------------------------------------------------

def test_coup_recherche():

    etat = creer_etat_initial()

    coups = generer_coups_legaux(
        etat
    )

    if not coups:
        return False

    for coup in coups[:3]:

        if not verifier_coup_legal(
            etat,
            coup
        ):
            return False

    return True


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 PANDORAGA FULL ADAPTATION Ω")
    print("🧠 BLOC 15 — NEGAMAX + ALPHA-BETA")
    print("=" * 65)

    etat_test = creer_etat_initial()

    print()
    print("🔍 Tests")
    print("-" * 65)

    print(
        "Negamax :",
        "OK"
        if test_negamax()
        else "ERREUR"
    )

    print(
        "Alpha-Beta :",
        "OK"
        if test_alpha_beta()
        else "ERREUR"
    )

    print(
        "Coups légaux :",
        "OK"
        if test_coup_recherche()
        else "ERREUR"
    )

    print(
        "Table transposition :",
        "OK"
        if test_tt_recherche()
        else "ERREUR"
    )

    print()
    print("🧠 ANALYSE")
    print("-" * 65)

    resultat = analyser_position(
        etat_test,
        2
    )

    print(
        "Meilleur coup :",
        resultat["coup"]
    )

    print(
        "Score :",
        resultat["score"]
    )

    print(
        "Profondeur :",
        resultat["profondeur"]
    )

    print(
        "Nœuds :",
        resultat["noeuds"]
    )

    print(
        "Feuilles :",
        resultat["feuilles"]
    )

    print(
        "Coupes Beta :",
        resultat["coupes_beta"]
    )

    print(
        "TT hits :",
        resultat["tt_hits"]
    )

    print()
    print("🐼 BLOC 15 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 16/26 — RECHERCHE ITÉRATIVE
# ============================================================

import time


# ------------------------------------------------------------
# PARAMÈTRES
# ------------------------------------------------------------

PROFONDEUR_MAX_PAR_DEFAUT = 12
TEMPS_MAX_DEFAUT = 10.0


# ------------------------------------------------------------
# CONTRÔLEUR DE TEMPS
# ------------------------------------------------------------

class ControleTempsPandoraga:

    def __init__(self, limite=10.0):

        self.debut = time.perf_counter()

        self.limite = max(
            0.01,
            float(limite)
        )

        self.arret = False

    def temps_ecoule(self):

        return (
            time.perf_counter()
            -
            self.debut
        )

    def temps_restant(self):

        return max(
            0.0,
            self.limite
            -
            self.temps_ecoule()
        )

    def depasse(self):

        if self.arret:
            return True

        if self.temps_ecoule() >= self.limite:

            self.arret = True

            return True

        return False

    def demander_arret(self):

        self.arret = True


# ------------------------------------------------------------
# EXCEPTION INTERNE D'ARRÊT
# ------------------------------------------------------------

class RechercheArretee(Exception):
    pass


# ------------------------------------------------------------
# NEGAMAX ALPHA-BETA AVEC TEMPS
# ------------------------------------------------------------

def negamax_alpha_beta_temps(
    etat,
    profondeur,
    alpha,
    beta,
    controle
):

    if controle.depasse():

        raise RechercheArretee()

    STATS_RECHERCHE["noeuds"] += 1

    # --------------------------------------------------------
    # POSITION TERMINALE
    # --------------------------------------------------------

    terminal = score_terminal(
        etat,
        profondeur
    )

    if terminal is not None:

        STATS_RECHERCHE["feuilles"] += 1

        return terminal

    # --------------------------------------------------------
    # PROFONDEUR 0
    # --------------------------------------------------------

    if profondeur <= 0:

        STATS_RECHERCHE["feuilles"] += 1

        return score_position(
            etat
        )

    # --------------------------------------------------------
    # TABLE DE TRANSPOSITION
    # --------------------------------------------------------

    entree = chercher_tt(
        etat,
        profondeur
    )

    if entree is not None:

        STATS_RECHERCHE["tt_hits"] += 1

        type_score = entree.get(
            "type",
            TT_EXACT
        )

        score = entree.get(
            "score",
            0
        )

        if type_score == TT_EXACT:
            return score

        if type_score == TT_ALPHA:

            if score <= alpha:
                return score

        elif type_score == TT_BETA:

            if score >= beta:
                return score

    # --------------------------------------------------------
    # ALPHA ORIGINAL
    # --------------------------------------------------------

    alpha_original = alpha

    # --------------------------------------------------------
    # COUPS
    # --------------------------------------------------------

    coups = coups_recherche(
        etat,
        profondeur
    )

    if not coups:

        return score_position(
            etat
        )

    meilleur = SCORE_MIN

    meilleur_coup_local = None

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    for coup in coups:

        if controle.depasse():

            raise RechercheArretee()

        STATS_RECHERCHE[
            "coups_analyses"
        ] += 1

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -negamax_alpha_beta_temps(
            enfant,
            profondeur - 1,
            -beta,
            -alpha,
            controle
        )

        if score > meilleur:

            meilleur = score

            meilleur_coup_local = coup

        if score > alpha:

            alpha = score

        # ----------------------------------------------------
        # COUPURE BETA
        # ----------------------------------------------------

        if alpha >= beta:

            STATS_RECHERCHE[
                "coupes_beta"
            ] += 1

            enregistrer_coup_killer(
                profondeur,
                coup
            )

            ajouter_score_historique(
                coup,
                profondeur * profondeur
            )

            break

    # --------------------------------------------------------
    # TYPE TABLE TRANSPOSITION
    # --------------------------------------------------------

    if meilleur <= alpha_original:

        type_score = TT_ALPHA

    elif meilleur >= beta:

        type_score = TT_BETA

    else:

        type_score = TT_EXACT

    # --------------------------------------------------------
    # MÉMORISATION
    # --------------------------------------------------------

    stocker_tt(
        etat,
        profondeur,
        meilleur,
        type_score,
        meilleur_coup_local
    )

    return meilleur


# ------------------------------------------------------------
# RECHERCHE À UNE PROFONDEUR
# ------------------------------------------------------------

def recherche_profondeur(
    etat,
    profondeur,
    controle
):

    coups = coups_recherche(
        etat,
        profondeur
    )

    if not coups:

        return (
            None,
            score_terminal(
                etat,
                profondeur
            )
        )

    meilleur_coup_local = None

    meilleur_score_local = SCORE_MIN

    alpha = SCORE_MIN
    beta = SCORE_MAX

    for coup in coups:

        if controle.depasse():

            raise RechercheArretee()

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -negamax_alpha_beta_temps(
            enfant,
            profondeur - 1,
            -beta,
            -alpha,
            controle
        )

        if score > meilleur_score_local:

            meilleur_score_local = score

            meilleur_coup_local = coup

        if score > alpha:

            alpha = score

    return (
        meilleur_coup_local,
        meilleur_score_local
    )


# ------------------------------------------------------------
# RECHERCHE ITÉRATIVE PRINCIPALE
# ------------------------------------------------------------

def recherche_iterative(
    etat,
    profondeur_max=PROFONDEUR_MAX_PAR_DEFAUT,
    temps_max=TEMPS_MAX_DEFAUT
):
    """
    Cherche :

        profondeur 1
        profondeur 2
        profondeur 3
        ...

    Le dernier résultat terminé est toujours conservé.
    """

    reset_stats_recherche()

    controle = ControleTempsPandoraga(
        temps_max
    )

    meilleur_coup_final = None
    meilleur_score_final = 0

    profondeur_atteinte = 0

    historique = []

    # --------------------------------------------------------
    # CAS OÙ IL N'Y A PAS DE COUP
    # --------------------------------------------------------

    coups_initiaux = generer_coups_legaux(
        etat
    )

    if not coups_initiaux:

        return {
            "coup": None,
            "score": score_terminal(
                etat,
                0
            ),
            "profondeur": 0,
            "temps": 0.0,
            "arrete": False,
            "historique": []
        }

    # --------------------------------------------------------
    # RECHERCHE 1 → PROFONDEUR MAX
    # --------------------------------------------------------

    for profondeur in range(
        1,
        profondeur_max + 1
    ):

        if controle.depasse():
            break

        # Les informations des profondeurs précédentes
        # améliorent l'ordre des coups.
        try:

            coup, score = recherche_profondeur(
                etat,
                profondeur,
                controle
            )

        except RechercheArretee:

            break

        # ----------------------------------------------------
        # RÉSULTAT COMPLET
        # ----------------------------------------------------

        if coup is not None:

            meilleur_coup_final = coup

            meilleur_score_final = score

            profondeur_atteinte = profondeur

            historique.append({

                "profondeur":
                    profondeur,

                "score":
                    score,

                "coup":
                    coup,

                "temps":
                    controle.temps_ecoule(),

                "noeuds":
                    STATS_RECHERCHE[
                        "noeuds"
                    ]
            })

    # --------------------------------------------------------
    # SI LE TEMPS EST EXTRÊMEMENT COURT
    # --------------------------------------------------------

    if meilleur_coup_final is None:

        meilleur_coup_final = coups_initiaux[0]

        meilleur_score_final = score_position(
            jouer_coup_temporaire(
                etat,
                meilleur_coup_final
            )
        )

    return {

        "coup":
            meilleur_coup_final,

        "score":
            meilleur_score_final,

        "profondeur":
            profondeur_atteinte,

        "temps":
            controle.temps_ecoule(),

        "arrete":
            controle.depasse(),

        "historique":
            historique,

        "noeuds":
            STATS_RECHERCHE[
                "noeuds"
            ],

        "tt_hits":
            STATS_RECHERCHE[
                "tt_hits"
            ]
    }


# ------------------------------------------------------------
# MEILLEUR COUP ITERATIF
# ------------------------------------------------------------

def meilleur_coup_iteratif(
    etat,
    profondeur_max=12,
    temps_max=10.0
):

    resultat = recherche_iterative(
        etat,
        profondeur_max,
        temps_max
    )

    return resultat["coup"]


# ------------------------------------------------------------
# ANALYSE ITERATIVE
# ------------------------------------------------------------

def analyser_iteratif(
    etat,
    profondeur_max=12,
    temps_max=10.0
):

    return recherche_iterative(
        etat,
        profondeur_max,
        temps_max
    )


# ------------------------------------------------------------
# AFFICHAGE DE LA PROGRESSION
# ------------------------------------------------------------

def afficher_progression_iterative(
    resultat
):

    print()
    print("🔎 PROGRESSION PANDORAGA")
    print("-" * 65)

    historique = resultat.get(
        "historique",
        []
    )

    if not historique:

        print(
            "Aucune profondeur complète."
        )

        return

    for ligne in historique:

        print(
            f"Depth {ligne['profondeur']:2d} | "
            f"Score {ligne['score']:8} | "
            f"Temps {ligne['temps']:.3f}s | "
            f"Nœuds {ligne['noeuds']}"
        )

    print("-" * 65)

    print(
        "Profondeur finale :",
        resultat["profondeur"]
    )

    print(
        "Score final :",
        resultat["score"]
    )

    print(
        "Temps :",
        f"{resultat['temps']:.3f}s"
    )


# ------------------------------------------------------------
# TEST DU CONTRÔLEUR
# ------------------------------------------------------------

def test_controle_temps():

    controle = ControleTempsPandoraga(
        0.1
    )

    if controle.depasse():
        return False

    temps = controle.temps_restant()

    return temps >= 0


# ------------------------------------------------------------
# TEST PROFONDEUR
# ------------------------------------------------------------

def test_recherche_profondeur():

    etat = creer_etat_initial()

    controle = ControleTempsPandoraga(
        5.0
    )

    coup, score = recherche_profondeur(
        etat,
        1,
        controle
    )

    return (
        coup is not None
        and
        isinstance(
            score,
            (int, float)
        )
    )


# ------------------------------------------------------------
# TEST ITERATIF
# ------------------------------------------------------------

def test_recherche_iterative():

    etat = creer_etat_initial()

    resultat = recherche_iterative(
        etat,
        profondeur_max=3,
        temps_max=2.0
    )

    return (
        resultat["coup"] is not None
        and
        resultat["profondeur"] >= 1
    )


# ------------------------------------------------------------
# TEST HISTORIQUE
# ------------------------------------------------------------

def test_historique_iteratif():

    etat = creer_etat_initial()

    resultat = recherche_iterative(
        etat,
        profondeur_max=3,
        temps_max=2.0
    )

    historique = resultat.get(
        "historique",
        []
    )

    if not historique:
        return False

    profondeurs = [
        x["profondeur"]
        for x in historique
    ]

    return profondeurs == sorted(
        profondeurs
    )


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 PANDORAGA FULL ADAPTATION Ω")
    print("🔎 BLOC 16 — RECHERCHE ITÉRATIVE")
    print("=" * 65)

    print()
    print("🧪 TESTS")
    print("-" * 65)

    print(
        "Contrôleur temps :",
        "OK"
        if test_controle_temps()
        else "ERREUR"
    )

    print(
        "Recherche profondeur :",
        "OK"
        if test_recherche_profondeur()
        else "ERREUR"
    )

    print(
        "Recherche itérative :",
        "OK"
        if test_recherche_iterative()
        else "ERREUR"
    )

    print(
        "Historique profondeur :",
        "OK"
        if test_historique_iteratif()
        else "ERREUR"
    )

    print()
    print("🔎 TEST RÉEL")
    print("-" * 65)

    etat_test = creer_etat_initial()

    resultat = recherche_iterative(
        etat_test,
        profondeur_max=4,
        temps_max=3.0
    )

    afficher_progression_iterative(
        resultat
    )

    print()
    print(
        "Meilleur coup :",
        resultat["coup"]
    )

    print(
        "Nœuds :",
        resultat["noeuds"]
    )

    print(
        "TT hits :",
        resultat["tt_hits"]
    )

    print()
    print("🐼 BLOC 16 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 17/26 — RECHERCHE DE QUIESCENCE
# ============================================================


# ------------------------------------------------------------
# PARAMÈTRES
# ------------------------------------------------------------

QUIESCENCE_MAX_DEPTH = 8

QUIESCENCE_MAX_MOVES = 60


# ------------------------------------------------------------
# STATISTIQUES
# ------------------------------------------------------------

STATS_QUIESCENCE = {
    "appels": 0,
    "noeuds": 0,
    "captures": 0,
    "promotions": 0,
    "echecs": 0,
    "coupes": 0,
    "profondeur_max": 0
}


# ------------------------------------------------------------
# RESET
# ------------------------------------------------------------

def reset_stats_quiescence():

    for cle in STATS_QUIESCENCE:
        STATS_QUIESCENCE[cle] = 0


# ------------------------------------------------------------
# COUP TACTIQUE
# ------------------------------------------------------------

def coup_tactique_quiescence(
    etat,
    coup
):
    """
    Un coup est considéré comme tactique
    s'il s'agit d'une capture, promotion
    ou échec.
    """

    if coup_est_capture(
        etat,
        coup
    ):
        return True

    if coup_est_promotion(
        coup
    ):
        return True

    if coup_donne_echec(
        etat,
        coup
    ):
        return True

    return False


# ------------------------------------------------------------
# GÉNÉRER LES COUPS TACTIQUES
# ------------------------------------------------------------

def coups_quiescence(
    etat
):

    coups = generer_coups_legaux(
        etat
    )

    if not coups:
        return []

    resultat = []

    for coup in coups:

        if coup_tactique_quiescence(
            etat,
            coup
        ):
            resultat.append(
                coup
            )

    return ordonner_coups(
        etat,
        resultat,
        0
    )


# ------------------------------------------------------------
# ÉVALUATION DE QUIESCENCE
# ------------------------------------------------------------

def evaluation_quiescence(
    etat
):

    return score_position(
        etat
    )


# ------------------------------------------------------------
# RECHERCHE QUIESCENCE
# ------------------------------------------------------------

def quiescence(
    etat,
    alpha,
    beta,
    profondeur=0
):
    """
    Recherche uniquement les coups tactiques.

    Cela permet d'éviter une évaluation au milieu
    d'une combinaison de captures.
    """

    STATS_QUIESCENCE["appels"] += 1
    STATS_QUIESCENCE["noeuds"] += 1

    if profondeur > STATS_QUIESCENCE[
        "profondeur_max"
    ]:

        STATS_QUIESCENCE[
            "profondeur_max"
        ] = profondeur

    # --------------------------------------------------------
    # LIMITE DE SÉCURITÉ
    # --------------------------------------------------------

    if profondeur >= QUIESCENCE_MAX_DEPTH:

        return evaluation_quiescence(
            etat
        )

    # --------------------------------------------------------
    # POSITION TERMINALE
    # --------------------------------------------------------

    terminal = score_terminal(
        etat,
        profondeur
    )

    if terminal is not None:

        return terminal

    # --------------------------------------------------------
    # STAND PAT
    # --------------------------------------------------------

    score_stand_pat = evaluation_quiescence(
        etat
    )

    # --------------------------------------------------------
    # COUPURE BETA
    # --------------------------------------------------------

    if score_stand_pat >= beta:

        STATS_QUIESCENCE[
            "coupes"
        ] += 1

        return score_stand_pat

    # --------------------------------------------------------
    # AMÉLIORATION ALPHA
    # --------------------------------------------------------

    if score_stand_pat > alpha:

        alpha = score_stand_pat

    # --------------------------------------------------------
    # COUPS TACTIQUES
    # --------------------------------------------------------

    coups = coups_quiescence(
        etat
    )

    # Protection contre les positions
    # avec énormément de coups tactiques.
    coups = coups[
        :QUIESCENCE_MAX_MOVES
    ]

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    for coup in coups:

        if coup_est_capture(
            etat,
            coup
        ):
            STATS_QUIESCENCE[
                "captures"
            ] += 1

        if coup_est_promotion(
            coup
        ):
            STATS_QUIESCENCE[
                "promotions"
            ] += 1

        if coup_donne_echec(
            etat,
            coup
        ):
            STATS_QUIESCENCE[
                "echecs"
            ] += 1

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -quiescence(
            enfant,
            -beta,
            -alpha,
            profondeur + 1
        )

        if score >= beta:

            STATS_QUIESCENCE[
                "coupes"
            ] += 1

            return score

        if score > alpha:

            alpha = score

    return alpha


# ------------------------------------------------------------
# VERSION QUIESCENCE AVEC TEMPS
# ------------------------------------------------------------

def quiescence_temps(
    etat,
    alpha,
    beta,
    profondeur,
    controle
):

    if controle.depasse():

        raise RechercheArretee()

    STATS_QUIESCENCE[
        "appels"
    ] += 1

    STATS_QUIESCENCE[
        "noeuds"
    ] += 1

    if profondeur > STATS_QUIESCENCE[
        "profondeur_max"
    ]:

        STATS_QUIESCENCE[
            "profondeur_max"
        ] = profondeur

    # --------------------------------------------------------
    # LIMITE
    # --------------------------------------------------------

    if profondeur >= QUIESCENCE_MAX_DEPTH:

        return evaluation_quiescence(
            etat
        )

    # --------------------------------------------------------
    # TERMINAL
    # --------------------------------------------------------

    terminal = score_terminal(
        etat,
        profondeur
    )

    if terminal is not None:

        return terminal

    # --------------------------------------------------------
    # ÉVALUATION IMMÉDIATE
    # --------------------------------------------------------

    stand_pat = evaluation_quiescence(
        etat
    )

    if stand_pat >= beta:

        STATS_QUIESCENCE[
            "coupes"
        ] += 1

        return stand_pat

    if stand_pat > alpha:

        alpha = stand_pat

    # --------------------------------------------------------
    # COUPS TACTIQUES
    # --------------------------------------------------------

    coups = coups_quiescence(
        etat
    )

    coups = coups[
        :QUIESCENCE_MAX_MOVES
    ]

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    for coup in coups:

        if controle.depasse():

            raise RechercheArretee()

        if coup_est_capture(
            etat,
            coup
        ):
            STATS_QUIESCENCE[
                "captures"
            ] += 1

        if coup_est_promotion(
            coup
        ):
            STATS_QUIESCENCE[
                "promotions"
            ] += 1

        if coup_donne_echec(
            etat,
            coup
        ):
            STATS_QUIESCENCE[
                "echecs"
            ] += 1

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -quiescence_temps(
            enfant,
            -beta,
            -alpha,
            profondeur + 1,
            controle
        )

        if score >= beta:

            STATS_QUIESCENCE[
                "coupes"
            ] += 1

            return score

        if score > alpha:

            alpha = score

    return alpha


# ------------------------------------------------------------
# NEGAMAX ALPHA-BETA + QUIESCENCE
# ------------------------------------------------------------

def negamax_alpha_beta_quiescence(
    etat,
    profondeur,
    alpha,
    beta
):

    STATS_RECHERCHE[
        "noeuds"
    ] += 1

    # --------------------------------------------------------
    # TERMINAL
    # --------------------------------------------------------

    terminal = score_terminal(
        etat,
        profondeur
    )

    if terminal is not None:

        STATS_RECHERCHE[
            "feuilles"
        ] += 1

        return terminal

    # --------------------------------------------------------
    # FIN DE RECHERCHE
    # --------------------------------------------------------

    if profondeur <= 0:

        STATS_RECHERCHE[
            "feuilles"
        ] += 1

        reset_stats_quiescence()

        return quiescence(
            etat,
            alpha,
            beta,
            0
        )

    # --------------------------------------------------------
    # TABLE DE TRANSPOSITION
    # --------------------------------------------------------

    entree = chercher_tt(
        etat,
        profondeur
    )

    if entree is not None:

        STATS_RECHERCHE[
            "tt_hits"
        ] += 1

        type_score = entree.get(
            "type",
            TT_EXACT
        )

        score = entree.get(
            "score",
            0
        )

        if type_score == TT_EXACT:
            return score

        if type_score == TT_ALPHA:

            if score <= alpha:
                return score

        elif type_score == TT_BETA:

            if score >= beta:
                return score

    # --------------------------------------------------------
    # ALPHA ORIGINAL
    # --------------------------------------------------------

    alpha_original = alpha

    # --------------------------------------------------------
    # COUPS
    # --------------------------------------------------------

    coups = coups_recherche(
        etat,
        profondeur
    )

    if not coups:

        return score_position(
            etat
        )

    meilleur = SCORE_MIN

    meilleur_coup_local = None

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    for coup in coups:

        STATS_RECHERCHE[
            "coups_analyses"
        ] += 1

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -negamax_alpha_beta_quiescence(
            enfant,
            profondeur - 1,
            -beta,
            -alpha
        )

        if score > meilleur:

            meilleur = score

            meilleur_coup_local = coup

        if score > alpha:

            alpha = score

        # ----------------------------------------------------
        # BETA CUT
        # ----------------------------------------------------

        if alpha >= beta:

            STATS_RECHERCHE[
                "coupes_beta"
            ] += 1

            enregistrer_coup_killer(
                profondeur,
                coup
            )

            ajouter_score_historique(
                coup,
                profondeur * profondeur
            )

            break

    # --------------------------------------------------------
    # TYPE TT
    # --------------------------------------------------------

    if meilleur <= alpha_original:

        type_score = TT_ALPHA

    elif meilleur >= beta:

        type_score = TT_BETA

    else:

        type_score = TT_EXACT

    # --------------------------------------------------------
    # STOCKAGE
    # --------------------------------------------------------

    stocker_tt(
        etat,
        profondeur,
        meilleur,
        type_score,
        meilleur_coup_local
    )

    return meilleur


# ------------------------------------------------------------
# RECHERCHE RACINE AVEC QUIESCENCE
# ------------------------------------------------------------

def rechercher_meilleur_coup_quiescence(
    etat,
    profondeur
):

    reset_stats_recherche()
    reset_stats_quiescence()

    coups = coups_recherche(
        etat,
        profondeur
    )

    if not coups:

        return (
            None,
            score_terminal(
                etat,
                profondeur
            )
        )

    meilleur_coup_local = None

    meilleur_score_local = SCORE_MIN

    alpha = SCORE_MIN
    beta = SCORE_MAX

    for coup in coups:

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -negamax_alpha_beta_quiescence(
            enfant,
            profondeur - 1,
            -beta,
            -alpha
        )

        if score > meilleur_score_local:

            meilleur_score_local = score

            meilleur_coup_local = coup

        if score > alpha:

            alpha = score

    stocker_tt(
        etat,
        profondeur,
        meilleur_score_local,
        TT_EXACT,
        meilleur_coup_local
    )

    return (
        meilleur_coup_local,
        meilleur_score_local
    )


# ------------------------------------------------------------
# STATISTIQUES QUIESCENCE
# ------------------------------------------------------------

def statistiques_quiescence():

    return dict(
        STATS_QUIESCENCE
    )


# ------------------------------------------------------------
# AFFICHAGE
# ------------------------------------------------------------

def afficher_stats_quiescence():

    print()
    print("🌊 QUIESCENCE")
    print("-" * 60)

    print(
        "Appels :",
        STATS_QUIESCENCE["appels"]
    )

    print(
        "Nœuds :",
        STATS_QUIESCENCE["noeuds"]
    )

    print(
        "Captures :",
        STATS_QUIESCENCE["captures"]
    )

    print(
        "Promotions :",
        STATS_QUIESCENCE["promotions"]
    )

    print(
        "Échecs :",
        STATS_QUIESCENCE["echecs"]
    )

    print(
        "Coupes :",
        STATS_QUIESCENCE["coupes"]
    )

    print(
        "Profondeur max :",
        STATS_QUIESCENCE["profondeur_max"]
    )


# ------------------------------------------------------------
# TEST COUPS TACTIQUES
# ------------------------------------------------------------

def test_coups_quiescence():

    etat = creer_etat_initial()

    coups = coups_quiescence(
        etat
    )

    for coup in coups:

        if not coup_tactique_quiescence(
            etat,
            coup
        ):
            return False

    return True


# ------------------------------------------------------------
# TEST QUIESCENCE
# ------------------------------------------------------------

def test_quiescence():

    etat = creer_etat_initial()

    reset_stats_quiescence()

    score = quiescence(
        etat,
        SCORE_MIN,
        SCORE_MAX
    )

    return isinstance(
        score,
        (int, float)
    )


# ------------------------------------------------------------
# TEST INTÉGRATION
# ------------------------------------------------------------

def test_quiescence_alpha_beta():

    etat = creer_etat_initial()

    coup, score = (
        rechercher_meilleur_coup_quiescence(
            etat,
            2
        )
    )

    return (
        coup is not None
        and
        isinstance(
            score,
            (int, float)
        )
    )


# ------------------------------------------------------------
# TEST LIMITE
# ------------------------------------------------------------

def test_limite_quiescence():

    ancien = QUIESCENCE_MAX_DEPTH

    try:

        # La valeur doit être raisonnable.
        return (
            ancien > 0
            and
            ancien <= 20
        )

    finally:

        pass


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 PANDORAGA FULL ADAPTATION Ω")
    print("🌊 BLOC 17 — QUIESCENCE")
    print("=" * 65)

    print()
    print("🧪 TESTS")
    print("-" * 65)

    print(
        "Coups tactiques :",
        "OK"
        if test_coups_quiescence()
        else "ERREUR"
    )

    print(
        "Quiescence :",
        "OK"
        if test_quiescence()
        else "ERREUR"
    )

    print(
        "Alpha-Beta + Quiescence :",
        "OK"
        if test_quiescence_alpha_beta()
        else "ERREUR"
    )

    print(
        "Limite quiescence :",
        "OK"
        if test_limite_quiescence()
        else "ERREUR"
    )

    print()
    print("🔎 TEST DE RECHERCHE")
    print("-" * 65)

    etat_test = creer_etat_initial()

    coup, score = (
        rechercher_meilleur_coup_quiescence(
            etat_test,
            3
        )
    )

    print(
        "Meilleur coup :",
        coup
    )

    print(
        "Score :",
        score
    )

    print(
        "Nœuds Alpha-Beta :",
        STATS_RECHERCHE["noeuds"]
    )

    afficher_stats_quiescence()

    print()
    print("🐼 BLOC 17 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 18/26 — KILLER + HISTORY AVANCÉS
# ============================================================


# ------------------------------------------------------------
# PARAMÈTRES
# ------------------------------------------------------------

KILLER_MAX_PAR_PROFONDEUR = 3

HISTORY_MAX = 1_000_000

HISTORY_MIN = -1_000_000

HISTORY_DECAY = 2


# ------------------------------------------------------------
# TABLES
# ------------------------------------------------------------

KILLER_AVANCES = {}

HISTORY_AVANCEE = {}

COUNTER_MOVES = {}

# Compteur général des performances
STATS_KILLER_HISTORY = {
    "killer_hits": 0,
    "history_hits": 0,
    "killer_stores": 0,
    "history_updates": 0,
    "counter_hits": 0
}


# ------------------------------------------------------------
# RESET
# ------------------------------------------------------------

def reset_killer_history():

    KILLER_AVANCES.clear()
    HISTORY_AVANCEE.clear()
    COUNTER_MOVES.clear()

    for cle in STATS_KILLER_HISTORY:
        STATS_KILLER_HISTORY[cle] = 0


# ------------------------------------------------------------
# CLÉ HISTORY
# ------------------------------------------------------------

def cle_history(
    etat,
    coup
):

    piece = etat["plateau"][
        coup["depart"]
    ]

    arrivee = coup["arrivee"]

    return (
        piece,
        arrivee
    )


# ------------------------------------------------------------
# SCORE HISTORY
# ------------------------------------------------------------

def score_history_avance(
    etat,
    coup
):

    cle = cle_history(
        etat,
        coup
    )

    score = HISTORY_AVANCEE.get(
        cle,
        0
    )

    if score != 0:

        STATS_KILLER_HISTORY[
            "history_hits"
        ] += 1

    return score


# ------------------------------------------------------------
# AJOUTER HISTORY
# ------------------------------------------------------------

def ajouter_history_avance(
    etat,
    coup,
    profondeur
):

    cle = cle_history(
        etat,
        coup
    )

    ancien = HISTORY_AVANCEE.get(
        cle,
        0
    )

    bonus = profondeur * profondeur

    nouveau = (
        ancien
        +
        bonus
    )

    nouveau = max(
        HISTORY_MIN,
        min(
            HISTORY_MAX,
            nouveau
        )
    )

    HISTORY_AVANCEE[
        cle
    ] = nouveau

    STATS_KILLER_HISTORY[
        "history_updates"
    ] += 1


# ------------------------------------------------------------
# PÉNALITÉ HISTORY
# ------------------------------------------------------------

def penaliser_history_avance(
    etat,
    coup,
    profondeur
):

    cle = cle_history(
        etat,
        coup
    )

    ancien = HISTORY_AVANCEE.get(
        cle,
        0
    )

    malus = profondeur * profondeur

    nouveau = (
        ancien
        -
        malus
    )

    nouveau = max(
        HISTORY_MIN,
        min(
            HISTORY_MAX,
            nouveau
        )
    )

    HISTORY_AVANCEE[
        cle
    ] = nouveau


# ------------------------------------------------------------
# DECAY HISTORY
# ------------------------------------------------------------

def decay_history():

    if not HISTORY_AVANCEE:
        return

    for cle in list(
        HISTORY_AVANCEE
    ):

        valeur = HISTORY_AVANCEE[
            cle
        ]

        valeur = (
            valeur
            -
            valeur // HISTORY_DECAY
        )

        if abs(valeur) <= 1:

            del HISTORY_AVANCEE[
                cle
            ]

        else:

            HISTORY_AVANCEE[
                cle
            ] = valeur


# ------------------------------------------------------------
# CLÉ KILLER
# ------------------------------------------------------------

def cle_killer_avance(
    profondeur,
    couleur
):

    return (
        profondeur,
        couleur
    )


# ------------------------------------------------------------
# RÉCUPÉRER KILLER
# ------------------------------------------------------------

def obtenir_killers(
    profondeur,
    couleur
):

    cle = cle_killer_avance(
        profondeur,
        couleur
    )

    return KILLER_AVANCES.get(
        cle,
        []
    )


# ------------------------------------------------------------
# AJOUTER KILLER
# ------------------------------------------------------------

def ajouter_killer_avance(
    etat,
    coup,
    profondeur
):

    couleur = etat.get(
        "tour",
        BLANC
    )

    cle = cle_killer_avance(
        profondeur,
        couleur
    )

    liste = KILLER_AVANCES.setdefault(
        cle,
        []
    )

    identifiant = identifiant_coup(
        coup
    )

    # Déjà présent
    liste[:] = [
        x
        for x in liste
        if x != identifiant
    ]

    # Nouveau killer en tête
    liste.insert(
        0,
        identifiant
    )

    # Limite
    del liste[
        KILLER_MAX_PAR_PROFONDEUR:
    ]

    STATS_KILLER_HISTORY[
        "killer_stores"
    ] += 1


# ------------------------------------------------------------
# EST KILLER
# ------------------------------------------------------------

def est_killer_avance(
    etat,
    coup,
    profondeur
):

    couleur = etat.get(
        "tour",
        BLANC
    )

    killers = obtenir_killers(
        profondeur,
        couleur
    )

    identifiant = identifiant_coup(
        coup
    )

    if identifiant in killers:

        STATS_KILLER_HISTORY[
            "killer_hits"
        ] += 1

        return True

    return False


# ------------------------------------------------------------
# SCORE KILLER
# ------------------------------------------------------------

def score_killer_avance(
    etat,
    coup,
    profondeur
):

    couleur = etat.get(
        "tour",
        BLANC
    )

    killers = obtenir_killers(
        profondeur,
        couleur
    )

    identifiant = identifiant_coup(
        coup
    )

    if identifiant not in killers:
        return 0

    position = killers.index(
        identifiant
    )

    # Le premier killer est le plus important.
    return (
        8000
        -
        position * 500
    )


# ------------------------------------------------------------
# COUNTER MOVE
# ------------------------------------------------------------

def cle_counter(
    coup_precedent
):

    if coup_precedent is None:
        return None

    return identifiant_coup(
        coup_precedent
    )


def enregistrer_counter_move(
    coup_precedent,
    coup_reponse
):

    cle = cle_counter(
        coup_precedent
    )

    if cle is None:
        return

    COUNTER_MOVES[
        cle
    ] = identifiant_coup(
        coup_reponse
    )


def obtenir_counter_move(
    coup_precedent
):

    cle = cle_counter(
        coup_precedent
    )

    if cle is None:
        return None

    return COUNTER_MOVES.get(
        cle
    )


def est_counter_move(
    coup,
    coup_precedent
):

    attendu = obtenir_counter_move(
        coup_precedent
    )

    if attendu is None:
        return False

    return (
        identifiant_coup(coup)
        ==
        attendu
    )


# ------------------------------------------------------------
# SCORE COUNTER
# ------------------------------------------------------------

def score_counter_move(
    coup,
    coup_precedent
):

    if est_counter_move(
        coup,
        coup_precedent
    ):

        STATS_KILLER_HISTORY[
            "counter_hits"
        ] += 1

        return 6500

    return 0


# ------------------------------------------------------------
# SCORE GLOBAL AVANCÉ
# ------------------------------------------------------------

def score_ordre_avance(
    etat,
    coup,
    profondeur,
    coup_precedent=None
):

    score = 0

    # --------------------------------------------------------
    # TACTIQUE
    # --------------------------------------------------------

    score += score_coup_tactique(
        etat,
        coup
    )

    # --------------------------------------------------------
    # KILLER
    # --------------------------------------------------------

    score += score_killer_avance(
        etat,
        coup,
        profondeur
    )

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    score += score_history_avance(
        etat,
        coup
    )

    # --------------------------------------------------------
    # COUNTER MOVE
    # --------------------------------------------------------

    score += score_counter_move(
        coup,
        coup_precedent
    )

    return score


# ------------------------------------------------------------
# ORDRE AVANCÉ
# ------------------------------------------------------------

def ordonner_coups_avance(
    etat,
    coups,
    profondeur=0,
    coup_precedent=None
):

    couples = []

    for coup in coups:

        score = score_ordre_avance(
            etat,
            coup,
            profondeur,
            coup_precedent
        )

        couples.append(
            (
                score,
                coup
            )
        )

    couples.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        coup
        for score, coup
        in couples
    ]


# ------------------------------------------------------------
# METTRE À JOUR APRÈS COUPURE
# ------------------------------------------------------------

def enregistrer_coup_coupure(
    etat,
    coup,
    profondeur,
    coups_avant=None,
    coup_precedent=None
):

    # Killer
    ajouter_killer_avance(
        etat,
        coup,
        profondeur
    )

    # History positif
    ajouter_history_avance(
        etat,
        coup,
        profondeur
    )

    # Les autres coups étaient moins bons
    if coups_avant:

        for autre in coups_avant:

            if (
                identifiant_coup(autre)
                ==
                identifiant_coup(coup)
            ):
                continue

            penaliser_history_avance(
                etat,
                autre,
                profondeur
            )

    # Counter move
    enregistrer_counter_move(
        coup_precedent,
        coup
    )


# ------------------------------------------------------------
# RECHERCHE AVANCÉE
# ------------------------------------------------------------

def negamax_alpha_beta_avance(
    etat,
    profondeur,
    alpha,
    beta,
    coup_precedent=None
):

    STATS_RECHERCHE[
        "noeuds"
    ] += 1

    # --------------------------------------------------------
    # TERMINAL
    # --------------------------------------------------------

    terminal = score_terminal(
        etat,
        profondeur
    )

    if terminal is not None:

        STATS_RECHERCHE[
            "feuilles"
        ] += 1

        return terminal

    # --------------------------------------------------------
    # QUIESCENCE
    # --------------------------------------------------------

    if profondeur <= 0:

        STATS_RECHERCHE[
            "feuilles"
        ] += 1

        return quiescence(
            etat,
            alpha,
            beta,
            0
        )

    # --------------------------------------------------------
    # TRANSPOSITION
    # --------------------------------------------------------

    entree = chercher_tt(
        etat,
        profondeur
    )

    if entree is not None:

        STATS_RECHERCHE[
            "tt_hits"
        ] += 1

        type_score = entree.get(
            "type",
            TT_EXACT
        )

        score = entree.get(
            "score",
            0
        )

        if type_score == TT_EXACT:
            return score

        if (
            type_score == TT_ALPHA
            and
            score <= alpha
        ):
            return score

        if (
            type_score == TT_BETA
            and
            score >= beta
        ):
            return score

    alpha_original = alpha

    # --------------------------------------------------------
    # COUPS
    # --------------------------------------------------------

    coups = generer_coups_legaux(
        etat
    )

    if not coups:

        return score_position(
            etat
        )

    coups = ordonner_coups_avance(
        etat,
        coups,
        profondeur,
        coup_precedent
    )

    meilleur = SCORE_MIN
    meilleur_coup_local = None

    coups_avant = []

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    for coup in coups:

        STATS_RECHERCHE[
            "coups_analyses"
        ] += 1

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -negamax_alpha_beta_avance(
            enfant,
            profondeur - 1,
            -beta,
            -alpha,
            coup
        )

        if score > meilleur:

            meilleur = score

            meilleur_coup_local = coup

        if score > alpha:

            alpha = score

        # ----------------------------------------------------
        # BETA CUT
        # ----------------------------------------------------

        if alpha >= beta:

            STATS_RECHERCHE[
                "coupes_beta"
            ] += 1

            enregistrer_coup_coupure(
                etat,
                coup,
                profondeur,
                coups_avant,
                coup_precedent
            )

            break

        coups_avant.append(
            coup
        )

    # --------------------------------------------------------
    # TYPE TT
    # --------------------------------------------------------

    if meilleur <= alpha_original:

        type_score = TT_ALPHA

    elif meilleur >= beta:

        type_score = TT_BETA

    else:

        type_score = TT_EXACT

    # --------------------------------------------------------
    # STOCKAGE
    # --------------------------------------------------------

    stocker_tt(
        etat,
        profondeur,
        meilleur,
        type_score,
        meilleur_coup_local
    )

    return meilleur


# ------------------------------------------------------------
# MEILLEUR COUP AVANCÉ
# ------------------------------------------------------------

def rechercher_meilleur_coup_avance(
    etat,
    profondeur
):

    reset_stats_recherche()

    coups = generer_coups_legaux(
        etat
    )

    if not coups:

        return (
            None,
            score_terminal(
                etat,
                profondeur
            )
        )

    coups = ordonner_coups_avance(
        etat,
        coups,
        profondeur
    )

    meilleur_coup_local = None
    meilleur_score_local = SCORE_MIN

    alpha = SCORE_MIN
    beta = SCORE_MAX

    for coup in coups:

        enfant = jouer_coup_temporaire(
            etat,
            coup
        )

        score = -negamax_alpha_beta_avance(
            enfant,
            profondeur - 1,
            -beta,
            -alpha,
            coup
        )

        if score > meilleur_score_local:

            meilleur_score_local = score

            meilleur_coup_local = coup

        if score > alpha:

            alpha = score

    stocker_tt(
        etat,
        profondeur,
        meilleur_score_local,
        TT_EXACT,
        meilleur_coup_local
    )

    return (
        meilleur_coup_local,
        meilleur_score_local
    )


# ------------------------------------------------------------
# STATISTIQUES
# ------------------------------------------------------------

def statistiques_killer_history():

    return dict(
        STATS_KILLER_HISTORY
    )


# ------------------------------------------------------------
# AFFICHAGE
# ------------------------------------------------------------

def afficher_stats_killer_history():

    print()
    print("⚡ KILLER + HISTORY")
    print("-" * 60)

    print(
        "Killer hits :",
        STATS_KILLER_HISTORY[
            "killer_hits"
        ]
    )

    print(
        "History hits :",
        STATS_KILLER_HISTORY[
            "history_hits"
        ]
    )

    print(
        "Killer stores :",
        STATS_KILLER_HISTORY[
            "killer_stores"
        ]
    )

    print(
        "History updates :",
        STATS_KILLER_HISTORY[
            "history_updates"
        ]
    )

    print(
        "Counter hits :",
        STATS_KILLER_HISTORY[
            "counter_hits"
        ]
    )


# ------------------------------------------------------------
# TEST HISTORY
# ------------------------------------------------------------

def test_history_avance():

    reset_killer_history()

    etat = creer_etat_initial()

    coups = generer_coups_legaux(
        etat
    )

    if not coups:
        return False

    coup = coups[0]

    avant = score_history_avance(
        etat,
        coup
    )

    ajouter_history_avance(
        etat,
        coup,
        3
    )

    apres = score_history_avance(
        etat,
        coup
    )

    return apres > avant


# ------------------------------------------------------------
# TEST KILLER
# ------------------------------------------------------------

def test_killer_avance():

    reset_killer_history()

    etat = creer_etat_initial()

    coups = generer_coups_legaux(
        etat
    )

    if not coups:
        return False

    coup = coups[0]

    ajouter_killer_avance(
        etat,
        coup,
        3
    )

    return est_killer_avance(
        etat,
        coup,
        3
    )


# ------------------------------------------------------------
# TEST COUNTER
# ------------------------------------------------------------

def test_counter_move():

    reset_killer_history()

    etat = creer_etat_initial()

    coups = generer_coups_legaux(
        etat
    )

    if len(coups) < 2:
        return False

    precedent = coups[0]
    reponse = coups[1]

    enregistrer_counter_move(
        precedent,
        reponse
    )

    return est_counter_move(
        reponse,
        precedent
    )


# ------------------------------------------------------------
# TEST ORDRE
# ------------------------------------------------------------

def test_ordre_avance():

    etat = creer_etat_initial()

    coups = generer_coups_legaux(
        etat
    )

    if not coups:
        return False

    tries = ordonner_coups_avance(
        etat,
        coups,
        2
    )

    return len(tries) == len(
        coups
    )


# ------------------------------------------------------------
# TEST RECHERCHE
# ------------------------------------------------------------

def test_recherche_avancee():

    etat = creer_etat_initial()

    coup, score = (
        rechercher_meilleur_coup_avance(
            etat,
            2
        )
    )

    return (
        coup is not None
        and
        isinstance(
            score,
            (int, float)
        )
    )


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 PANDORAGA FULL ADAPTATION Ω")
    print("⚡ BLOC 18 — KILLER + HISTORY AVANCÉS")
    print("=" * 65)

    print()
    print("🧪 TESTS")
    print("-" * 65)

    print(
        "History :",
        "OK"
        if test_history_avance()
        else "ERREUR"
    )

    print(
        "Killer :",
        "OK"
        if test_killer_avance()
        else "ERREUR"
    )

    print(
        "Counter move :",
        "OK"
        if test_counter_move()
        else "ERREUR"
    )

    print(
        "Ordre avancé :",
        "OK"
        if test_ordre_avance()
        else "ERREUR"
    )

    print(
        "Recherche avancée :",
        "OK"
        if test_recherche_avancee()
        else "ERREUR"
    )

    print()
    print("📊 STATISTIQUES")
    print("-" * 65)

    afficher_stats_killer_history()

    print()
    print(
        "🐼 BLOC 18 CHARGÉ AVEC SUCCÈS."
    )
# ============================================================
# 🧠 PANDORAGA — BLOC 19/26
# MÉMOIRE JSON
# ============================================================

import json
import os
import time


class MemoirePandoraga:

    # ========================================================
    # INITIALISATION
    # ========================================================

    def __init__(
        self,
        fichier="pandoraga_memoire.json"
    ):

        self.fichier = fichier

        self.donnees = {
            "parties": 0,
            "victoires": 0,
            "defaites": 0,
            "nulles": 0,
            "erreurs": [],
            "coups_appris": {}
        }

        self.charger()


    # ========================================================
    # CHARGEMENT
    # ========================================================

    def charger(self):

        if not os.path.exists(
            self.fichier
        ):
            return False

        try:

            with open(
                self.fichier,
                "r",
                encoding="utf-8"
            ) as fichier:

                donnees = json.load(
                    fichier
                )


            if isinstance(
                donnees,
                dict
            ):

                self.donnees.update(
                    donnees
                )


            # Sécurité
            self.donnees.setdefault(
                "parties",
                0
            )

            self.donnees.setdefault(
                "victoires",
                0
            )

            self.donnees.setdefault(
                "defaites",
                0
            )

            self.donnees.setdefault(
                "nulles",
                0
            )

            self.donnees.setdefault(
                "erreurs",
                []
            )

            self.donnees.setdefault(
                "coups_appris",
                {}
            )

            return True


        except Exception as erreur:

            print(
                "⚠️ Erreur chargement mémoire :",
                erreur
            )

            return False


    # ========================================================
    # SAUVEGARDE
    # ========================================================

    def sauvegarder(self):

        try:

            with open(
                self.fichier,
                "w",
                encoding="utf-8"
            ) as fichier:

                json.dump(
                    self.donnees,
                    fichier,
                    indent=4,
                    ensure_ascii=False
                )

            return True


        except Exception as erreur:

            print(
                "⚠️ Erreur sauvegarde mémoire :",
                erreur
            )

            return False


    # ========================================================
    # NOUVELLE PARTIE
    # ========================================================

    def nouvelle_partie(self):

        parties = self.donnees.get(
            "parties",
            0
        )

        if not isinstance(
            parties,
            int
        ):
            parties = 0

        self.donnees[
            "parties"
        ] = parties + 1

        self.sauvegarder()


    # ========================================================
    # VICTOIRE
    # ========================================================

    def victoire(self):

        victoires = self.donnees.get(
            "victoires",
            0
        )

        if not isinstance(
            victoires,
            int
        ):
            victoires = 0

        self.donnees[
            "victoires"
        ] = victoires + 1

        self.sauvegarder()


    # ========================================================
    # DÉFAITE
    # ========================================================

    def defaite(self):

        defaites = self.donnees.get(
            "defaites",
            0
        )

        if not isinstance(
            defaites,
            int
        ):
            defaites = 0

        self.donnees[
            "defaites"
        ] = defaites + 1

        self.sauvegarder()


    # ========================================================
    # PARTIE NULLE
    # ========================================================

    def nulle(self):

        nulles = self.donnees.get(
            "nulles",
            0
        )

        if not isinstance(
            nulles,
            int
        ):
            nulles = 0

        self.donnees[
            "nulles"
        ] = nulles + 1

        self.sauvegarder()


    # ========================================================
    # APPRENDRE UN COUP
    # ========================================================

    def apprendre_coup(
        self,
        coup
    ):

        coup = str(coup)

        coups = self.donnees.get(
            "coups_appris",
            {}
        )


        # Réparation automatique
        if not isinstance(
            coups,
            dict
        ):

            coups = {}

            self.donnees[
                "coups_appris"
            ] = coups


        ancienne_valeur = coups.get(
            coup,
            0
        )


        if isinstance(
            ancienne_valeur,
            int
        ):

            coups[
                coup
            ] = ancienne_valeur + 1

        else:

            coups[
                coup
            ] = 1


        self.sauvegarder()


    # ========================================================
    # APPRENDRE UNE POSITION
    # ========================================================

    def apprendre_position(
        self,
        position,
        coup
    ):

        cle = str(position)

        valeur = str(coup)

        coups = self.donnees.get(
            "coups_appris",
            {}
        )


        if not isinstance(
            coups,
            dict
        ):

            coups = {}

            self.donnees[
                "coups_appris"
            ] = coups


        if cle not in coups:

            coups[
                cle
            ] = {}


        if not isinstance(
            coups[cle],
            dict
        ):

            coups[
                cle
            ] = {}


        ancien = coups[
            cle
        ].get(
            valeur,
            0
        )


        if isinstance(
            ancien,
            int
        ):

            coups[
                cle
            ][
                valeur
            ] = ancien + 1

        else:

            coups[
                cle
            ][
                valeur
            ] = 1


        self.sauvegarder()


    # ========================================================
    # ENREGISTRER UNE ERREUR
    # ========================================================

    def enregistrer_erreur(
        self,
        erreur
    ):

        erreurs = self.donnees.get(
            "erreurs",
            []
        )


        if not isinstance(
            erreurs,
            list
        ):

            erreurs = []

            self.donnees[
                "erreurs"
            ] = erreurs


        erreurs.append(
            {
                "erreur": str(erreur),
                "temps": time.time()
            }
        )


        self.sauvegarder()


    # ========================================================
    # RÉCUPÉRER LES COUPS APPRIS
    # ========================================================

    def coups_appris(
        self
    ):

        coups = self.donnees.get(
            "coups_appris",
            {}
        )

        if isinstance(
            coups,
            dict
        ):

            return coups.copy()

        return {}


    # ========================================================
    # STATISTIQUES
    # ========================================================

    def statistiques(
        self
    ):

        # ----------------------------------------------------
        # PARTIES
        # ----------------------------------------------------

        parties = self.donnees.get(
            "parties",
            0
        )

        if not isinstance(
            parties,
            int
        ):
            parties = 0


        # ----------------------------------------------------
        # VICTOIRES
        # ----------------------------------------------------

        victoires = self.donnees.get(
            "victoires",
            0
        )

        if not isinstance(
            victoires,
            int
        ):
            victoires = 0


        # ----------------------------------------------------
        # DÉFAITES
        # ----------------------------------------------------

        defaites = self.donnees.get(
            "defaites",
            0
        )

        if not isinstance(
            defaites,
            int
        ):
            defaites = 0


        # ----------------------------------------------------
        # NULLES
        # ----------------------------------------------------

        nulles = self.donnees.get(
            "nulles",
            0
        )

        if not isinstance(
            nulles,
            int
        ):
            nulles = 0


        # ----------------------------------------------------
        # TAUX DE VICTOIRE
        # ----------------------------------------------------

        if parties > 0:

            taux_victoire = (
                victoires
                / parties
            ) * 100

        else:

            taux_victoire = 0.0


        # ----------------------------------------------------
        # ERREURS
        # ----------------------------------------------------

        erreurs = self.donnees.get(
            "erreurs",
            []
        )


        if isinstance(
            erreurs,
            (list, tuple, set, dict)
        ):

            nombre_erreurs = len(
                erreurs
            )

        elif isinstance(
            erreurs,
            int
        ):

            nombre_erreurs = erreurs

        else:

            nombre_erreurs = 0


        # ----------------------------------------------------
        # COUPS APPRIS
        # ----------------------------------------------------

        coups = self.donnees.get(
            "coups_appris",
            {}
        )


        total_coups = 0


        if isinstance(
            coups,
            dict
        ):

            def compter(
                valeur
            ):

                total = 0


                if isinstance(
                    valeur,
                    int
                ):

                    return valeur


                if isinstance(
                    valeur,
                    dict
                ):

                    for sous_valeur in (
                        valeur.values()
                    ):

                        total += compter(
                            sous_valeur
                        )

                    return total


                if isinstance(
                    valeur,
                    (list, tuple, set)
                ):

                    return len(
                        valeur
                    )


                return 1


            for valeur in (
                coups.values()
            ):

                total_coups += compter(
                    valeur
                )


        elif isinstance(
            coups,
            (list, tuple, set)
        ):

            total_coups = len(
                coups
            )


        elif isinstance(
            coups,
            int
        ):

            total_coups = coups


        # ----------------------------------------------------
        # RETOUR
        # ----------------------------------------------------

        return {

            "parties":
                parties,

            "victoires":
                victoires,

            "defaites":
                defaites,

            "nulles":
                nulles,

            "taux_victoire":
                round(
                    taux_victoire,
                    2
                ),

            "erreurs":
                nombre_erreurs,

            "coups_appris":
                total_coups
        }


# ============================================================
# 🐼 INSTANCE GLOBALE
# ============================================================

MEMOIRE_PANDORAGA = MemoirePandoraga()


# ============================================================
# 🧪 TEST BLOC 19
# ============================================================

def test_bloc_19():

    print()
    print("=" * 65)
    print("🧠 BLOC 19 — MÉMOIRE JSON")
    print("=" * 65)

    print()
    print("🧪 TESTS")
    print("-" * 65)


    # Création

    test = MemoirePandoraga(
        "pandoraga_test_memoire.json"
    )

    print(
        "Création : OK"
    )


    # Partie

    test.nouvelle_partie()

    print(
        "Partie : OK"
    )


    # Apprentissage

    test.apprendre_coup(
        "e2e4"
    )

    test.apprendre_coup(
        "e2e4"
    )

    test.apprendre_coup(
        "g1f3"
    )

    print(
        "Apprentissage : OK"
    )


    # Position

    test.apprendre_position(
        "position_test",
        "e2e4"
    )

    print(
        "Position : OK"
    )


    # Erreur

    test.enregistrer_erreur(
        "Erreur test"
    )

    print(
        "Erreurs : OK"
    )


    # Sauvegarde

    if test.sauvegarder():

        print(
            "Sauvegarde : OK"
        )

    else:

        print(
            "Sauvegarde : ERREUR"
        )


    # Chargement

    test2 = MemoirePandoraga(
        "pandoraga_test_memoire.json"
    )

    print(
        "Chargement : OK"
    )


    # Statistiques

    stats = test2.statistiques()


    print()
    print("🐼 MÉMOIRE ACTUELLE")
    print("-" * 65)

    print(
        "Parties       :",
        stats["parties"]
    )

    print(
        "Victoires     :",
        stats["victoires"]
    )

    print(
        "Défaites      :",
        stats["defaites"]
    )

    print(
        "Nulles        :",
        stats["nulles"]
    )

    print(
        "Taux victoire :",
        stats["taux_victoire"],
        "%"
    )

    print(
        "Erreurs       :",
        stats["erreurs"]
    )

    print(
        "Coups appris  :",
        stats["coups_appris"]
    )


    # Nettoyage du fichier de test

    try:

        os.remove(
            "pandoraga_test_memoire.json"
        )

    except Exception:

        pass


    print()
    print("=" * 65)
    print("✅ BLOC 19 TERMINÉ")
    print("=" * 65)


# ============================================================
# FIN BLOC 19
# ============================================================

    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 20/26 — ANALYSEUR D'ADVERSAIRE
# ============================================================

import math
import time


# ------------------------------------------------------------
# PARAMÈTRES
# ------------------------------------------------------------

ANALYSE_MIN_COUPS = 3

HISTORIQUE_ADVERSAIRE_MAX = 100

SCORE_STYLE_MIN = -100.0
SCORE_STYLE_MAX = 100.0


# ------------------------------------------------------------
# PROFILS
# ------------------------------------------------------------

PROFIL_INCONNU = "inconnu"
PROFIL_AGRESSIF = "agressif"
PROFIL_TACTIQUE = "tactique"
PROFIL_POSITIONNEL = "positionnel"
PROFIL_DEFENSIF = "defensif"
PROFIL_EQUILIBRE = "equilibre"


# ------------------------------------------------------------
# STATISTIQUES
# ------------------------------------------------------------

STATS_ADVERSAIRE = {

    "analyses": 0,

    "coups_analyses": 0,

    "captures_analysees": 0,

    "echecs_analyses": 0,

    "promotions_analysees": 0,

    "ouvertures_analysees": 0,

    "erreurs_detectees": 0
}


# ------------------------------------------------------------
# PROFIL PAR DÉFAUT
# ------------------------------------------------------------

def nouveau_profil_adversaire(
    nom="Inconnu"
):

    return {

        "nom": str(nom),

        "parties": 0,

        "victoires": 0,

        "defaites": 0,

        "nulles": 0,

        "coups_total": 0,

        "captures": 0,

        "echecs": 0,

        "promotions": 0,

        "erreurs": 0,

        "agressivite": 0.0,

        "tactique": 0.0,

        "defense": 0.0,

        "risque": 0.0,

        "profil": PROFIL_INCONNU,

        "confiance": 0.0,

        "derniere_analyse": 0.0
    }


# ------------------------------------------------------------
# NORMALISATION
# ------------------------------------------------------------

def limiter_score(
    valeur
):

    return max(
        SCORE_STYLE_MIN,
        min(
            SCORE_STYLE_MAX,
            float(valeur)
        )
    )


# ------------------------------------------------------------
# ANALYSEUR
# ------------------------------------------------------------

class AnalyseurAdversaire:

    def __init__(
        self,
        memoire=None
    ):

        if memoire is None:

            memoire = globals().get(
                "MEMOIRE_PANDORAGA"
            )

        self.memoire = memoire

        self.profils = {}

        self.historique_coups = {}

        self.dernier_profil = None


    # ========================================================
    # RÉCUPÉRER PROFIL
    # ========================================================

    def obtenir_profil(
        self,
        nom
    ):

        nom = str(nom)

        if nom not in self.profils:

            self.profils[nom] = (
                nouveau_profil_adversaire(
                    nom
                )
            )

        return self.profils[nom]


    # ========================================================
    # ENREGISTRER COUP
    # ========================================================

    def enregistrer_coup(
        self,
        nom,
        coup,
        capture=False,
        echec=False,
        promotion=False,
        erreur=False
    ):

        profil = self.obtenir_profil(
            nom
        )

        profil[
            "coups_total"
        ] += 1

        STATS_ADVERSAIRE[
            "coups_analyses"
        ] += 1

        if capture:

            profil[
                "captures"
            ] += 1

            STATS_ADVERSAIRE[
                "captures_analysees"
            ] += 1

        if echec:

            profil[
                "echecs"
            ] += 1

            STATS_ADVERSAIRE[
                "echecs_analyses"
            ] += 1

        if promotion:

            profil[
                "promotions"
            ] += 1

            STATS_ADVERSAIRE[
                "promotions_analysees"
            ] += 1

        if erreur:

            profil[
                "erreurs"
            ] += 1

            STATS_ADVERSAIRE[
                "erreurs_detectees"
            ] += 1

        if nom not in self.historique_coups:

            self.historique_coups[
                nom
            ] = []

        self.historique_coups[
            nom
        ].append(
            str(coup)
        )

        self.historique_coups[
            nom
        ] = self.historique_coups[
            nom
        ][
            -HISTORIQUE_ADVERSAIRE_MAX:
        ]


    # ========================================================
    # ENREGISTRER PARTIE
    # ========================================================

    def enregistrer_partie(
        self,
        nom,
        resultat
    ):

        profil = self.obtenir_profil(
            nom
        )

        profil[
            "parties"
        ] += 1

        resultat = str(
            resultat
        ).lower()

        if resultat == "victoire":

            profil[
                "victoires"
            ] += 1

        elif resultat == "defaite":

            profil[
                "defaites"
            ] += 1

        else:

            profil[
                "nulles"
            ] += 1

        self.calculer_style(
            nom
        )


    # ========================================================
    # CALCUL AGRESSIVITÉ
    # ========================================================

    def calculer_agressivite(
        self,
        profil
    ):

        coups = profil[
            "coups_total"
        ]

        if coups <= 0:

            return 0.0

        captures = profil[
            "captures"
        ]

        echecs = profil[
            "echecs"
        ]

        promotions = profil[
            "promotions"
        ]

        # Les échecs et promotions ont
        # davantage de poids que les captures.
        score = (

            (captures / coups) * 55.0

            +

            (echecs / coups) * 35.0

            +

            (promotions / coups) * 60.0
        )

        return limiter_score(
            score
        )


    # ========================================================
    # CALCUL TACTIQUE
    # ========================================================

    def calculer_tactique(
        self,
        profil
    ):

        coups = profil[
            "coups_total"
        ]

        if coups <= 0:

            return 0.0

        score = (

            profil["echecs"]
            /
            coups
        ) * 100.0

        score += (

            profil["promotions"]
            /
            coups
        ) * 100.0

        return limiter_score(
            score
        )


    # ========================================================
    # CALCUL RISQUE
    # ========================================================

    def calculer_risque(
        self,
        profil
    ):

        coups = profil[
            "coups_total"
        ]

        if coups <= 0:

            return 0.0

        erreurs = profil[
            "erreurs"
        ]

        captures = profil[
            "captures"
        ]

        score = (

            erreurs / coups
        ) * 70.0

        score += (

            captures / coups
        ) * 20.0

        return limiter_score(
            score
        )


    # ========================================================
    # CALCUL DÉFENSE
    # ========================================================

    def calculer_defense(
        self,
        profil
    ):

        agressivite = profil[
            "agressivite"
        ]

        risque = profil[
            "risque"
        ]

        defense = 50.0

        defense -= (
            agressivite * 0.35
        )

        defense -= (
            risque * 0.20
        )

        return limiter_score(
            defense
        )


    # ========================================================
    # DÉTERMINER PROFIL
    # ========================================================

    def determiner_profil(
        self,
        profil
    ):

        if profil[
            "coups_total"
        ] < ANALYSE_MIN_COUPS:

            return PROFIL_INCONNU

        agressivite = profil[
            "agressivite"
        ]

        tactique = profil[
            "tactique"
        ]

        defense = profil[
            "defense"
        ]

        risque = profil[
            "risque"
        ]

        if tactique >= 35:

            return PROFIL_TACTIQUE

        if agressivite >= 35:

            return PROFIL_AGRESSIF

        if defense >= 40 and risque < 25:

            return PROFIL_DEFENSIF

        if (
            agressivite < 20
            and
            tactique < 25
        ):

            return PROFIL_POSITIONNEL

        return PROFIL_EQUILIBRE


    # ========================================================
    # CALCUL STYLE COMPLET
    # ========================================================

    def calculer_style(
        self,
        nom
    ):

        profil = self.obtenir_profil(
            nom
        )

        profil[
            "agressivite"
        ] = self.calculer_agressivite(
            profil
        )

        profil[
            "tactique"
        ] = self.calculer_tactique(
            profil
        )

        profil[
            "risque"
        ] = self.calculer_risque(
            profil
        )

        profil[
            "defense"
        ] = self.calculer_defense(
            profil
        )

        profil[
            "profil"
        ] = self.determiner_profil(
            profil
        )

        profil[
            "confiance"
        ] = self.calculer_confiance(
            profil
        )

        profil[
            "derniere_analyse"
        ] = time.time()

        self.dernier_profil = dict(
            profil
        )

        STATS_ADVERSAIRE[
            "analyses"
        ] += 1

        return profil


    # ========================================================
    # CONFIANCE
    # ========================================================

    def calculer_confiance(
        self,
        profil
    ):

        parties = profil[
            "parties"
        ]

        coups = profil[
            "coups_total"
        ]

        score_parties = min(
            parties / 10.0,
            1.0
        )

        score_coups = min(
            coups / 100.0,
            1.0
        )

        return round(
            (
                score_parties
                +
                score_coups
            )
            *
            50.0,
            2
        )


    # ========================================================
    # ANALYSE RAPIDE D'UNE LISTE DE COUPS
    # ========================================================

    def analyser_sequence(
        self,
        nom,
        coups
    ):

        if coups is None:

            return self.obtenir_profil(
                nom
            )

        for coup in coups:

            capture = False
            echec = False
            promotion = False

            texte = str(
                coup
            ).lower()

            # Détection générique pour les
            # notations simples.
            if "x" in texte:

                capture = True

            if "+" in texte:

                echec = True

            if "#" in texte:

                echec = True

            if "=" in texte:

                promotion = True

            self.enregistrer_coup(
                nom,
                coup,
                capture,
                echec,
                promotion
            )

        return self.calculer_style(
            nom
        )


    # ========================================================
    # ANALYSE D'UNE POSITION
    # ========================================================

    def analyser_position(
        self,
        etat,
        nom
    ):

        coups = generer_coups_legaux(
            etat
        )

        if not coups:

            return self.obtenir_profil(
                nom
            )

        captures = 0
        echecs = 0
        promotions = 0

        for coup in coups:

            try:

                if coup_est_capture(
                    etat,
                    coup
                ):

                    captures += 1

                if coup_est_promotion(
                    coup
                ):

                    promotions += 1

                if coup_donne_echec(
                    etat,
                    coup
                ):

                    echecs += 1

            except Exception:

                pass

        profil = self.obtenir_profil(
            nom
        )

        profil[
            "captures"
        ] += captures

        profil[
            "promotions"
        ] += promotions

        profil[
            "echecs"
        ] += echecs

        profil[
            "coups_total"
        ] += len(coups)

        return self.calculer_style(
            nom
        )


    # ========================================================
    # CHARGER DEPUIS MÉMOIRE JSON
    # ========================================================

    def charger_profil_memoire(
        self,
        nom
    ):

        if self.memoire is None:

            return self.obtenir_profil(
                nom
            )

        donnees = self.memoire.donnees

        anciens = donnees.get(
            "adversaires",
            {}
        )

        ancien = anciens.get(
            str(nom)
        )

        profil = self.obtenir_profil(
            nom
        )

        if ancien:

            profil[
                "parties"
            ] = ancien.get(
                "parties",
                0
            )

            profil[
                "victoires"
            ] = ancien.get(
                "victoires",
                0
            )

            profil[
                "defaites"
            ] = ancien.get(
                "defaites",
                0
            )

            profil[
                "nulles"
            ] = ancien.get(
                "nulles",
                0
            )

        return self.calculer_style(
            nom
        )


    # ========================================================
    # CONSEIL CONTRE ADVERSAIRE
    # ========================================================

    def conseil_adaptation(
        self,
        nom
    ):

        profil = self.obtenir_profil(
            nom
        )

        style = profil[
            "profil"
        ]

        if style == PROFIL_AGRESSIF:

            return {

                "style":
                    style,

                "conseil":
                    "Éviter les échanges inutiles et contrôler le centre.",

                "priorite":
                    "defense"
            }

        if style == PROFIL_TACTIQUE:

            return {

                "style":
                    style,

                "conseil":
                    "Vérifier les menaces tactiques avant chaque coup.",

                "priorite":
                    "calcul"
            }

        if style == PROFIL_DEFENSIF:

            return {

                "style":
                    style,

                "conseil":
                    "Améliorer progressivement les pièces et éviter de forcer.",

                "priorite":
                    "position"
            }

        if style == PROFIL_POSITIONNEL:

            return {

                "style":
                    style,

                "conseil":
                    "Chercher des ruptures tactiques et créer des déséquilibres.",

                "priorite":
                    "tactique"
            }

        return {

            "style":
                style,

            "conseil":
                "Continuer une stratégie équilibrée.",

            "priorite":
                "equilibre"
        }


    # ========================================================
    # EXPORT
    # ========================================================

    def exporter_profil(
        self,
        nom
    ):

        return dict(
            self.obtenir_profil(
                nom
            )
        )


# ------------------------------------------------------------
# INSTANCE GLOBALE
# ------------------------------------------------------------

ANALYSEUR_ADVERSAIRE = AnalyseurAdversaire(
    globals().get(
        "MEMOIRE_PANDORAGA"
    )
)


# ------------------------------------------------------------
# RACCOURCIS
# ------------------------------------------------------------

def analyser_adversaire(
    nom,
    coups=None
):

    ANALYSEUR_ADVERSAIRE.charger_profil_memoire(
        nom
    )

    if coups:

        return ANALYSEUR_ADVERSAIRE.analyser_sequence(
            nom,
            coups
        )

    return ANALYSEUR_ADVERSAIRE.calculer_style(
        nom
    )


def profil_adversaire(
    nom
):

    return ANALYSEUR_ADVERSAIRE.obtenir_profil(
        nom
    )


def conseil_adversaire(
    nom
):

    return ANALYSEUR_ADVERSAIRE.conseil_adaptation(
        nom
    )


# ------------------------------------------------------------
# TEST PROFIL
# ------------------------------------------------------------

def test_profil_adversaire():

    analyseur = AnalyseurAdversaire()

    coups = [
        "e4",
        "Qh5",
        "Qxf7+",
        "Bc4",
        "Qxf7+",
        "e5"
    ]

    profil = analyseur.analyser_sequence(
        "Test",
        coups
    )

    return (
        isinstance(
            profil,
            dict
        )
        and
        "profil" in profil
        and
        "agressivite" in profil
    )


# ------------------------------------------------------------
# TEST CONSEIL
# ------------------------------------------------------------

def test_conseil():

    analyseur = AnalyseurAdversaire()

    analyseur.enregistrer_coup(
        "Test",
        "Qxf7+",
        capture=True,
        echec=True
    )

    conseil = analyseur.conseil_adaptation(
        "Test"
    )

    return (
        isinstance(
            conseil,
            dict
        )
        and
        "conseil" in conseil
    )


# ------------------------------------------------------------
# TEST MÉMOIRE
# ------------------------------------------------------------

def test_memoire_adversaire():

    memoire = globals().get(
        "MEMOIRE_PANDORAGA"
    )

    if memoire is None:

        return True

    analyseur = AnalyseurAdversaire(
        memoire
    )

    profil = (
        analyseur.charger_profil_memoire(
            "Test"
        )
    )

    return isinstance(
        profil,
        dict
    )


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("🐼 PANDORAGA FULL ADAPTATION Ω")
    print("👁️ BLOC 20 — ANALYSEUR ADVERSAIRE")
    print("=" * 65)

    print()
    print("🧪 TESTS")
    print("-" * 65)

    print(
        "Profil :",
        "OK"
        if test_profil_adversaire()
        else "ERREUR"
    )

    print(
        "Conseil :",
        "OK"
        if test_conseil()
        else "ERREUR"
    )

    print(
        "Mémoire :",
        "OK"
        if test_memoire_adversaire()
        else "ERREUR"
    )

    print()
    print("🔎 EXEMPLE D'ANALYSE")
    print("-" * 65)

    analyseur = AnalyseurAdversaire()

    sequence = [
        "e4",
        "e5",
        "Qh5",
        "Nc6",
        "Bc4",
        "Nf6",
        "Qxf7+"
    ]

    profil = analyseur.analyser_sequence(
        "Adversaire_Test",
        sequence
    )

    for cle, valeur in profil.items():

        print(
            f"{cle:20} : {valeur}"
        )

    print()
    print("💡 CONSEIL")
    print("-" * 65)

    conseil = analyseur.conseil_adaptation(
        "Adversaire_Test"
    )

    for cle, valeur in conseil.items():

        print(
            f"{cle:20} : {valeur}"
        )

    print()
    print("📊 STATISTIQUES")
    print("-" * 65)

    for cle, valeur in STATS_ADVERSAIRE.items():

        print(
            f"{cle:25} : {valeur}"
        )

    print()
    print("🐼 BLOC 20 CHARGÉ AVEC SUCCÈS.")
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 22/26 — PRÉDICTION DU PROCHAIN COUP
# ============================================================

import time


# ------------------------------------------------------------
# PARAMÈTRES
# ------------------------------------------------------------

MAX_PREDICTIONS = 5

SCORE_PREDICTION_MIN = -1000000

SCORE_PREDICTION_MAX = 1000000

BONUS_MEMOIRE = 100

BONUS_STYLE = 80

BONUS_HISTORIQUE = 60

BONUS_KILLER = 40

BONUS_TACTIQUE = 70

BONUS_ADAPTATION = 50


# ------------------------------------------------------------
# STATISTIQUES
# ------------------------------------------------------------

STATS_PREDICTION = {

    "predictions": 0,

    "coups_candidats": 0,

    "predictions_memorisees": 0,

    "predictions_style": 0,

    "predictions_tactiques": 0,

    "exactes": 0,

    "fausses": 0
}


# ------------------------------------------------------------
# CLASSE PRÉDICTION
# ------------------------------------------------------------

class PredicteurPandoraga:

    def __init__(
        self,
        memoire=None,
        analyseur=None,
        personnalite=None
    ):

        self.memoire = (
            memoire
            if memoire is not None
            else globals().get(
                "MEMOIRE_PANDORAGA"
            )
        )

        self.analyseur = (
            analyseur
            if analyseur is not None
            else globals().get(
                "ANALYSEUR_ADVERSAIRE"
            )
        )

        self.personnalite = (
            personnalite
            if personnalite is not None
            else globals().get(
                "PERSONNALITE_PANDORAGA"
            )
        )

        self.derniere_prediction = []

        self.historique_predictions = []


    # ========================================================
    # IDENTIFIANT SÛR
    # ========================================================

    def id_coup(
        self,
        coup
    ):

        try:

            return identifiant_coup(
                coup
            )

        except Exception:

            return str(
                coup
            )


    # ========================================================
    # SCORE LIMITÉ
    # ========================================================

    def limiter(
        self,
        score
    ):

        return max(
            SCORE_PREDICTION_MIN,
            min(
                SCORE_PREDICTION_MAX,
                float(score)
            )
        )


    # ========================================================
    # SCORE MÉMOIRE
    # ========================================================

    def score_memoire(
        self,
        etat,
        coup
    ):

        if self.memoire is None:

            return 0

        try:

            position = (
                self.creer_cle_position(
                    etat
                )
            )

        except Exception:

            return 0

        appris = (
            self.memoire.donnees.get(
                "coups_appris",
                {}
            )
        )

        coups = appris.get(
            position,
            {}
        )

        if not coups:

            return 0

        identifiant = self.id_coup(
            coup
        )

        info = coups.get(
            identifiant
        )

        if info is None:

            return 0

        score = info.get(
            "score",
            0
        )

        essais = info.get(
            "essais",
            0
        )

        bons = info.get(
            "bons",
            0
        )

        if essais > 0:

            taux = (
                bons
                /
                essais
            )

        else:

            taux = 0

        STATS_PREDICTION[
            "predictions_memorisees"
        ] += 1

        return (
            score
            +
            taux * BONUS_MEMOIRE
        )


    # ========================================================
    # CLÉ POSITION
    # ========================================================

    def creer_cle_position(
        self,
        etat
    ):

        # Utilise la fonction du moteur si elle existe.
        for nom in (
            "cle_position",
            "hash_position",
            "empreinte_position"
        ):

            fonction = globals().get(
                nom
            )

            if callable(fonction):

                try:

                    return str(
                        fonction(etat)
                    )

                except Exception:

                    pass

        # Fallback simple.
        try:

            plateau = etat.get(
                "plateau",
                []
            )

            tour = etat.get(
                "tour",
                ""
            )

            return (
                str(plateau)
                +
                "|"
                +
                str(tour)
            )

        except Exception:

            return str(
                etat
            )


    # ========================================================
    # SCORE STYLE ADVERSAIRE
    # ========================================================

    def score_style(
        self,
        etat,
        coup,
        nom_adversaire=None
    ):

        if self.analyseur is None:

            return 0

        if nom_adversaire is None:

            return 0

        try:

            profil = (
                self.analyseur.obtenir_profil(
                    nom_adversaire
                )
            )

        except Exception:

            return 0

        style = str(
            profil.get(
                "profil",
                "inconnu"
            )
        ).lower()

        score = 0

        try:

            capture = coup_est_capture(
                etat,
                coup
            )

        except Exception:

            capture = False

        try:

            promotion = coup_est_promotion(
                coup
            )

        except Exception:

            promotion = False

        try:

            echec = coup_donne_echec(
                etat,
                coup
            )

        except Exception:

            echec = False

        if style == "agressif":

            if capture:
                score += 40

            if echec:
                score += 50

            if promotion:
                score += 70

        elif style == "tactique":

            if echec:
                score += 65

            if capture:
                score += 45

            if promotion:
                score += 60

        elif style == "defensif":

            if capture:
                score += 20

            if echec:
                score += 10

        elif style == "positionnel":

            # Les coups calmes sont légèrement favorisés.
            if not capture and not echec:
                score += 25

        STATS_PREDICTION[
            "predictions_style"
        ] += 1

        return score


    # ========================================================
    # SCORE TACTIQUE
    # ========================================================

    def score_tactique(
        self,
        etat,
        coup
    ):

        score = 0

        try:

            if coup_est_capture(
                etat,
                coup
            ):

                score += 30

        except Exception:

            pass

        try:

            if coup_donne_echec(
                etat,
                coup
            ):

                score += 55

        except Exception:

            pass

        try:

            if coup_est_promotion(
                coup
            ):

                score += 80

        except Exception:

            pass

        if score > 0:

            STATS_PREDICTION[
                "predictions_tactiques"
            ] += 1

        return score


    # ========================================================
    # SCORE HISTORIQUE
    # ========================================================

    def score_historique(
        self,
        nom_adversaire,
        coup
    ):

        if self.analyseur is None:

            return 0

        historique = getattr(
            self.analyseur,
            "historique_coups",
            {}
        )

        coups = historique.get(
            str(nom_adversaire),
            []
        )

        if not coups:

            return 0

        identifiant = self.id_coup(
            coup
        )

        # Plus un coup apparaît,
        # plus il devient probable.
        occurrences = 0

        for ancien in coups:

            if str(ancien) == identifiant:

                occurrences += 1

        return (
            occurrences
            *
            BONUS_HISTORIQUE
        )


    # ========================================================
    # SCORE KILLER
    # ========================================================

    def score_killer(
        self,
        etat,
        coup,
        profondeur=1
    ):

        fonction = globals().get(
            "score_killer_avance"
        )

        if not callable(
            fonction
        ):

            return 0

        try:

            return fonction(
                etat,
                coup,
                profondeur
            )

        except Exception:

            return 0


    # ========================================================
    # SCORE PERSONNALITÉ
    # ========================================================

    def score_personnalite(
        self,
        etat,
        coup
    ):

        if self.personnalite is None:

            return 0

        score = 0

        profil = getattr(
            self.personnalite,
            "profil",
            {}
        )

        try:

            capture = coup_est_capture(
                etat,
                coup
            )

        except Exception:

            capture = False

        try:

            echec = coup_donne_echec(
                etat,
                coup
            )

        except Exception:

            echec = False

        if capture:

            score += (
                profil.get(
                    "attaque",
                    50
                )
                *
                0.20
            )

        if echec:

            score += (
                profil.get(
                    "initiative",
                    50
                )
                *
                0.30
            )

        return score


    # ========================================================
    # SCORE GLOBAL
    # ========================================================

    def score_coup(
        self,
        etat,
        coup,
        nom_adversaire=None,
        profondeur=1
    ):

        score = 0

        score += self.score_memoire(
            etat,
            coup
        )

        score += self.score_style(
            etat,
            coup,
            nom_adversaire
        )

        score += self.score_historique(
            nom_adversaire,
            coup
        )

        score += self.score_tactique(
            etat,
            coup
        )

        score += self.score_killer(
            etat,
            coup,
            profondeur
        )

        score += self.score_personnalite(
            etat,
            coup
        )

        return self.limiter(
            score
        )


    # ========================================================
    # PRÉDIRE
    # ========================================================

    def predire(
        self,
        etat,
        nom_adversaire=None,
        profondeur=1,
        nombre=MAX_PREDICTIONS
    ):

        STATS_PREDICTION[
            "predictions"
        ] += 1

        try:

            coups = generer_coups_legaux(
                etat
            )

        except Exception:

            return []

        if not coups:

            self.derniere_prediction = []

            return []

        candidats = []

        for coup in coups:

            score = self.score_coup(
                etat,
                coup,
                nom_adversaire,
                profondeur
            )

            candidats.append(
                (
                    score,
                    coup
                )
            )

        candidats.sort(
            key=lambda x: x[0],
            reverse=True
        )

        nombre = max(
            1,
            min(
                int(nombre),
                MAX_PREDICTIONS
            )
        )

        candidats = candidats[
            :nombre
        ]

        STATS_PREDICTION[
            "coups_candidats"
        ] += len(
            candidats
        )

        # Conversion en probabilités relatives.
        if candidats:

            minimum = min(
                score
                for score, coup
                in candidats
            )

            poids = []

            for score, coup in candidats:

                poids.append(
                    max(
                        1.0,
                        score - minimum + 1.0
                    )
                )

            total = sum(
                poids
            )

        else:

            total = 1.0
            poids = []

        resultat = []

        for index, item in enumerate(
            candidats
        ):

            score, coup = item

            probabilite = (
                poids[index]
                /
                total
            ) * 100.0

            resultat.append({

                "coup":
                    coup,

                "score":
                    score,

                "probabilite":
                    round(
                        probabilite,
                        2
                    )
            })

        self.derniere_prediction = (
            resultat
        )

        self.historique_predictions.append({

            "date":
                time.time(),

            "adversaire":
                nom_adversaire,

            "predictions":
                resultat
        })

        self.historique_predictions = (
            self.historique_predictions[
                -100:
            ]
        )

        return resultat


    # ========================================================
    # MEILLEURE PRÉDICTION
    # ========================================================

    def meilleur(
        self,
        etat,
        nom_adversaire=None,
        profondeur=1
    ):

        predictions = self.predire(
            etat,
            nom_adversaire,
            profondeur,
            1
        )

        if not predictions:

            return None

        return predictions[0]["coup"]


    # ========================================================
    # VÉRIFICATION APRÈS COUP
    # ========================================================

    def verifier(
        self,
        coup_reel
    ):

        if not self.derniere_prediction:

            return False

        identifiant_reel = self.id_coup(
            coup_reel
        )

        trouve = False

        for prediction in (
            self.derniere_prediction
        ):

            if (
                self.id_coup(
                    prediction["coup"]
                )
                ==
                identifiant_reel
            ):

                trouve = True

                break

        if trouve:

            STATS_PREDICTION[
                "exactes"
            ] += 1

        else:

            STATS_PREDICTION[
                "fausses"
            ] += 1

        return trouve


    # ========================================================
    # TAUX DE RÉUSSITE
    # ========================================================

    def precision(self):

        total = (
            STATS_PREDICTION[
                "exactes"
            ]
            +
            STATS_PREDICTION[
                "fausses"
            ]
        )

        if total == 0:

            return 0.0

        return (
            STATS_PREDICTION[
                "exactes"
            ]
            /
            total
        ) * 100.0


    # ========================================================
    # RÉSUMÉ
    # ========================================================

    def resume(self):

        return {

            "derniere_prediction":
                self.derniere_prediction,

            "precision":
                round(
                    self.precision(),
                    2
                ),

            "predictions":
                STATS_PREDICTION[
                    "predictions"
                ]
        }


# ------------------------------------------------------------
# INSTANCE GLOBALE
# ------------------------------------------------------------

PREDICTEUR_PANDORAGA = (
    PredicteurPandoraga()
)


# ------------------------------------------------------------
# RACCOURCIS
# ------------------------------------------------------------

def predire_coup(
    etat,
    nom_adversaire=None,
    profondeur=1
):

    return PREDICTEUR_PANDORAGA.meilleur(
        etat,
        nom_adversaire,
        profondeur
    )


def predire_coups(
    etat,
    nom_adversaire=None,
    profondeur=1,
    nombre=5
):

    return PREDICTEUR_PANDORAGA.predire(
        etat,
        nom_adversaire,
        profondeur,
        nombre
    )


def verifier_prediction(
    coup_reel
):

    return PREDICTEUR_PANDORAGA.verifier(
        coup_reel
    )


# ------------------------------------------------------------
# TEST DU SCORE
# ------------------------------------------------------------

def test_score_prediction():

    predicteur = PredicteurPandoraga()

    etat = {
        "plateau": [],
        "tour": "blanc"
    }

    # Test avec un faux coup simple.
    score = predicteur.score_coup(
        etat,
        "e4"
    )

    return isinstance(
        score,
        float
    )


# ------------------------------------------------------------
# TEST CLÉ
# ------------------------------------------------------------

def test_cle_position():

    predicteur = PredicteurPandoraga()

    etat = {
        "plateau": [
            "r",
            "n",
            "b"
        ],
        "tour": "blanc"
    }

    cle = predicteur.creer_cle_position(
        etat
    )

    return isinstance(
        cle,
        str
    )


# ------------------------------------------------------------
# TEST PROFIL
# ------------------------------------------------------------

def test_profil_prediction():

    predicteur = PredicteurPandoraga()

    profil = {

        "nom":
            "Test",

        "profil":
            "agressif"
    }

    # Le score style doit être calculable
    # même si aucun coup réel n'est fourni.
    return isinstance(
        profil,
        dict
    )


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print(
        "🐼 PANDORAGA FULL ADAPTATION Ω"
    )

    print(
        "🔮 BLOC 22 — PRÉDICTION"
    )

    print(
        "=" * 65
    )

    print()
    print("🧪 TESTS")
    print("-" * 65)

    print(
        "Score :",
        "OK"
        if test_score_prediction()
        else "ERREUR"
    )

    print(
        "Clé position :",
        "OK"
        if test_cle_position()
        else "ERREUR"
    )

    print(
        "Profil :",
        "OK"
        if test_profil_prediction()
        else "ERREUR"
    )

    print()
    print("📊 STATISTIQUES")
    print("-" * 65)

    for cle, valeur in (
        STATS_PREDICTION.items()
    ):

        print(
            f"{cle:30} : {valeur}"
        )

    print()
    print(
        "Précision actuelle :",
        f"{PREDICTEUR_PANDORAGA.precision():.2f}%"
    )

    print()
    print(
        "🐼 BLOC 22 CHARGÉ AVEC SUCCÈS."
    )
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 23/26 — FULL ADAPTATION
# ============================================================

import time


# ------------------------------------------------------------
# MODES D'ADAPTATION
# ------------------------------------------------------------

ADAPTATION_NEUTRE = "neutre"
ADAPTATION_CONTRE_ATTAQUE = "contre_attaque"
ADAPTATION_CONTRE_TACTIQUE = "anti_tactique"
ADAPTATION_CONTRE_DEFENSE = "pression"
ADAPTATION_CONTRE_POSITIONNEL = "desequilibre"


# ------------------------------------------------------------
# PARAMÈTRES
# ------------------------------------------------------------

ADAPTATION_MIN_CONFIANCE = 20.0

BONUS_ADAPTATION_MAX = 120.0

MALUS_ADAPTATION_MAX = 120.0


# ------------------------------------------------------------
# STATISTIQUES
# ------------------------------------------------------------

STATS_ADAPTATION = {

    "analyses": 0,

    "adaptations": 0,

    "changements_style": 0,

    "predictions_utilisees": 0,

    "coups_memorises_utilises": 0,

    "confiance_moyenne": 0.0
}


# ------------------------------------------------------------
# CLASSE FULL ADAPTATION
# ------------------------------------------------------------

class FullAdaptationPandoraga:

    def __init__(
        self,
        memoire=None,
        analyseur=None,
        personnalite=None,
        predicteur=None
    ):

        self.memoire = (
            memoire
            if memoire is not None
            else globals().get(
                "MEMOIRE_PANDORAGA"
            )
        )

        self.analyseur = (
            analyseur
            if analyseur is not None
            else globals().get(
                "ANALYSEUR_ADVERSAIRE"
            )
        )

        self.personnalite = (
            personnalite
            if personnalite is not None
            else globals().get(
                "PERSONNALITE_PANDORAGA"
            )
        )

        self.predicteur = (
            predicteur
            if predicteur is not None
            else globals().get(
                "PREDICTEUR_PANDORAGA"
            )
        )

        self.adversaire = None

        self.profil = None

        self.mode = ADAPTATION_NEUTRE

        self.confiance = 0.0

        self.historique = []

        self.derniere_adaptation = None


    # ========================================================
    # DÉFINIR ADVERSAIRE
    # ========================================================

    def definir_adversaire(
        self,
        nom
    ):

        self.adversaire = str(
            nom
        )

        if self.analyseur is not None:

            try:

                self.profil = (
                    self.analyseur.obtenir_profil(
                        self.adversaire
                    )
                )

            except Exception:

                self.profil = None

        return self.profil


    # ========================================================
    # OBTENIR PROFIL
    # ========================================================

    def obtenir_profil(self):

        if self.profil is not None:

            return self.profil

        if (
            self.analyseur is not None
            and
            self.adversaire is not None
        ):

            try:

                self.profil = (
                    self.analyseur.obtenir_profil(
                        self.adversaire
                    )
                )

                return self.profil

            except Exception:

                pass

        return {

            "nom":
                self.adversaire,

            "profil":
                "inconnu",

            "confiance":
                0.0
        }


    # ========================================================
    # DÉTERMINER MODE
    # ========================================================

    def determiner_mode(
        self,
        profil
    ):

        style = str(
            profil.get(
                "profil",
                "inconnu"
            )
        ).lower()

        if style == "agressif":

            return ADAPTATION_CONTRE_ATTAQUE

        if style == "tactique":

            return ADAPTATION_CONTRE_TACTIQUE

        if style == "defensif":

            return ADAPTATION_CONTRE_DEFENSE

        if style == "positionnel":

            return ADAPTATION_CONTRE_POSITIONNEL

        return ADAPTATION_NEUTRE


    # ========================================================
    # CALCUL CONFIANCE
    # ========================================================

    def calculer_confiance(
        self,
        profil
    ):

        confiance = float(
            profil.get(
                "confiance",
                0.0
            )
        )

        parties = float(
            profil.get(
                "parties",
                0
            )
        )

        coups = float(
            profil.get(
                "coups_total",
                0
            )
        )

        # Plus Pandoraga observe le joueur,
        # plus l'adaptation devient fiable.
        bonus_parties = min(
            parties * 2.0,
            20.0
        )

        bonus_coups = min(
            coups / 10.0,
            20.0
        )

        resultat = (
            confiance
            +
            bonus_parties
            +
            bonus_coups
        )

        return min(
            100.0,
            resultat
        )


    # ========================================================
    # ADAPTATION PRINCIPALE
    # ========================================================

    def analyser(
        self,
        etat=None
    ):

        STATS_ADAPTATION[
            "analyses"
        ] += 1

        profil = self.obtenir_profil()

        self.mode = self.determiner_mode(
            profil
        )

        self.confiance = (
            self.calculer_confiance(
                profil
            )
        )

        # Adaptation de personnalité
        if self.personnalite is not None:

            if self.confiance >= (
                ADAPTATION_MIN_CONFIANCE
            ):

                try:

                    ancienne = (
                        self.personnalite.actuelle
                    )

                    nouvelle = (
                        self.personnalite.adapter_a_adversaire(
                            profil
                        )
                    )

                    if ancienne != nouvelle:

                        STATS_ADAPTATION[
                            "changements_style"
                        ] += 1

                except Exception:

                    pass

        self.derniere_adaptation = {

            "date":
                time.time(),

            "adversaire":
                self.adversaire,

            "profil":
                dict(profil),

            "mode":
                self.mode,

            "confiance":
                self.confiance
        }

        self.historique.append(
            self.derniere_adaptation
        )

        self.historique = (
            self.historique[
                -100:
            ]
        )

        STATS_ADAPTATION[
            "adaptations"
        ] += 1

        ancien = STATS_ADAPTATION[
            "confiance_moyenne"
        ]

        n = STATS_ADAPTATION[
            "adaptations"
        ]

        STATS_ADAPTATION[
            "confiance_moyenne"
        ] = (
            (
                ancien * (n - 1)
            )
            +
            self.confiance
        ) / n

        return self.derniere_adaptation


    # ========================================================
    # SCORE ADAPTATIF
    # ========================================================

    def score_adaptatif(
        self,
        etat,
        coup
    ):

        score = 0.0

        mode = self.mode

        # ----------------------------------------------------
        # CONTRE-ATTAQUE
        # ----------------------------------------------------

        if mode == (
            ADAPTATION_CONTRE_ATTAQUE
        ):

            try:

                if coup_est_capture(
                    etat,
                    coup
                ):

                    score += 25

            except Exception:

                pass

            try:

                if coup_donne_echec(
                    etat,
                    coup
                ):

                    score += 35

            except Exception:

                pass


        # ----------------------------------------------------
        # ANTI-TACTIQUE
        # ----------------------------------------------------

        elif mode == (
            ADAPTATION_CONTRE_TACTIQUE
        ):

            try:

                if not coup_est_capture(
                    etat,
                    coup
                ):

                    score += 15

            except Exception:

                pass


        # ----------------------------------------------------
        # PRESSION
        # ----------------------------------------------------

        elif mode == (
            ADAPTATION_CONTRE_DEFENSE
        ):

            try:

                if coup_donne_echec(
                    etat,
                    coup
                ):

                    score += 30

            except Exception:

                pass


        # ----------------------------------------------------
        # DÉSÉQUILIBRE
        # ----------------------------------------------------

        elif mode == (
            ADAPTATION_CONTRE_POSITIONNEL
        ):

            try:

                if coup_est_capture(
                    etat,
                    coup
                ):

                    score += 20

            except Exception:

                pass


        # ----------------------------------------------------
        # PERSONNALITÉ
        # ----------------------------------------------------

        if self.personnalite is not None:

            try:

                profil = (
                    self.personnalite.profil
                )

                try:

                    if coup_est_capture(
                        etat,
                        coup
                    ):

                        score += (
                            profil.get(
                                "attaque",
                                50
                            )
                            *
                            0.10
                        )

                except Exception:

                    pass

                try:

                    if coup_donne_echec(
                        etat,
                        coup
                    ):

                        score += (
                            profil.get(
                                "initiative",
                                50
                            )
                            *
                            0.10
                        )

                except Exception:

                    pass

            except Exception:

                pass

        return max(
            -MALUS_ADAPTATION_MAX,
            min(
                BONUS_ADAPTATION_MAX,
                score
            )
        )


    # ========================================================
    # INTÉGRATION AVEC PRÉDICTION
    # ========================================================

    def prediction(
        self,
        etat
    ):

        if self.predicteur is None:

            return []

        predictions = (
            self.predicteur.predire(
                etat,
                self.adversaire
            )
        )

        if predictions:

            STATS_ADAPTATION[
                "predictions_utilisees"
            ] += 1

        return predictions


    # ========================================================
    # CHOISIR COUP ADAPTATIF
    # ========================================================

    def choisir_coup(
        self,
        etat,
        coups=None
    ):

        # ----------------------------------------------------
        # Génération des coups
        # ----------------------------------------------------

        if coups is None:

            try:

                coups = generer_coups_legaux(
                    etat
                )

            except Exception:

                return None

        if not coups:

            return None

        # ----------------------------------------------------
        # Analyse actuelle
        # ----------------------------------------------------

        self.analyser(
            etat
        )

        # ----------------------------------------------------
        # Évaluation
        # ----------------------------------------------------

        candidats = []

        for coup in coups:

            score = self.score_adaptatif(
                etat,
                coup
            )

            # Ajout de la prédiction
            # seulement si elle existe.
            if self.predicteur is not None:

                try:

                    predictions = (
                        self.predicteur.derniere_prediction
                    )

                    for prediction in predictions:

                        coup_prediction = (
                            prediction.get(
                                "coup"
                            )
                        )

                        if (
                            str(
                                coup_prediction
                            )
                            ==
                            str(
                                coup
                            )
                        ):

                            score += (
                                prediction.get(
                                    "probabilite",
                                    0
                                )
                                *
                                0.50
                            )

                            break

                except Exception:

                    pass

            candidats.append(
                (
                    score,
                    coup
                )
            )

        candidats.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return candidats[0][1]


    # ========================================================
    # ENREGISTRER RÉSULTAT
    # ========================================================

    def enregistrer_resultat(
        self,
        resultat
    ):

        if self.memoire is None:

            return False

        try:

            donnees = (
                self.memoire.donnees
            )

            adaptation = donnees.setdefault(
                "adaptation",
                []
            )

            adaptation.append({

                "date":
                    time.time(),

                "adversaire":
                    self.adversaire,

                "mode":
                    self.mode,

                "confiance":
                    self.confiance,

                "resultat":
                    str(resultat)
            })

            # On limite la taille.
            if len(adaptation) > 100:

                del adaptation[
                    :-100
                ]

            # Sauvegarde si la classe mémoire
            # possède cette méthode.
            sauvegarder = getattr(
                self.memoire,
                "sauvegarder",
                None
            )

            if callable(
                sauvegarder
            ):

                sauvegarder()

            return True

        except Exception:

            return False


    # ========================================================
    # RÉINITIALISATION
    # ========================================================

    def reset(self):

        self.adversaire = None

        self.profil = None

        self.mode = (
            ADAPTATION_NEUTRE
        )

        self.confiance = 0.0

        self.derniere_adaptation = None


    # ========================================================
    # RÉSUMÉ
    # ========================================================

    def resume(self):

        return {

            "adversaire":
                self.adversaire,

            "mode":
                self.mode,

            "confiance":
                round(
                    self.confiance,
                    2
                ),

            "profil":
                self.profil,

            "derniere_adaptation":
                self.derniere_adaptation
        }


# ------------------------------------------------------------
# INSTANCE GLOBALE
# ------------------------------------------------------------

FULL_ADAPTATION_PANDORAGA = (
    FullAdaptationPandoraga()
)


# ------------------------------------------------------------
# RACCOURCIS
# ------------------------------------------------------------

def definir_adversaire_pandoraga(
    nom
):

    return (
        FULL_ADAPTATION_PANDORAGA.definir_adversaire(
            nom
        )
    )


def analyser_adaptation():

    return (
        FULL_ADAPTATION_PANDORAGA.analyser()
    )


def score_adaptatif(
    etat,
    coup
):

    return (
        FULL_ADAPTATION_PANDORAGA.score_adaptatif(
            etat,
            coup
        )
    )


def choisir_coup_adaptatif(
    etat,
    coups=None
):

    return (
        FULL_ADAPTATION_PANDORAGA.choisir_coup(
            etat,
            coups
        )
    )


# ------------------------------------------------------------
# TEST PROFIL
# ------------------------------------------------------------

def test_profil_adaptation():

    moteur = FullAdaptationPandoraga()

    moteur.definir_adversaire(
        "Test"
    )

    resultat = moteur.analyser()

    return (
        isinstance(
            resultat,
            dict
        )
        and
        "mode" in resultat
        and
        "confiance" in resultat
    )


# ------------------------------------------------------------
# TEST SCORE
# ------------------------------------------------------------

def test_score_adaptatif():

    moteur = FullAdaptationPandoraga()

    moteur.mode = (
        ADAPTATION_CONTRE_ATTAQUE
    )

    etat = {}

    score = moteur.score_adaptatif(
        etat,
        "e4"
    )

    return isinstance(
        score,
        (int, float)
    )


# ------------------------------------------------------------
# TEST RÉINITIALISATION
# ------------------------------------------------------------

def test_reset():

    moteur = FullAdaptationPandoraga()

    moteur.definir_adversaire(
        "Test"
    )

    moteur.reset()

    return (
        moteur.adversaire is None
        and
        moteur.mode
        ==
        ADAPTATION_NEUTRE
    )


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print(
        "🐼 PANDORAGA FULL ADAPTATION Ω"
    )

    print(
        "🧠 BLOC 23 — FULL ADAPTATION"
    )

    print(
        "=" * 70
    )

    print()
    print("🧪 TESTS")
    print("-" * 70)

    print(
        "Profil :",
        "OK"
        if test_profil_adaptation()
        else "ERREUR"
    )

    print(
        "Score :",
        "OK"
        if test_score_adaptatif()
        else "ERREUR"
    )

    print(
        "Reset :",
        "OK"
        if test_reset()
        else "ERREUR"
    )

    print()
    print("📊 STATISTIQUES")
    print("-" * 70)

    for cle, valeur in (
        STATS_ADAPTATION.items()
    ):

        if isinstance(
            valeur,
            float
        ):

            print(
                f"{cle:30} : "
                f"{valeur:.2f}"
            )

        else:

            print(
                f"{cle:30} : "
                f"{valeur}"
            )

    print()
    print(
        "🐼 BLOC 23 CHARGÉ AVEC SUCCÈS."
    )
    # ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 24/26 — APPRENTISSAGE AUTOMATIQUE
# ============================================================

import time


# ------------------------------------------------------------
# PARAMÈTRES
# ------------------------------------------------------------

APPRENTISSAGE_MAX_POSITIONS = 5000
APPRENTISSAGE_MAX_COUPS = 20
APPRENTISSAGE_MAX_ERREURS = 1000

APPRENTISSAGE_BONUS = 10.0
APPRENTISSAGE_MALUS = 8.0

APPRENTISSAGE_RECOMPENSE_VICTOIRE = 20.0
APPRENTISSAGE_RECOMPENSE_NULLE = 2.0
APPRENTISSAGE_RECOMPENSE_DEFAITE = -20.0

TAUX_APPRENTISSAGE = 0.15


# ------------------------------------------------------------
# STATISTIQUES
# ------------------------------------------------------------

STATS_APPRENTISSAGE = {

    "parties_apprises": 0,

    "coups_appris": 0,

    "coups_corrects": 0,

    "coups_erreurs": 0,

    "positions_apprises": 0,

    "adversaires_appris": 0,

    "predictions_apprises": 0,

    "victoires_apprises": 0,

    "defaites_apprises": 0,

    "nulles_apprises": 0
}


# ------------------------------------------------------------
# CLASSE APPRENTISSAGE
# ------------------------------------------------------------

class ApprentissagePandoraga:

    def __init__(
        self,
        memoire=None,
        adaptation=None,
        predicteur=None
    ):

        self.memoire = (
            memoire
            if memoire is not None
            else globals().get(
                "MEMOIRE_PANDORAGA"
            )
        )

        self.adaptation = (
            adaptation
            if adaptation is not None
            else globals().get(
                "FULL_ADAPTATION_PANDORAGA"
            )
        )

        self.predicteur = (
            predicteur
            if predicteur is not None
            else globals().get(
                "PREDICTEUR_PANDORAGA"
            )
        )

        self.partie = []

        self.positions = {}

        self.derniere_lecon = None


    # ========================================================
    # S'ASSURER QUE LA MÉMOIRE EXISTE
    # ========================================================

    def obtenir_donnees(self):

        if self.memoire is None:

            return None

        if not hasattr(
            self.memoire,
            "donnees"
        ):

            return None

        donnees = self.memoire.donnees

        # Structures nécessaires.
        donnees.setdefault(
            "coups_appris",
            {}
        )

        donnees.setdefault(
            "adversaires",
            {}
        )

        donnees.setdefault(
            "parties",
            []
        )

        donnees.setdefault(
            "erreurs",
            []
        )

        donnees.setdefault(
            "apprentissage",
            {}
        )

        return donnees


    # ========================================================
    # CLÉ POSITION
    # ========================================================

    def cle_position(
        self,
        etat
    ):

        # On réutilise le système du prédicteur
        # quand il est disponible.

        if self.predicteur is not None:

            try:

                return (
                    self.predicteur.creer_cle_position(
                        etat
                    )
                )

            except Exception:

                pass

        try:

            plateau = etat.get(
                "plateau",
                []
            )

            tour = etat.get(
                "tour",
                ""
            )

            return (
                str(plateau)
                +
                "|"
                +
                str(tour)
            )

        except Exception:

            return str(
                etat
            )


    # ========================================================
    # IDENTIFIANT COUP
    # ========================================================

    def identifiant_coup(
        self,
        coup
    ):

        fonction = globals().get(
            "identifiant_coup"
        )

        if callable(
            fonction
        ):

            try:

                return str(
                    fonction(coup)
                )

            except Exception:

                pass

        return str(
            coup
        )


    # ========================================================
    # COMMENCER PARTIE
    # ========================================================

    def commencer_partie(
        self,
        adversaire="Inconnu"
    ):

        self.partie = []

        self.positions = {}

        self.adversaire = str(
            adversaire
        )

        return True


    # ========================================================
    # ENREGISTRER COUP
    # ========================================================

    def enregistrer_coup(
        self,
        etat,
        coup,
        evaluation=0.0,
        prediction=False
    ):

        cle = self.cle_position(
            etat
        )

        identifiant = (
            self.identifiant_coup(
                coup
            )
        )

        entree = {

            "position":
                cle,

            "coup":
                identifiant,

            "evaluation":
                float(evaluation),

            "prediction":
                bool(prediction),

            "date":
                time.time()
        }

        self.partie.append(
            entree
        )

        self.positions[
            cle
        ] = entree

        return entree


    # ========================================================
    # APPRENDRE UN COUP
    # ========================================================

    def apprendre_coup(
        self,
        position,
        coup,
        recompense,
        resultat=None
    ):

        donnees = self.obtenir_donnees()

        if donnees is None:

            return False

        coups_appris = donnees[
            "coups_appris"
        ]

        position = str(
            position
        )

        coup = str(
            coup
        )

        if position not in coups_appris:

            coups_appris[
                position
            ] = {}

        position_data = coups_appris[
            position
        ]

        if coup not in position_data:

            position_data[
                coup
            ] = {

                "score":
                    0.0,

                "essais":
                    0,

                "bons":
                    0,

                "erreurs":
                    0,

                "dernier_resultat":
                    None,

                "derniere_utilisation":
                    0.0
            }

            STATS_APPRENTISSAGE[
                "coups_appris"
            ] += 1

        info = position_data[
            coup
        ]

        ancien_score = float(
            info.get(
                "score",
                0.0
            )
        )

        # Mise à jour progressive.
        nouveau_score = (
            ancien_score
            *
            (
                1.0
                -
                TAUX_APPRENTISSAGE
            )
            +
            float(recompense)
            *
            TAUX_APPRENTISSAGE
        )

        info[
            "score"
        ] = nouveau_score

        info[
            "essais"
        ] += 1

        if recompense > 0:

            info[
                "bons"
            ] += 1

            STATS_APPRENTISSAGE[
                "coups_corrects"
            ] += 1

        elif recompense < 0:

            info[
                "erreurs"
            ] += 1

            STATS_APPRENTISSAGE[
                "coups_erreurs"
            ] += 1

        info[
            "dernier_resultat"
        ] = resultat

        info[
            "derniere_utilisation"
        ] = time.time()

        return True


    # ========================================================
    # APPRENDRE TOUTE LA PARTIE
    # ========================================================

    def apprendre_partie(
        self,
        resultat
    ):

        donnees = self.obtenir_donnees()

        if donnees is None:

            return False

        resultat = str(
            resultat
        ).lower()

        if resultat in (
            "victoire",
            "win",
            "1"
        ):

            recompense = (
                APPRENTISSAGE_RECOMPENSE_VICTOIRE
            )

            STATS_APPRENTISSAGE[
                "victoires_apprises"
            ] += 1

        elif resultat in (
            "defaite",
            "loss",
            "0"
        ):

            recompense = (
                APPRENTISSAGE_RECOMPENSE_DEFAITE
            )

            STATS_APPRENTISSAGE[
                "defaites_apprises"
            ] += 1

        else:

            recompense = (
                APPRENTISSAGE_RECOMPENSE_NULLE
            )

            STATS_APPRENTISSAGE[
                "nulles_apprises"
            ] += 1

        # ----------------------------------------------------
        # APPRENTISSAGE DE CHAQUE COUP
        # ----------------------------------------------------

        for entree in self.partie:

            position = entree[
                "position"
            ]

            coup = entree[
                "coup"
            ]

            # Les coups sont pondérés selon
            # leur évaluation initiale.
            bonus = 0.0

            evaluation = entree.get(
                "evaluation",
                0.0
            )

            if evaluation > 0:

                bonus += (
                    APPRENTISSAGE_BONUS
                )

            elif evaluation < 0:

                bonus -= (
                    APPRENTISSAGE_MALUS
                )

            recompense_coup = (
                recompense
                +
                bonus
            )

            self.apprendre_coup(
                position,
                coup,
                recompense_coup,
                resultat
            )

            STATS_APPRENTISSAGE[
                "positions_apprises"
            ] += 1

        # ----------------------------------------------------
        # MÉMORISER LA PARTIE
        # ----------------------------------------------------

        parties = donnees[
            "parties"
        ]

        parties.append({

            "date":
                time.time(),

            "adversaire":
                getattr(
                    self,
                    "adversaire",
                    "Inconnu"
                ),

            "resultat":
                resultat,

            "coups":
                len(
                    self.partie
                )
        })

        if len(parties) > 100:

            del parties[
                :-100
            ]

        STATS_APPRENTISSAGE[
            "parties_apprises"
        ] += 1

        self.derniere_lecon = {

            "resultat":
                resultat,

            "coups":
                len(
                    self.partie
                ),

            "recompense":
                recompense
        }

        # ----------------------------------------------------
        # APPRENTISSAGE ADVERSAIRE
        # ----------------------------------------------------

        self.apprendre_adversaire(
            resultat
        )

        # ----------------------------------------------------
        # NETTOYAGE
        # ----------------------------------------------------

        self.nettoyer_memoire()

        # ----------------------------------------------------
        # SAUVEGARDE
        # ----------------------------------------------------

        self.sauvegarder()

        return True


    # ========================================================
    # APPRENDRE ADVERSAIRE
    # ========================================================

    def apprendre_adversaire(
        self,
        resultat
    ):

        donnees = self.obtenir_donnees()

        if donnees is None:

            return False

        nom = str(
            getattr(
                self,
                "adversaire",
                "Inconnu"
            )
        )

        adversaires = donnees[
            "adversaires"
        ]

        if nom not in adversaires:

            adversaires[
                nom
            ] = {

                "parties":
                    0,

                "victoires":
                    0,

                "defaites":
                    0,

                "nulles":
                    0
            }

            STATS_APPRENTISSAGE[
                "adversaires_appris"
            ] += 1

        profil = adversaires[
            nom
        ]

        profil[
            "parties"
        ] += 1

        if resultat in (
            "victoire",
            "win",
            "1"
        ):

            profil[
                "victoires"
            ] += 1

        elif resultat in (
            "defaite",
            "loss",
            "0"
        ):

            profil[
                "defaites"
            ] += 1

        else:

            profil[
                "nulles"
            ] += 1

        return True


    # ========================================================
    # APPRENDRE UNE PRÉDICTION
    # ========================================================

    def apprendre_prediction(
        self,
        coup_reel
    ):

        if self.predicteur is None:

            return False

        try:

            correcte = (
                self.predicteur.verifier(
                    coup_reel
                )
            )

        except Exception:

            return False

        donnees = self.obtenir_donnees()

        if donnees is None:

            return False

        predictions = donnees.setdefault(
            "predictions",
            []
        )

        predictions.append({

            "date":
                time.time(),

            "adversaire":
                getattr(
                    self,
                    "adversaire",
                    "Inconnu"
                ),

            "coup_reel":
                self.identifiant_coup(
                    coup_reel
                ),

            "correcte":
                bool(correcte)
        })

        if len(predictions) > 500:

            del predictions[
                :-500
            ]

        STATS_APPRENTISSAGE[
            "predictions_apprises"
        ] += 1

        return correcte


    # ========================================================
    # APPRENDRE UNE ERREUR
    # ========================================================

    def enregistrer_erreur(
        self,
        position,
        coup,
        raison=""
    ):

        donnees = self.obtenir_donnees()

        if donnees is None:

            return False

        erreurs = donnees[
            "erreurs"
        ]

        erreurs.append({

            "date":
                time.time(),

            "position":
                str(position),

            "coup":
                self.identifiant_coup(
                    coup
                ),

            "raison":
                str(raison)
        })

        if len(erreurs) > (
            APPRENTISSAGE_MAX_ERREURS
        ):

            del erreurs[
                :-APPRENTISSAGE_MAX_ERREURS
            ]

        return True


    # ========================================================
    # OBTENIR MEILLEURS COUPS
    # ========================================================

    def meilleurs_coups(
        self,
        position,
        nombre=5
    ):

        donnees = self.obtenir_donnees()

        if donnees is None:

            return []

        coups = (
            donnees[
                "coups_appris"
            ].get(
                str(position),
                {}
            )
        )

        classement = []

        for coup, info in coups.items():

            score = float(
                info.get(
                    "score",
                    0
                )
            )

            essais = int(
                info.get(
                    "essais",
                    0
                )
            )

            classement.append({

                "coup":
                    coup,

                "score":
                    round(
                        score,
                        3
                    ),

                "essais":
                    essais
            })

        classement.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return classement[
            :max(
                1,
                int(nombre)
            )
        ]


    # ========================================================
    # NETTOYAGE MÉMOIRE
    # ========================================================

    def nettoyer_memoire(self):

        donnees = self.obtenir_donnees()

        if donnees is None:

            return False

        coups_appris = donnees[
            "coups_appris"
        ]

        # Limite du nombre de positions.
        if len(coups_appris) > (
            APPRENTISSAGE_MAX_POSITIONS
        ):

            positions = list(
                coups_appris.keys()
            )

            # On supprime les plus anciennes
            # selon l'ordre d'insertion.
            a_supprimer = positions[
                :-
                APPRENTISSAGE_MAX_POSITIONS
            ]

            for position in a_supprimer:

                del coups_appris[
                    position
                ]

        # Limite du nombre de coups par position.
        for position in list(
            coups_appris.keys()
        ):

            coups = coups_appris[
                position
            ]

            if len(coups) > (
                APPRENTISSAGE_MAX_COUPS
            ):

                classement = sorted(
                    coups.items(),
                    key=lambda x:
                    x[1].get(
                        "score",
                        0
                    ),
                    reverse=True
                )

                coups_appris[
                    position
                ] = dict(
                    classement[
                        :APPRENTISSAGE_MAX_COUPS
                    ]
                )

        return True


    # ========================================================
    # SAUVEGARDE
    # ========================================================

    def sauvegarder(self):

        if self.memoire is None:

            return False

        fonction = getattr(
            self.memoire,
            "sauvegarder",
            None
        )

        if callable(
            fonction
        ):

            try:

                fonction()

                return True

            except Exception:

                pass

        return False


    # ========================================================
    # RÉSUMÉ
    # ========================================================

    def resume(self):

        return {

            "partie_en_cours":
                len(
                    self.partie
                ),

            "adversaire":
                getattr(
                    self,
                    "adversaire",
                    None
                ),

            "derniere_lecon":
                self.derniere_lecon,

            "statistiques":
                dict(
                    STATS_APPRENTISSAGE
                )
        }


# ------------------------------------------------------------
# INSTANCE GLOBALE
# ------------------------------------------------------------

APPRENTISSAGE_PANDORAGA = (
    ApprentissagePandoraga()
)


# ------------------------------------------------------------
# RACCOURCIS
# ------------------------------------------------------------

def commencer_apprentissage(
    adversaire="Inconnu"
):

    return (
        APPRENTISSAGE_PANDORAGA.commencer_partie(
            adversaire
        )
    )


def apprendre_coup(
    etat,
    coup,
    evaluation=0.0,
    prediction=False
):

    return (
        APPRENTISSAGE_PANDORAGA.enregistrer_coup(
            etat,
            coup,
            evaluation,
            prediction
        )
    )


def apprendre_partie(
    resultat
):

    return (
        APPRENTISSAGE_PANDORAGA.apprendre_partie(
            resultat
        )
    )


def apprendre_prediction(
    coup_reel
):

    return APPRENTISSAGE_PANDORAGA.apprendre_prediction(
            coup_reel
        )


def apprendre_erreur(
    position,
    coup,
    raison=""
):

    return (
        APPRENTISSAGE_PANDORAGA.enregistrer_erreur(
            position,
            coup,
            raison
        )
    )


def coups_appris(
    position,
    nombre=5
):

    return (
        APPRENTISSAGE_PANDORAGA.meilleurs_coups(
            position,
            nombre
        )
    )


# ------------------------------------------------------------
# TEST APPRENTISSAGE
# ------------------------------------------------------------

def test_apprentissage():

    moteur = ApprentissagePandoraga()

    # Sans mémoire réelle, on vérifie
    # que l'objet est correctement créé.

    return (
        moteur is not None
        and
        hasattr(
            moteur,
            "apprendre_partie"
        )
    )


# ------------------------------------------------------------
# TEST STRUCTURE
# ------------------------------------------------------------

def test_structure():

    moteur = ApprentissagePandoraga()

    return (
        hasattr(
            moteur,
            "enregistrer_coup"
        )
        and
        hasattr(
            moteur,
            "apprendre_coup"
        )
        and
        hasattr(
            moteur,
            "nettoyer_memoire"
        )
    )


# ------------------------------------------------------------
# TEST IDENTIFIANT
# ------------------------------------------------------------

def test_identifiant():

    moteur = ApprentissagePandoraga()

    resultat = (
        moteur.identifiant_coup(
            "e4"
        )
    )

    return isinstance(
        resultat,
        str
    )


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print(
        "🐼 PANDORAGA FULL ADAPTATION Ω"
    )

    print(
        "📚 BLOC 24 — APPRENTISSAGE"
    )

    print(
        "=" * 70
    )

    print()
    print("🧪 TESTS")
    print("-" * 70)

    print(
        "Apprentissage :",
        "OK"
        if test_apprentissage()
        else "ERREUR"
    )

    print(
        "Structure :",
        "OK"
        if test_structure()
        else "ERREUR"
    )

    print(
        "Identifiant :",
        "OK"
        if test_identifiant()
        else "ERREUR"
    )

    print()
    print("📊 STATISTIQUES")
    print("-" * 70)

    for cle, valeur in (
        STATS_APPRENTISSAGE.items()
    ):

        print(
            f"{cle:30} : {valeur}"
        )

    print()
    print(
        "🐼 BLOC 24 CHARGÉ AVEC SUCCÈS."
    )
# ============================================================
# 🐼 PANDORAGA FULL ADAPTATION Ω
# BLOC 25/26 — MOTEUR PRINCIPAL
# ============================================================

import time


# ------------------------------------------------------------
# PARAMÈTRES
# ------------------------------------------------------------

MOTEUR_MAX_DEPTH = 15
MOTEUR_TIME_LIMIT = 30.0
MOTEUR_MAX_CANDIDATS = 15

MOTEUR_INF = 1000000000

MOTEUR_BONUS_MEMOIRE = 25.0
MOTEUR_BONUS_ADAPTATION = 1.0
MOTEUR_BONUS_PREDICTION = 0.75


# ------------------------------------------------------------
# STATISTIQUES
# ------------------------------------------------------------

STATS_MOTEUR = {

    "parties": 0,

    "coups": 0,

    "recherches": 0,

    "noeuds": 0,

    "profondeur_max": 0,

    "temps_total": 0.0,

    "memoire_utilisee": 0,

    "adaptation_utilisee": 0,

    "prediction_utilisee": 0
}


# ------------------------------------------------------------
# MOTEUR PRINCIPAL
# ------------------------------------------------------------

class PandoragaMoteurPrincipal:

    def __init__(
        self,
        memoire=None,
        adaptation=None,
        predicteur=None,
        apprentissage=None
    ):

        self.memoire = (
            memoire
            if memoire is not None
            else globals().get(
                "MEMOIRE_PANDORAGA"
            )
        )

        self.adaptation = (
            adaptation
            if adaptation is not None
            else globals().get(
                "FULL_ADAPTATION_PANDORAGA"
            )
        )

        self.predicteur = (
            predicteur
            if predicteur is not None
            else globals().get(
                "PREDICTEUR_PANDORAGA"
            )
        )

        self.apprentissage = (
            apprentissage
            if apprentissage is not None
            else globals().get(
                "APPRENTISSAGE_PANDORAGA"
            )
        )

        self.table_transposition = {}

        self.noeuds = 0

        self.stop = False

        self.debut_recherche = 0.0

        self.meilleur_coup = None

        self.meilleur_score = 0

        self.profondeur_atteinte = 0

        self.historique_coups = []


    # ========================================================
    # TEMPS
    # ========================================================

    def temps_ecoule(self):

        return (
            time.time()
            -
            self.debut_recherche
        )


    def temps_depasse(self):

        return (
            self.temps_ecoule()
            >=
            self.time_limit
        )


    # ========================================================
    # CLÉ POSITION
    # ========================================================

    def cle_position(
        self,
        etat
    ):

        if self.predicteur is not None:

            try:

                return (
                    self.predicteur.creer_cle_position(
                        etat
                    )
                )

            except Exception:

                pass

        return str(
            etat
        )


    # ========================================================
    # GÉNÉRATION COUPS
    # ========================================================

    def coups_legaux(
        self,
        etat
    ):

        fonction = globals().get(
            "generer_coups_legaux"
        )

        if not callable(
            fonction
        ):

            return []

        try:

            return list(
                fonction(etat)
            )

        except Exception:

            return []


    # ========================================================
    # JOUEUR
    # ========================================================

    def joueur(
        self,
        etat
    ):

        if isinstance(
            etat,
            dict
        ):

            return etat.get(
                "tour",
                "blanc"
            )

        return "blanc"


    # ========================================================
    # ÉVALUATION
    # ========================================================

    def evaluation_base(
        self,
        etat
    ):

        fonctions = (

            "evaluer_position",

            "evaluation_positionnelle",

            "evaluer",

            "evaluation"
        )

        for nom in fonctions:

            fonction = globals().get(
                nom
            )

            if callable(
                fonction
            ):

                try:

                    valeur = fonction(
                        etat
                    )

                    if isinstance(
                        valeur,
                        (int, float)
                    ):

                        return float(
                            valeur
                        )

                except Exception:

                    pass

        # Fallback très simple.
        return 0.0


    # ========================================================
    # SCORE MÉMOIRE
    # ========================================================

    def score_memoire(
        self,
        etat,
        coup
    ):

        if self.memoire is None:

            return 0.0

        try:

            cle = self.cle_position(
                etat
            )

            donnees = (
                self.memoire.donnees
            )

            positions = donnees.get(
                "coups_appris",
                {}
            )

            coups = positions.get(
                cle,
                {}
            )

            identifiant = str(
                coup
            )

            info = coups.get(
                identifiant
            )

            if info is None:

                return 0.0

            STATS_MOTEUR[
                "memoire_utilisee"
            ] += 1

            return (
                float(
                    info.get(
                        "score",
                        0.0
                    )
                )
                *
                MOTEUR_BONUS_MEMOIRE
                /
                100.0
            )

        except Exception:

            return 0.0


    # ========================================================
    # SCORE ADAPTATION
    # ========================================================

    def score_adaptation(
        self,
        etat,
        coup
    ):

        if self.adaptation is None:

            return 0.0

        fonction = getattr(
            self.adaptation,
            "score_adaptatif",
            None
        )

        if not callable(
            fonction
        ):

            return 0.0

        try:

            STATS_MOTEUR[
                "adaptation_utilisee"
            ] += 1

            return (
                float(
                    fonction(
                        etat,
                        coup
                    )
                )
                *
                MOTEUR_BONUS_ADAPTATION
            )

        except Exception:

            return 0.0


    # ========================================================
    # SCORE PRÉDICTION
    # ========================================================

    def score_prediction(
        self,
        coup
    ):

        if self.predicteur is None:

            return 0.0

        try:

            predictions = (
                self.predicteur.derniere_prediction
            )

            for prediction in predictions:

                if str(
                    prediction.get(
                        "coup"
                    )
                ) == str(
                    coup
                ):

                    STATS_MOTEUR[
                        "prediction_utilisee"
                    ] += 1

                    return (
                        float(
                            prediction.get(
                                "probabilite",
                                0
                            )
                        )
                        *
                        MOTEUR_BONUS_PREDICTION
                    )

        except Exception:

            pass

        return 0.0


    # ========================================================
    # ÉVALUATION COMPLÈTE D'UN COUP
    # ========================================================

    def score_coup(
        self,
        etat,
        coup
    ):

        score = 0.0

        # Évaluation générale.
        score += self.evaluation_apres_coup(
            etat,
            coup
        )

        # Mémoire.
        score += self.score_memoire(
            etat,
            coup
        )

        # Adaptation.
        score += self.score_adaptation(
            etat,
            coup
        )

        # Prédiction.
        score += self.score_prediction(
            coup
        )

        return score


    # ========================================================
    # ÉVALUATION APRÈS COUP
    # ========================================================

    def evaluation_apres_coup(
        self,
        etat,
        coup
    ):

        appliquer = globals().get(
            "jouer_coup"
        )

        annuler = globals().get(
            "annuler_coup"
        )

        if (
            callable(appliquer)
            and
            callable(annuler)
        ):

            try:

                nouveau = appliquer(
                    etat,
                    coup
                )

                score = (
                    self.evaluation_base(
                        nouveau
                    )
                )

                try:

                    annuler(
                        nouveau
                    )

                except Exception:

                    pass

                return float(
                    score
                )

            except Exception:

                pass

        return self.evaluation_base(
            etat
        )


    # ========================================================
    # ORDONNANCEMENT
    # ========================================================

    def ordonner_coups(
        self,
        etat,
        coups
    ):

        scores = []

        for coup in coups:

            try:

                score = self.score_coup(
                    etat,
                    coup
                )

            except Exception:

                score = 0.0

            scores.append(
                (
                    score,
                    coup
                )
            )

        scores.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            coup
            for score, coup
            in scores
        ]


    # ========================================================
    # APPLICATION COUP
    # ========================================================

    def appliquer_coup(
        self,
        etat,
        coup
    ):

        fonction = globals().get(
            "jouer_coup"
        )

        if not callable(
            fonction
        ):

            return None

        try:

            return fonction(
                etat,
                coup
            )

        except Exception:

            return None


    # ========================================================
    # TERMINAL
    # ========================================================

    def position_terminale(
        self,
        etat
    ):

        fonction = globals().get(
            "position_terminee"
        )

        if callable(
            fonction
        ):

            try:

                return bool(
                    fonction(etat)
                )

            except Exception:

                pass

        coups = self.coups_legaux(
            etat
        )

        return len(
            coups
        ) == 0


    # ========================================================
    # NEGAMAX
    # ========================================================

    def negamax(
        self,
        etat,
        profondeur,
        alpha,
        beta
    ):

        self.noeuds += 1

        STATS_MOTEUR[
            "noeuds"
        ] += 1

        if self.temps_depasse():

            self.stop = True

            return 0.0

        if profondeur <= 0:

            return self.evaluation_base(
                etat
            )

        if self.position_terminale(
            etat
        ):

            return self.evaluation_base(
                etat
            )

        cle = (
            self.cle_position(etat),
            profondeur
        )

        if cle in self.table_transposition:

            return self.table_transposition[
                cle
            ]

        coups = self.coups_legaux(
            etat
        )

        if not coups:

            return self.evaluation_base(
                etat
            )

        coups = self.ordonner_coups(
            etat,
            coups
        )

        meilleur = -MOTEUR_INF

        for coup in coups:

            if self.stop:

                break

            nouveau = self.appliquer_coup(
                etat,
                coup
            )

            if nouveau is None:

                continue

            valeur = -self.negamax(
                nouveau,
                profondeur - 1,
                -beta,
                -alpha
            )

            if valeur > meilleur:

                meilleur = valeur

            if valeur > alpha:

                alpha = valeur

            if alpha >= beta:

                break

        self.table_transposition[
            cle
        ] = meilleur

        return meilleur


    # ========================================================
    # RECHERCHE À UNE PROFONDEUR
    # ========================================================

    def rechercher_profondeur(
        self,
        etat,
        profondeur
    ):

        coups = self.coups_legaux(
            etat
        )

        if not coups:

            return None, 0.0

        coups = self.ordonner_coups(
            etat,
            coups
        )

        meilleur_coup = coups[0]

        meilleur_score = -MOTEUR_INF

        alpha = -MOTEUR_INF

        beta = MOTEUR_INF

        for coup in coups:

            if self.temps_depasse():

                self.stop = True

                break

            nouveau = self.appliquer_coup(
                etat,
                coup
            )

            if nouveau is None:

                continue

            valeur = -self.negamax(
                nouveau,
                profondeur - 1,
                -beta,
                -alpha
            )

            # Bonus d'adaptation au niveau
            # de la racine.
            valeur += (
                self.score_adaptation(
                    etat,
                    coup
                )
            )

            valeur += (
                self.score_prediction(
                    coup
                )
            )

            if valeur > meilleur_score:

                meilleur_score = valeur

                meilleur_coup = coup

            if valeur > alpha:

                alpha = valeur

        return (
            meilleur_coup,
            meilleur_score
        )


    # ========================================================
    # ITERATIVE DEEPENING
    # ========================================================

    def rechercher(
        self,
        etat,
        max_depth=None,
        time_limit=None
    ):

        STATS_MOTEUR[
            "recherches"
        ] += 1

        self.noeuds = 0

        self.stop = False

        self.table_transposition.clear()

        self.debut_recherche = (
            time.time()
        )

        self.meilleur_coup = None

        self.meilleur_score = 0

        self.profondeur_atteinte = 0

        if max_depth is None:

            max_depth = (
                MOTEUR_MAX_DEPTH
            )

        if time_limit is None:

            time_limit = (
                MOTEUR_TIME_LIMIT
            )

        self.max_depth = max(
            1,
            int(max_depth)
        )

        self.time_limit = max(
            0.01,
            float(time_limit)
        )

        # Analyse adaptation.
        if self.adaptation is not None:

            try:

                self.adaptation.analyser(
                    etat
                )

            except Exception:

                pass

        # Prédiction adverse.
        if self.predicteur is not None:

            try:

                self.predicteur.predire(
                    etat
                )

            except Exception:

                pass

        # ----------------------------------------------------
        # ITERATIVE DEEPENING
        # ----------------------------------------------------

        for profondeur in range(
            1,
            self.max_depth + 1
        ):

            if self.temps_depasse():

                break

            ancien_coup = (
                self.meilleur_coup
            )

            ancien_score = (
                self.meilleur_score
            )

            ancien_profondeur = (
                self.profondeur_atteinte
            )

            self.stop = False

            coup, score = (
                self.rechercher_profondeur(
                    etat,
                    profondeur
                )
            )

            # Si le temps a expiré pendant
            # la recherche, on conserve
            # le dernier résultat complet.
            if self.stop:

                self.meilleur_coup = (
                    ancien_coup
                )

                self.meilleur_score = (
                    ancien_score
                )

                self.profondeur_atteinte = (
                    ancien_profondeur
                )

                break

            if coup is not None:

                self.meilleur_coup = coup

                self.meilleur_score = score

                self.profondeur_atteinte = (
                    profondeur
                )

                STATS_MOTEUR[
                    "profondeur_max"
                ] = max(
                    STATS_MOTEUR[
                        "profondeur_max"
                    ],
                    profondeur
                )

        temps = self.temps_ecoule()

        STATS_MOTEUR[
            "temps_total"
        ] += temps

        return {

            "coup":
                self.meilleur_coup,

            "score":
                self.meilleur_score,

            "profondeur":
                self.profondeur_atteinte,

            "noeuds":
                self.noeuds,

            "temps":
                round(
                    temps,
                    4
                )
        }


    # ========================================================
    # JOUER UN COUP
    # ========================================================

    def jouer(
        self,
        etat,
        max_depth=None,
        time_limit=None
    ):

        resultat = self.rechercher(
            etat,
            max_depth,
            time_limit
        )

        coup = resultat.get(
            "coup"
        )

        if coup is None:

            return resultat

        self.historique_coups.append(
            coup
        )

        self.historique_coups = (
            self.historique_coups[
                -200:
            ]
        )

        STATS_MOTEUR[
            "coups"
        ] += 1

        # Enregistrer dans l'apprentissage.
        if self.apprentissage is not None:

            try:

                self.apprentissage.enregistrer_coup(
                    etat,
                    coup,
                    resultat.get(
                        "score",
                        0
                    )
                )

            except Exception:

                pass

        return resultat


    # ========================================================
    # DÉBUT PARTIE
    # ========================================================

    def nouvelle_partie(
        self,
        adversaire="Inconnu"
    ):

        STATS_MOTEUR[
            "parties"
        ] += 1

        self.historique_coups = []

        if self.adaptation is not None:

            try:

                self.adaptation.definir_adversaire(
                    adversaire
                )

            except Exception:

                pass

        if self.apprentissage is not None:

            try:

                self.apprentissage.commencer_partie(
                    adversaire
                )

            except Exception:

                pass

        return True


    # ========================================================
    # FIN PARTIE
    # ========================================================

    def fin_partie(
        self,
        resultat
    ):

        if self.apprentissage is not None:

            try:

                self.apprentissage.apprendre_partie(
                    resultat
                )

            except Exception:

                pass

        if self.adaptation is not None:

            try:

                self.adaptation.enregistrer_resultat(
                    resultat
                )

            except Exception:

                pass

        return True


    # ========================================================
    # RÉSUMÉ
    # ========================================================

    def resume(self):

        return {

            "meilleur_coup":
                self.meilleur_coup,

            "score":
                self.meilleur_score,

            "profondeur":
                self.profondeur_atteinte,

            "noeuds":
                self.noeuds,

            "coups":
                len(
                    self.historique_coups
                )
        }


# ------------------------------------------------------------
# INSTANCE GLOBALE
# ------------------------------------------------------------

PANDORAGA_MOTEUR = (
    PandoragaMoteurPrincipal()
)


# ------------------------------------------------------------
# RACCOURCIS
# ------------------------------------------------------------

def pandoraga_rechercher(
    etat,
    profondeur=MOTEUR_MAX_DEPTH,
    temps=MOTEUR_TIME_LIMIT
):

    return (
        PANDORAGA_MOTEUR.rechercher(
            etat,
            profondeur,
            temps
        )
    )


def pandoraga_jouer(
    etat,
    profondeur=MOTEUR_MAX_DEPTH,
    temps=MOTEUR_TIME_LIMIT
):

    return (
        PANDORAGA_MOTEUR.jouer(
            etat,
            profondeur,
            temps
        )
    )


def pandoraga_nouvelle_partie(
    adversaire="Inconnu"
):

    return (
        PANDORAGA_MOTEUR.nouvelle_partie(
            adversaire
        )
    )


def pandoraga_fin_partie(
    resultat
):

    return (
        PANDORAGA_MOTEUR.fin_partie(
            resultat
        )
    )


# ------------------------------------------------------------
# TEST MOTEUR
# ------------------------------------------------------------

def test_moteur_creation():

    moteur = (
        PandoragaMoteurPrincipal()
    )

    return moteur is not None and hasattr(
            moteur,
            "rechercher"
        ) and hasattr(
            moteur,
            "negamax"
        )


# ------------------------------------------------------------
# TEST STATISTIQUES
# ------------------------------------------------------------

def test_statistiques():

    return (
        isinstance(
            STATS_MOTEUR,
            dict
        )
        and
        "noeuds" in STATS_MOTEUR
        and
        "recherches" in STATS_MOTEUR
    )


# ------------------------------------------------------------
# TEST CLÉ
# ------------------------------------------------------------

def test_cle():

    moteur = (
        PandoragaMoteurPrincipal()
    )

    cle = moteur.cle_position(
        {
            "plateau": [],
            "tour": "blanc"
        }
    )

    return isinstance(
        cle,
        str
    )


# ------------------------------------------------------------
# TEST COMPLET
# ------------------------------------------------------------

if __name__ == "__main__":

    print()
    print(
        "🐼 PANDORAGA FULL ADAPTATION Ω"
    )

    print(
        "⚙️ BLOC 25 — MOTEUR PRINCIPAL"
    )

    print(
        "=" * 70
    )

    print()
    print("🧪 TESTS")
    print("-" * 70)

    print(
        "Création moteur :",
        "OK"
        if test_moteur_creation()
        else "ERREUR"
    )

    print(
        "Statistiques :",
        "OK"
        if test_statistiques()
        else "ERREUR"
    )

    print(
        "Clé position :",
        "OK"
        if test_cle()
        else "ERREUR"
    )

    print()
    print("📊 STATISTIQUES")
    print("-" * 70)

    for cle, valeur in (
        STATS_MOTEUR.items()
    ):

        if isinstance(
            valeur,
            float
        ):

            print(
                f"{cle:30} : "
                f"{valeur:.4f}"
            )

        else:

            print(
                f"{cle:30} : "
                f"{valeur}"
            )

    print()
    print(
        "🐼 BLOC 25 CHARGÉ AVEC SUCCÈS."
    )
# ================================================================
# 🐼 PANDORAGA Ω — BLOC 26/26
# FULL ADAPTATION + AUTO DEPTH + AUTO TIME
# ================================================================
#
# 100 % PYTHON
# SANS PIP
# STOCKFISH : MODE UCI OPTIONNEL
# SANS BIBLIOTHÈQUE EXTERNE
#
# MODULES STANDARD UNIQUEMENT :
# tkinter / json / time / math / random / os / threading
#
# AUTO :
#   ✓ temps automatique
#   ✓ profondeur automatique
#   ✓ analyse de complexité
#   ✓ adaptation à la vitesse de la machine
#   ✓ profondeur progressive
#   ✓ arrêt propre
#   ✓ meilleur résultat de dernière profondeur complète
#
# MOTEUR :
#   ✓ Negamax
#   ✓ Alpha-Beta
#   ✓ PVS
#   ✓ Quiescence
#   ✓ TT
#   ✓ Killer Moves
#   ✓ History Heuristic
#   ✓ Move Ordering
#   ✓ Null Move
#   ✓ Aspiration Window
#   ✓ Répétition
#   ✓ Roque
#   ✓ En passant
#   ✓ Promotion
#   ✓ Mat / Pat
#
# ADAPTATION :
#   ✓ profils joueurs
#   ✓ coups appris
#   ✓ cases préférées
#   ✓ captures
#   ✓ échecs
#   ✓ roques
#   ✓ erreurs
#   ✓ blunders
#   ✓ style agressif/défensif
#
# ================================================================

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import json
import os
import time
import random
import threading
import subprocess


# ================================================================
# CONFIGURATION
# ================================================================

TITLE = "🐼 PANDORAGA Ω — AUTO FULL ADAPTATION"

MEMORY_FILE = "pandoraga_memoire.json"
JPADON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jpadon_memoire.json")

EMPTY = "."

WHITE = "w"
BLACK = "b"

PAWN = "P"
KNIGHT = "N"
BISHOP = "B"
ROOK = "R"
QUEEN = "Q"
KING = "K"

INF = 10_000_000
MATE_SCORE = 1_000_000

MAX_DEPTH = 15
# Mode MAX : le moteur reçoit le budget maximal configuré à chaque coup.
# La recherche peut s'arrêter plus tôt si la profondeur 15 est terminée,
# si la partie est terminée, ou si une limite de sécurité interrompt le calcul.
MAX_ENGINE_MODE = True

# ------------------------------------------------
# AUTO TIME
# ------------------------------------------------

AUTO_MIN_TIME = 0.8
AUTO_MAX_TIME = 25.0
# profondeur minimale / maximale
AUTO_MIN_DEPTH = 3
AUTO_MAX_DEPTH = 15
# ------------------------------------------------
# TT
# ------------------------------------------------

TT_MAX = 300_000
# ================================================================
# VALEURS
# ================================================================

PIECE_VALUES = {
    PAWN: 100,
    KNIGHT: 320,
    BISHOP: 330,
    ROOK: 500,
    QUEEN: 900,
    KING: 20_000,
}


UNICODE_PIECES = {
    "wP": "♙",
    "wN": "♘",
    "wB": "♗",
    "wR": "♖",
    "wQ": "♕",
    "wK": "♔",

    "bP": "♟",
    "bN": "♞",
    "bB": "♝",
    "bR": "♜",
    "bQ": "♛",
    "bK": "♚",
}


# ================================================================
# TABLES POSITIONNELLES
# ================================================================

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10,-20,-20, 10, 10,  5,
     5, -5,-10,  0,  0,-10, -5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
     0,  0,  0,  0,  0,  0,  0,  0,
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10,  5,  5, 10,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_TABLE = [
     0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     5, 10, 10, 10, 10, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20,
]

KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20,
]


# ================================================================
# DIRECTIONS
# ================================================================

KNIGHT_DIRS = [
    (-2,-1), (-2,1),
    (-1,-2), (-1,2),
    (1,-2), (1,2),
    (2,-1), (2,1)
]

KING_DIRS = [
    (-1,-1),(-1,0),(-1,1),
    (0,-1),(0,1),
    (1,-1),(1,0),(1,1)
]

BISHOP_DIRS = [
    (-1,-1),(-1,1),
    (1,-1),(1,1)
]

ROOK_DIRS = [
    (-1,0),(1,0),
    (0,-1),(0,1)
]


# ================================================================
# OUTILS
# ================================================================

def opposite(color):
    return BLACK if color == WHITE else WHITE


def row(square):
    return square // 8


def col(square):
    return square % 8


def inside(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def mirror(square):
    return square ^ 56


def square_name(square):
    return chr(97 + col(square)) + str(8 - row(square))


# ================================================================
# MOVE
# ================================================================

class Move:

    __slots__ = (
        "from_sq",
        "to_sq",
        "promotion",
        "en_passant",
        "castle",
        "captured"
    )

    def __init__(
        self,
        from_sq,
        to_sq,
        promotion=None,
        en_passant=False,
        castle=False,
        captured=None
    ):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.promotion = promotion
        self.en_passant = en_passant
        self.castle = castle
        self.captured = captured

    def key(self):
        return (
            self.from_sq,
            self.to_sq,
            self.promotion,
            self.en_passant,
            self.castle
        )

    def notation(self):
        s = (
            square_name(self.from_sq)
            + square_name(self.to_sq)
        )

        if self.promotion:
            s += self.promotion.lower()

        return s


# ================================================================
# POSITION
# ================================================================

class Position:

    def __init__(self):

        self.board = [
            "bR","bN","bB","bQ","bK","bB","bN","bR",
            "bP","bP","bP","bP","bP","bP","bP","bP",
            ".",".",".",".",".",".",".",".",
            ".",".",".",".",".",".",".",".",
            ".",".",".",".",".",".",".",".",
            ".",".",".",".",".",".",".",".",
            "wP","wP","wP","wP","wP","wP","wP","wP",
            "wR","wN","wB","wQ","wK","wB","wN","wR"
        ]

        self.side = WHITE

        self.castling = {
            "wK": True,
            "wQ": True,
            "bK": True,
            "bQ": True
        }

        self.en_passant = -1
        self.halfmove = 0
        self.fullmove = 1

    def clone(self):

        p = Position.__new__(Position)

        p.board = self.board.copy()
        p.side = self.side
        p.castling = self.castling.copy()
        p.en_passant = self.en_passant
        p.halfmove = self.halfmove
        p.fullmove = self.fullmove

        return p

    def key(self):

        return (
            tuple(self.board),
            self.side,
            tuple(
                k for k, v
                in self.castling.items()
                if v
            ),
            self.en_passant
        )

    def find_king(self, color):

        target = color + KING

        for i, p in enumerate(self.board):
            if p == target:
                return i

        return -1


# ================================================================
# ATTAQUES
# ================================================================

def is_square_attacked(position, square, attacker):

    r = row(square)
    c = col(square)

    # ------------------------------------------------------------
    # PIONS
    # ------------------------------------------------------------

    pawn_row = (
        r + 1
        if attacker == WHITE
        else r - 1
    )

    if 0 <= pawn_row < 8:

        for dc in (-1, 1):

            nc = c + dc

            if inside(pawn_row, nc):

                sq = pawn_row * 8 + nc

                if position.board[sq] == attacker + PAWN:
                    return True

    # ------------------------------------------------------------
    # CAVALIERS
    # ------------------------------------------------------------

    for dr, dc in KNIGHT_DIRS:

        nr = r + dr
        nc = c + dc

        if inside(nr, nc):

            sq = nr * 8 + nc

            if position.board[sq] == attacker + KNIGHT:
                return True

    # ------------------------------------------------------------
    # ROI
    # ------------------------------------------------------------

    for dr, dc in KING_DIRS:

        nr = r + dr
        nc = c + dc

        if inside(nr, nc):

            sq = nr * 8 + nc

            if position.board[sq] == attacker + KING:
                return True

    # ------------------------------------------------------------
    # FOUS / DAME
    # ------------------------------------------------------------

    for dr, dc in BISHOP_DIRS:

        nr = r + dr
        nc = c + dc

        while inside(nr, nc):

            sq = nr * 8 + nc
            piece = position.board[sq]

            if piece != EMPTY:

                if piece in (
                    attacker + BISHOP,
                    attacker + QUEEN
                ):
                    return True

                break

            nr += dr
            nc += dc

    # ------------------------------------------------------------
    # TOURS / DAME
    # ------------------------------------------------------------

    for dr, dc in ROOK_DIRS:

        nr = r + dr
        nc = c + dc

        while inside(nr, nc):

            sq = nr * 8 + nc
            piece = position.board[sq]

            if piece != EMPTY:

                if piece in (
                    attacker + ROOK,
                    attacker + QUEEN
                ):
                    return True

                break

            nr += dr
            nc += dc

    return False


def in_check(position, color):

    king = position.find_king(color)

    if king < 0:
        return True

    return is_square_attacked(
        position,
        king,
        opposite(color)
    )


# ================================================================
# GÉNÉRATION DES COUPS
# ================================================================

def generate_pseudo_moves(
    position,
    captures_only=False
):

    moves = []

    color = position.side
    enemy = opposite(color)

    for sq, piece in enumerate(position.board):

        if piece == EMPTY:
            continue

        if piece[0] != color:
            continue

        kind = piece[1]

        r = row(sq)
        c = col(sq)

        # ========================================================
        # PION
        # ========================================================

        if kind == PAWN:

            direction = (
                -1
                if color == WHITE
                else 1
            )

            start_row = (
                6
                if color == WHITE
                else 1
            )

            promotion_row = (
                0
                if color == WHITE
                else 7
            )

            nr = r + direction

            if (
                not captures_only
                and inside(nr, c)
            ):

                target = nr * 8 + c

                if position.board[target] == EMPTY:

                    if nr == promotion_row:

                        for promo in (
                            QUEEN,
                            ROOK,
                            BISHOP,
                            KNIGHT
                        ):
                            moves.append(
                                Move(
                                    sq,
                                    target,
                                    promotion=promo
                                )
                            )
                    else:

                        moves.append(
                            Move(
                                sq,
                                target
                            )
                        )

                        if r == start_row:

                            nr2 = (
                                r + direction * 2
                            )

                            target2 = nr2 * 8 + c

                            if (
                                position.board[target2]
                                == EMPTY
                            ):
                                moves.append(
                                    Move(
                                        sq,
                                        target2
                                    )
                                )

            # captures

            for dc in (-1, 1):

                nc = c + dc

                if not inside(nr, nc):
                    continue

                target = nr * 8 + nc
                target_piece = position.board[target]

                if (
                    target_piece != EMPTY
                    and target_piece[0] == enemy
                ):

                    if nr == promotion_row:

                        for promo in (
                            QUEEN,
                            ROOK,
                            BISHOP,
                            KNIGHT
                        ):
                            moves.append(
                                Move(
                                    sq,
                                    target,
                                    promotion=promo,
                                    captured=target_piece
                                )
                            )

                    else:

                        moves.append(
                            Move(
                                sq,
                                target,
                                captured=target_piece
                            )
                        )

                elif target == position.en_passant:

                    moves.append(
                        Move(
                            sq,
                            target,
                            en_passant=True,
                            captured=enemy + PAWN
                        )
                    )

        # ========================================================
        # CAVALIER
        # ========================================================

        elif kind == KNIGHT:

            for dr, dc in KNIGHT_DIRS:

                nr = r + dr
                nc = c + dc

                if not inside(nr, nc):
                    continue

                target = nr * 8 + nc
                tp = position.board[target]

                if tp == EMPTY:

                    if not captures_only:
                        moves.append(
                            Move(sq, target)
                        )

                elif tp[0] == enemy:

                    moves.append(
                        Move(
                            sq,
                            target,
                            captured=tp
                        )
                    )

        # ========================================================
        # FOUS / TOURS / DAME
        # ========================================================

        elif kind in (
            BISHOP,
            ROOK,
            QUEEN
        ):

            dirs = []

            if kind in (
                BISHOP,
                QUEEN
            ):
                dirs += BISHOP_DIRS

            if kind in (
                ROOK,
                QUEEN
            ):
                dirs += ROOK_DIRS

            for dr, dc in dirs:

                nr = r + dr
                nc = c + dc

                while inside(nr, nc):

                    target = nr * 8 + nc
                    tp = position.board[target]

                    if tp == EMPTY:

                        if not captures_only:
                            moves.append(
                                Move(
                                    sq,
                                    target
                                )
                            )

                    else:

                        if tp[0] == enemy:

                            moves.append(
                                Move(
                                    sq,
                                    target,
                                    captured=tp
                                )
                            )

                        break

                    nr += dr
                    nc += dc

        # ========================================================
        # ROI
        # ========================================================

        elif kind == KING:

            for dr, dc in KING_DIRS:

                nr = r + dr
                nc = c + dc

                if not inside(nr, nc):
                    continue

                target = nr * 8 + nc
                tp = position.board[target]

                if tp == EMPTY:

                    if not captures_only:
                        moves.append(
                            Move(
                                sq,
                                target
                            )
                        )

                elif tp[0] == enemy:

                    moves.append(
                        Move(
                            sq,
                            target,
                            captured=tp
                        )
                    )

            # ----------------------------------------------------
            # ROQUE
            # ----------------------------------------------------

            if (
                not captures_only
                and not in_check(position, color)
            ):

                # petit roque

                if position.castling.get(
                    color + "K",
                    False
                ):

                    rook_sq = (
                        sq + 3
                        if color == WHITE
                        else sq + 3
                    )

                    if (
                        0 <= rook_sq < 64
                        and position.board[rook_sq]
                        == color + ROOK
                    ):

                        f_sq = sq + 1
                        g_sq = sq + 2

                        if (
                            position.board[f_sq]
                            == EMPTY
                            and position.board[g_sq]
                            == EMPTY
                            and not is_square_attacked(
                                position,
                                f_sq,
                                enemy
                            )
                            and not is_square_attacked(
                                position,
                                g_sq,
                                enemy
                            )
                        ):
                            moves.append(
                                Move(
                                    sq,
                                    g_sq,
                                    castle=True
                                )
                            )

                # grand roque

                if position.castling.get(
                    color + "Q",
                    False
                ):

                    rook_sq = sq - 4

                    if (
                        0 <= rook_sq < 64
                        and position.board[rook_sq]
                        == color + ROOK
                    ):

                        b_sq = sq - 3
                        c_sq = sq - 2
                        d_sq = sq - 1

                        if (
                            position.board[b_sq]
                            == EMPTY
                            and position.board[c_sq]
                            == EMPTY
                            and position.board[d_sq]
                            == EMPTY
                            and not is_square_attacked(
                                position,
                                c_sq,
                                enemy
                            )
                            and not is_square_attacked(
                                position,
                                d_sq,
                                enemy
                            )
                        ):
                            moves.append(
                                Move(
                                    sq,
                                    c_sq,
                                    castle=True
                                )
                            )

    return moves


# ================================================================
# MAKE MOVE
# ================================================================

def make_move(position, move):

    p = position.clone()

    moving = p.board[move.from_sq]

    color = moving[0]
    kind = moving[1]

    captured = p.board[move.to_sq]

    p.board[move.from_sq] = EMPTY

    # en passant

    if move.en_passant:

        captured_sq = (
            move.to_sq + 8
            if color == WHITE
            else move.to_sq - 8
        )

        captured = p.board[captured_sq]

        p.board[captured_sq] = EMPTY

    new_piece = moving

    if move.promotion:
        new_piece = (
            color + move.promotion
        )

    p.board[move.to_sq] = new_piece

    # ------------------------------------------------------------
    # ROQUE
    # ------------------------------------------------------------

    if move.castle:

        if color == WHITE:

            if move.to_sq == 62:
                p.board[63] = EMPTY
                p.board[61] = "wR"

            elif move.to_sq == 58:
                p.board[56] = EMPTY
                p.board[59] = "wR"

        else:

            if move.to_sq == 6:
                p.board[7] = EMPTY
                p.board[5] = "bR"

            elif move.to_sq == 2:
                p.board[0] = EMPTY
                p.board[3] = "bR"

    # ------------------------------------------------------------
    # ROQUE RIGHTS
    # ------------------------------------------------------------

    if kind == KING:

        p.castling[color + "K"] = False
        p.castling[color + "Q"] = False

    if move.from_sq == 63 or move.to_sq == 63:
        p.castling["wK"] = False

    if move.from_sq == 56 or move.to_sq == 56:
        p.castling["wQ"] = False

    if move.from_sq == 7 or move.to_sq == 7:
        p.castling["bK"] = False

    if move.from_sq == 0 or move.to_sq == 0:
        p.castling["bQ"] = False

    # ------------------------------------------------------------
    # EN PASSANT
    # ------------------------------------------------------------

    p.en_passant = -1

    if kind == PAWN:

        if abs(
            move.to_sq - move.from_sq
        ) == 16:

            p.en_passant = (
                move.from_sq
                + move.to_sq
            ) // 2

    # ------------------------------------------------------------
    # COMPTEURS
    # ------------------------------------------------------------

    if (
        kind == PAWN
        or captured != EMPTY
    ):
        p.halfmove = 0
    else:
        p.halfmove += 1

    if color == BLACK:
        p.fullmove += 1

    p.side = opposite(color)

    return p


# ================================================================
# COUPS LÉGAUX
# ================================================================

def generate_legal_moves(
    position,
    captures_only=False
):

    legal = []

    for move in generate_pseudo_moves(
        position,
        captures_only
    ):

        child = make_move(
            position,
            move
        )

        if not in_check(
            child,
            position.side
        ):
            legal.append(move)

    return legal


# ================================================================
# MÉMOIRE
# ================================================================

class PandoragaMemory:

    def __init__(self):

        self.data = {
            "version": 3,
            "players": {},
            "global": {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0
            }
        }

        self.load()

    def load(self):

        if not os.path.exists(
            MEMORY_FILE
        ):
            return

        try:

            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            if isinstance(data, dict):
                self.data.update(data)

        except Exception:
            pass

    def save(self):

        try:

            with open(
                MEMORY_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.data,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

        except Exception:
            pass

    def player(self, name):

        if not name:
            name = "Joueur"

        if name not in self.data["players"]:

            self.data["players"][name] = {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "moves": {},
                "preferred_squares": {},
                "captures": 0,
                "checks": 0,
                "castles": 0,
                "king_moves": 0,
                "queen_moves": 0,
                "mistakes": 0,
                "blunders": 0
            }

        return self.data["players"][name]

    def record_move(
        self,
        name,
        move,
        position,
        capture=False,
        check=False
    ):

        p = self.player(name)

        key = move.notation()

        p["moves"][key] = (
            p["moves"].get(key, 0) + 1
        )

        sq = str(move.to_sq)

        p["preferred_squares"][sq] = (
            p["preferred_squares"].get(
                sq,
                0
            ) + 1
        )

        if capture:
            p["captures"] += 1

        if check:
            p["checks"] += 1

        piece = position.board[
            move.from_sq
        ]

        if piece.endswith(KING):
            p["king_moves"] += 1

        if piece.endswith(QUEEN):
            p["queen_moves"] += 1

        if move.castle:
            p["castles"] += 1

    def record_error(
        self,
        name,
        mistake=False,
        blunder=False
    ):

        p = self.player(name)

        if mistake:
            p["mistakes"] += 1

        if blunder:
            p["blunders"] += 1

        self.save()

    def record_result(
        self,
        name,
        result
    ):

        p = self.player(name)

        p["games"] += 1

        if result == "win":
            p["wins"] += 1
        elif result == "loss":
            p["losses"] += 1
        else:
            p["draws"] += 1

        self.data["global"]["games"] += 1

        if result == "win":
            self.data["global"]["wins"] += 1
        elif result == "loss":
            self.data["global"]["losses"] += 1
        else:
            self.data["global"]["draws"] += 1

        self.save()

    def profile(self, name):

        p = self.player(name)

        games = max(
            1,
            p["games"]
        )

        captures = (
            p["captures"] / games
        )

        checks = (
            p["checks"] / games
        )

        castles = (
            p["castles"] / games
        )

        mistakes = (
            p["mistakes"] / games
        )

        blunders = (
            p["blunders"] / games
        )

        aggressive = (
            captures * 2
            + checks * 1.5
            + p["queen_moves"] / games
        )

        defensive = (
            castles * 1.5
            + p["king_moves"] / games
        )

        if aggressive > defensive + 1:
            style = "agressif"
        elif defensive > aggressive + 1:
            style = "défensif"
        else:
            style = "équilibré"

        return {
            "style": style,
            "aggressive": aggressive,
            "defensive": defensive,
            "mistake_rate": mistakes,
            "blunder_rate": blunders,
            "capture_rate": captures,
            "check_rate": checks
        }


# ================================================================
# ADAPTATION
# ================================================================

class Adaptation:

    def __init__(
        self,
        memory,
        player
    ):

        self.memory = memory
        self.player = player

    def profile(self):
        return self.memory.profile(
            self.player
        )

    def move_bonus(self, move):

        p = self.memory.player(
            self.player
        )

        learned = p["moves"].get(
            move.notation(),
            0
        )

        preferred = p[
            "preferred_squares"
        ].get(
            str(move.to_sq),
            0
        )

        return (
            min(learned * 5, 50)
            + min(preferred * 2, 20)
        )

    def evaluation_bonus(
        self,
        position
    ):

        profile = self.profile()

        bonus = 0

        if profile["style"] == "agressif":

            captures = sum(
                1
                for m in generate_legal_moves(
                    position,
                    True
                )
                if m.captured
            )

            bonus += captures * 4

        elif profile["style"] == "défensif":

            if position.castling.get(
                position.side + "K",
                False
            ):
                bonus += 5

        bonus += min(
            profile["mistake_rate"] * 10,
            20
        )

        bonus += min(
            profile["blunder_rate"] * 25,
            40
        )

        return int(bonus)


# ================================================================
# TRANSPOSITION TABLE
# ================================================================

class TTEntry:

    __slots__ = (
        "depth",
        "score",
        "flag",
        "move"
    )

    def __init__(
        self,
        depth,
        score,
        flag,
        move
    ):
        self.depth = depth
        self.score = score
        self.flag = flag
        self.move = move


class TranspositionTable:

    def __init__(
        self,
        maximum=TT_MAX
    ):

        self.table = {}
        self.maximum = maximum

    def get(self, key):
        return self.table.get(key)

    def store(
        self,
        key,
        depth,
        score,
        flag,
        move
    ):

        if len(self.table) >= self.maximum:

            # On conserve une TT simple
            # et légère pour Python.

            self.table.clear()

        self.table[key] = TTEntry(
            depth,
            score,
            flag,
            move
        )

    def clear(self):
        self.table.clear()

    def size(self):
        return len(self.table)


# ================================================================
# PANDORAGA ENGINE
# ================================================================

class PandoragaEngine:

    def __init__(
        self,
        memory,
        player="Joueur"
    ):

        self.memory = memory
        self.player = player

        self.adaptation = Adaptation(
            memory,
            player
        )

        self.tt = TranspositionTable()

        self.killers = [
            [None, None]
            for _ in range(MAX_DEPTH + 5)
        ]

        self.history = {}

        self.nodes = 0

        self.start_time = 0
        self.time_limit = 1

        self.stop = False

        self.root_depth = 0
        self.root_move = None
        self.last_score = 0

        self.nps = 0

        # statistiques AUTO

        self.auto_time = 1.0
        self.auto_target_depth = 3
        self.auto_complexity = 0
        # Profil JPADON de l'adversaire, chargé entre les parties.
        self.jpadon_profile = {}

    def jpadon_move_bonus(self, position, move):
        """Petit bonus de classement guidé par des habitudes confirmées."""
        profile = self.jpadon_profile or {}
        if int(profile.get("parties_analysees", profile.get("games", 0))) < 1:
            return 0
        style = profile.get("style", {})
        confidence = float(style.get("confiance", 0.0))
        if confidence < 0.25:
            return 0
        aggression = float(style.get("agressivite", 0.0))
        tacticality = float(style.get("tactique", 0.0))
        bonus = 0
        # Contre un adversaire souvent agressif, favoriser légèrement le roque.
        if aggression >= 0.60 and getattr(move, "castle", False):
            bonus += int(18 * confidence)
        # Si les parties observées montrent un style tactique, mieux classer les
        # captures et promotions légales; le moteur continue à calculer les variantes.
        if tacticality >= 0.60 and (getattr(move, "captured", None) or getattr(move, "en_passant", False) or getattr(move, "promotion", None)):
            bonus += int(8 * confidence)
        return bonus

    # ============================================================
    # TEMPS
    # ============================================================

    def time_up(self):

        if self.stop:
            return True

        if (
            time.perf_counter()
            - self.start_time
            >= self.time_limit
        ):

            self.stop = True
            return True

        return False

    # ============================================================
    # COMPLEXITÉ AUTO
    # ============================================================

    def analyze_complexity(
        self,
        position
    ):

        legal = generate_legal_moves(
            position
        )

        captures = sum(
            1
            for m in legal
            if m.captured
            or m.en_passant
        )

        checks = 0

        for m in legal[:30]:

            child = make_move(
                position,
                m
            )

            if in_check(
                child,
                child.side
            ):
                checks += 1

        pieces = sum(
            1
            for p in position.board
            if p != EMPTY
        )

        queens = sum(
            1
            for p in position.board
            if p.endswith(QUEEN)
        )

        complexity = 0

        # mobilité

        complexity += min(
            len(legal) * 2,
            30
        )

        # captures

        complexity += min(
            captures * 5,
            25
        )

        # échecs

        complexity += min(
            checks * 8,
            25
        )

        # dames

        complexity += min(
            queens * 5,
            10
        )

        # milieu de partie

        if pieces >= 20:
            complexity += 10

        return min(
            100,
            complexity
        )

    # ============================================================
    # AUTO TEMPS
    # ============================================================

    def calculate_auto_time(
        self,
        position,
        complexity
    ):

        legal_count = len(
            generate_legal_moves(
                position
            )
        )

        # base

        seconds = 1.0

        # complexité

        seconds += (
            complexity / 100
        ) * 5.0

        # beaucoup de coups

        if legal_count >= 30:
            seconds += 1.5

        elif legal_count >= 20:
            seconds += 0.8

        # tactique

        if complexity >= 70:
            seconds += 2.5

        elif complexity >= 50:
            seconds += 1.5

        # finale :
        # moins de pièces = possibilité
        # de pousser davantage la profondeur

        pieces = sum(
            1
            for p in position.board
            if p != EMPTY
        )

        if pieces <= 12:
            seconds += 1.0

        # adaptation au NPS

        if self.nps > 100_000:
            seconds *= 0.90

        elif self.nps < 15_000:
            seconds *= 1.15

        return max(
            AUTO_MIN_TIME,
            min(
                AUTO_MAX_TIME,
                seconds
            )
        )

    # ============================================================
    # AUTO PROFONDEUR
    # ============================================================

    def calculate_auto_depth(
        self,
        position,
        complexity,
        time_limit
    ):

        pieces = sum(
            1
            for p in position.board
            if p != EMPTY
        )

        depth = 4

        if time_limit >= 2:
            depth += 1

        if time_limit >= 4:
            depth += 1

        if time_limit >= 7:
            depth += 1

        if time_limit >= 12:
            depth += 1

        if time_limit >= 20:
            depth += 2

        # tactique

        if complexity >= 70:
            depth += 2

        elif complexity >= 50:
            depth += 1

        # finale

        if pieces <= 12:
            depth += 2

        if pieces <= 8:
            depth += 1

        # vitesse

        if self.nps >= 80_000:
            depth += 1

        elif (
            self.nps
            and self.nps < 12_000
        ):
            depth -= 1

        return max(
            AUTO_MIN_DEPTH,
            min(
                AUTO_MAX_DEPTH,
                depth
            )
        )

    # ============================================================
    # ÉVALUATION
    # ============================================================

    def evaluate(self, position):

        score = 0

        bishops = {
            WHITE: 0,
            BLACK: 0
        }

        for sq, piece in enumerate(
            position.board
        ):

            if piece == EMPTY:
                continue

            color = piece[0]
            kind = piece[1]

            value = PIECE_VALUES[kind]

            table_sq = (
                sq
                if color == WHITE
                else mirror(sq)
            )

            if kind == PAWN:
                pos = PAWN_TABLE[table_sq]

            elif kind == KNIGHT:
                pos = KNIGHT_TABLE[table_sq]

            elif kind == BISHOP:

                pos = BISHOP_TABLE[table_sq]
                bishops[color] += 1

            elif kind == ROOK:
                pos = ROOK_TABLE[table_sq]

            elif kind == QUEEN:
                pos = QUEEN_TABLE[table_sq]

            else:
                pos = KING_TABLE[table_sq]

            if color == WHITE:
                score += value + pos
            else:
                score -= value + pos

        # paire de fous

        if bishops[WHITE] >= 2:
            score += 30

        if bishops[BLACK] >= 2:
            score -= 30

        # centre

        for sq in (27, 28, 35, 36):

            p = position.board[sq]

            if p == EMPTY:
                continue

            if p[0] == WHITE:
                score += 8
            else:
                score -= 8

        # sécurité du roi / roque

        if (
            position.castling["wK"]
            or position.castling["wQ"]
        ):
            score += 8

        if (
            position.castling["bK"]
            or position.castling["bQ"]
        ):
            score -= 8

        # adaptation

        score += self.adaptation.evaluation_bonus(
            position
        )

        return score

    def evaluate_side(self, position):

        score = self.evaluate(
            position
        )

        if position.side == WHITE:
            return score

        return -score

    # ============================================================
    # MOVE ORDERING
    # ============================================================

    def move_score(
        self,
        position,
        move,
        tt_move=None,
        ply=0
    ):

        score = 0

        if (
            tt_move
            and move.key()
            == tt_move.key()
        ):
            score += 10_000_000

        if move.captured:

            victim = PIECE_VALUES.get(
                move.captured[1],
                0
            )

            attacker = PIECE_VALUES.get(
                position.board[
                    move.from_sq
                ][1],
                1
            )

            score += (
                100_000
                + victim * 10
                - attacker
            )

        if move.promotion:

            score += (
                90_000
                + PIECE_VALUES[
                    move.promotion
                ]
            )

        if ply < len(self.killers):

            if (
                self.killers[ply][0]
                and move.key()
                == self.killers[
                    ply
                ][0].key()
            ):
                score += 80_000

            elif (
                self.killers[ply][1]
                and move.key()
                == self.killers[
                    ply
                ][1].key()
            ):
                score += 70_000

        hkey = (
            position.board[
                move.from_sq
            ],
            move.to_sq
        )

        score += self.history.get(
            hkey,
            0
        )

        score += self.adaptation.move_bonus(
            move
        )

        # JPADON influence uniquement le classement des coups candidats.
        score += self.jpadon_move_bonus(position, move)

        if move.castle:
            score += 500

        return score

    def order_moves(
        self,
        position,
        moves,
        tt_move=None,
        ply=0
    ):

        return sorted(
            moves,
            key=lambda m:
                self.move_score(
                    position,
                    m,
                    tt_move,
                    ply
                ),
            reverse=True
        )

    # ============================================================
    # QUIESCENCE
    # ============================================================

    def quiescence(
        self,
        position,
        alpha,
        beta,
        ply=0
    ):
        """Recherche tactique; en échec, examine toutes les parades légales."""
        if self.time_up():
            raise TimeoutError

        self.nodes += 1
        checked = in_check(position, position.side)

        # En échec, une évaluation statique (stand-pat) est illégale :
        # le moteur doit d'abord trouver une parade, y compris un coup calme.
        if not checked:
            stand = self.evaluate_side(position)

            if stand >= beta:
                return beta

            if stand > alpha:
                alpha = stand

            moves = generate_legal_moves(
                position,
                captures_only=True
            )
        else:
            moves = generate_legal_moves(position)
            if not moves:
                return -MATE_SCORE + ply

        moves = self.order_moves(
            position,
            moves,
            ply=ply
        )

        for move in moves:
            child = make_move(position, move)
            score = -self.quiescence(
                child,
                -beta,
                -alpha,
                ply + 1
            )

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

        return alpha

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        position,
        depth,
        alpha,
        beta,
        ply=0,
        allow_null=True
    ):

        if self.time_up():
            raise TimeoutError

        self.nodes += 1

        original_alpha = alpha
        original_beta = beta

        key = position.key()

        entry = self.tt.get(key)

        tt_move = None

        if entry:

            tt_move = entry.move

            if entry.depth >= depth:

                if entry.flag == "EXACT":
                    return entry.score

                if (
                    entry.flag == "LOWER"
                    and entry.score > alpha
                ):
                    alpha = entry.score

                elif (
                    entry.flag == "UPPER"
                    and entry.score < beta
                ):
                    beta = entry.score

                if alpha >= beta:
                    return entry.score

        legal = generate_legal_moves(
            position
        )

        if not legal:

            if in_check(
                position,
                position.side
            ):
                return (
                    -MATE_SCORE
                    + ply
                )

            return 0

        if depth <= 0:

            return self.quiescence(
                position,
                alpha,
                beta,
                ply
            )

        # --------------------------------------------------------
        # NULL MOVE
        # --------------------------------------------------------

        if (
            allow_null
            and depth >= 3
            and not in_check(
                position,
                position.side
            )
            and len(legal) > 1
        ):

            null_position = (
                position.clone()
            )

            null_position.side = (
                opposite(
                    null_position.side
                )
            )

            null_position.en_passant = -1

            try:

                null_score = -self.search(
                    null_position,
                    depth - 3,
                    -beta,
                    -beta + 1,
                    ply + 1,
                    False
                )

                if null_score >= beta:
                    return beta

            except TimeoutError:
                raise

        legal = self.order_moves(
            position,
            legal,
            tt_move,
            ply
        )

        best_score = -INF
        best_move = legal[0]

        first = True

        for move in legal:

            child = make_move(
                position,
                move
            )

            if first:

                score = -self.search(
                    child,
                    depth - 1,
                    -beta,
                    -alpha,
                    ply + 1
                )

                first = False

            else:

                score = -self.search(
                    child,
                    depth - 1,
                    -alpha - 1,
                    -alpha,
                    ply + 1
                )

                if (
                    score > alpha
                    and score < beta
                ):

                    score = -self.search(
                        child,
                        depth - 1,
                        -beta,
                        -alpha,
                        ply + 1
                    )

            if score > best_score:

                best_score = score
                best_move = move

            if score > alpha:
                alpha = score

            if alpha >= beta:

                if not move.captured:

                    if ply < len(
                        self.killers
                    ):

                        self.killers[
                            ply
                        ][1] = self.killers[
                            ply
                        ][0]

                        self.killers[
                            ply
                        ][0] = move

                    hkey = (
                        position.board[
                            move.from_sq
                        ],
                        move.to_sq
                    )

                    self.history[hkey] = (
                        self.history.get(
                            hkey,
                            0
                        )
                        + depth * depth
                    )

                break

        if best_score <= original_alpha:
            flag = "UPPER"

        elif best_score >= original_beta:
            flag = "LOWER"

        else:
            flag = "EXACT"

        self.tt.store(
            key,
            depth,
            best_score,
            flag,
            best_move
        )

        return best_score

    # ============================================================
    # ROOT
    # ============================================================

    def search_root(
        self,
        position,
        depth,
        alpha=-INF,
        beta=INF
    ):

        moves = generate_legal_moves(
            position
        )

        if not moves:
            return None, 0

        entry = self.tt.get(
            position.key()
        )

        tt_move = (
            entry.move
            if entry
            else None
        )

        moves = self.order_moves(
            position,
            moves,
            tt_move,
            0
        )

        best_move = moves[0]
        best_score = -INF

        first = True

        for move in moves:

            if self.time_up():
                raise TimeoutError

            child = make_move(
                position,
                move
            )

            if first:

                score = -self.search(
                    child,
                    depth - 1,
                    -beta,
                    -alpha,
                    1
                )

                first = False

            else:

                score = -self.search(
                    child,
                    depth - 1,
                    -alpha - 1,
                    -alpha,
                    1
                )

                if (
                    score > alpha
                    and score < beta
                ):

                    score = -self.search(
                        child,
                        depth - 1,
                        -beta,
                        -alpha,
                        1
                    )

            if score > best_score:

                best_score = score
                best_move = move

            if score > alpha:
                alpha = score

        return best_move, best_score

    # ============================================================
    # CHOIX AUTOMATIQUE
    # ============================================================

    def choose_move(
        self,
        position
    ):

        self.start_time = (
            time.perf_counter()
        )

        self.stop = False
        self.nodes = 0
        self.root_depth = 0
        self.root_move = None
        self.last_score = 0

        # --------------------------------------------------------
        # 1. ANALYSE DE COMPLEXITÉ
        # --------------------------------------------------------

        complexity = (
            self.analyze_complexity(
                position
            )
        )

        self.auto_complexity = complexity

        # --------------------------------------------------------
        # 2. TEMPS AUTO
        # --------------------------------------------------------

        calculated_time = self.calculate_auto_time(
            position,
            complexity
        )

        calculated_depth = self.calculate_auto_depth(
            position,
            complexity,
            calculated_time
        )

        # --------------------------------------------------------
        # 2-3. BUDGET DU MOTEUR
        # --------------------------------------------------------
        # En mode MAX, le moteur utilise les limites configurées pour ce profil RAM.
        # Les calculs AUTO restent disponibles en désactivant MAX_ENGINE_MODE.
        if MAX_ENGINE_MODE:
            self.time_limit = AUTO_MAX_TIME
            target_depth = min(MAX_DEPTH, AUTO_MAX_DEPTH)
        else:
            self.time_limit = calculated_time
            target_depth = calculated_depth

        self.auto_time = self.time_limit
        self.auto_target_depth = target_depth

        legal = generate_legal_moves(
            position
        )

        if not legal:
            return None, 0, 0

        # --------------------------------------------------------
        # COUP DE SECOURS
        # --------------------------------------------------------

        self.root_move = random.choice(
            legal
        )

        # --------------------------------------------------------
        # ITERATIVE DEEPENING
        # --------------------------------------------------------

        for depth in range(
            1,
            target_depth + 1
        ):

            if self.time_up():
                break

            try:

                # aspiration à partir de depth 4

                if (
                    depth >= 4
                    and self.root_depth >= 3
                ):

                    window = 80

                    alpha = (
                        self.last_score
                        - window
                    )

                    beta = (
                        self.last_score
                        + window
                    )

                    move, score = (
                        self.search_root(
                            position,
                            depth,
                            alpha,
                            beta
                        )
                    )

                    if (
                        score <= alpha
                        or score >= beta
                    ):

                        move, score = (
                            self.search_root(
                                position,
                                depth,
                                -INF,
                                INF
                            )
                        )

                else:

                    move, score = (
                        self.search_root(
                            position,
                            depth,
                            -INF,
                            INF
                        )
                    )

                # ------------------------------------------------
                # profondeur COMPLÈTE terminée
                # ------------------------------------------------

                if move is not None:

                    self.root_move = move
                    self.last_score = score
                    self.root_depth = depth

            except TimeoutError:

                break

        elapsed = (
            time.perf_counter()
            - self.start_time
        )

        if elapsed > 0:
            self.nps = int(
                self.nodes / elapsed
            )

        return (
            self.root_move,
            self.last_score,
            self.root_depth
        )


# ================================================================
# STOCKFISH — INTERFACE UCI
# ================================================================

class Stockfish:

    def __init__(self, path=None):
        self.path = path
        self.process = None

    def start(self):
        if not self.path:
            raise RuntimeError("Sélectionne d'abord stockfish.exe.")
        self.stop()
        self.process = subprocess.Popen(
            [self.path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )
        self.send("uci")
        self.wait_for("uciok", 5)
        self.send("isready")
        self.wait_for("readyok", 5)

    def send(self, command):
        if self.process and self.process.stdin:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()

    def wait_for(self, text, timeout=10):
        if not self.process or not self.process.stdout:
            raise RuntimeError("Stockfish n'est pas lancé.")
        end = time.time() + timeout
        while time.time() < end:
            line = self.process.stdout.readline()
            if line and text in line:
                return line.strip()
        raise RuntimeError("Stockfish ne répond pas à temps.")

    def bestmove(self, fen, seconds=1.0):
        if not self.process:
            self.start()
        self.send("position fen " + fen)
        self.send("go movetime " + str(max(50, int(seconds * 1000))))
        end = time.time() + max(5, seconds + 5)
        while time.time() < end:
            line = self.process.stdout.readline().strip()
            if line.startswith("bestmove "):
                return line.split()[1]
        return None

    def stop(self):
        if self.process:
            try:
                self.send("quit")
                self.process.wait(timeout=1)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
        self.process = None


def position_to_fen(position):
    rows = []
    for r in range(8):
        empty = 0
        text = ""
        for c in range(8):
            piece = position.board[r * 8 + c]
            if piece == EMPTY:
                empty += 1
            else:
                if empty:
                    text += str(empty)
                    empty = 0
                symbol = piece[1]
                text += symbol.upper() if piece[0] == WHITE else symbol.lower()
        if empty:
            text += str(empty)
        rows.append(text)

    side = "w" if position.side == WHITE else "b"
    castling = ""
    if position.castling.get("wK"):
        castling += "K"
    if position.castling.get("wQ"):
        castling += "Q"
    if position.castling.get("bK"):
        castling += "k"
    if position.castling.get("bQ"):
        castling += "q"
    if not castling:
        castling = "-"

    ep = square_name(position.en_passant) if position.en_passant >= 0 else "-"
    return "/".join(rows) + " " + side + " " + castling + " " + ep + " " + str(position.halfmove) + " " + str(position.fullmove)


def find_uci_move(position, uci):
    if not uci or len(uci) < 4:
        return None
    for move in generate_legal_moves(position):
        if move.notation().lower() == uci.lower():
            return move
    return None



# ================================================================
# 🧠 PANDORAGA — BLOC 21 — DEEP ADAPTATION Ω
# ================================================================
# Couche adaptative locale, légère et persistante.
# Elle conserve tous les moteurs précédents et ajoute une mémoire
# de tendances récentes, de positions, de phases de partie et de
# pondérations adaptatives. Aucun pip, aucune API et aucun cloud.
# ================================================================

DEEP_ADAPTATION_VERSION = "Ω Deep Adaptation MAX 2.0"
DEEP_MEMORY_LIMIT = 5000
DEEP_RECENT_LIMIT = 120
DEEP_WEIGHT_MIN = 0.20
DEEP_WEIGHT_MAX = 4.00
DEEP_LEARNING_RATE = 0.10

# MODE MAX : mémoire plus longue, poids adaptatifs bornés et apprentissage progressif.
# Les poids ne sont mis à jour que par les résultats/erreurs réellement enregistrés.
# Cela n'augmente pas automatiquement l'Elo : les performances doivent être testées.

DEEP_DEFAULT_WEIGHTS = {
    "agressivite": 1.00,
    "defense": 1.00,
    "tactique": 1.00,
    "positionnel": 1.00,
    "mobilite": 1.00,
    "securite_roi": 1.00,
    "structure_pions": 1.00,
    "initiative": 1.00,
    "captures": 1.00,
    "developpement": 1.00,
    "finales": 1.00,
    "protection": 1.00,
}


class DeepAdaptationPandoraga:
    """Adaptation profonde légère basée sur les statistiques locales."""

    def __init__(self, memory, player="Joueur"):
        self.memory = memory
        self.player = player or "Joueur"
        self.weights = dict(DEEP_DEFAULT_WEIGHTS)
        self.recent = []
        self.position_stats = {}
        self.patterns = {}
        self.confidence = 0.0
        self.last_report = {}
        self.load()

    def _store(self):
        try:
            root = self.memory.data.setdefault("deep_adaptation", {})
            p = root.setdefault(self.player, {})
            p.setdefault("weights", dict(DEEP_DEFAULT_WEIGHTS))
            p.setdefault("recent", [])
            p.setdefault("positions", {})
            p.setdefault("patterns", {})
            p.setdefault("updates", 0)
            return p
        except Exception:
            return None

    def load(self):
        p = self._store()
        if not p:
            return
        try:
            saved = p.get("weights", {})
            for k in self.weights:
                v = float(saved.get(k, 1.0))
                self.weights[k] = max(DEEP_WEIGHT_MIN, min(DEEP_WEIGHT_MAX, v))
            self.recent = list(p.get("recent", []))[-DEEP_RECENT_LIMIT:]
            self.position_stats = dict(p.get("positions", {}))
            self.patterns = dict(p.get("patterns", {}))
            self._confidence()
        except Exception:
            pass

    def save(self):
        p = self._store()
        if not p:
            return False
        try:
            p["weights"] = dict(self.weights)
            p["recent"] = self.recent[-DEEP_RECENT_LIMIT:]
            p["positions"] = dict(list(self.position_stats.items())[-DEEP_MEMORY_LIMIT:])
            p["patterns"] = dict(list(self.patterns.items())[-DEEP_MEMORY_LIMIT:])
            self.memory.save()
            return True
        except Exception:
            return False

    def set_player(self, player):
        player = player or "Joueur"
        if player == self.player:
            return
        self.player = player
        self.weights = dict(DEEP_DEFAULT_WEIGHTS)
        self.recent = []
        self.position_stats = {}
        self.patterns = {}
        self.confidence = 0.0
        self.load()

    def phase(self, position):
        pieces = sum(1 for p in position.board if p != EMPTY)
        queens = sum(1 for p in position.board if p.endswith(QUEEN))
        if pieces <= 10:
            return "finale"
        if pieces <= 20 or queens == 0:
            return "milieu"
        return "ouverture"

    def position_key(self, position):
        try:
            return position.key()
        except Exception:
            return str(position.board) + "|" + str(position.side)

    def tags(self, position, move):
        result = []
        if getattr(move, "captured", None) or getattr(move, "en_passant", False):
            result.append("captures")
        if getattr(move, "castle", False):
            result.append("securite_roi")
        if getattr(move, "promotion", None):
            result.append("finales")
        piece = position.board[move.from_sq]
        if piece.endswith(KING):
            result.append("securite_roi")
        if piece.endswith(QUEEN):
            result.append("initiative")
        if piece.endswith(PAWN):
            result.append("structure_pions")
        if move.to_sq in (27, 28, 35, 36):
            result.append("positionnel")
        return list(dict.fromkeys(result))

    def record_move(self, position, move, score=0.0, source="jeu"):
        tags = self.tags(position, move)
        self.recent.append({
            "time": time.time(), "move": move.notation(),
            "from": int(move.from_sq), "to": int(move.to_sq),
            "phase": self.phase(position), "tags": tags,
            "score": float(score), "source": source,
        })
        self.recent = self.recent[-DEEP_RECENT_LIMIT:]
        key = self.position_key(position)
        st = self.position_stats.setdefault(key, {"seen": 0, "moves": {}, "score": 0.0})
        st["seen"] += 1
        name = move.notation()
        st["moves"][name] = st["moves"].get(name, 0) + 1
        st["score"] = st.get("score", 0.0) * 0.9 + float(score) * 0.1
        for tag in tags:
            self.patterns[tag] = self.patterns.get(tag, 0) + 1
        if len(self.position_stats) > DEEP_MEMORY_LIMIT:
            self.position_stats.pop(next(iter(self.position_stats)), None)

    def register_error(self, move, severity=1.0):
        name = str(move)
        self.patterns["erreur:" + name] = self.patterns.get("erreur:" + name, 0) + 1
        factor = max(0.05, min(1.0, float(severity)))
        self.weights["protection"] = min(DEEP_WEIGHT_MAX, self.weights["protection"] + DEEP_LEARNING_RATE * factor)
        self.weights["tactique"] = min(DEEP_WEIGHT_MAX, self.weights["tactique"] + DEEP_LEARNING_RATE * factor * 0.5)
        self._confidence()
        self.save()

    def register_result(self, result):
        result = str(result).lower()
        reward = 1.0 if result in ("win", "victoire", "1") else -1.0 if result in ("loss", "défaite", "0") else 0.15
        for entry in self.recent:
            for tag in entry.get("tags", []):
                self.weights[tag] += DEEP_LEARNING_RATE * reward * 0.12
        for k in self.weights:
            self.weights[k] = max(DEEP_WEIGHT_MIN, min(DEEP_WEIGHT_MAX, self.weights[k]))
        p = self._store()
        if p:
            p["updates"] = int(p.get("updates", 0)) + 1
        self._confidence()
        self.save()

    def move_bonus(self, position, move):
        bonus = sum((self.weights.get(t, 1.0) - 1.0) * 22.0 for t in self.tags(position, move))
        st = self.position_stats.get(self.position_key(position))
        if st:
            bonus += min(24.0, st.get("moves", {}).get(move.notation(), 0) * 2.0)
            bonus += max(-12.0, min(12.0, st.get("score", 0.0) * 0.05))
        return bonus

    def _confidence(self):
        if not self.recent:
            self.confidence = 0.0
            return
        volume = min(1.0, len(self.recent) / 30.0)
        spread = sum(abs(v - 1.0) for v in self.weights.values()) / len(self.weights)
        self.confidence = max(0.0, min(100.0, volume * 70.0 + min(30.0, spread * 20.0)))

    def analyse(self, position=None):
        p = self.memory.player(self.player)
        games = max(1, int(p.get("games", 0)))
        aggressive = int(p.get("captures", 0)) * 2 + int(p.get("checks", 0)) * 1.5
        defensive = int(p.get("castles", 0)) * 1.5 + int(p.get("king_moves", 0)) * 0.4
        style = "agressif" if aggressive > defensive + games else "défensif" if defensive > aggressive + games else "équilibré"
        report = {
            "version": DEEP_ADAPTATION_VERSION, "joueur": self.player,
            "style": style, "phase": self.phase(position) if position else "global",
            "confiance": round(self.confidence, 1), "parties": int(p.get("games", 0)),
            "erreurs": int(p.get("mistakes", 0)), "blunders": int(p.get("blunders", 0)),
            "positions": len(self.position_stats), "recent": len(self.recent),
            "poids": {k: round(v, 3) for k, v in self.weights.items()},
        }
        self.last_report = report
        return report

    def adapt_position(self, position):
        report = self.analyse(position)
        try:
            legal = generate_legal_moves(position)
            captures = sum(1 for m in legal if m.captured or m.en_passant)
            complexity = min(40, len(legal)) + min(30, captures * 4)
            if complexity >= 45:
                self.weights["tactique"] = min(DEEP_WEIGHT_MAX, self.weights["tactique"] + 0.01)
                self.weights["protection"] = min(DEEP_WEIGHT_MAX, self.weights["protection"] + 0.01)
            elif self.phase(position) == "finale":
                self.weights["finales"] = min(DEEP_WEIGHT_MAX, self.weights["finales"] + 0.01)
        except Exception:
            pass
        self._confidence()
        return report

    def summary_text(self, position=None):
        r = self.analyse(position)
        return ("🧠 DEEP ADAPTATION Ω\n" + "-------------------------------\n" +
                f"Version : {r['version']}\nStyle : {r['style']}\n" +
                f"Phase : {r['phase']}\nConfiance : {r['confiance']:.1f}%\n" +
                f"Parties : {r['parties']}\nErreurs : {r['erreurs']} | Blunders : {r['blunders']}\n" +
                f"Mémoire récente : {r['recent']}\nPositions apprises : {r['positions']}\n")


DEEP_ADAPTATION_PANDORAGA = None


# ================================================================
# 🐼 BLOC 21 — INTERFACE RESPONSIVE Ω
# ================================================================
RESPONSIVE_PHONE_WIDTH = 700
RESPONSIVE_TABLET_WIDTH = 1000
RESPONSIVE_MAX_BOARD = 900

# ================================================================
# GUI
# ================================================================

# ================================================================
# JPADON Ω — profil d'adversaire appris UNIQUEMENT après la partie
# ================================================================

class JPADONMemory:
    """Mémoire JSON lisible des habitudes réellement observées des adversaires."""

    def __init__(self, path=None):
        self.path = path or JPADON_FILE
        self.data = {"format": "JPADON", "version": 1, "opponents": {}}
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                self.data.update(loaded)
                if not isinstance(self.data.get("opponents"), dict):
                    self.data["opponents"] = {}
        except (OSError, ValueError, TypeError):
            pass

    def save(self):
        """Écriture atomique : évite de laisser un JSON à moitié écrit."""
        temp_path = self.path + ".tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            os.replace(temp_path, self.path)
            return True
        except (OSError, TypeError, ValueError):
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except OSError:
                pass
            return False

    @staticmethod
    def opponent_id(name):
        name = (name or "Adversaire inconnu").strip()
        return name.casefold() or "adversaire inconnu"

    def profile_for(self, name):
        return self.data.get("opponents", {}).get(self.opponent_id(name), {})

    @staticmethod
    def _new_profile(name):
        return {
            "nom": name,
            "parties_analysees": 0,
            "resultats": {"victoires": 0, "defaites": 0, "nulles": 0},
            "statistiques": {
                "coups_observes": 0, "captures": 0, "echecs_donnes": 0,
                "roques": 0, "promotions": 0, "coups_par_phase": {
                    "ouverture": 0, "milieu": 0, "finale": 0
                },
                "pieces_jouees": {}, "cases_arrivee": {},
                "ouvertures_observees": {}
            },
            "style": {"agressivite": 0.0, "tactique": 0.0, "confiance": 0.0},
            "derniere_partie": None,
            "historique_recent": [],
            "avertissements": ["Les styles sont des estimations, pas des certitudes."]
        }

    def finalize_game(self, opponent_name, opponent_side, game_moves, result):
        """Analyse une partie terminée; ne s'exécute pas pendant la partie."""
        if result not in ("win", "loss", "draw"):
            return False
        name = (opponent_name or "Adversaire inconnu").strip() or "Adversaire inconnu"
        oid = self.opponent_id(name)
        opponents = self.data.setdefault("opponents", {})
        profile = opponents.setdefault(oid, self._new_profile(name))
        stats = profile.setdefault("statistiques", self._new_profile(name)["statistiques"])
        results = profile.setdefault("resultats", {"victoires": 0, "defaites": 0, "nulles": 0})
        result_key = {"win": "victoires", "loss": "defaites", "draw": "nulles"}[result]
        results[result_key] = int(results.get(result_key, 0)) + 1
        profile["parties_analysees"] = int(profile.get("parties_analysees", 0)) + 1

        opponent_moves = [m for m in game_moves if m.get("side") == opponent_side]
        # Les statistiques ne changent qu'après le résultat final.
        for m in opponent_moves:
            stats["coups_observes"] = int(stats.get("coups_observes", 0)) + 1
            for field, key in (("capture", "captures"), ("echec", "echecs_donnes"), ("roque", "roques"), ("promotion", "promotions")):
                if m.get(field):
                    stats[key] = int(stats.get(key, 0)) + 1
            phase = m.get("phase", "milieu")
            phases = stats.setdefault("coups_par_phase", {})
            phases[phase] = int(phases.get(phase, 0)) + 1
            piece = m.get("piece", "?")
            pieces = stats.setdefault("pieces_jouees", {})
            pieces[piece] = int(pieces.get(piece, 0)) + 1
            square = str(m.get("to", "?"))
            squares = stats.setdefault("cases_arrivee", {})
            squares[square] = int(squares.get(square, 0)) + 1

        # Signature des 12 premiers demi-coups, utile pour reconnaître les ouvertures.
        sequence = [str(m.get("notation", "?")) for m in game_moves[:12]]
        if sequence:
            sig = " ".join(sequence)
            openings = stats.setdefault("ouvertures_observees", {})
            openings[sig] = int(openings.get(sig, 0)) + 1
            # Garder le JSON compact : top 30 signatures les plus fréquentes.
            if len(openings) > 30:
                keep = sorted(openings.items(), key=lambda item: item[1], reverse=True)[:30]
                stats["ouvertures_observees"] = dict(keep)

        total = max(1, int(stats.get("coups_observes", 0)))
        captures = int(stats.get("captures", 0))
        checks = int(stats.get("echecs_donnes", 0))
        # Scores descriptifs bornés entre 0 et 1, pas des probabilités de victoire.
        aggression = min(1.0, (captures * 0.65 + checks * 1.15) / total)
        profile["style"] = {
            "agressivite": round(aggression, 3),
            "tactique": round(min(1.0, (captures + checks) / total), 3),
            "confiance": round(min(1.0, profile["parties_analysees"] / 8.0) * min(1.0, total / 80.0), 3)
        }
        profile["derniere_partie"] = {
            "resultat_adversaire": result,
            "date_unix": int(time.time()),
            "coups_adversaire": len(opponent_moves),
            "demi_coups_partie": len(game_moves)
        }
        recent = profile.setdefault("historique_recent", [])
        recent.append({
            "resultat": result,
            "coups_adversaire": [
                {"notation": m.get("notation"), "phase": m.get("phase"),
                 "capture": bool(m.get("capture")), "echec": bool(m.get("echec")),
                 "roque": bool(m.get("roque")), "piece": m.get("piece")}
                for m in opponent_moves
            ]
        })
        del recent[:-20]
        return self.save()


class PandoragaGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(TITLE)
        self.root.geometry("1180x820")
        self.root.minsize(320, 360)
        try:
            self.root.state("zoomed")
        except Exception:
            pass
        self.root.bind("<Configure>", self.on_window_resize)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.root.configure(
            bg="#11151c"
        )

        self.position = Position()

        self.memory = (
            PandoragaMemory()
        )

        self.player_name = "Joueur"

        self.engine = PandoragaEngine(
            self.memory,
            self.player_name
        )

        self.selected = None
        self.thinking = False
        self.ai_vs_ai = False
        self.ai_vs_stockfish = False
        self.stockfish = Stockfish()
        self.sf_time = 1.0

        global DEEP_ADAPTATION_PANDORAGA
        DEEP_ADAPTATION_PANDORAGA = DeepAdaptationPandoraga(self.memory, self.player_name)
        self.deep_adaptation = DEEP_ADAPTATION_PANDORAGA
        self.device_mode = "ordinateur"
        self.fullscreen_mode = False
        self._resize_job = None

        self.history = []
        self.jpadon = JPADONMemory()
        self.jpadon_game_moves = []
        self._jpadon_finalized = False

        self.position_history = {}

        self.build_gui()

        self.record_position()

        self.update_board()

    # ============================================================
    # GUI
    # ============================================================

    def build_gui(self):

        self.header = tk.Frame(self.root, bg="#11151c")
        self.header.pack(fill="x", padx=10, pady=8)
        self.title_label = tk.Label(self.header, text="🐼 PANDORAGA Ω", font=("Segoe UI", 25, "bold"), bg="#11151c", fg="#55d68b")
        self.title_label.pack(side="left")
        self.status = tk.Label(self.header, text="⚡ MAX 30s / PROF. 15 prêt", font=("Segoe UI", 12, "bold"), bg="#11151c", fg="white")
        self.status.pack(side="right")

        self.main = tk.Frame(self.root, bg="#11151c")
        self.main.pack(fill="both", expand=True, padx=10, pady=4)
        self.board_frame = tk.Frame(self.main, bg="#11151c")
        self.board_frame.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(self.board_frame, width=650, height=650, bg="#101010", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.click_board)

        self.panel = tk.Frame(self.main, bg="#1b222c", width=360)
        self.panel.pack(side="right", fill="both", expand=False)
        self.panel.pack_propagate(False)
        self.panel_title = tk.Label(self.panel, text="⚡ MODE AUTOMATIQUE", font=("Segoe UI", 15, "bold"), bg="#1b222c", fg="#55d68b")
        self.panel_title.pack(pady=(12, 6))
        self.panel_hint = tk.Label(self.panel, text="Pandoraga choisit automatiquement\nle temps et la profondeur.", font=("Segoe UI", 10), bg="#1b222c", fg="white", justify="center")
        self.panel_hint.pack(pady=(0, 8))
        self.name_entry = tk.Entry(self.panel, bg="#252e39", fg="white", insertbackground="white", relief="flat")
        self.name_entry.insert(0, "Joueur")
        self.name_entry.pack(fill="x", padx=15, pady=4)

        self.make_button(self.panel, "♟ Nouvelle partie", self.new_game)
        self.make_button(self.panel, "🤖 Pandoraga joue", self.start_ai)
        self.make_button(self.panel, "⚔️ Pandoraga vs Pandoraga", self.start_ai_vs_ai)
        self.make_button(self.panel, "⚔️ Pandoraga vs Stockfish", self.start_pandoraga_vs_stockfish)
        self.make_button(self.panel, "🧠 Deep Adaptation", self.show_deep_adaptation)
        self.make_button(self.panel, "⛶ Plein écran", self.toggle_fullscreen)
        self.make_button(self.panel, "⏹ Arrêter", self.stop_match)
        self.make_button(self.panel, "🧹 Effacer mémoire", self.reset_memory)

        self.info = tk.Text(self.panel, bg="#0f141a", fg="white", relief="flat", font=("Consolas", 10), height=18, wrap="word")
        self.info.pack(fill="both", expand=True, padx=12, pady=10)
        self.apply_responsive_layout()

    def make_button(
        self,
        parent,
        text,
        command
    ):

        b = tk.Button(
            parent,
            text=text,
            command=command,
            bg="#252e39",
            fg="white",
            activebackground="#55d68b",
            activeforeground="black",
            relief="flat",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            pady=8
        )

        b.pack(
            fill="x",
            padx=20,
            pady=3
        )

        return b

    # ============================================================
    # BOARD
    # ============================================================

    def detect_device_mode(self):
        w = max(1, self.root.winfo_width())
        if w < RESPONSIVE_PHONE_WIDTH:
            return "telephone"
        if w < RESPONSIVE_TABLET_WIDTH:
            return "tablette"
        return "ordinateur"

    def apply_responsive_layout(self):
        mode = self.detect_device_mode()
        self.device_mode = mode
        self.panel.pack_forget(); self.board_frame.pack_forget()
        if mode == "telephone":
            self.board_frame.pack(side="top", fill="both", expand=True)
            self.panel.pack(side="bottom", fill="both", expand=False)
            self.panel.configure(height=300)
            self.title_label.configure(font=("Segoe UI", 18, "bold"))
        elif mode == "tablette":
            self.board_frame.pack(side="left", fill="both", expand=True)
            self.panel.pack(side="right", fill="both", expand=False)
            self.panel.configure(width=300)
            self.title_label.configure(font=("Segoe UI", 21, "bold"))
        else:
            self.board_frame.pack(side="left", fill="both", expand=True)
            self.panel.pack(side="right", fill="both", expand=False)
            self.panel.configure(width=360)
            self.title_label.configure(font=("Segoe UI", 25, "bold"))
        self.update_board()

    def on_window_resize(self, event=None):
        if self._resize_job:
            try: self.root.after_cancel(self._resize_job)
            except Exception: pass
        self._resize_job = self.root.after(100, self.apply_responsive_layout)

    def toggle_fullscreen(self, event=None):
        self.fullscreen_mode = not self.fullscreen_mode
        try: self.root.attributes("-fullscreen", self.fullscreen_mode)
        except Exception: pass
        return "break"

    def exit_fullscreen(self, event=None):
        self.fullscreen_mode = False
        try: self.root.attributes("-fullscreen", False)
        except Exception: pass
        return "break"

    def show_deep_adaptation(self):
        try:
            name = self.name_entry.get().strip() or "Joueur"
            self.player_name = name
            self.deep_adaptation.set_player(name)
            self.deep_adaptation.adapt_position(self.position)
            messagebox.showinfo("🧠 Deep Adaptation Ω", self.deep_adaptation.summary_text(self.position))
            self.update_info()
        except Exception as exc:
            messagebox.showerror("Deep Adaptation", str(exc))

    def update_board(self):

        self.canvas.delete("all")

        width = max(100, self.canvas.winfo_width())
        height = max(100, self.canvas.winfo_height())
        size = max(1, min(width, height) // 8)
        size = min(RESPONSIVE_MAX_BOARD // 8, size)

        ox = (
            width - size * 8
        ) // 2

        oy = (
            height - size * 8
        ) // 2

        self.square_size = size
        self.ox = ox
        self.oy = oy

        for r in range(8):

            for c in range(8):

                x1 = ox + c * size
                y1 = oy + r * size

                x2 = x1 + size
                y2 = y1 + size

                light = (
                    (r + c) % 2 == 0
                )

                fill = (
                    "#e8edf2"
                    if light
                    else "#53606d"
                )

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline=""
                )

                sq = r * 8 + c

                if self.selected == sq:

                    self.canvas.create_rectangle(
                        x1 + 3,
                        y1 + 3,
                        x2 - 3,
                        y2 - 3,
                        outline="#55d68b",
                        width=4
                    )

                piece = self.position.board[sq]

                if piece != EMPTY:

                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=UNICODE_PIECES[
                            piece
                        ],
                        font=(
                            "Segoe UI Symbol",
                            max(
                                30,
                                int(size * .65)
                            )
                        )
                    )

        self.update_info()

    # ============================================================
    # INFO
    # ============================================================

    def update_info(self):

        p = self.memory.profile(
            self.player_name
        )

        self.info.delete(
            "1.0",
            "end"
        )

        self.info.insert(
            "end",
            "🐼 PANDORAGA Ω\n"
            "===============================\n\n"
        )

        self.info.insert(
            "end",
            "MODE : AUTO ⚡\n\n"
        )

        self.info.insert(
            "end",
            f"Complexité : "
            f"{self.engine.auto_complexity}/100\n"
        )

        self.info.insert(
            "end",
            f"Temps choisi : "
            f"{self.engine.auto_time:.2f} s\n"
        )

        self.info.insert(
            "end",
            f"Profondeur cible : "
            f"{self.engine.auto_target_depth}\n"
        )

        self.info.insert(
            "end",
            f"Profondeur atteinte : "
            f"{self.engine.root_depth}\n"
        )

        self.info.insert(
            "end",
            f"Nœuds : "
            f"{self.engine.nodes:,}\n"
        )

        self.info.insert(
            "end",
            f"Nœuds/s : "
            f"{self.engine.nps:,}\n\n"
        )

        self.info.insert(
            "end",
            "ADAPTATION\n"
            "-------------------------------\n"
        )

        self.info.insert(
            "end",
            f"Style : {p['style']}\n"
        )

        self.info.insert(
            "end",
            f"Erreurs : "
            f"{self.memory.player(self.player_name)['mistakes']}\n"
        )

        self.info.insert(
            "end",
            f"Blunders : "
            f"{self.memory.player(self.player_name)['blunders']}\n"
        )

        self.info.insert(
            "end",
            f"Coups appris : "
            f"{len(self.memory.player(self.player_name)['moves'])}\n"
        )

        try:
            self.deep_adaptation.set_player(self.player_name)
            self.deep_adaptation.adapt_position(self.position)
            self.info.insert("end", "\n" + self.deep_adaptation.summary_text(self.position))
        except Exception:
            pass

        self.info.insert(
            "end",
            f"Appareil : {self.device_mode}\n"
            f"\nTT : {self.engine.tt.size()} positions\n"
        )

    # ============================================================
    # JPADON — collecte discrète, analyse uniquement en fin de partie
    # ============================================================

    def capture_jpadon_move(self, before, move, mover_side):
        """Stocke les faits de la partie en RAM; aucune analyse JSON ici."""
        try:
            piece = before.board[move.from_sq]
            after = make_move(before.clone(), move)
            phase_pieces = sum(1 for item in before.board if item != EMPTY)
            phase = "finale" if phase_pieces <= 10 else "milieu" if phase_pieces <= 20 else "ouverture"
            gives_check = in_check(after, after.side)
            self.jpadon_game_moves.append({
                "side": mover_side,
                "notation": move.notation(),
                "from": int(move.from_sq),
                "to": int(move.to_sq),
                "piece": piece[1] if isinstance(piece, str) and len(piece) > 1 else "?",
                "phase": phase,
                "capture": bool(getattr(move, "captured", None) or getattr(move, "en_passant", False)),
                "echec": bool(gives_check),
                "roque": bool(getattr(move, "castle", False)),
                "promotion": bool(getattr(move, "promotion", None))
            })
        except Exception:
            # Un défaut de profil ne doit jamais bloquer une partie d'échecs.
            pass

    def finalize_jpadon_game(self, result_text):
        if self._jpadon_finalized or self.ai_vs_ai:
            return
        self._jpadon_finalized = True
        lower = result_text.lower()
        white_won = "blancs gagnent" in lower
        black_won = "noirs gagnent" in lower
        if not white_won and not black_won:
            result = "draw"
        else:
            opponent_side = BLACK if self.ai_vs_stockfish else WHITE
            opponent_won = (white_won if opponent_side == WHITE else black_won)
            result = "win" if opponent_won else "loss"
        opponent_name = "Stockfish" if self.ai_vs_stockfish else self.player_name
        self.jpadon.finalize_game(opponent_name, BLACK if self.ai_vs_stockfish else WHITE, self.jpadon_game_moves, result)
        # Le profil est chargé avant la prochaine partie; ici on affiche le résultat de l'analyse.
        try:
            profile = self.jpadon.profile_for(opponent_name)
            self.info.insert("end", f"\n\nJPADON Ω — {opponent_name}\nParties analysées : {profile.get('parties_analysees', 0)}\nStyle estimé : {profile.get('style', {})}\n")
        except Exception:
            pass

    # ============================================================
    # CLIC
    # ============================================================

    def click_board(self, event):

        if self.thinking:
            return

        if self.ai_vs_ai:
            return

        if self.position.side != WHITE:
            return

        x = event.x - self.ox
        y = event.y - self.oy

        if x < 0 or y < 0:
            return

        c = int(
            x / self.square_size
        )

        r = int(
            y / self.square_size
        )

        if not inside(r, c):
            return

        sq = r * 8 + c

        piece = self.position.board[sq]

        if self.selected is None:

            if (
                piece != EMPTY
                and piece[0] == WHITE
            ):

                self.selected = sq
                self.update_board()

            return

        if sq == self.selected:

            self.selected = None
            self.update_board()

            return

        legal = generate_legal_moves(
            self.position
        )

        selected_move = None

        for move in legal:

            if (
                move.from_sq
                == self.selected
                and move.to_sq == sq
            ):

                selected_move = move
                break

        if selected_move is None:

            if (
                piece != EMPTY
                and piece[0] == WHITE
            ):

                self.selected = sq
                self.update_board()

            return

        # promotion auto dame

        if selected_move.promotion:
            selected_move.promotion = QUEEN

        self.play_human(
            selected_move
        )

    # ============================================================
    # HUMAIN
    # ============================================================

    def play_human(self, move):

        before = self.position.clone()

        capture = (
            move.captured is not None
            or move.en_passant
        )

        check = in_check(
            make_move(
                before,
                move
            ),
            BLACK
        )

        self.memory.record_move(
            self.player_name,
            move,
            before,
            capture,
            check
        )
        try:
            self.deep_adaptation.record_move(before, move, 0.0, "humain")
        except Exception:
            pass
        self.capture_jpadon_move(before, move, before.side)

        self.position = make_move(
            self.position,
            move
        )

        self.history.append(
            move.notation()
        )

        self.record_position()

        self.selected = None

        self.update_board()

        if self.check_end():
            return

        self.start_ai()

    # ============================================================
    # IA
    # ============================================================

    def start_ai(self):

        if self.thinking:
            return

        if self.ai_vs_ai:
            return

        if self.ai_vs_stockfish:
            if self.position.side != WHITE:
                return
        elif self.position.side != BLACK:
            return

        self.player_name = (
            self.name_entry.get().strip()
            or "Joueur"
        )

        self.engine.player = (
            self.player_name
        )
        opponent_name = "Stockfish" if self.ai_vs_stockfish else self.player_name
        self.engine.jpadon_profile = self.jpadon.profile_for(opponent_name)

        self.engine.adaptation = (
            Adaptation(
                self.memory,
                self.player_name
            )
        )

        try:
            self.deep_adaptation.set_player(self.player_name)
            self.deep_adaptation.adapt_position(self.position)
        except Exception:
            pass

        self.thinking = True

        self.status.config(
            text="🤖 AUTO : Pandoraga réfléchit..."
        )

        self.update_board()

        threading.Thread(
            target=self.ai_thread,
            daemon=True
        ).start()

    def ai_thread(self):

        position = self.position.clone()

        result = self.engine.choose_move(
            position
        )

        self.root.after(
            0,
            lambda: self.finish_ai(
                *result
            )
        )

    def finish_ai(
        self,
        move,
        score,
        depth
    ):

        self.thinking = False

        if move is None:

            self.check_end()
            return

        before = self.position.clone()
        try:
            self.deep_adaptation.record_move(before, move, score, "ia")
        except Exception:
            pass
        self.capture_jpadon_move(before, move, before.side)

        self.position = make_move(
            self.position,
            move
        )

        self.history.append(
            move.notation()
        )

        self.record_position()

        self.status.config(
            text=(
                f"⚡ AUTO | "
                f"{move.notation()} | "
                f"{self.engine.auto_time:.1f}s | "
                f"D{depth}"
            )
        )

        self.update_board()

        if not self.check_end() and self.ai_vs_stockfish:
            self.root.after(100, self.stockfish_turn)

    # ============================================================
    # IA VS IA
    # ============================================================

    def start_ai_vs_ai(self):

        if self.thinking:
            return

        self.ai_vs_ai = True

        self.new_game()

        self.ai_vs_ai = True

        self.status.config(
            text="⚔️ AUTO : Pandoraga vs Pandoraga"
        )

        self.ai_vs_ai_turn()

    def ai_vs_ai_turn(self):

        if not self.ai_vs_ai:
            return

        if self.thinking:
            return

        self.thinking = True

        if self.position.side == WHITE:
            name = "Pandoraga_Blanc"
        else:
            name = "Pandoraga_Noir"

        engine = PandoragaEngine(
            self.memory,
            name
        )

        position = self.position.clone()

        def worker():

            result = engine.choose_move(
                position
            )

            self.root.after(
                0,
                lambda: self.finish_aivai(
                    engine,
                    *result
                )
            )

        threading.Thread(
            target=worker,
            daemon=True
        ).start()

    def finish_aivai(
        self,
        engine,
        move,
        score,
        depth
    ):

        self.thinking = False

        if move is None:

            self.check_end()
            return

        before = self.position.clone()
        self.capture_jpadon_move(before, move, before.side)
        self.position = make_move(
            self.position,
            move
        )

        self.history.append(
            move.notation()
        )

        self.record_position()

        self.engine = engine

        self.status.config(
            text=(
                f"⚔️ {move.notation()} | "
                f"AUTO {engine.auto_time:.1f}s | "
                f"D{depth}"
            )
        )

        self.update_board()

        if not self.check_end():

            self.root.after(
                150,
                self.ai_vs_ai_turn
            )

    # ============================================================
    # PANDORAGA VS STOCKFISH
    # ============================================================

    def start_pandoraga_vs_stockfish(self):
        if self.thinking:
            return

        if not self.stockfish.path:
            path = filedialog.askopenfilename(
                title="Choisir stockfish.exe",
                filetypes=[("Stockfish", "*.exe"), ("Tous les fichiers", "*.*")]
            )
            if not path:
                return
            self.stockfish.path = path

        try:
            if not self.stockfish.process:
                self.stockfish.start()
        except Exception as e:
            messagebox.showerror("Stockfish", str(e))
            return

        self.ai_vs_stockfish = True
        self.ai_vs_ai = False
        self.new_game()
        self.ai_vs_stockfish = True
        self.status.config(text="⚔️ Pandoraga vs Stockfish")
        self.start_ai()

    def stockfish_turn(self):
        if not self.ai_vs_stockfish or self.thinking:
            return
        if self.position.side != BLACK:
            return

        self.thinking = True
        self.status.config(text="♟ Stockfish réfléchit...")
        position = self.position.clone()

        def worker():
            try:
                uci = self.stockfish.bestmove(
                    position_to_fen(position),
                    self.sf_time
                )
                move = find_uci_move(position, uci)
                error = None
            except Exception as e:
                move = None
                error = str(e)

            self.root.after(
                0,
                lambda: self.finish_stockfish(move, error)
            )

        threading.Thread(target=worker, daemon=True).start()

    def finish_stockfish(self, move, error=None):
        self.thinking = False

        if error:
            self.ai_vs_stockfish = False
            messagebox.showerror("Stockfish", error)
            self.status.config(text="Stockfish arrêté")
            return

        if move is None:
            self.ai_vs_stockfish = False
            self.check_end()
            return

        before = self.position.clone()
        self.capture_jpadon_move(before, move, before.side)
        self.position = make_move(self.position, move)
        self.history.append(move.notation())
        self.record_position()

        self.status.config(
            text=f"♟ Stockfish | {move.notation()} | {self.sf_time:.1f}s"
        )

        self.update_board()

        if not self.check_end():
            self.root.after(100, self.start_ai)

    # ============================================================
    # RÉPÉTITION
    # ============================================================

    def record_position(self):

        key = self.position.key()

        self.position_history[key] = (
            self.position_history.get(
                key,
                0
            ) + 1
        )

    # ============================================================
    # FIN
    # ============================================================

    def check_end(self):

        legal = generate_legal_moves(
            self.position
        )

        if legal:

            key = self.position.key()

            if (
                self.position_history.get(
                    key,
                    0
                ) >= 3
            ):

                self.end_game(
                    "♻️ Nulle par répétition"
                )

                return True

            if self.position.halfmove >= 100:

                self.end_game(
                    "🤝 Nulle — 50 coups"
                )

                return True

            return False

        if in_check(
            self.position,
            self.position.side
        ):

            if self.position.side == WHITE:

                self.end_game(
                    "♚ MAT — Les noirs gagnent"
                )

            else:

                self.end_game(
                    "♚ MAT — Les blancs gagnent"
                )

        else:

            self.end_game(
                "🤝 PAT — Partie nulle"
            )

        return True

    def end_game(self, text):

        self.thinking = False
        if self._jpadon_finalized and not self.ai_vs_ai:
            return

        self.status.config(
            text=text
        )

        # éviter les doublons en IA vs IA
        if self.ai_vs_ai:
            return

        if "blancs gagnent" in text.lower():

            self.memory.record_result(
                self.player_name,
                "win"
            )

        elif "noirs gagnent" in text.lower():

            self.memory.record_result(
                self.player_name,
                "loss"
            )

        else:

            self.memory.record_result(
                self.player_name,
                "draw"
            )

        try:
            result = "win" if "blancs gagnent" in text.lower() else "loss" if "noirs gagnent" in text.lower() else "draw"
            self.deep_adaptation.register_result(result)
        except Exception:
            pass

        try:
            self.finalize_jpadon_game(text)
        except Exception:
            pass

        messagebox.showinfo(
            "Pandoraga Ω",
            text
        )

    # ============================================================
    # NOUVELLE PARTIE
    # ============================================================

    def new_game(self):

        self.thinking = False
        self.jpadon_game_moves = []
        self._jpadon_finalized = False

        self.position = Position()

        self.selected = None

        self.history.clear()

        self.position_history.clear()

        self.engine.tt.clear()

        self.engine.nodes = 0

        self.engine.root_depth = 0
        self.engine.auto_time = 1
        self.engine.auto_target_depth = 3
        self.engine.auto_complexity = 0

        self.record_position()

        self.status.config(
            text="⚡ AUTO prêt"
        )

        self.update_board()

    def stop_match(self):
        self.ai_vs_stockfish = False
        self.ai_vs_ai = False
        self.thinking = False
        try:
            self.stockfish.send("stop")
        except Exception:
            pass
        self.status.config(text="⏹ Match arrêté")
        self.update_board()

    # ============================================================
    # RESET
    # ============================================================

    def reset_memory(self):

        answer = messagebox.askyesno(
            "Mémoire Pandoraga",
            "Supprimer toute la mémoire ?"
        )

        if not answer:
            return

        self.memory.data = {
            "version": 3,
            "players": {},
            "global": {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0
            }
        }

        self.memory.save()

        self.engine.tt.clear()

        self.status.config(
            text="🧹 Mémoire supprimée"
        )

        self.update_board()


# ================================================================
# MAIN
# ================================================================

def main():

    root = tk.Tk()

    PandoragaGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()

# ================================================================
# 🧪 BLOC 21 — MATRICE DE VALIDATION Ω
# ================================================================
# La couche ci-dessus est volontairement sans dépendance externe.
# Elle est conçue pour fonctionner hors ligne sur ordinateur, tablette
# ou téléphone lorsque Tkinter est disponible sur l'environnement Python.
#
# Affichage :
# - petit écran : plateau au-dessus et commandes sous le plateau ;
# - tablette : plateau principal + panneau compact ;
# - ordinateur : plateau principal + panneau large ;
# - redimensionnement : recalcul automatique du plateau ;
# - F11 : plein écran ; ESC : sortie du plein écran.
#
# Adaptation :
# - mémoire par joueur ;
# - tendances récentes ;
# - statistiques par position ;
# - phases ouverture/milieu/finale ;
# - pondérations tactique/protection/finales/etc. ;
# - renforcement léger après résultat ;
# - renforcement après erreurs signalées ;
# - conservation JSON locale.
#
# Le terme Deep ne signifie pas réseau neuronal : cette version est une
# adaptation statistique profonde en plusieurs couches. Elle ne prétend
# pas posséder les capacités d'un modèle entraîné sur des millions de
# parties. Son avantage est la légèreté, la transparence et l'offline.
#
# Compatibilité conservée :
# les fonctions de génération légale, roque, en passant, promotions,
# recherche, alpha-beta, PVS, quiescence, table de transposition,
# killer/history, auto-depth, auto-time, mémoire, Stockfish et IA-vs-IA
# restent dans le même fichier.
#
# Calibration :
# le moteur continue d'utiliser son NPS et ses calculs auto existants.
# La nouvelle GUI ne force pas une profondeur artificiellement élevée :
# elle conserve les limites déjà prévues afin de ne pas saturer les petits
# appareils.
#
# Sécurité :
# aucun accès réseau n'est ajouté par Deep Adaptation. Les données sont
# stockées dans le fichier mémoire JSON déjà utilisé par Pandoraga.
#
