import requests
import re
import time
import os

# CONFIGURACIÓN
ARCHIVO_FINAL = "lista_danju80.m3u"
URLS = ["https://futbollibre.ec", "https://librefutboltv.com", "https://futbollibretv.me"]
# Palabras clave para los canales que pediste
PRIORIDAD = ["espn", "fox", "tudn", "directv", "caliente", "telemundo", "univision"]

def cazar_profundo():
    print("--- Iniciando Rastreo Profundo de Canales ---")
    enlaces = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Referer': 'https://google.com'
    }
    
    for url_base in URLS:
        try:
            print(f"Escaneando superficie: {url_base}")
            r = requests.get(url_base, headers=headers, timeout=10).text
            # Buscamos los contenedores de los canales
            bloques = list(set(re.findall(r'href="(/embed/[^"]+)"', r)))
            
            for path in bloques:
                nombre_raw = path.replace("/embed/", "").replace("-", " ").lower()
                
                if any(p in nombre_raw for p in PRIORIDAD):
                    try:
                        print(f"Haciendo 'Toque' en: {nombre_raw.upper()}...")
                        # SEGUNDA PETICIÓN: Entramos al reproductor
                        r_reproductor = requests.get(url_base + path, headers=headers, timeout=10).text
                        
                        # Buscamos el m3u8 con una expresión más agresiva
                        # Busca links que empiezan con http y terminan en m3u8, incluso si tienen tokens
                        match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', r_reproductor)
                        
                        if match:
                            link = match.group(1)
                            nombre_final = nombre_raw.upper()
                            formato = f"#EXTINF:-1, [IPTV] {nombre_final}\n{link}|Referer={url_base}/"
                            if formato not in enlaces:
                                enlaces.append(formato)
                                print(f"¡LOGRADO!: {nombre_final}")
                        else:
                            # Intento alternativo por si el link está en base64 o escondido
                            match_alt = re.search(r'source:\s*"([^"]+)"', r_reproductor)
                            if match_alt and ".m3u8" in match_alt.group(1):
                                link = match_alt.group(1)
                                enlaces.append(f"#EXTINF:-1, [IPTV] {nombre_raw.upper()}\n{link}|Referer={url_base}/")
                                print(f"¡LOGRADO (Alt)!: {nombre_raw.upper()}")
                    except: continue
        except: continue
    return enlaces

def principal():
    # Siempre empezamos con el encabezado estándar
    base = "#EXTM3U\n"
    nuevos = cazar_profundo()
    
    if nuevos:
        with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
            f.write(base + "\n".join(nuevos))
        print(f"PROCESO TERMINADO: {len(nuevos)} canales encontrados.")
    else:
        print("La web no entregó enlaces m3u8 válidos en este momento.")

if __name__ == "__main__":
    principal()
