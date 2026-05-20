import os

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print("Archivo origen no encontrado")
        return

    mascara_vlc = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    tv, movies, series = ["#EXTM3U"], ["#EXTM3U"], ["#EXTM3U"]

    # Leer el archivo línea por línea
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = [l.strip() for l in f if l.strip()]

    # Procesar bloques detectando el patrón de Planetweb
    i = 0
    while i < len(lineas) - 1:
        if lineas[i].startswith("#EXTINF"):
            info = lineas[i]
            # Buscar la URL en la siguiente línea o línea cercana
            url = ""
            for j in range(i+1, min(i+4, len(lineas))):
                if lineas[j].startswith("http"):
                    url = lineas[j]
                    break
            
            if url:
                # Construir el bloque perfecto de 3 líneas
                bloque = [info, mascara_vlc, url]
                
                # Clasificación mejorada
                inf_low = info.lower()
                url_low = url.lower()
                
                if "series" in url_low or "s0" in inf_low or "episodio" in inf_low:
                    series.extend(bloque)
                elif "movie" in url_low or "movie" in inf_low:
                    movies.extend(bloque)
                else:
                    tv.extend(bloque)
            i += 1
        else:
            i += 1

    # Guardar archivos
    for nombre, lista in [("DANJU80", tv), ("DANJU_MOVIES", movies), ("DANJU_SERIES", series)]:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write("\n".join(lista))

if __name__ == "__main__":
    procesar_listas()
