import os
import re

def procesar_listas_vercel():
    # Nombre del archivo original actualizado a dany88.txt
    archivo_origen = "dany88.txt"
    
    if not os.path.exists(archivo_origen):
        print("ERROR: No se encontró dany88.txt en la raíz del repositorio.")
        return

    print("Procesando lista: Inyectando máscara de iPhone desde dany88.txt...")
    
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Conservar la cabecera estándar M3U
    cabecera = lineas[0] if lineas and lineas[0].startswith("#EXTM3U") else "#EXTM3U"

    listado_tv = [cabecera]
    listado_movies = [cabecera]
    listado_series = [cabecera]

    # La máscara mágica para que Roku engañe al servidor original
    mascara_iphone = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"

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

            # 1. FILTRO PARA SERIES: Mantienen enlace original + Máscara
            if "/series" in linea_url_lower or 'group-title="series' in linea_inf_lower:
                listado_series.append(linea_inf)
                listado_series.append(mascara_iphone)  # Inyecta máscara
                if linea_url: 
                    listado_series.append(linea_url)
                
            # 2. FILTRO PARA PELÍCULAS (VOD): Mantienen enlace original + Máscara
            elif "/movie" in linea_url_lower or ".mp4" in linea_url_lower or ".mkv" in linea_url_lower or "movie" in linea_inf_lower or "pelic" in linea_inf_lower:
                listado_movies.append(linea_inf)
                listado_movies.append(mascara_iphone
