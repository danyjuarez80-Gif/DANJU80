import os
import urllib.request
import re

def obtener_ip_publica():
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=text", timeout=10) as respuesta:
            ip = respuesta.read().decode("utf-8").strip()
            print(f"IP Pública detectada con éxito: {ip}")
            return ip
    except Exception as e:
        print(f"Error al obtener la IP: {e}")
        return None

def segmentar_y_procesar_listas():
    archivo_origen = "dan88.m3u"
    
    if not os.path.exists(archivo_origen):
        print("ERROR: No se encontro dan88.m3u en la raiz del repositorio.")
        return

    mi_ip = obtener_ip_publica()

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

            # BÚSQUEDA MEJORADA Y ULTRA FLEXIBLE:
            # Detecta "movie", "movies", "pelicula", "películas", ".mp4", ".mkv"
            es_pelicula = (
                "/movie" in linea_url_lower or 
                "movie" in linea_inf_lower or 
                "pelic" in linea_inf_lower or 
                ".mp4" in linea_url_lower or 
                ".mkv" in linea_url_lower
            )
            
            # Detectes "series", "serie", "tvshows"
            es_serie = (
                "/series" in linea_url_lower or 
                "serie" in linea_inf_lower or 
                "tvshow" in linea_inf_lower
            )

            if es_pelicula:
                # PELÍCULAS: Enlace puro original (sin tocarle la IP)
                listado_movies.append(linea_inf)
                if linea_url: listado_movies.append(linea_url)
            elif es_serie:
                # SERIES: Enlace puro original (sin tocarle la IP)
                listado_series.append(linea_inf)
                if linea_url: listado_series.append(linea_url)
            else:
                # LIVE TV: Forzamos el reemplazo de tu IP pública en la URL del canal en vivo
                if mi_ip and linea_url:
                    linea_url = re.sub(r'(https?://)[^/:]+(:\d+)?', f'\\1{mi_ip}\\2', linea_url)
                
                listado_tv.append(linea_inf)
                if linea_url: listado_tv.append(linea_url)
            i += 2
        else:
            i += 1

    # Guardamos los 3 archivos sueltos en la raíz
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_tv))
    print("¡DANJU80 (En vivo) guardado!")

    with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_movies))
    print("¡DANJU_MOVIES (Películas) guardado!")

    with open("DANJU_SERIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_series))
    print("¡DANJU_SERIES (Series) guardado!")

    # Sincronización para Render
    with open("lista_canales_render.txt", "w", encoding="utf-8") as f:
        f.write("https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80")

if __name__ == "__main__":
    segmentar_y_procesar_listas()
