import re

def procesar_canales():
    archivo_entrada = "dan88.txt"
    archivo_salida = "lista_canales_render.txt"
    url_render = "https://danju80.onrender.com"
    
    lineas_resultado = ["#EXTM3U\n\n"]
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.read()
    except FileNotFoundError:
        print("Error: No se encontro el archivo dan88.txt en el repositorio.")
        return

    # Separamos por bloques usando #EXTINF:
    bloques = contenido.split("#EXTINF:")
    print(f"Total de bloques detectados: {len(bloques) - 1}")
    
    for bloque in bloques:
        if not bloque.strip():
            continue
            
        lineas_bloque = bloque.strip().split("\n")
        if len(lineas_bloque) < 2:
            continue
            
        # Reconstruimos la cabecera del canal
        extinf_line = "#EXTINF:" + lineas_bloque[0]
        # La última línea siempre contiene la URL
        url_line = lineas_bloque[-1].strip()
        
        # FILTRO CRÍTICO: Si detecta que es película o serie, la ignora por completo
        if "/movie/" in url_line or "/series/" in url_line:
            continue
            
        # Si contiene la IP y puerto viejo, reestructuramos el link
        if "planettvweb.com:8091" in url_line:
            id_match = re.search(r'/(\d+)$', url_line)
            if id_match and id_match.group(1) is not None:
                id_canal = id_match.group(1)
                nueva_url = f"{url_render}/canal/{id_canal}"
            else:
                # Si la URL viene rara o con texto extra, extrae la última parte limpiamente
                id_limpio = url_line.split("/")[-1]
                nueva_url = f"{url_render}/canal/{id_limpio}"
        else:
            # Si el canal es un enlace externo (Pluto TV, etc.), se conserva idéntico
            nueva_url = url_line
            
        # Guardamos la info del canal y el nuevo link con formato /canal/ID
        lineas_resultado.append(extinf_line + "\n")
        lineas_resultado.append(nueva_url + "\n\n")

    with open(archivo_salida, 'w', encoding='utf-8') as f_out:
        f_out.writelines(lineas_resultado)
        
    print(f"¡Proceso completado! Se generó '{archivo_salida}' con éxito.")

if __name__ == "__main__":
    procesar_canales()
