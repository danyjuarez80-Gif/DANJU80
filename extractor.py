import requests

# URL que me proporcionaste
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def automatizar_lista():
    try:
        # 1. Intentamos obtener la lista completa
        print("Descargando lista desde DANJU80...")
        r = requests.get(URL_FUENTE, timeout=20)
        
        if r.status_code != 200:
            print(f"❌ Error al conectar con GitHub: {r.status_code}")
            return

        lineas = r.text.splitlines()
        
        # 2. Creamos el archivo M3U final
        with open("lista_dany.m3u", "w", encoding="utf-8") as f:
            # Escribimos la cabecera
            f.write("#EXTM3U\n\n")
            
            # Contador para verificar los 86 canales
            conteo = 0
            
            for i in range(len(lineas)):
                linea = lineas[i].strip()
                
                # Buscamos las líneas que empiezan con #EXTINF
                if linea.startswith("#EXTINF"):
                    # Escribimos la línea de info del canal
                    f.write(linea + "\n")
                    # La siguiente línea suele ser la URL, la buscamos
                    if i + 1 < len(lineas):
                        url_canal = lineas[i+1].strip()
                        f.write(url_canal + "\n\n")
                        conteo += 1
            
        print(f"✅ ¡Proceso terminado! Se han procesado {conteo} canales.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    automatizar_lista()
