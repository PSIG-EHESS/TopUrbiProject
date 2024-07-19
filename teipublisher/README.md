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
        - `config.xqm` : fichier qui contient les configurations générales de l'instance. Les modifications principales sont : 
            - `declare variable $config:default-view :="page";` : modification de la manière dont le texte des manuscrits est présenté.
            - `declare variable $config:default-template :="alcedo_facs.html";` : modification du _template_ d'affichage du manuscrit.
            - `declare variable $config:data-exclude := doc($config:data-root || "/taxonomy.xml")//tei:text, doc($config:data-root || "/TopUrbiIndex_completo.xml")//tei:text, collection($config:register-root)//tei:text;` : documents qui n'apparaissent pas dans la section corpus (`index.html`).
            - `declare variable $config:odd-available :=("teipublisher.odd", "places.odd");` : ajout d'une seconde ODD personnalisée.
        - `app.xml` : création d'une fonction `app:load-place` qui permet de récupérer des informations dans les documents xml pour les afficher dans les pages html (utilisée dans la page `place.html`). Repose sur des requêtes en xQuery. À partir du @xml:id du lieu, elle récupère : son nom, ses coordonnées géographiques, le numéro du volume, le texte du volume décrivant le lieu et les corrections associées.
        - `` : 
        - `` : 
- `topurbi-alcedo.zip` : instance TEI Publisher complète.