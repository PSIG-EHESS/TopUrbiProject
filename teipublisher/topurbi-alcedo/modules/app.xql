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
    
    (: RECUP TEXTE :)
    
    let $vol-id := (doc($config:data-root || $vol)//tei:div//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../../@xml:id,
        doc($config:data-root || $vol)/tei:div//tei:superEntry//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../../@xml:id)
        
    let $path_text := 
        if (doc($config:data-root || $vol)//tei:div[@n='toponyms']//tei:entry[@xml:id=$vol-id]) then "//text//body//div[@n='toponyms']//entry[@xml:id='"||$vol-id||"']//sense"
        else if (doc($config:data-root || $vol)/tei:back//tei:div[@n="corrections"]//tei:superEntry//tei:entry//tei:entry[@xml:id=$vol-id]) then "//text//back//div[@n='corrections']//superEntry//entry[@xml:id='"||$vol-id||"']"
        else "//text//back//div[@n='corrections']//entry[@xml:id='"||$vol-id||"']//sense"
    
    (: RECUP CORR :)
    
    let $id_corr_temp := ($cas//tei:link[@type="entry"]/following-sibling::tei:link[@type="entry"]/@target)[1]
    let $id_corr := tokenize($id_corr_temp, '#')[2]
    
    (: TEXTE BRUT :let $text_corr := 
        if ($id_corr) then "Correction :"||doc($config:data-root || $vol)//tei:div//tei:entry[@xml:id=$id_corr]//tei:sense
        else "":)
        
    let $path_corr := 
        if (doc($config:data-root || $vol)/tei:back//tei:div[@n="corrections"]//tei:div//tei:superEntry//tei:entry//tei:entry[@xml:id=$id_corr]) then "//text//back//div[@n='corrections']//div//superEntry//entry[@xml:id="||$id_corr||"]//sense"
        else if (doc($config:data-root || $vol)//tei:back//tei:div[@n="corrections"]//tei:div//tei:entry[@xml:id=$id_corr]) then "//text//back//div[@n='corrections']//div//entry[@xml:id='"||$id_corr||"']//sense"
        (: Pour le volume 4, correction sont dans description des toponymes. 1 cas?:)
        else if (doc($config:data-root ||"/Alcedo_vol_4.xml")//tei:div[@n='toponyms']//tei:entry[@xml:id=$id_corr]) then "//text//body//div[@n='toponyms']//entry[@xml:id='"||$id_corr||"']//sense"
         (: Pour le volume 5, correction sont dans description des toponymes. 1 cas? :)
        else if (doc($config:data-root ||"/Alcedo_vol_5.xml")//tei:div[@n='toponyms']//tei:entry[@xml:id=$id_corr]) then "//text//body//div[@n='toponyms']//entry[@xml:id='"||$id_corr||"']//sense"
        (: Vides pour ceux qui n'ont pas de correction avec un cas pour chaque volume:)
        else if (doc($config:data-root || $vol)//tei:div[@n='toponyms']//tei:entry[@xml:id='id_00659a']) then "//text//body//div[@n='toponyms']//entry[@xml:id='id_00659a']//fs//f[@name='region']"
        else if (doc($config:data-root || $vol)//tei:div[@n='toponyms']//tei:entry[@xml:id='id_05355']) then "//text//body//div[@n='toponyms']//entry[@xml:id='id_05355']//fs//f[@name='region']"
        else if (doc($config:data-root || $vol)//tei:div[@n='toponyms']//tei:entry[@xml:id='id_09255']) then "//text//body//div[@n='toponyms']//entry[@xml:id='id_09255']//fs//f[@name='region']"
        else if (doc($config:data-root || $vol)//tei:div[@n='toponyms']//tei:entry[@xml:id='id_11904']) then "//text//body//div[@n='toponyms']//entry[@xml:id='id_11904']//fs//f[@name='region']"
        else "//text//body//div[@n='toponyms']//entry[@xml:id='id_15475']//fs//f[@name='region']"
    
    (: TEXTE BRUT :let $text := (doc($config:data-root || $vol)//tei:div//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../..//tei:sense,
        doc($config:data-root || $vol)/tei:div//tei:superEntry//tei:entry//tei:fs//tei:f[@name='PlaceID' and @fVal=$name]/../..//tei:sense):)


    return
       map {
            "title": $title,
            "key":$geo,
            "latitude": replace($geo-token[1],',','.'),
            "longitude": replace($geo-token[2],',','.'),
            (:  :"text": $text,:)
            "id": $name,
            "path_text" : $path_text,
            "vol_id" : "'"||$vol-id||"'",
            "id_corr" :  "'"||$id_corr||"'",
            "path_corr" : $path_corr,
            "vol" : $vol
        }
        
};