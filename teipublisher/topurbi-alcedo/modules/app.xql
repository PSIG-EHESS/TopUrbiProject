xquery version "3.1";

(: 
 : Module for app-specific template functions
 :
 : Add your own templating functions here, e.g. if you want to extend the template used for showing
 : the browsing view.
 :)
 
module namespace app="teipublisher.com/app";

import module namespace templates="http://exist-db.org/xquery/html-templating";
import module namespace config="http://www.tei-c.org/tei-simple/config" at "config.xqm";

declare namespace tei="http://www.tei-c.org/ns/1.0";

declare
    %templates:wrap
function app:foo($node as node(), $model as map(*)) {
    <p>Dummy templating function.</p>
};

(:~
 : List documents in data collection
 :)

declare
    %templates:wrap
function app:load-place($node as node(), $model as map(*), $name as xs:string) {

    let $geo := (doc($config:data-root || "/TopUrbiIndex.xml")//tei:listPlace//tei:place[@xml:id=xmldb:decode($name)],
        doc($config:data-root || "/TopUrbiIndex.xml")//tei:listOrg//tei:org//tei:orgName[@xml:id=xmldb:decode($name)]) 
    (: dès là ne fonctionne pas :)
    
    let $cas :=
        if ($geo/tei:settlement) then $geo/tei:settlement
        else if ($geo/tei:district) then $geo/tei:district
        else if ($geo/tei:geogName) then $geo/tei:geogName
        else $geo/..
        
    let $title := 
        if ($cas/tei:orgName/tei:name) then $cas/tei:orgName/tei:name/string()
        else $cas/tei:placeName/string()

    let $geo-token := tokenize($cas/tei:location/tei:geo) (:  Ajouter un cas si pas de geo ? Dump point ? :)
    
    let $vol_ := $cas//tei:linkGrp/tei:link[@type="page"]/@facs
    
    let $vol- := tokenize($vol_, ':')[2]
    
    let $vol := '/'||tokenize($vol-, '-')[1]||'.xml'
    
    (: TEXTE BRUT :let $text := (doc($config:data-root || $vol)//tei:div//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../..//tei:sense,
        doc($config:data-root || $vol)/tei:div//tei:superEntry//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../..//tei:sense):)
        
    (:  :let $vol-id := (doc($config:data-root || "/Alcedo_vol_1.xml")//tei:div//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../../@xml:id,
        doc($config:data-root || "/Alcedo_vol_1.xml")/tei:div//tei:superEntry//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../../@xml:id):)
    
    let $vol-id := (doc($config:data-root || $vol)//tei:div//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../../@xml:id,
        doc($config:data-root || $vol)/tei:div//tei:superEntry//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../../@xml:id)

    return
       map {
            "title": $title,
            "key":$geo,
            "latitude": replace($geo-token[1],',','.'),
            "longitude": replace($geo-token[2],',','.'),
            (:  :"text": $text,:)
            "id": $name,
            (:  :"path" : $path,:)
            "vol_id" : "'"||$vol-id||"'",
            "vol" : $vol
        }
        
};