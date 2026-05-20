import os

def procesar_listas_vercel():
    archivo_origen = "dan88.txt"
    
    if not os.path.exists(archivo_origen):
        print(f"ERROR: No se encontró {archivo_origen}")
        return
    
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    cabecera = "#EXTM3U"
    listado_tv = [cabecera]
    listado_movies = [cabecera]
    listado_series = [cabecera]

    i = 1
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            linea_inf = linea
            linea_url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            
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

    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_tv))
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_movies))
    with open("DANJU_SERIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_series))

if __name__ == "__main__":
    procesar_listas_vercel()
