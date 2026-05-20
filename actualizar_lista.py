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

    i = 1
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            linea_inf = linea
            linea_url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            
            # Clasificación sin agregar ninguna máscara
            inf_low = linea_inf.lower()
            url_low = linea_url.lower()

            if "/series" in url_low or 'series' in inf_low:
                listado_series.append(linea_inf)
                if linea_url: listado_series.append(linea_url)
            elif "/movie" in url_low or ".mp4" in url_low or ".mkv" in url_low or "movie" in inf_low or "pelic" in inf_low:
                listado_movies.append(linea_inf)
                if linea_url: listado_movies.append(linea_url)
            else:
                listado_tv.append(linea_inf)
                if linea_url: listado_tv.append(linea_url)
            
            i += 2
        else:
            i += 1

    # Guardado forzando el reemplazo total
    def guardar_limpio(nombre, lista):
        with open(nombre, "w", encoding="utf-8") as f:
            f.truncate(0) # Vacía el archivo por completo
            f.write("\n".join(lista))

    guardar_limpio("DANJU80", listado_tv)
    guardar_limpio("DANJU_MOVIES", listado_
