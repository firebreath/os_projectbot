<?php
/*
 * Copyright 2011 Richard Bateman
 *
 * Licensed under the New BSD License
 **/

$cathost = "127.0.0.1";
$catport = 54321;

$debug = true;

$input = file_get_contents("php://input", 1000000);
$value = json_decode($input, true);

if (isset($value["commits"])) {
    foreach ($commit as $value["commits"]) {
        $message = "Commit " . substr($commit["id"], 0, 7) . " by " . $commit["author"]["name"] . ": \"" . substr($commit["message"], 0, 60) . "\"";
        $message .= " " . $commit["url"];
        echo $message . "\n";
    }
}

function sendToCat($message) {
    $fs = fsockopen($cathost, $catport);
    fwrite($fs, $message . "\n");
    fclose($fs);
}
