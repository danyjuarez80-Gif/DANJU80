import os
import re

def procesar_listas_vercel():
    archivo_origen = "dan88.txt"
    
    if not os.path.exists(archivo_origen):
        print(f"ERROR: No se encontró {archivo_origen}")
        return
    
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Logos por categoría (puedes cambiar las URLs)
    logo_tv = 'tvg-logo="https://i.imgur.com/tv_icon.png"'
    logo_movies = 'tvg-logo="https://i.imgur.com/movie_icon.png"'
    logo_series = 'tvg-logo="https://i.imgur.com/series_icon.png"'

    def obtener_nueva_linea(linea_inf, logo):
        """Reconstruye la línea para asegurar que tenga el logo."""
        # Limpiamos la línea eliminando atributos tvg-logo previos si existen
        limpia = re.sub(r'tvg-logo=".*?"', '', linea_inf).strip()
        # Aseguramos que tenga el formato #EXTINF:-1 y le inyectamos el logo
        if limpia.startswith("#EXTINF"):
            return limpia.replace("#EXTINF", f"#EXTINF:-1 {logo}")
        return linea_inf

    cabecera = "#EXTM3U"
    listado_tv = [cabecera]
    listado_movies = [cabecera]
    listado_series = [cabecera]

    i = 0 # Corregido a 0 para asegurar lectura total
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            linea_url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            inf_low = linea.lower()
            url_low = linea_url.lower()

            if "/series" in url_low or 'series' in inf_low:
                linea_final = obtener_nueva_linea(linea, logo_series)
                listado_series.extend([linea_final, linea_url])
            elif "/movie" in url_low or ".mp4" in url_low or ".mkv" in url_low or "movie" in inf_low or "pelic" in inf_low:
                linea_final = obtener_nueva_linea(linea, logo_movies)
                listado_movies.extend([linea_final, linea_url])
            else:
                linea_final = obtener_nueva_linea(linea, logo_tv)
                listado_tv.extend([linea_final, linea_url])
            i += 2
        else:
            i += 1

    with open("DANJU80", "w", encoding="utf-8") as f: f.write("\n".join(listado_tv))
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f: f.write("\n".join(listado_movies))
    with open("DANJU_SERIES", "w", encoding="utf-8") as f: f.write("\n".join(listado_series))

if __name__ == "__main__":
    procesar_listas_vercel()
