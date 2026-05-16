import os
import urllib.request
import re

def obtener_ip_publica():
    try:
        # El script busca la IP en automático de internet, tú no haces nada
        with urllib.request.urlopen("https://api.ipify.org?format=text", timeout=10) as respuesta:
            ip = respuesta.read().decode("utf-8").strip()
            print(f"IP Pública detectada automáticamente: {ip}")
            return ip
    except Exception as e:
        print(f"Error al obtener la IP: {e}")
        return None

def segmentar_y_procesar_listas():
    archivo_origen = "dan88.m3u"
    
    if not os.path.exists(archivo_origen):
        print("ERROR: No se encontro dan88.m3u en la raiz.")
        return

    # Aquí el script obtiene la IP solito sin pedirte nada
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

            # Filtros súper flexibles para separar el VOD (Películas y Series)
            es_pelicula = (
                "/movie" in linea_url_lower or 
                ".mp4" in linea_url_lower or 
                ".mkv" in linea_url_lower or
                "movie" in linea_inf_lower or
                "pelic" in linea_inf_lower
            )
            
            es_serie = (
                "/series" in linea_url_lower or 
                "serie" in linea_inf_lower or
                "tvshow" in linea_inf_lower
            )

            if es_pelicula:
                # PELÍCULAS: Se quedan con el enlace original del proveedor
                listado_movies.append(linea_inf)
                if linea_url: listado_movies.append(linea_url)
            elif es_serie:
                # SERIES: Se quedan con el enlace original del proveedor
                listado_series.append(linea_inf)
                if linea_url: listado_series.append(linea_url)
            else:
                # LIVE TV: Aquí sí le metemos la IP que el script detectó en automático
                if mi_ip and linea_url:
                    linea_url = re.sub(r'(https?://)[^/:]+(:\d+)?', f'\\1{mi_ip}\\2', linea_url)
                
                listado_tv.append(linea_inf)
                if linea_url: listado_tv.append(linea_url)
            i += 2
        else:
            i += 1

    # Guardamos los 3 archivos limpios en tu raíz de GitHub
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_tv))

    with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_movies))

    with open("DANJU_SERIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_series))

    # Guardamos el archivo que lee tu Render
    with open("lista_canales_render.txt", "w", encoding="utf-8") as f:
        f.write("https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80")
    print("¡Todo automatizado con éxito!")

if __name__ == "__main__":
    segmentar_y_procesar_listas()
