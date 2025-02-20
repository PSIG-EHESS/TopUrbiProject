# Réalisation du site TEI Publisher pour la diffusion de l'édition numérique du dictionnaire d'Alcedo.

### Description
Ce dossier contient l'ensemble des documents modifiés/créés dans le cadre de la création du site [TEI Publisher](https://teipublisher.com/exist/apps/tei-publisher-home/index.html).

Le site est organisé autour de deux fonctionnalités principales : 
- Dictionnaire d'Alcedo complet, mettant en parallèle les fascimilés et leurs transcriptions : https://sourcesetdonnees.huma-num.fr/exist/apps/topurbi-alcedo/index.html
- Représentation cartographique des données d'Alcedo avec une carte principale contenant l'ensemble des objets géographiques présentés dans le dictionnaire et une page de description pour chacun de ces lieux : https://sourcesetdonnees.huma-num.fr/exist/apps/topurbi-alcedo/carte/lieux.html?search=&category=A&view=all

### Éléments présents dans le dépôt
- `topurbi-alcedo/` : dossier contenant les documents modifiés/créés dans le cadre de la création du site.
    - `odd/` : dossier contenant les différentes ODD utilisées pour mettre en forme le texte.
        - __`teipublisher.odd`__ : ODD Tei Publisher modifié. Les modifications concernent les éléments `<term>` (hover avec définition), `<district>` (lien vers la page lieu) et `<idno>` (suppression de l'affichage des liens externes vers le thésaurus).
        - __`places.odd`__ : ODD créé pour les extraits de manuscrit dans les pages `place.html`, déclaré dans `config.xqm`, inutilisé pour le moment.
    - `templates/`: dossier contenant les pages HTML créées/modifiées au sein du site.
        - __`home.html`__ : _Template_ d'une page d'accueil avec titre, images et liens vers les autres pages du site (en travaux :construction:).
        - __`footer.html`__ : Modification texte "Contact".
        - __`places2.html`__ : _Template_ de la page "carte" contenant la carte principale  `<pb-leaflet-map>` ainsi que la liste des lieux `<pb-split-list>`. Les informations de la carte sont requêtées par l'API `api:places-all` définie dans le document __`custom-api.xql`__. Les informations de la liste sont requêtées par l'API `api:places` définie dans le document __`custom-api.xql`__.  Le tri de la liste selon les catégories "lieux" et "groupes humains" et la barre de recherche sont définis dans le _web component_ `<pb-custom-form>` et dans la `<div class="radios">`. La `<div class="loading-message">` permet de faire apparaître un message de chargement tant que la requête n'est pas terminée. 
        - __`place.html`__ : _Template_ des pages de description des lieux. Au moment de la définition de la page, on appelle la fonction `app:load-place` à laquelle on fournit le paramètre `name` qui est l'identifiant du lieu dans l'index : `<html data-template="app:load-place" data-template-name="${name}">`. Cette fonction nous permet de récupérer les informations sur les lieux pour les afficher ensuite en texte brut ou bien au sein des _web components_ `<pb-view>` qui appellent les parties des manuscrits correspondantes.
    - `modules/`: dossier contenant les modules utilisés au sein du site : API, configuration générale et fonctions annexes.
        - __`config.xqm`__ : fichier qui contient les configurations générales de l'instance. Les modifications principales sont : 
            - `declare variable $config:default-view :="page";` : modification de la manière dont le texte des manuscrits est présenté.
            - `declare variable $config:default-template :="alcedo_facs.html";` : modification du _template_ d'affichage du manuscrit.
            - `declare variable $config:data-exclude := doc($config:data-root || "/taxonomy.xml")//tei:text, doc($config:data-root || "/TopUrbiIndex_completo.xml")//tei:text,doc($config:data-root || "/TopUrbiIndex_old01072024.xml")//tei:text,doc($config:data-root || "/id_00005.xml")//tei:text,doc($config:data-root || "/imagemapping.xml")//tei:text,doc($config:data-root || "/placestest.xml")//tei:text,collection($config:register-root)//tei:text;` : documents qui n'apparaissent pas dans la section corpus (`index.html`).
            - `declare variable $config:odd-available :=("teipublisher.odd", "places.odd");` : ajout d'une seconde ODD personnalisée.
        - __`app.xml`__ : création d'une fonction `app:load-place` qui permet de récupérer des informations dans les documents xml et les afficher dans les pages HTML (utilisée dans la page `place.html`). Repose sur des requêtes en xQuery. À partir du @xml:id du lieu, elle récupère : son nom, ses coordonnées géographiques, le numéro du volume, le texte du volume décrivant le lieu et les corrections associées.
        - __`custom-api.xql`__ : création de différentes requêtes API pour récupérer les informations dans les documents xml et les appeler dans les pages HTML.
            - Fonction `api:places-all` : à partir des données de `TopUrbiIndex.xml`, renvoie un dictionnaire qui contient le nom du lieu, son identifiant, sa latitude et sa longitude (permet d'afficher les lieux sur la carte principale de la page `places2.html`).
            - Fonction `api:places` : Permet de créer la liste de lieux utilisée dans la page `places2.html`. Récupère le nom d'un lieu et ses coordonnées selon la recherche et selon la catégorie sélectionnée (paramètre `view`qui peut être "lieux", "groupes humains" ou "lieux et groupes humains"). Récupère l'ordre alphabétique des lieux et renvoie un dictionnaire créé au sein de la fonction `api:output-place`.
            - Fonction `api:output-place` : fonction appelée au sein de `api:places`. En fonction des paramètres fournis `category` (lettre selectionnée), `view` (type) et `search` (recherche utilisateur), renvoie un bloc HTML contenant les informations des lieux et le lien de la page `place.html`.
        - __`custom-api.json`__ : document JSON qui contient les paramètres des requêtes API ainsi que les URL des pages HTML. 
- `topurbi-alcedo.zip` : instance TEI Publisher complète.