import re

def procesar_canales():
    archivo_entrada = "dan88.m3u"
    archivo_salida = "lista_canales_render.txt"
    url_render = "https://danju80.onrender.com"
    
    lineas_resultado = ["#EXTM3U\n\n"]
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {archivo_entrada}")
        return

    # Separamos el archivo completo por bloques de canales
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
        
        # 1. IDENTIFICAR LA CATEGORÍA ORIGINAL POR DEFECTO
        # Buscamos el group-title original (ej. group-title="MEXICO")
        match_group = re.search(r'group-title="([^"]+)"', extinf_line)
        if match_group:
            group_actual = match_group.group(1)
        else:
            group_actual = "VARIOS"

        # 2. REDIRECCIÓN UNIVERSAL DE ENLACES A TU SERVIDOR RENDER
        # Modificamos la IP vieja en canales, películas o series para que apunten a tu Render
        if "planettvweb.com:8091" in url_line:
            nueva_url = url_line.replace("http://planettvweb.com:8091", url_render)
        else:
            nueva_url = url_line

        # 3. CONSTRUIR CABECERA LIMPIA RE-INYECTANDO SU CATEGORÍA ORIGINAL
        # Limpiamos duplicados para asegurar que el Roku lea el group-title sin problemas
        cabecera_limpia = re.sub(r'group-title="[^"]*"', '', extinf_line)
        partes_cabecera = cabecera_limpia.split(",")
        meta_info = partes_cabecera[0].strip()
        nombre_final = partes_cabecera[-1].strip()
        
        # Formateamos la línea manteniendo la info original y su categoría intacta
        extinf_final = f'#EXTINF:{meta_info.replace("#EXTINF:", "")} group-title="{group_actual}",{nombre_final}'
        
        lineas_resultado.append(extinf_final + "\n")
        lineas_resultado.append(nueva_url + "\n\n")

    with open(archivo_salida, 'w', encoding='utf-8') as f_out:
        f_out.writelines(lineas_resultado)
        
    print(f"¡Proceso terminado! Lista idéntica y redirigida en {archivo_salida}")

if __name__ == "__main__":
    procesar_canales()
