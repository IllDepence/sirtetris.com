<?php

require_once('/homez.151/sirtetri/www/keys.php');
$valid_files = array('output.png','kanji.dat');
$fn = $_FILES['data']['name'];

if (in_array($fn, $valid_files) && ($_POST['token'] == $stats_token)) {
    if ($_FILES['data']['error'] > 0) {
        echo 'Return Code: '.$_FILES['data']['error'];
        }
    else {
        $fn = ($fn == 'output.png' ? 'kanjistats.png' : $fn);
        move_uploaded_file($_FILES['data']['tmp_name'], getcwd().'/'.$fn);
        echo 'Done '.$fn;
        }
    }
else {
    echo 'Invalid file or key';
    }

?>
