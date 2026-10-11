# Architecture (vue d'ensemble)

Le projet est livré sous forme d'un fichier Python principal afin de conserver le format monofichier de la version source.

- **Moteur** : représentation des positions, génération de coups, évaluation et recherche sont regroupées dans `Pandoraga.py`.
- **Recherche** : le code contient des mécanismes de recherche et de gestion du temps/de la profondeur. Consultez le code source pour les paramètres exacts.
- **Adaptation** : les données persistantes sont conservées localement dans un fichier JSON.
- **Interface** : l'interface graphique utilise Tkinter.
- **Stockfish** : l'intégration éventuelle utilise un moteur externe distinct ; Stockfish n'est pas inclus dans ce dépôt.

Cette documentation n'affirme pas que chaque fonction a fait l'objet d'une validation indépendante.
