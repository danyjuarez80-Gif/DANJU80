import requests
import re

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"

def extraer_con_fuerza():
    canales = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
        'Referer': 'https://futbollibre.ec/'
    }
    
    # Intentamos con diferentes dominios que usa la web
    dominios = ["https://futbollibre.ec", "https://librefutboltv.com", "https://futbollibretv.me"]
    
    for url in dominios:
        try:
            print(f"Probando con {url}...")
            r = requests.get(url, headers=headers, timeout=10)
            # Buscamos patrones de canales (ej: /embed/?r=...)
            links = re.findall(r'href="([^"]*embed[^"]*)"', r.text)
            
            for l in set(links):
                full_url = l if l.startswith('http') else url + l
                nombre = l.split('=')[-1].upper() if '=' in l else "CANAL-FUTBOL"
                canales.append({"n": nombre, "u": full_url})
            
            if canales: break # Si encontramos algo, dejamos de probar dominios
        except:
            continue
    return canales

def main():
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    encontrados = extraer_con_fuerza()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        f.write("# --- CANALES DETECTADOS (PLAN C) ---\n")
        if encontrados:
            for c in encontrados:
                f.write(f"#EXTINF:-1, [TV] {c['n']}\n")
                f.write(f"{c['u']}\n")
            print(f"Se encontraron {len(encontrados)} canales.")
        else:
            f.write("# Bloqueo total de IP detectado. GitHub no puede ver la web.\n")

if __name__ == "__main__":
    main()
