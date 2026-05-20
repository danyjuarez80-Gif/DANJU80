import os

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen): return

    mascara_vlc = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    tv, movies, series = ["#EXTM3U"], ["#EXTM3U"], ["#EXTM3U"]

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    i = 0
    while i < len(lineas):
        if lineas[i].startswith("#EXTINF"):
            linea_inf = lineas[i]
            linea_url = lineas[i+1] if i + 1 < len(lineas) else ""
            
            # --- CORRECCIÓN CRÍTICA DE ESTRUCTURA ---
            # Si detectamos que es una serie, inyectamos group-title para VLC
            if "series" in linea_url.lower() or "s0" in linea_inf.lower():
                if 'group-title=' not in linea_inf:
                    linea_inf = linea_inf.replace("#EXTINF:-1", '#EXTINF:-1 group-title="Series"')
                series.extend([linea_inf, mascara_vlc, linea_url])
            
            # Clasificación de películas
            elif any(ext in linea_url.lower() for ext in [".mp4", ".mkv", "/movie"]):
                movies.extend([linea_inf, mascara_vlc, linea_url])
            
            # Clasificación de canales TV
            else:
                tv.extend([linea_inf, mascara_vlc, linea_url])
            
            i += 2
        else:
            i += 1

    # Guardado obligatorio con la estructura de 3 líneas
    with open("DANJU80", "w", encoding="utf-8") as f: f.write("\n".join(tv))
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f: f.write("\n".join(movies))
    with open("DANJU_SERIES", "w", encoding="utf-8") as f: f.write("\n".join(series))

if __name__ == "__main__":
    procesar_listas()
