xquery version "3.1";

(:~
 : This is the place to import your own XQuery modules for either:
 :
 : 1. custom API request handling functions
 : 2. custom templating functions to be called from one of the HTML templates
 
 :)
 
module namespace api="http://teipublisher.com/api/custom";
declare namespace tei="http://www.tei-c.org/ns/1.0";

(: Add your own module imports here :)
import module namespace rutil="http://e-editiones.org/roaster/util";
import module namespace app="teipublisher.com/app" at "app.xql";
import module namespace config="http://www.tei-c.org/tei-simple/config" at "config.xqm";
import module namespace vapi="http://teipublisher.com/api/view" at "lib/api/view.xql";

(:~
 : Keep this. This function does the actual lookup in the imported modules.
 :)
declare function api:lookup($name as xs:string, $arity as xs:integer) {
    try {
        function-lookup(xs:QName($name), $arity)
    } catch * {
        ()
    }
};

(:~
 : LBL Ensemble de fonctions nécessaires à la création d'une carte avec index. :)

declare function api:places-all($request as map(*)) {
    let $places := 
        (doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:place,
        doc($config:data-root || "/TopUrbiIndex.xml")//tei:listOrg//tei:org)
    return 
      array { 
            for $place in $places
               let $test := 
                    if ($place/tei:settlement/tei:location/tei:geo) then $place/tei:settlement/tei:location/tei:geo
                    else if ($place/tei:geogName/tei:location/tei:geo) then $place/tei:geogName/tei:location/tei:geo
                    else if ($place/tei:district/tei:location/tei:geo) then $place/tei:district/tei:location/tei:geo
                    else $place/tei:location/tei:geo
                let $tokenized := tokenize($test)
                let $id := 
                    if ($place/@xml:id/string()) then $place/@xml:id/string()
                    else $place/tei:orgName/@xml:id/string()
                
                let $placename := 
                    if ($place/tei:settlement/tei:placeName/string()) then $place/tei:settlement/tei:placeName/string()
                    else if ($place/tei:geogName/tei:placeName/string()) then $place/tei:geogName/tei:placeName/string()
                    else if ($place/tei:district/tei:placeName/string()) then $place/tei:district/tei:placeName/string()
                    else $place//tei:orgName/tei:name/string()
                    
                let $view := 
                    if ($place/tei:settlement/tei:placeName/string()) then "place"
                    else if ($place/tei:geogName/tei:placeName/string()) then "place"
                    else if ($place/tei:district/tei:placeName/string()) then "place"
                    else "org"
                    
                return 
                    map {
                        "latitude": replace($tokenized[1],',','.'),
                        "longitude": replace($tokenized[2],',','.'),
                        "label":$placename,
                        "id":$id,
                        "view" : $view
                    }
                    
            }  
};

declare function api:places($request as map(*)) {
    let $search := normalize-space($request?parameters?search)(: Nom du lieu est le paramètre search de l'API :)
    let $letterParam := $request?parameters?category (: Lettre est le paramètre catagory de l'API :)
    let $view := $request?parameters?view
    let $limit := $request?parameters?limit
    
     (: let $places :=
        if ($search and $search != '') then
            (doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:settlement/tei:placeName[matches(string(.), "^" || $search, "i")],
            doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:district/tei:placeName[matches(string(.), "^" || $search, "i")],
            doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:geogName/tei:placeName[matches(string(.), "^" || $search, "i")],
            doc($config:data-root || "/TopUrbiIndex.xml")//tei:listOrg//tei:org//tei:orgName/tei:name[matches(string(.), "^" || $search, "i")])
                 
        else
            (doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:settlement/tei:placeName, 
             doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:district/tei:placeName, 
             doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:geogName/tei:placeName, 
             doc($config:data-root || "/TopUrbiIndex.xml")//tei:listOrg//tei:org//tei:orgName/tei:name) 

     VERSION API pour avoir liste selectionnable, NON FONCTIONNEL :)
    
        let $places :=
            if ($view = "org") then 
                 if ($search and $search != '') then
                    doc($config:data-root || "/TopUrbiIndex.xml")//tei:listOrg/tei:org/tei:orgName/tei:name[matches(string(.), "^" || $search, "i")]
                 else
                     doc($config:data-root || "/TopUrbiIndex.xml")//tei:listOrg/tei:org/tei:orgName/tei:name
                     
            else if ($view = "place") then 
                if ($search and $search != '') then
                    (doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:settlement/tei:placeName[matches(string(.), "^" || $search, "i")],
                    doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:district/tei:placeName[matches(string(.), "^" || $search, "i")],
                    doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:geogName/tei:placeName[matches(string(.), "^" || $search, "i")])
                         
                else
                    (doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:settlement/tei:placeName, 
                     doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:district/tei:placeName, 
                     doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:geogName/tei:placeName)
            
            else 
                if ($search and $search != '') then
                (doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:settlement/tei:placeName[matches(string(.), "^" || $search, "i")],
                doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:district/tei:placeName[matches(string(.), "^" || $search, "i")],
                doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:geogName/tei:placeName[matches(string(.), "^" || $search, "i")],
                doc($config:data-root || "/TopUrbiIndex.xml")//tei:listOrg/tei:org/tei:orgName/tei:name[matches(string(.), "^" || $search, "i")])
                 
            else
                (doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:settlement/tei:placeName, 
                 doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:district/tei:placeName, 
                 doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:geogName/tei:placeName, 
                 doc($config:data-root || "/TopUrbiIndex.xml")//tei:listOrg/tei:org/tei:orgName/tei:name) 
                 
    let $sorted := sort($places, "?lang=es-ES", function($place){lower-case($place/string())})
    let $letter := 
        if (count($places) < $limit) then "All"
        else if ($letterParam = '') then substring($sorted[1], 1, 1) => upper-case()
        else $letterParam
    let $byLetter :=
        if ($letter = 'All') then $sorted
        else
            filter($sorted, function($entry) {
                starts-with(lower-case($entry), lower-case($letter))
            })
    return
        map {
            "items": api:output-place($byLetter, $letter, $view, $search),
            "categories":
                if (count($places) < $limit) then
                    []
                else array {
                    for $index in 1 to string-length('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                    let $alpha := substring('ABCDEFGHIJKLMNOPQRSTUVWXYZ', $index, 1)
                    let $hits := count(filter($sorted, function($entry) {starts-with(lower-case($entry/string()), lower-case($alpha))}))
                    where $hits > 0
                    return
                        map {
                            "category": $alpha,
                            "count": $hits
                        },
                    map {
                        "category": "All",
                        "count": count($sorted)
                    }
                }
        }
};

declare function api:output-place($list, $category as xs:string, $view as xs:string, $search as xs:string?) {
    array {
        for $place in $list
            let $categoryParam := if ($category = "all") then substring($place, 1, 1) else $category
            let $params := "category="||$categoryParam||"&amp;view="||$view||"&amp;search="||$search
            let $label := $place/string()
            let $coords := (tokenize($place/../../tei:location/tei:geo),
                            tokenize($place/../tei:location/tei:geo))
            let $id := ($place/../../@xml:id,
                        $place/../@xml:id)
            
            (:  LBL Réfléchir à créer un dump point pour les lieux qui n'ont pas de coordonnées ou les enlever de la liste (mais n'apparaitront pas du tout ? :)
            
            return
                <span class="place">
                    <a href="place.html?name={$id}">{$label}</a>
                    <pb-geolocation latitude="{replace($coords[1],',','.')}" longitude="{replace($coords[2],',','.')}" label="{$label}" id="{$id}" zoom="7" emit="map" event="click">
                        <iron-icon icon="maps:map"></iron-icon>
                    </pb-geolocation>
                </span>
    }
};