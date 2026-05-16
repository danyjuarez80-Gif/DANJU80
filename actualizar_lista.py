import os
import re

def procesar_listas_final():
    archivo_origen = "dan88.m3u"
    
    if not os.path.exists(archivo_origen):
        print("ERROR: No se encontro dan88.m3u en la raiz.")
        return

    print("Procesando lista: Render proxy para TV, enlaces originales para VOD...")
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

            # 1. Filtro para Series (Se quedan con IP y enlace ORIGINAL)
            if "/series" in linea_url_lower or 'group-title="series' in linea_inf_lower:
                listado_series.append(linea_inf)
                if linea_url: listado_series.append(linea_url)
                
            # 2. Filtro para Películas (Se quedan con IP y enlace ORIGINAL)
            elif "/movie" in linea_url_lower or ".mp4" in linea_url_lower or ".mkv" in linea_url_lower or "movie" in linea_inf_lower or "pelic" in linea_inf_lower:
                listado_movies.append(linea_inf)
                if linea_url: listado_movies.append(linea_url)
                
            # 3. EN VIVO (DANJU80): Aquí SÍ aplicamos la máscara de tu Render
            else:
                if linea_url:
                    # Extraemos el número final del canal (ej. 12816)
                    match = re.search(r'/([^/]+)$', linea_url)
                    if match:
                        id_canal = match.group(1)
                        # Reemplazamos el enlace por tu Render proxy
                        linea_url = f"https://danju80.onrender.com/{id_canal}"
                
                listado_tv.append(linea_inf)
                if linea_url: listado_tv.append(linea_url)
            
            i += 2
        else:
            i += 1

    # Guardamos los archivos actualizados en tu GitHub
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_tv))
    
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_movies))
        
    with open("DANJU_SERIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_series))

    # Dejamos listo el puente de Render
    with open("lista_canales_render.txt", "w", encoding="utf-8") as f:
        f.write("https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80")
        
    print("¡Proceso terminado con las reglas solicitadas!")

if __name__ == "__main__":
    procesar_listas_final()
