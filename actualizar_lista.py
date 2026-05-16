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
        print(f"Error: No se encontro el archivo {archivo_entrada} en tu repositorio.")
        return

    bloques = contenido.split("#EXTINF:")
    print(f"Total de bloques detectados: {len(bloques) - 1}")
    
    for bloque in bloques:
        if not bloque.strip():
            continue
            
        lineas_bloque = block_lines = bloque.strip().split("\n")
        if len(lineas_bloque) < 2:
            continue
            
        extinf_line = "#EXTINF:" + lineas_bloque[0]
        url_line = lineas_bloque[-1].strip()
        
        # REEMPLAZO DIRECTO Y UNIVERSAL:
        # No importa si es canal, serie o película, si tiene la IP vieja, se redirige a tu Render
        if "planettvweb.com:8091" in url_line:
            nueva_url = url_line.replace("http://planettvweb.com:8091", url_render)
        else:
            nueva_url = url_line
            
        # Mantenemos la cabecera idéntica para que "PELICULAS" y "SERIES" salgan en su propia sección
        lineas_resultado.append(extinf_line + "\n")
        lineas_resultado.append(nueva_url + "\n\n")

    with open(archivo_salida, 'w', encoding='utf-8') as f_out:
        f_out.writelines(lineas_resultado)
        
    print(f"¡Modificación completada! Todo redirigido a Render en {archivo_salida}")

if __name__ == "__main__":
    procesar_canales()
