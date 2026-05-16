import os

def procesar_lista_directa():
    archivo_origen = "dan88.m3u"
    
    if not os.path.exists(archivo_origen):
        print("ERROR: No se encontro dan88.m3u en la raiz.")
        return

    print("Leyendo lista pura de Planet Web...")
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

            # DETECCIÓN BASADA EN TU FORMATO REAL (Captura 86310)
            # Si el enlace termina directo en número o tiene /live/ es TV en vivo
            es_live = "/live" in linea_url_lower or (linea_url and linea_url[-1].isdigit() and not linea_url_lower.endswith((".mp4", ".mkv", ".avi")))

            if es_live:
                # Canales en vivo: Directos a DANJU80 con su IP de Planet Web
                listado_tv.append(linea_inf)
                if linea_url: listado_tv.append(linea_url)
            elif "/series" in linea_url_lower or "group-title=\"series" in linea_inf_lower:
                # Series originales
                listado_series.append(linea_inf)
                if linea_url: listado_series.append(linea_url)
            else:
                # Por descarte, si no es live ni serie, va a películas (VOD)
                listado_movies.append(linea_inf)
                if linea_url: listado_movies.append(linea_url)
            
            i += 2
        else:
            i += 1

    # Guardar cambios a la brava en los archivos físicos
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_tv))
    
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_movies))
        
    with open("DANJU_SERIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_series))

    with open("lista_canales_render.txt", "w", encoding="utf-8") as f:
        f.write("https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80")
        
    print("¡Sincronización terminada de forma exitosa!")

if __name__ == "__main__":
    procesar_lista_automatica = procesar_lista_directa()
