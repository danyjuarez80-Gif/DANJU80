import os

def procesar_lista_automatica():
    archivo_origen = "dan88.m3u"
    
    if not os.path.exists(archivo_origen):
        print("ERROR: No existe dan88.m3u en el repositorio.")
        return

    print("Abriendo lista original...")
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

            # Separador de Películas
            if "/movie" in linea_url_lower or ".mp4" in linea_url_lower or ".mkv" in linea_url_lower or "movie" in linea_inf_lower or "pelic" in linea_inf_lower:
                listado_movies.append(linea_inf)
                if linea_url: listado_movies.append(linea_url)
            
            # Separador de Series
            elif "/series" in linea_url_lower or "serie" in linea_inf_lower or "tvshow" in linea_inf_lower:
                listado_series.append(linea_inf)
                if linea_url: listado_series.append(linea_url)
            
            # Canales de TV en Vivo (Mantiene urls puros de Planet Web)
            else:
                listado_tv.append(linea_inf)
                if linea_url: listado_tv.append(linea_url)
            
            i += 2
        else:
            i += 1

    # Escritura en la raíz del repositorio
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_tv))
    
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_movies))
        
    with open("DANJU_SERIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_series))

    with open("lista_canales_render.txt", "w", encoding="utf-8") as f:
        f.write("https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80")
        
    print("¡Listas divididas con éxito!")

if __name__ == "__main__":
    procesar_lista_automatica()
