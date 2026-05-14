import requests
import re

ARCHIVO = "lista_danju80.m3u"
# Las fuentes maestras que mencionó el usuario de la foto
FUENTES = [
    "https://futbollibre.ec", 
    "https://www.rojadirectatv.tv", 
    "https://jeinzmacias.net"
]

def operacion_sniffer():
    print("--- INICIANDO RASTREO DE TRÁFICO INTERNO ---")
    enlaces = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6)',
        'Referer': 'https://google.com'
    }

    for url in FUENTES:
        try:
            print(f"Analizando componentes de: {url}")
            r = requests.get(url, headers=headers, timeout=10).text
            
            # Buscamos todos los iframes (donde realmente vive el video)
            iframes = re.findall(r'src="([^"]+)"', r)
            
            for src in iframes:
                # Buscamos patrones de servidores de video conocidos
                if any(x in src for x in ["embed", "stream", "player", "vagu", "cvattv"]):
                    print(f"¡Componente sospechoso detectado!: {src[:40]}")
                    
                    # Entramos al componente para ver su tráfico interno
                    try:
                        inner = requests.get(src if src.startswith('http') else url+src, headers=headers, timeout=5).text
                        # Buscamos el link m3u8 real, limpiando las barras de seguridad (\/)
                        m3u8 = re.search(r'["\'](http[^"\']+\.m3u8[^"\']*)["\']', inner.replace('\\/', '/'))
                        
                        if m3u8:
                            link = m3u8.group(1)
                            enlaces.append(f"#EXTINF:-1, [HACKED] {url.split('//')[1].split('.')[0].upper()}\n{link}")
                            print("✅ ¡SISTEMA VULNERADO! Link de video capturado.")
                    except: continue
        except: continue
    return enlaces

if __name__ == "__main__":
    lista = operacion_sniffer()
    if lista:
        with open(ARCHIVO, "w") as f:
            f.write("#EXTM3U\n" + "\n".join(lista))
        print(f"\nSe capturaron {len(lista)} flujos de video internos.")
    else:
        print("\nLa encriptación es fuerte. Necesitamos un bypass de cookies.")
