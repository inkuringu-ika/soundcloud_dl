<?php
//Warning: This program is pre-release and may be unstable.
//Copyright (c) 2020 inkuringu-ika
//This software is released under the GPL3.0 License, see LICENSE.txt.


header("Content-Type: text/plan");

$input = $_GET["url"];



//テスト用
//$client_id = "00000000000000000000000000000000";

//有効期限がある
//$client_id = "L1Tsmo5VZ0rup3p9fjY67862DyPiWGaG";

//こっちのほうが有効期限長いかも?
$client_id = "LBCcHmRB8XSStWL6wKH2HPACspQlXg2P";



$json1 = file_get_contents("https://soundcloud.com/oembed?format=json&url=".$input);

$json1 = json_decode($json1, true);

$html = $json1["html"];

$id = strstr($html, 'tracks%2F');

$id = strstr($id, '&', true);

$id = str_replace("tracks%2F", "", $id);

$json2 = file_get_contents("https://api-v2.soundcloud.com/tracks?ids=".$id."&client_id=".$client_id);

$json2 = json_decode($json2, true);

//$json2[0]["downloadable"]
//$json2[0]["has_downloads_left"]

if($json2[0]["downloadable"] and $json2[0]["has_downloads_left"]){

echo $json2[0]["download_url"]."?client_id=".$client_id;

}else{

$json_url = $json2[0]["media"]["transcodings"][1]["url"]."?client_id=".$client_id;

$json3 = file_get_contents($json_url);

$json3 = json_decode($json3, true);

echo $json3["url"];

};

?>