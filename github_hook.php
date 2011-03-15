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
        $message = "Commit " . substr($commit->id, 0, 7) . " by " . $commit->author->name . ": \"" . substr($commit->message, 0, 60) . "\"";
        $message .= " " . $commit->url;
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
