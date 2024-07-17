# Réalisation du site TEI Publisher pour la diffusion de l'édition numérique du dictionnaire d'Alcedo.

### Description
Ce dossier contient l'ensemble des documents modifiés/créés dans le cadre de la création du site [TEI Publisher](https://teipublisher.com/exist/apps/tei-publisher-home/index.html).

Le site est organisé autour de deux fonctionnalités principales : 
- Dictionnaire d'Alcedo complet, mettant en parallèle les fascimilés et leurs transcriptions : https://sourcesetdonnees.huma-num.fr/exist/apps/topurbi-alcedo/index.html
- Représentation cartographique des données d'Alcedo avec une carte principale contenant l'ensemble des objets géographiques présenté dans le dictionnaire et une page de description pour chacun de ces lieux : https://sourcesetdonnees.huma-num.fr/exist/apps/topurbi-alcedo/carte/lieux.html?search=&category=A&view=all

### Éléments présent dans le dépôt
- `topurbi-alcedo/` : dossier contenant les documents modifiés/créés dans le cadre de la création du site.
    - `odd/` : dossier contenant les différentes ODD utilisées pour mettre en forme le texte.
    - `templates/`: dossier contenant les pages HTML créées/modifiées au sein du site.
    - `modules/`: dossier contenant les modules utilisés au sein du site : API, configuration générale et fonctions annexes.
- `topurbi-alcedo.zip` : instance TEI Publisher complète.