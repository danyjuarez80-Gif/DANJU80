import re

def procesar_canales():
    archivo_entrada = "dan88.m3u"
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
    
    # Categoría por defecto por si el archivo empieza sin grupo
    group_actual = "VARIOS"
    
    for bloque in bloques:
        if not bloque.strip():
            continue
            
        lineas_bloque = bloque.strip().split("\n")
        if len(lineas_bloque) < 2:
            continue
            
        extinf_line = lineas_bloque[0]
        url_line = lineas_bloque[-1].strip()
        
        # Conseguir el nombre del canal o separador
        partes_cabecera = extinf_line.split(",")
        nombre_canal = partes_cabecera[-1].strip()
        
        # DETECTAR SI LA LÍNEA ES UN SEPARADOR VISUAL (Ej: ----DEPORTES----)
        if "---" in nombre_canal:
            nombre_limpio = nombre_canal.replace("-", "").replace("[", "").replace("]", "").strip()
            if nombre_limpio:
                group_actual = nombre_limpio
        else:
            # Si no es un separador, buscamos el group-title clásico
            match_group = re.search(r'group-title="([^"]+)"', extinf_line)
            if match_group:
                group_actual = match_group.group(1)

        # FILTRADO DE ENLACES: Pelis y series intactas, TV en vivo a tu Render
        if "/movie/" in url_line or "/series/" in url_line:
            nueva_url = url_line
        elif "planettvweb.com" in url_line:
            nueva_url = url_line.replace("http://planettvweb.com", url_render)
        else:
            nueva_url = url_line

        # CONSTRUIR LA CABECERA EN BASE A LA CATEGORÍA DETECTADA
        cabecera_limpia = re.sub(r'group-title="[^"]*"', '', extinf_line)
        meta_info = cabecera_limpia.split(",")[0].strip()
        
        extinf_final = f'#EXTINF:{meta_info.replace("#EXTINF:", "")} group-title="{group_actual}",{nombre_canal}'
        
        lineas_resultado.append(extinf_final + "\n")
        lineas_resultado.append(nueva_url + "\n\n")

    # Guardar ambos archivos en la raíz del repositorio
    with open(archivo_salida_1, 'w', encoding='utf-8') as f_out1:
        f_out1.writelines(lineas_resultado)
        
    with open(archivo_salida_2, 'w', encoding='utf-8') as f_out2:
        f_out2.writelines(lineas_resultado)
        
    print("¡Lista organizada por grupos reales para el Roku exitosamente!")

if __name__ == "__main__":
    procesar_canales()
