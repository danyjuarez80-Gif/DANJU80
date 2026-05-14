import requests
import re
import time

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def capturar_canales():
    enlaces = []
    # Usamos headers de un navegador real que acepta cookies
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Referer': URL_BASE + '/'
    }
    
    with requests.Session() as s:
        try:
            # 1. Entrar a la Home (esto nos da las cookies iniciales)
            r_home = s.get(URL_BASE, headers=headers, timeout=10)
            
            # Buscamos los IDs de los canales activos
            canales_ids = re.findall(r'href="(/embed/[^"]+)"', r_home.text)
            
            for path in set(canales_ids):
                url_canal = URL_BASE + path
                # 2. Simulamos el "Clic" al canal (ignora los comerciales, vamos al código)
                # Aquí la sesión de requests ya guardó las cookies del paso 1
                r_canal = s.get(url_canal, headers=headers, timeout=10)
                
                # 3. BUSCADOR DE M3U8 (Incluso si están ocultos en scripts)
                # El video se carga usualmente en una variable llamada 'source' o 'file'
                m3u8_links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r_canal.text)
                
                for link in set(m3u8_links):
                    # Filtramos links de publicidad que a veces terminan en .m3u8
                    if "futbollibre" in link or "cvatt" in link or "fsl" in link:
                        nombre = path.split('/')[-1].replace('-', ' ').upper()
                        enlaces.append({"n": nombre, "u": link})
                        
        except Exception as e:
            print(f"Error detectado: {e}")
            
    return enlaces

def actualizar_repo():
    # Leer tus canales fijos (los que no se borran)
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    canales_bot = capturar_canales()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        f.write("# --- CANALES ENCONTRADOS (POST-COMERCIALES) ---\n")
        
        if canales_bot:
            for c in canales_bot:
                f.write(f"#EXTINF:-1, [BOT] {c['n']}\n")
                # El Referer y User-Agent son obligatorios para saltar el bloqueo del comercial
                f.write(f"{c['u']}|Referer={URL_BASE}/&User-Agent=Mozilla/5.0\n")
            print(f"¡Hecho! {len(canales_bot)} canales listos.")
        else:
            f.write("# No se hallaron links. Es posible que el token haya expirado.\n")

if __name__ == "__main__":
    actualizar_repo()
