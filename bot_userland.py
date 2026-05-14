import requests
import re

ARCHIVO = "lista_danju80.m3u"
FUENTES = ["https://futbollibre.ec", "https://jeinzmacias.net", "https://www.rojadirectatv.tv"]

def operacion_infiltrado_total():
    print("--- INICIANDO EXTRACCIÓN DE FLUJO INTERNO ---")
    enlaces = []
    # Usamos una sesión para que las cookies se guarden entre peticiones
    sesion = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'es-MX,es;q=0.9',
    }

    for url in FUENTES:
        try:
            print(f"Infiltrando en: {url}")
            # 1. Contacto inicial para capturar cookies
            r_home = sesion.get(url, headers=headers, timeout=12).text
            # 2. Buscamos los contenedores de video (iframes)
            bloques = re.findall(r'src="([^"]+)"', r_home)
            
            for src in bloques:
                # Buscamos patrones de servidores de video (vagu, stream, embed)
                if any(x in src for x in ["embed", "stream", "player", "vagu", "cvattv"]):
                    target = src if src.startswith('http') else url + src
                    print(f"Vulnerando componente: {target[:40]}...")
                    
                    # 3. Entramos al componente simulando que venimos de la web oficial
                    r_video = sesion.get(target, headers={'Referer': url}, timeout=7).text
                    
                    # 4. Buscamos el m3u8 limpiando las barras de seguridad (\/)
                    # Usamos una regex más flexible para capturar links con tokens
                    match = re.search(r'["\'](http[^"\']+\.m3u8[^"\']*)["\']', r_video.replace('\\/', '/'))
                    
                    if match:
                        link_final = match.group(1).split('"')[0].split("'")[0]
                        nombre = url.split('//')[1].split('.')[0].upper()
                        # Formato con Referer para que no muera en la app de IPTV
                        formato = f"#EXTINF:-1, [HACKED] {nombre}\n{link_final}|Referer={url}/"
                        if formato not in enlaces:
                            enlaces.append(formato)
                            print(f"✅ ¡SISTEMA VULNERADO! Link de {nombre} capturado.")
        except: continue
    return enlaces

if __name__ == "__main__":
    final = operacion_infiltrado_total()
    if final:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(final))
        print(f"\nOperación exitosa: {len(final)} flujos interceptados.")
    else:
        print("\nEl muro de encriptación sigue firme. El token es dinámico.")
