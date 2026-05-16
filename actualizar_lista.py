import os

def segmentar_listas():
    archivo_origen = "dan88.m3u"
    
    if not os.path.exists(archivo_origen):
        print("ERROR: No se encontro dan88.m3u en la raiz.")
        return

    print("Leyendo archivo base dan88.m3u...")
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
            linea_url = ""
            if i + 1 < len(lineas):
                linea_url = lineas[i + 1].strip()
            
            linea_inf_lower = linea_inf.lower()
            linea_url_lower = linea_url.lower()

            # Clasificación estricta
            es_pelicula = "/movie/" in linea_url_lower or 'group-title="películas"' in linea_inf_lower or ".mp4" in linea_url_lower or ".mkv" in linea_url_lower
            es_serie = "/series/" in linea_url_lower or 'group-title="series"' in linea_inf_lower

            if es_pelicula:
                listado_movies.append(linea_inf)
                if linea_url: listado_movies.append(linea_url)
            elif es_serie:
                listado_series.append(linea_inf)
                if linea_url: listado_series.append(linea_url)
            else:
                listado_tv.append(linea_inf)
                if linea_url: listado_tv.append(linea_url)
            i += 2
        else:
            i += 1

    # Guardar los 3 archivos de texto independientes en tu raíz
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_tv))
    print("¡Archivo DANJU80 (En vivo) generado!")

    with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_movies))
    print("¡Archivo DANJU_MOVIES (Películas) generado!")

    with open("DANJU_SERIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_series))
    print("¡Archivo DANJU_SERIES (Series) generado!")

    # Actualizar tu enlace de Render
    with open("lista_canales_render.txt", "w", encoding="utf-8") as f:
        f.write("https://raw.githubusercontent.com/damjuarez80-Gif/DANJU80/main/DANJU80")

if __name__ == "__main__":
    segmentar_listas()
