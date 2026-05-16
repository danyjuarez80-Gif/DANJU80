import re

def procesar_canales():
    archivo_entrada = "dan88.m3u"
    archivo_salida_1 = "lista_canales_render.txt"
    archivo_salida_2 = "DANJU80"
    
    url_render = "https://danju80.onrender.com"
    # La IP real de almacenamiento que sacamos de tu captura de pantalla
    url_storage_peliculas = "http://53.217.93:25461"
    
    lineas_resultado = ["#EXTM3U\n\n"]
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {archivo_entrada}")
        return

    bloques = content_blocks = contenido.split("#EXTINF:")
    print(f"Total de bloques detectados: {len(bloques) - 1}")
    
    for bloque in bloques:
        if not bloque.strip():
            continue
            
        lineas_bloque = bloque.strip().split("\n")
        if len(lineas_bloque) < 2:
            continue
            
        extinf_line = lineas_bloque[0]
        url_line = lineas_bloque[-1].strip()
        
        # 1. IDENTIFICAR LA CATEGORÍA ORIGINAL (group-title)
        match_group = re.search(r'group-title="([^"]+)"', extinf_line)
        if match_group:
            group_actual = match_group.group(1)
        else:
            group_actual = "VARIOS"

        # 2. CIRUGÍA INTELIGENTE DE ENLACES
        if "planettvweb.com:8091" in url_line:
            # Si es Película o Serie, cambiamos el dominio a la IP real de almacenamiento (Storage)
            if "/movie/" in url_line or "/series/" in url_line:
                nueva_url = url_line.replace("http://planettvweb.com:8091", url_storage_peliculas)
            else:
                # Si es Canal en Vivo, lo mandamos directo a tu Render
                nueva_url = url_line.replace("http://planettvweb.com:8091", url_render)
        else:
            nueva_url = url_line

        # 3. ARMAR CABECERA MANTENIENDO LAS CATEGORÍAS EN LA IZQUIERDA
        cabecera_limpia = re.sub(r'group-title="[^"]*"', '', extinf_line)
        partes_cabecera = cabecera_limpia.split(",")
        meta_info = partes_cabecera[0].strip()
        nombre_final = partes_cabecera[-1].strip()
        
        extinf_final = f'#EXTINF:{meta_info.replace("#EXTINF:", "")} group-title="{group_actual}",{nombre_final}'
        
        lineas_resultado.append(extinf_final + "\n")
        lineas_resultado.append(nueva_url + "\n\n")

    # Guardar ambos archivos simultáneos en tu GitHub
    with open(archivo_salida_1, 'w', encoding='utf-8') as f_out1:
        f_out1.writelines(lineas_resultado)
        
    with open(archivo_salida_2, 'w', encoding='utf-8') as f_out2:
        f_out2.writelines(lineas_resultado)
        
    print(f"¡Joyita lograda! Canales a Render y Pelis/Series directo a la IP real {url_storage_peliculas}")

if __name__ == "__main__":
    procesar_canales()
 re

def procesar_canales():
    archivo_entrada = "dan88.m3u"
    
    # Definimos los dos archivos de salida que quieres actualizar a la vez
    archivo_salida_1 = "lista_canales_render.txt"
    archivo_salida_2 = "DANJU80"
    
    url_render = "https://danju80.onrender.com"
    
    lineas_resultado = ["#EXTM3U\n\n"]
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {archivo_entrada}")
        return

    bloques = contenido.split("#EXTINF:")
    print(f"Total de bloques detectados: {len(bloques) - 1}")
    
    for bloque in bloques:
        if not bloque.strip():
            continue
            
        lineas_bloque = bloque.strip().split("\n")
        if len(lineas_bloque) < 2:
            continue
            
        extinf_line = lineas_bloque[0]
        url_line = lineas_bloque[-1].strip()
        
        # 1. IDENTIFICAR LA CATEGORÍA ORIGINAL (Ej: group-title="MEXICO")
        match_group = re.search(r'group-title="([^"]+)"', extinf_line)
        if match_group:
            group_actual = match_group.group(1)
        else:
            group_actual = "VARIOS"

        # 2. REDIRECCIÓN DE ENLACES A TU SERVIDOR RENDER
        if "planettvweb.com:8091" in url_line:
            nueva_url = url_line.replace("http://planettvweb.com:8091", url_render)
        else:
            nueva_url = url_line

        # 3. CONSTRUIR CABECERA MANTENIENDO LAS CATEGORÍAS ORIGINALES EN LA IZQUIERDA
        cabecera_limpia = re.sub(r'group-title="[^"]*"', '', extinf_line)
        partes_cabecera = cabecera_limpia.split(",")
        meta_info = partes_cabecera[0].strip()
        nombre_final = partes_cabecera[-1].strip()
        
        extinf_final = f'#EXTINF:{meta_info.replace("#EXTINF:", "")} group-title="{group_actual}",{nombre_final}'
        
        lineas_resultado.append(extinf_final + "\n")
        lineas_resultado.append(nueva_url + "\n\n")

    # GUARDAR EN EL PRIMER ARCHIVO (lista_canales_render.txt)
    with open(archivo_salida_1, 'w', encoding='utf-8') as f_out1:
        f_out1.writelines(lineas_resultado)
        
    # GUARDAR EN EL SEGUNDO ARCHIVO (DANJU80)
    with open(archivo_salida_2, 'w', encoding='utf-8') as f_out2:
        f_out2.writelines(lineas_resultado)
        
    print(f"¡Doble play logrado! Se actualizaron '{archivo_salida_1}' y '{archivo_salida_2}' con éxito.")

if __name__ == "__main__":
    procesar_canales()
