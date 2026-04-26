import requests

# URL de tu archivo fuente RAW
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def generar_m3u():
    try:
        # 1. Bajamos la lista de canales que pegaste
        r = requests.get(URL_FUENTE, timeout=20)
        if r.status_code != 200:
            print(f"Error al bajar fuente: {r.status_code}")
            return

        lineas = r.text.splitlines()
        
        # 2. Guardamos el archivo final
        with open("lista_dany.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            for linea in lineas:
                l = linea.strip()
                if not l or l == "#EXTM3U": 
                    continue
                
                # Escribimos cada línea (info y URL) tal cual viene de la fuente
                f.write(l + "\n")
                
        print("✅ ¡Lista generada! Ya puedes cargarla en tu app.")

    except Exception as e:
        print(f"❌ Falló el script: {e}")

if __name__ == "__main__":
    generar_m3u()
