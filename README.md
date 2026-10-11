# 🐼 Pandoraga Full Adaptation Ω

Moteur d'échecs Python orienté recherche, adaptation statistique locale et interface graphique Tkinter.

> **État du dépôt :** paquet de publication préparé à partir du fichier Pandoraga Ω fourni dans les fichiers du projet. La compilation syntaxique Python a été vérifiée. Le fonctionnement complet de l'interface, toutes les règles d'échecs et la force Elo n'ont pas été validés indépendamment : faites les tests décrits ci-dessous avant de présenter une version comme stable.

## Fonctionnalités annoncées par le projet

- Recherche d'échecs avec Negamax / Alpha-Beta et améliorations de recherche présentes dans le code.
- Profondeur et temps de réflexion adaptatifs, dans les limites définies par le moteur.
- Mémoire locale JSON pour les données d'adaptation.
- Interface graphique Tkinter.
- Mode Stockfish optionnel, si la version du programme et le système utilisé le prennent en charge et si Stockfish est installé séparément.
- Fonctionnement local ; aucune connexion réseau n'est nécessaire au moteur de base.

Les éléments ci-dessus décrivent les objectifs et éléments présents dans le code, pas une certification indépendante de leur exactitude ni une garantie de niveau Elo.

## Prérequis

- Python 3.10 ou plus récent recommandé.
- Tkinter disponible dans l'installation Python pour utiliser la fenêtre graphique.
- Aucun paquet `pip` n'est requis par le fichier principal.
- Stockfish est facultatif et n'est pas distribué dans ce dépôt.

## Démarrage

### Windows

1. Installez Python depuis le site officiel et activez l'option d'ajout au `PATH`.
2. Ouvrez un terminal dans le dossier du projet.
3. Lancez :

```powershell
py Pandoraga.py
```

Vous pouvez aussi lancer `run_windows.bat`.

### Linux

Vérifiez que Python et Tkinter sont installés, puis exécutez :

```bash
python3 Pandoraga.py
```

### Android

Le code utilise Tkinter : beaucoup d'environnements Python Android ne le prennent pas en charge. Le fichier n'est donc **pas garanti compatible Android** sans environnement graphique compatible.

## Mémoire et confidentialité

Le moteur utilise un fichier de mémoire JSON local nommé `pandoraga_memoire.json` (ou le nom défini dans le code). Ce fichier peut contenir des données de parties ou d'adaptation. Ne publiez pas votre mémoire personnelle dans GitHub ; elle est exclue par `.gitignore`.

## Vérification rapide

```bash
python -m py_compile Pandoraga.py
```

Cette commande vérifie la syntaxe, pas la qualité des coups ni le fonctionnement de la GUI. Avant une publication stable, vérifiez notamment : coups légaux, roque, en passant, promotions, échec et mat, pat, répétition, arrêt de recherche, sauvegarde/chargement JSON et fermeture propre de l'application.

## Limites importantes

- La profondeur maximale configurée n'est pas une promesse que chaque coup atteindra cette profondeur : le temps, le matériel et la complexité de la position comptent.
- Le score d'évaluation n'est pas un classement Elo officiel.
- L'adaptation JSON/statistique ne doit pas être décrite comme un réseau neuronal entraîné si aucun tel modèle n'est présent.
- Ne présentez pas « 2000 Elo » ou un autre niveau comme acquis sans un protocole de parties mesuré et reproductible.

## Structure

```text
Pandoraga-Full-Adaptation-Omega/
├── Pandoraga.py
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── .gitignore
├── run_windows.bat
├── docs/
│   ├── ARCHITECTURE.md
│   └── TESTS.md
├── tests/
│   └── test_syntax.py
└── .github/workflows/
    └── python-check.yml
```

## Licence

Voir `LICENSE`. Remplacez le détenteur du copyright par le nom ou l'organisation appropriée avant publication si nécessaire.
