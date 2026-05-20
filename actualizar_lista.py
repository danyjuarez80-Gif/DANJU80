import os
import re

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print("Error: dan88.txt no encontrado")
        return

    mascara_vlc = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    tv, movies, series = ["#EXTM3U"], ["#EXTM3U"], ["#EXTM3U"]

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    i = 0
    while i < len(lineas):
        if lineas[i].startswith("#EXTINF"):
            linea_inf = lineas[i]
            linea_url = lineas[i+1] if i + 1 < len(lineas) else ""
            info_low = linea_inf.lower()
            url_low = linea_url.lower()

            # Clasificación robusta
            if any(x in info_low or x in url_low for x in ["series", "s01", "s02", "s03", "s04", "s05", "episodio"]):
                # Agrupación para VLC
                if 'group-title=' not in linea_inf:
                    linea_inf = linea_inf.replace("#EXTINF:-1", '#EXTINF:-1 group-title="Series"')
                series.extend([linea_inf, mascara_vlc, linea_url])
            
            elif any(ext in url_low for ext in [".mp4", ".mkv", ".avi", "/movie"]):
                movies.extend([linea_inf, mascara_vlc, linea_url])
            
            else:
                tv.extend([linea_inf, mascara_vlc, linea_url])
            i += 2
        else:
            i += 1

    with open("DANJU80", "w", encoding="utf-8") as f: f.write("\n".join(tv))
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
