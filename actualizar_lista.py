import os
import re

def procesar_listas_vercel():
    # Busca exactamente "dan88.txt" en la raíz
    archivo_origen = "dan88.txt"
    
    if not os.path.exists(archivo_origen):
        print(f"ERROR: No se encontró {archivo_origen} en la raíz del repositorio.")
        return

    print(f"Procesando lista: Inyectando máscara de iPhone y eliminando contenido 4K...")
    
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Conservar la cabecera estándar M3U
    cabecera = lineas[0] if lineas and lineas[0].startswith("#EXTM3U") else "#EXTM3U"

    listado_tv = [cabecera]
    listado_movies = [cabecera]
    listado_series = [cabecera]

    # La máscara mágica para que Roku engañe al servidor original
    mascara_iphone = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"

    # Palabras clave que delatan que una película o serie es 4K
    palabras_4k = ["4k", "uhd", "2160p", "[4k]", "(4k)"]

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

            # Comprobar si el título contiene alguna palabra clave de 4K
            es_contenido_4k = any(palabra in linea_inf_lower for palabra in palabras_4k)

            # 1. FILTRO PARA SERIES
            if "/series" in linea_url_lower or 'group-title="series' in linea_inf_lower:
                if not es_contenido_4k:  # Solo pasa si NO es 4K
                    listado_series.append(linea_inf)
                    listado_series.append(mascara_iphone)
                    if linea_url: 
                        listado_series.append(linea_url)
                else:
                    print(f"-> Saltando Serie 4K por incompatibilidad: {linea_inf[:50]}...")
                
            # 2. FILTRO PARA PELÍCULAS (VOD)
            elif "/movie" in linea_url_lower or ".mp4" in linea_url_lower or ".mkv" in linea_url_lower or "movie" in linea_inf_lower or "pelic" in linea_inf_lower:
                if not es_contenido_4k:  # Solo pasa si NO es 4K
                    listado_movies.append(linea_inf)
                    listado_movies.append(mascara_iphone)
                    if linea_url: 
                        listado_movies.append(linea_url)
                else:
                    print(f"-> Saltando Película 4K por incompatibilidad: {linea_inf[:50]}...")
                
            # 3. EN VIVO (DANJU80): Canales de TV directo (Aquí no filtramos resolución)
            else:
                listado_tv.append(linea_inf)
                listado_tv.append(mascara_iphone)
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

    print(f"¡Proceso terminado con éxito!")
    print(f"Películas listas: {len(listado_movies) // 3} | Series listas: {len(listado_series) // 3}")

if __name__ == "__main__":
    procesar_listas_vercel()
