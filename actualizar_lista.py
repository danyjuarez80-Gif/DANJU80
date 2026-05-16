import re

def procesar_canales():
    # Nombre exacto de tu archivo M3U
    archivo_entrada = "dan88.m3u"
    archivo_salida = "lista_canales_render.txt"
    url_render = "https://danju80.onrender.com"
    
    lineas_resultado = ["#EXTM3U\n\n"]
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {archivo_entrada} en tu repositorio.")
        return

    # Separamos el archivo por bloques usando #EXTINF:
    bloques = contenido.split("#EXTINF:")
    print(f"Total de bloques detectados: {len(bloques) - 1}")
    
    for bloque in bloques:
        if not bloque.strip():
            continue
            
        lineas_bloque = bloque.strip().split("\n")
        if len(lineas_bloque) < 2:
            continue
            
        extinf_line = "#EXTINF:" + lineas_bloque[0]
        url_line = lineas_bloque[-1].strip()
        
        # Filtro estricto: Eliminamos peliculas y series del archivo final
        if "/movie/" in url_line or "/series/" in url_line:
            continue
            
        # Cambiamos las IPs viejas por tu formato /canal/ID de Render
        if "planettvweb.com:8091" in url_line:
            id_match = re.search(r'/(\d+)$', url_line)
            if id_match and id_match.group(1) is not None:
                id_canal = id_match.group(1)
                nueva_url = f"{url_render}/canal/{id_canal}"
            else:
                id_limpio = url_line.split("/")[-1]
                nueva_url = f"{url_render}/canal/{id_limpio}"
        else:
            nueva_url = url_line
            
        # Guardamos el canal manteniendo su categoria intacta
        lineas_resultado.append(extinf_line + "\n")
        lineas_resultado.append(nueva_url + "\n\n")

    with open(archivo_salida, 'w', encoding='utf-8') as f_out:
        f_out.writelines(lineas_resultado)
        
    print(f"¡Listo! Se proceso tu archivo {archivo_entrada} y se genero {archivo_salida}")

if __name__ == "__main__":
    procesar_canales()
