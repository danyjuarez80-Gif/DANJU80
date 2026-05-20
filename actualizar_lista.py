import os
import re

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print(f"ERROR: {archivo_origen} no encontrado.")
        return

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    cabecera = "#EXTM3U"
    tv, movies, series = [cabecera], [cabecera], [cabecera]

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            # Lógica de limpieza: elimina logos, imágenes y metadatos visuales
            linea_limpia = re.sub(r'tvg-logo=".*?"', '', linea)
            linea_limpia = re.sub(r'tvg-image=".*?"', '', linea_limpia)
            linea_limpia = re.sub(r'logo=".*?"', '', linea_limpia)
            linea_limpia = re.sub(r'\s+', ' ', linea_limpia).strip()
            
            url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            inf_low = linea_limpia.lower()
            url_low = url.lower()

            # Clasificación básica
            if "/series" in url_low or "series" in inf_low:
                series.extend([linea_limpia, url])
            elif "/movie" in url_low or "movie" in inf_low or "pelic" in inf_low:
                movies.extend([linea_limpia, url])
            else:
                tv.extend([linea_limpia, url])
            i += 2
        else:
            i += 1

    with open("DANJU80", "w", encoding="utf-8") as f: f.write("\n".join(tv))
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f: f.write("\n".join(movies))
    with open("DANJU_SERIES", "w", encoding="utf-8") as f: f.write("\n".join(series))
    print("Listas procesadas y limpias exitosamente.")

if __name__ == "__main__":
    procesar_listas()
