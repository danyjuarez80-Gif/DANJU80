import requests
import re
import os

ARCHIVO_FINAL = "lista_danju80.m3u"
# Añadimos la fuente que se ve en tu video
URLS = ["https://futbollibre.ec", "https://librefutboltv.com", "https://tvplusgratis2.com"]
PRIORIDAD = ["espn", "fox", "tudn", "directv", "caliente", "telemundo", "univision", "azteca"]

def cazar_con_opciones():
    enlaces = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6) AppleWebKit/537.36',
        'Referer': 'https://google.com'
    }
    
    for base in URLS:
        try:
            print(f"Escaneando fuente: {base}")
            r = requests.get(base, headers=headers, timeout=10).text
            # Captura rutas de canales y de opciones (como se ve en tu video)
            items = re.findall(r'href="((?:/embed/|/opcion)[^"]+)"', r)
            
            for path in list(set(items)):
                nombre = path.split("/")[-1].replace("-", " ").lower()
                if any(p in nombre for p in PRIORIDAD):
                    print(f"Analizando opción para: {nombre.upper()}")
                    # Simulamos el clic en la 'Opción' del video
                    r_opt = requests.get(base + path, headers=headers, timeout=10).text
                    # Buscamos el m3u8 real (el enlace que copiaste al final del video)
                    match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', r_opt)
                    
                    if match:
                        link = match.group(1)
                        # Agregamos el link con el formato adecuado para IPTV
                        enlaces.append(f"#EXTINF:-1, [TV] {nombre.upper()}\n{link}|Referer={base}/")
                        print(f"¡Enlace de {nombre.upper()} capturado!")
        except: continue
    return enlaces

if __name__ == "__main__":
    lista_canales = cazar_con_opciones()
    if lista_canales:
        with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(lista_canales))
        print(f"Proceso completo: {len(lista_canales)} canales guardados.")
    else:
        print("No se detectaron flujos activos en las opciones actuales.")
