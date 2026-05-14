import requests
import re

# La lista final
ARCHIVO = "lista_danju80.m3u"

# Servidores que suelen alojar los canales que buscas
# Vamos a atacar directamente a los proveedores, no a la web principal
SERVIDORES = [
    "https://cdn.futbollibretv.me",
    "https://clon.futbollibre.net",
    "https://unblock.fandroid.top"
]

CANALES = {
    "ESPN": "espn1",
    "ESPN 2": "espn2",
    "FOX SPORTS": "foxsports1",
    "TUDN": "tudn",
    "AZTECA 7": "azteca7"
}

def forzar_caza():
    print("--- Recuperando Logros Anteriores ---")
    enlaces = []
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'}

    for nombre, slug in CANALES.items():
        for serv in SERVIDORES:
            try:
                # Intentamos construir la URL que la web genera después del "clic"
                url_test = f"{serv}/embed/{slug}"
                r = requests.get(url_test, headers=headers, timeout=5).text
                
                # Buscamos el m3u8 con una regex que ignora protecciones básicas
                match = re.search(r'["\'](http[^"\']+\.m3u8[^"\']*)["\']', r.replace('\\/', '/'))
                
                if match:
                    link = match.group(1)
                    enlaces.append(f"#EXTINF:-1, [LOGRADO] {nombre}\n{link}")
                    print(f"✅ {nombre} RECUPERADO")
                    break # Si lo hallamos en un servidor, pasamos al siguiente canal
            except:
                continue
    return enlaces

if __name__ == "__main__":
    final = forzar_caza()
    if final:
        with open(ARCHIVO, "w") as f:
            f.write("#EXTM3U\n" + "\n".join(final))
        print(f"\nSe recuperaron {len(final)} canales de la lista prioritaria.")
    else:
        print("\nLas fuentes están blindadas. Necesitan actualización de tokens manual.")
