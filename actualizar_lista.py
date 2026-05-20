import os
import re

def procesar_listas_vercel():
    archivo_origen = "dan88.txt"
    
    if not os.path.exists(archivo_origen):
        print(f"ERROR: No se encontró {archivo_origen}")
        return
    
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    def limpiar_linea_inf(linea_inf):
        """Elimina todos los atributos de logo e imagen de la línea #EXTINF."""
        # Elimina: tvg-logo, tvg-image, logo, y atributos comunes de metadatos
        linea_limpia = re.sub(r'tvg-logo=".*?"', '', linea_inf)
        linea_limpia = re.sub(r'tvg-image=".*?"', '', linea_limpia)
        linea_limpia = re.sub(r'logo=".*?"', '', linea_limpia)
        
        # Limpieza final: asegura que no queden espacios dobles y mantenga el formato
        linea_limpia = re.sub(r'\s+', ' ', linea_limpia).strip()
        return linea_limpia

    cabecera = "#EXTM3U"
    listado_tv = [cabecera]
    listado_movies = [cabecera]
    listado_series = [cabecera]

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            linea_url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            inf_low = linea.lower()
            url_low = linea_url.lower()

            # Limpiamos la línea de metadatos visuales antes de clasificar
            linea_final = limpiar_linea_inf(linea)

            if "/series" in url_low or 'series' in inf_low:
                listado_series.extend([linea_final, linea_url])
            elif "/movie" in url_low or ".mp4" in url_low or ".mkv" in url_low or "movie" in inf_low or "pelic" in inf_low:
                listado_movies.extend([linea_final, linea_url])
            else:
                listado_tv.extend([linea_final, linea_url])
            i += 2
        else:
            i += 1

    # Guardado de archivos sin logos
    with open("DANJU_TV.m3u", "w", encoding="utf-8") as f: f.write("\n".join(listado_tv))
    with open("DANJU_MOVIES.m3u", "w", encoding="utf-8") as f: f.write("\n".join(listado_movies))
    with open("DANJU_SERIES.m3u", "w", encoding="utf-8") as f: f.write("\n".join(listado_series))
    print("Procesamiento completado: Archivos limpios generados.")

if __name__ == "__main__":
    procesar_listas_vercel()
