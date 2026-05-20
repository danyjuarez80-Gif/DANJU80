import os
import re

def procesar_listas_vercel():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen): return
    
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    cabecera = lineas[0] if lineas and lineas[0].startswith("#EXTM3U") else "#EXTM3U"
    listado_tv, listado_movies, listado_series = [cabecera], [cabecera], [cabecera]
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"

    i = 1
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            inf = linea
            url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            inf_low, url_low = inf.lower(), url.lower()

            if "/series" in url_low or 'series' in inf_low:
                listado_series.append(inf); listado_series.append(mascara); listado_series.append(url)
            elif "/movie" in url_low or ".mp4" in url_low or ".mkv" in url_low or "movie" in inf_low or "pelic" in inf_low:
                listado_movies.append(inf); listado_movies.append(mascara); listado_movies.append(url)
            else:
                listado_tv.append(inf); listado_tv.append(mascara); listado_tv.append(url)
            i += 2
        else:
            i += 1

    with open("DANJU80", "w", encoding="utf-8") as f: f.write("\n".join(listado_tv))
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f: f.write("\n".join(listado_movies))
    with open("DANJU_SERIES", "w", encoding="utf-8") as f: f.write("\n".join(listado_series))

if __name__ == "__main__":
    procesar_listas_vercel()
