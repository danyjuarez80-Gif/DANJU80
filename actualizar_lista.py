import os
import re

def procesar_listas_vercel():
    # Nombre del archivo original que descarga tu extractor
    archivo_origen = "dan88.m3u"
    
    if not os.path.exists(archivo_origen):
        print("ERROR: No se encontró dan88.m3u en la raíz del repositorio.")
        return

    print("Procesando lista: Vercel proxy para TV, enlaces originales para VOD...")
    
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Conservar la cabecera estándar M3U
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

            # 1. FILTRO PARA SERIES: Mantienen su enlace original directo
            if "/series" in linea_url_lower or 'group-title="series' in linea_inf_lower:
                listado_series.append(linea_inf)
                if linea_url: 
                    listado_series.append(linea_url)
                
            # 2. FILTRO PARA PELÍCULAS (VOD): Mantienen su enlace original directo
            elif "/movie" in linea_url_lower or ".mp4" in linea_url_lower or ".mkv" in linea_url_lower or "movie" in linea_inf_lower or "pelic" in linea_inf_lower:
                listado_movies.append(linea_inf)
                if linea_url: 
                    listado_movies.append(linea_url)
                
            # 3. EN VIVO (DANJU80): Aquí se aplica la magia para Vercel
            else:
                if linea_url:
                    # Extrae el ID numérico al final de la URL de Planet Web
                    match = re.search(r'/([^/]+)$', linea_url)
                    if match:
                        id_canal = match.group(1)
                        # Reemplaza por tu nuevo dominio en Vercel (con HTTPS)
                        linea_url = f"https://danju-80.vercel.app/{id_canal}"
                
                listado_tv.append(linea_inf)
                if linea_url: 
                    listado_tv.append(linea_url)
            
            i += 2
        else:
            i += 1

    # Guardar los archivos finales actualizados en tu repositorio
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_tv))
    
    with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_movies))
        
    with open("DANJU_SERIES", "w", encoding="utf-8") as f:
        f.write("\n".join(listado_series))

    print("¡Listas generadas con éxito apuntando a danju-80.vercel.app!")

if __name__ == "__main__":
    procesar_listas_vercel()
