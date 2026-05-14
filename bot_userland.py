import requests
import re

ARCHIVO = "lista_danju80.m3u"
# Atacamos las fuentes que viste en la plática de Facebook
FUENTES = [
    "https://futbollibre.ec", 
    "https://www.rojadirectatv.tv", 
    "https://jeinzmacias.net"
]

def operacion_extrema():
    print("--- INICIANDO EXTRACCIÓN NIVEL: JHON DOE ---")
    enlaces = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6)',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    for url in FUENTES:
        try:
            print(f"Buscando grietas en: {url}")
            # Paso 1: Obtener la página base
            r = requests.get(url, headers=headers, timeout=10).text
            # Paso 2: Buscar scripts de servidores de video (Vagu, Stream, etc.)
            links_internos = re.findall(r'src="([^"]+)"', r)
            
            for src in links_internos:
                if any(x in src for x in ["embed", "stream", "player", "vagu"]):
                    print(f"Vulnerando componente: {src[:30]}...")
                    # Paso 3: Entrar al reproductor con el Referer de la web original
                    # Esto es lo que "rompe" la seguridad
                    try:
                        target = src if src.startswith('http') else url + src
                        r_video = requests.get(target, headers={'Referer': url}, timeout=5).text
                        
                        # Buscamos el m3u8 limpiando las barras escapadas
                        match = re.search(r'["\'](http[^"\']+\.m3u8[^"\']*)["\']', r_video.replace('\\/', '/'))
                        
                        if match:
                            link_final = match.group(1).split('"')[0]
                            # Construimos el link con el 'toque' de Jhon Doe
                            # Agregamos el Referer al final para que tu app de IPTV pueda abrirlo
                            formato = f"#EXTINF:-1, [HACK] {url.split('//')[1].split('.')[0].upper()}\n{link_final}|Referer={url}/"
                            if formato not in enlaces:
                                enlaces.append(formato)
                                print("✅ ¡LOGRADO! Sistema vulnerado.")
                    except: continue
        except: continue
    return enlaces

if __name__ == "__main__":
    final = operacion_extrema()
    if final:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(final))
        print(f"\nSe capturaron {len(final)} canales. ¡Victoria!")
    else:
        print("\nEl muro sigue en pie. El token es dinámico de corta duración.")
