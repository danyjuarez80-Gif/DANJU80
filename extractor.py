import requests

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def generar_lista_limpia():
    try:
        r = requests.get(URL_FUENTE, timeout=20)
        if r.status_code != 200: return

        lineas = r.text.splitlines()
        canales_vistos = set() # Para no repetir URLs
        lista_final = []

        # Usamos "w" para que SIEMPRE borre lo viejo antes de escribir
        with open("lista_dany.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n\n")
            
            for i in range(len(lineas)):
                linea = lineas[i].strip()
                
                if linea.startswith("#EXTINF"):
                    # Verificamos la siguiente línea (la URL)
                    if i + 1 < len(lineas):
                        url = lineas[i+1].strip()
                        # Si la URL no ha sido agregada todavía, la guardamos
                        if url not in canales_vistos:
                            f.write(linea + "\n")
                            f.write(url + "\n\n")
                            canales_vistos.add(url)
        
        print(f"✅ Lista generada sin duplicados. Canales únicos: {len(canales_vistos)}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generar_lista_limpia()
