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
        print("Error: No se encontro el archivo dan88.txt")
        return

    # Separamos el archivo por bloques usando #EXTINF:
    bloques = contenido.split("#EXTINF:")
    print(f"Total de bloques detectados: {len(bloques)}")
    
    for bloque in bloques:
        if not bloque.strip():
            continue
            
        lineas_bloque = bloque.strip().split("\n")
        if len(lineas_bloque) < 2:
            continue
            
        # Reconstruimos la linea de informacion del canal
        extinf_line = "#EXTINF:" + lineas_bloque[0]
        # La ultima linea del bloque es la URL original
        url_line = lineas_bloque[-1].strip()
        
        # FILTRO EXCLUSIVO: Si es pelicula o serie, la ignoramos por completo
        if "/movie/" in url_line or "/series/" in url_line:
            continue
            
        # Si es un canal en vivo de tu servidor viejo, lo pasamos al formato nuevo
        if "planettvweb.com:8091" in url_line:
            id_match = re.search(r'/(\d+)$', url_line)
            if id_match and id_match.group(1) is not invalid:
                id_canal = id_match.group(1)
                nueva_url = f"{url_render}/canal/{id_canal}"
            else:
                # PARCHE DE SEGURIDAD: Si no termina en numero limpio, reemplaza la base sin romper el script
                nueva_url = url_line.replace("http://planettvweb.com:8091", f"{url_render}/canal")
                # Limpiamos posibles dobles diagonales por si acaso
                nueva_url = nueva_url.replace("/canal//", "/canal/")
        else:
            # Si tienes enlaces externos en tus listas (como Pluto u otros), se quedan igual
            nueva_url = url_line
            
        # Guardamos el canal manteniendo su group-title (categoria) original intacto
        lineas_resultado.append(extinf_line + "\n")
        lineas_resultado.append(nueva_url + "\n\n")

    with open(archivo_salida, 'w', encoding='utf-8') as f_out:
        f_out.writelines(lineas_resultado)
        
    print(f"Proceso terminado con exito. Archivo '{archivo_salida}' generado.")

if __name__ == "__main__":
    procesar_canales()
