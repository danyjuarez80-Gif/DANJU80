<?php
// Desactivamos errores para que la app lea limpio
error_reporting(0);
set_time_limit(0);

// Limpiamos la ruta para saber qué pide la app
$ruta = trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/');
$id_canal = str_replace('.ts', '', $ruta);

// 1. SI LA RUTA ESTÁ VACÍA: Descarga y escupe tu lista de GitHub
if (empty($id_canal) || !is_numeric($id_canal)) {
    $github = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80";
    $lista = file_get_contents($github);
    
    header("HTTP/1.1 200 OK");
    header("Content-Type: audio/x-mpegurl; charset=utf-8");
    header("Content-Disposition: inline; filename=\"lista.m3u\"");
    echo $lista;
    exit();
}

// 2. SI PIDES UN CANAL: Hacemos el túnel directo usando la IP limpia
$url_original = "http://53.217.93.1:8091/PtaPta567/user8790/" . $id_canal;

header("HTTP/1.1 200 OK");
header("Content-Type: video/mp2t");
header("Cache-Control: no-cache, must-revalidate");
header("Pragma: no-cache");

// Nos disfrazamos de VLC para saltar bloqueos de Planet TV
$opciones = [
    "http" => [
        "method" => "GET",
        "header" => "User-Agent: VLC/3.0.18 LibVLC/3.0.18\r\n"
    ]
];
$contexto = stream_context_create($opciones);
$fp = fopen($url_original, 'rb', false, $contexto);

if ($fp) {
    while (!feof($fp) && (connection_status() == 0)) {
        echo fread($fp, 8192); // Transmitimos bloques de 8KB directos a tu pantalla
        flush();
    }
    fclose($fp);
}
exit();
?>
