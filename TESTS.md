# Plan de tests avant publication stable

- [ ] Le fichier se compile avec la version Python annoncée.
- [ ] L'interface s'ouvre et se ferme sans exception.
- [ ] La position initiale contient 20 coups légaux.
- [ ] Les coups illégaux sont refusés.
- [ ] Roque côté roi et côté dame correctement validés.
- [ ] Prise en passant validée et invalidée dans les cas appropriés.
- [ ] Promotions, y compris promotion en échec, correctement traitées.
- [ ] Échec, mat, pat et répétition correctement détectés.
- [ ] Recherche interrompue proprement après la limite de temps.
- [ ] La mémoire JSON se sauvegarde et se recharge ; JSON corrompu géré sans plantage.
- [ ] Plusieurs parties successives ne mélangent pas leurs historiques.
- [ ] Mode Stockfish testé uniquement si disponible.
- [ ] Force du moteur mesurée avec un protocole documenté, pas estimée à partir de la profondeur.
