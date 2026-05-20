import os
import re

def procesar_listas_vercel():
    archivo_origen = "dan88.txt"
    
    if not os.path.exists(archivo_origen):
        print(f"ERROR: No se encontró {archivo_origen}")
        return
    
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    cabecera = lineas[0] if lineas and lineas[0].startswith("#EXTM3U") else "#EXTM3U"

    listado_tv = [cabecera]
    listado_movies = [cabecera]
    listado_series = [cabecera]

    mascara_iphone = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"

    i = 1
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            linea_inf = linea
            linea_url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            
            linea_inf_lower = linea_inf.lower()
            linea_url_lower = linea_url.lower()

            # 1. FILTRO PARA SERIES (Sin máscara)
            if "/series" in linea_url_lower or 'group-title="series' in linea_inf_lower:
                listado_series.append(linea_inf)
                if linea_url: listado_series.append(linea_url)
                
            # 2. FILTRO PARA PELÍCULAS (Sin máscara)
            elif "/movie" in linea_url_lower or ".mp4" in linea_url_lower or ".mkv" in linea_url_lower or "movie" in linea_inf_lower or "pelic" in linea_inf_lower:
                listado_movies.append(linea_inf)
                if linea_url: listado_movies.append(linea_url)
                
            # 3. EN VIVO (DANJU80): Con máscara incluida
            else:
                listado_tv.append(linea_inf)
                listado_tv.append(mascara_iphone)
                if linea_url: listado_tv.append(linea_url)
            
            i += 2
        else:
            i += 1

    with open("DANJU80", "w", encoding="utf-8") as f: f.write("\n".join(listado_tv))
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f: f.write("\n".join(listado_movies))
    with open("DANJU_SERIES", "w", encoding="utf-8") as f: f.write("\n".join(listado_series))

if __name__ == "__main__":
    procesar_listas_vercel()
