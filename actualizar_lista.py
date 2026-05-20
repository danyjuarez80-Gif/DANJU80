import os

def procesar_listas_vercel():
    archivo_origen = "dan88.txt"
    
    if not os.path.exists(archivo_origen):
        print(f"ERROR: No se encontró {archivo_origen}")
        return

    # Esta máscara es la que permite que VLC "engañe" al servidor haciéndose pasar por un iPhone
    mascara_vlc = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    palabras_4k = ["4k", "uhd", "2160p", "[4k]", "(4k)"]

    def guardar_lista(nombre_archivo, lista):
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("\n".join(lista))

    listado_tv, listado_movies, listado_series = ["#EXTM3U"], ["#EXTM3U"], ["#EXTM3U"]

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    i = 0
    while i < len(lineas):
        if lineas[i].startswith("#EXTINF"):
            linea_inf = lineas[i]
            linea_url = lineas[i+1] if i + 1 < len(lineas) else ""
            
            # Filtro 4K
            if any(p in linea_inf.lower() for p in palabras_4k):
                i += 2
                continue

            # Construcción del bloque de 3 líneas obligatorio para VLC
            bloque = [linea_inf, mascara_vlc, linea_url]

            # Clasificación
            if "/series" in linea_url.lower() or 'group-title="series' in linea_inf.lower():
                listado_series.extend(bloque)
            elif any(x in linea_url.lower() for x in [".mp4", ".mkv", "/movie"]):
                listado_movies.extend(bloque)
            else:
                listado_tv.extend(bloque)
            
            i += 2
        else:
            i += 1

    guardar_lista("DANJU80.m3u", listado_tv)
    guardar_lista("DANJU_MOVIES.m3u", listado_movies)
    guardar_lista("DANJU_SERIES.m3u", listado_series)
    print("¡Listas generadas correctamente con formato VLC!")

if __name__ == "__main__":
    procesar_listas_vercel()
