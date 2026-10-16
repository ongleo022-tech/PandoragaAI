NETTOYAGE PROPOSÉ POUR LE DÉPÔT

Objectif: garder le repo propre et facile à maintenir. Ci‑dessous une liste
de recommandations et un plan d'action. Exécuter manuellement ou valider et
je peux appliquer les changements (création d'une branche + commits).

Fichiers à conserver (suggestion):
- Pandoraga_2GB.py
- Pandoraga.py
- Pandoraga_8GB.py
- tools/arena.py
- tools/elo_tournament.py (optionnel, utile pour simulation rapide)
- tools/get.py (outil CLI)
- requirements.txt
- run_scripts/*
- .github/workflows/arena.yml

Fichiers à archiver ou supprimer (à valider):
- fichiers temporaires ou essais multiples (messages d'erreur créés automatiquement)
- copies locales non désirées (*.py~ , *~)

Plan d'action proposé:
1) Créer une branche "clean/restructure" avec les suppressions/archives. (je peux le faire si tu confirmes)
2) Déplacer les fichiers historiques/obsolètes dans un répertoire `archive/` avec une note README.
3) Mettre à jour le README principal pour documenter comment lancer l'arène et installer les dépendances.
4) Ajouter un .gitignore pour ignorer les environnements virtuels et fichiers temporaires.

Commande utile locale (à exécuter sur ta machine):
  git checkout -b clean/restructure
  mkdir archive && git mv <files> archive/
  git commit -m "chore: archive obsolete files"
  git push -u origin clean/restructure

Si tu veux que j'applique automatiquement l'archivage dans le dépôt (je crée la branche et déplace les fichiers), dis "oui archive" et indique la liste exacte des fichiers à archiver si tu veux contrôler. Si tu préfères que je n'archive rien automatiquement, dis "non, juste créer les scripts et workflow".
