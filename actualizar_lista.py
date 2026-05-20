import os
import re

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        return

    mascara_vlc = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    listado_tv, listado_movies, listado_series = ["#EXTM3U"], ["#EXTM3U"], ["#EXTM3U"]

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    i = 0
    while i < len(lineas):
        if lineas[i].startswith("#EXTINF"):
            linea_inf = lineas[i]
            linea_url = lineas[i+1] if i + 1 < len(lineas) else ""
            
            # --- LÓGICA DE CLASIFICACIÓN Y AGRUPACIÓN ---
            
            # 1. Series: Intentamos extraer el nombre para el group-title
            if "series" in linea_url.lower() or "s0" in linea_inf.lower() or "episodio" in linea_inf.lower():
                # Extraer nombre para agrupar (limpieza básica del nombre)
                nombre_serie = "Series"
                match = re.search(r',(.+?) S\d', linea_inf)
                if match:
                    nombre_serie = match.group(1).strip()
                
                # Insertar group-title para que VLC separe por serie
                if 'group-title="' not in linea_inf:
                    linea_inf = linea_inf.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{nombre_serie}"')
                
                listado_series.extend([linea_inf, mascara_vlc, linea_url])

            # 2. Películas
            elif any(ext in linea_url.lower() for ext in [".mp4", ".mkv", ".avi", "/movie"]):
                listado_movies.extend([linea_inf, mascara_vlc, linea_url])
            
            # 3. TV en vivo
            else:
                listado_tv.extend([linea_inf, mascara_vlc, linea_url])
            
            i += 2
        else:
            i += 1

    # Guardado con nombres originales sin extensión
    with open("DANJU80", "w", encoding="utf-8") as f: f.write("\n".join(listado_tv))
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f: f.write("\n".join(listado_movies))
    with open("DANJU_SERIES", "w", encoding="utf-8") as f: f.write("\n".join(listado_series))

if __name__ == "__main__":
    procesar_listas()
