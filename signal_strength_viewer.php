<?php 

$iwconfig = '/usr/sbin/airport -I'; 

while (1) { 
    $out = `$iwconfig`; 
    $outa = explode("\n", $out); 
    list( $key, $value ) = explode(':', $outa[0]);
    print str_repeat('+', -1* $value)."\n"; 
    usleep(100000); 
} 
?> 

