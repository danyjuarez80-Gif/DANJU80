import requests

# URL donde está tu lista pegada (la que me acabas de enviar)
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def generar_lista_final():
    try:
        # 1. Leemos el contenido de tu archivo DANJU80
        response = requests.get(URL_FUENTE, timeout=20)
        if response.status_code != 200:
            print(f"❌ Error al conectar: {response.status_code}")
            return

        lineas = response.text.splitlines()
        
        # 2. Creamos el archivo lista_dany.m3u
        with open("lista_dany.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            for linea in lineas:
                linea = linea.strip()
                
                # Si la linea es información del canal
                if linea.startswith("#EXTINF"):
                    # Personalizamos el grupo a "Dany TV" y limpiamos espacios
                    linea_limpia = linea.replace('group-title="TV"', 'group-title="Dany TV"')
                    f.write(f"\n{linea_limpia}\n")
                
                # Si la linea es una URL (detectamos por http)
                elif linea.startswith("http"):
                    f.write(f"{linea}\n")
        
        print("✅ ¡Proceso completado! Se generó 'lista_dany.m3u' con éxito.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    generar_lista_final()
