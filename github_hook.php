<?php
/*
 * Copyright 2011 Richard Bateman
 *
 * Licensed under the New BSD License
 **/

$cathost = "127.0.0.1";
$catport = 54321;

$debug = true;

$input = $_POST["payload"];
$value = json_decode($input);

if ($debug) {
    $f = fopen("/tmp/github_hook.log", "w");
    fwrite($f, $input);
    fclose($f);
}
if (isset($value->commits)) {
    foreach ($value->commits as $commit) {
        $url = new goo_gl($commit->url);
        $message = "Commit " . substr($commit->id, 0, 7) . " by " . $commit->author->name . ": \"" . substr($commit->message, 0, 60) . "\"";
        $message .= " " . $url->result();
        sendToCat($message . "\n");
    }
}

function sendToCat($message) {
    global $cathost, $catport;
    echo "Trying to connect to $cathost : $catport";
    $fs = fsockopen($cathost, $catport);
    fwrite($fs, $message . "\n");
    fclose($fs);
}

/* 
API Google URL Shortner - goo.gl 
Marcus Nunes - marcusnunes.com - 9/18/2010

eg:
$googl = new goo_gl('http://marcusnunes.com');
echo $googl->result();
*/

class goo_gl{
    
    var $url, $resul;
    
    //goo.gl construct method
    function goo_gl($url){
        
        $this->url = $url;
        
        $curl = curl_init(); 
        curl_setopt($curl, CURLOPT_URL, 'http://goo.gl/api/url'); 
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1); 
        curl_setopt($curl, CURLOPT_POST, 1); 
        curl_setopt($curl, CURLOPT_POSTFIELDS, 'user=toolbar@google.com&url='.urlencode($this->url).'&auth_token='.$this->googlToken($url)); 
        $saida = curl_exec($curl); 
        curl_close($curl);
        if($saida){
            $json = json_decode($saida);
            $this->resul = $json->short_url;
        }
    }
    
    //show url shorted by goo.gl
    function result(){
        return $this->resul;
    }
    
    //token code
    function googlToken($b){
        $i = $this->tke($b);
        $i = $i >> 2 & 1073741823;
        $i = $i >> 4 & 67108800 | $i & 63;
        $i = $i >> 4 & 4193280 | $i & 1023;
        $i = $i >> 4 & 245760 | $i & 16383;
        $j = "7";
        $h = $this->tkf($b);
        $k = ($i >> 2 & 15) << 4 | $h & 15;
        $k |= ($i >> 6 & 15) << 12 | ($h >> 8 & 15) << 8;
        $k |= ($i >> 10 & 15) << 20 | ($h >> 16 & 15) << 16;
        $k |= ($i >> 14 & 15) << 28 | ($h >> 24 & 15) << 24;
        $j .= $this->tkd($k);
        return $j;
    }

    function tkc(){
        $l = 0;
        foreach(func_get_args() as $val){
            $val &= 4294967295;
            $val += $val > 2147483647 ? -4294967296 : ($val < -2147483647 ? 4294967296 : 0);
            $l   += $val;
            $l   += $l > 2147483647 ? -4294967296 : ($l < -2147483647 ? 4294967296 : 0);
        }
        return $l;
    }

    function tkd($l){
        $l = $l > 0 ? $l : $l + 4294967296;
        $m = "$l";  //deve ser uma string
        $o = 0;
        $n = false;
        for($p = strlen($m) - 1; $p >= 0; --$p){
            $q = $m[$p];
            if($n){
                $q *= 2;
                $o += floor($q / 10) + $q % 10;
            } else {
                $o += $q;
            }
            $n = !$n;
        }
        $m = $o % 10;
        $o = 0;
        if($m != 0){
            $o = 10 - $m;
            if(strlen($l) % 2 == 1){
                if ($o % 2 == 1){
                    $o += 9;
                }
                $o /= 2;
            }
        }
        return "$o$l";
    }

    function tke($l){
        $m = 5381;
        for($o = 0; $o < strlen($l); $o++){
            $m = $this->tkc($m << 5, $m, ord($l[$o]));
        }
        return $m;
    }

    function tkf($l){
        $m = 0;
        for($o = 0; $o < strlen($l); $o++){
            $m = $this->tkc(ord($l[$o]), $m << 6, $m << 16, -$m);
        }
        return $m;
    }
        
}
    

