import requests
import re
import time

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def motor_profundo():
    canales = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Referer': URL_BASE + '/'
    }
    
    with requests.Session() as s:
        try:
            # 1. Home
            res = s.get(URL_BASE, headers=headers, timeout=20)
            items = re.findall(r'href="(/embed/[^"]+)"', res.text)
            
            for path in set(items):
                url = URL_BASE + path
                time.sleep(2) # Pausa para no ser detectado como bot veloz
                
                # 2. Entrar al canal
                r_canal = s.get(url, headers=headers, timeout=15)
                
                # 3. Buscar m3u8 en todas sus formas posibles
                # Buscamos links directos, en variables JS o dentro de IFRAMES
                found = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r_canal.text)
                
                if not found:
                    # Intento extra: buscar si el link está dentro de un iframe src
                    iframes = re.findall(r'src="(https?://[^"]+)"', r_canal.text)
                    for ifr in iframes:
                        if "m3u8" in ifr or "embed" in ifr:
                            r_ifr = s.get(ifr, headers={'Referer': url}, timeout=10)
                            found += re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r_ifr.text)

                for link in set(found):
                    if "http" in link and len(link) > 40:
                        nombre = path.replace("/embed/", "").replace("-", " ").upper()
                        canales.append({"n": nombre, "u": link})
        except Exception as e:
            print(f"Error: {e}")
    return canales

def app():
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    lista_viva = motor_profundo()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        f.write("# --- CANALES DE FUTBOL LIBRE ---\n")
        if lista_viva:
            for c in lista_viva:
                f.write(f"#EXTINF:-1, [FUTBOL] {c['n']}\n")
                # El Referer es clave para que tu app de Android no de error 403
                f.write(f"{c['u']}|Referer={URL_BASE}/&User-Agent=Mozilla/5.0\n")
        else:
            f.write("# El bot fue bloqueado o no hay partidos vivos.\n")

if __name__ == "__main__":
    app()
