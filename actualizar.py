import requests
import re

ARCHIVOS_SALIDA = ["DANJU80", "lista_dany.m3u"]

# 1. Agregamos sitios web reales para "scrapear" (buscar dentro de ellos)
SITIOS_WEB = [
    "https://www.tvplusgratis.com/", # Ejemplo de sitio con canales de México
    "https://televisionlibre.net/es/" # Ejemplo de sitio multicanal
]

CANALES_FIJOS = [
    {"nombre": "Azteca 7 (Directo)", "url": "https://televisa-latam-azteca7-1-mx.samsung.wurl.com/manifest/playlist.m3u8"},
    {"nombre": "Telemundo HD", "url": "https://telemundo-usa-east-1-mx.samsung.wurl.com/manifest/playlist.m3u8"}
]

# --- NUEVA FUNCIÓN PARA BUSCAR EN PÁGINAS ---
def buscar_en_paginas():
    encontrados = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url_sitio in SITIOS_WEB:
        try:
            print(f"🔍 Buscando links en: {url_sitio}")
            r = requests.get(url_sitio, headers=headers, timeout=15)
            # Buscamos patrones de links .m3u8 dentro del código de la página
            links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+m3u8', r.text)
            
            for link in set(links):
                # Si el link parece ser de un canal que nos interesa
                if "azteca" in link.lower() or "deportes" in link.lower():
                    encontrados.append(("Canal Encontrado", link))
        except:
            continue
    return encontrados

def leer_lista_existente(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        urls_existentes = set(re.findall(r'http\S+', contenido))
        return contenido.rstrip(), urls_existentes
    except FileNotFoundError:
        return "#EXTM3U", set()

def ejecutar():
    contenido_actual, urls_existentes = leer_lista_existente(ARCHIVOS_SALIDA[0])
    canales_nuevos = []

    # A. Canales Fijos (Los que ya sabemos que funcionan)
    for c in CANALES_FIJOS:
        if c["url"] not in urls_existentes:
            canales_nuevos.append((c["nombre"], c["url"]))
            urls_existentes.add(c["url"])

    # B. BUSQUEDA EN PÁGINAS (Web Scraping)
    encontrados_web = buscar_en_paginas()
    for nombre, url in encontrados_web:
        if url not in urls_existentes:
            canales_nuevos.append((nombre, url))
            urls_existentes.add(url)
            print(f"✨ ¡Link extraído de la web!: {url}")

    if not canales_nuevos:
        print("✅ No se hallaron links nuevos en las webs.")
        return

    # Guardar resultados
    nuevas_lineas = []
    for nombre, url in canales_nuevos:
        # Añadimos el User-Agent para que VLC no se trabe
        nuevas_lineas.append(f"#EXTINF:-1,{nombre}")
        nuevas_lineas.append(url)

    contenido_final = contenido_actual + "\n" + "\n".join(nuevas_lineas)
    for archivo in ARCHIVOS_SALIDA:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido_final)
    print(f"✅ Lista actualizada con {len(canales_nuevos)} canales.")

if __name__ == "__main__":
    ejecutar()
