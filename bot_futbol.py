import requests
import re
import time

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def extraer_profundo():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Referer': URL_BASE + '/'
    }
    resultados = []
    
    with requests.Session() as s:
        try:
            # 1. Entramos a la home
            inicio = s.get(URL_BASE, headers=headers, timeout=15).text
            # Buscamos todos los botones "Ver Canal"
            links_canales = re.findall(r'href="(/embed/[^"]+)"', inicio)
            
            print(f"Se encontraron {len(links_canales)} botones de canales. Empezando rastreo uno por uno...")

            for path in set(links_canales):
                url_interna = URL_BASE + path
                try:
                    # SIMULAMOS EL CLIC: Entramos a la página del canal
                    # Agregamos un pequeño delay para que no nos bloqueen por ir rápido
                    time.sleep(1) 
                    r_canal = s.get(url_interna, headers=headers, timeout=10).text
                    
                    # Buscamos el m3u8 dentro del código del reproductor
                    # Esta es la parte que "salta" los comerciales
                    m3u8 = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_canal)
                    if not m3u8:
                        m3u8 = re.search(r'file:\s*"([^"]+\.m3u8[^"]*)"', r_canal)
                    
                    if m3u8:
                        link_directo = m3u8.group(1)
                        nombre = path.replace("/embed/", "").replace("-", " ").upper()
                        resultados.append({"n": nombre, "u": link_directo})
                        print(f"¡Éxito! Encontrado: {nombre}")
                except:
                    continue
                    
        except Exception as e:
            print(f"Error en la conexión principal: {e}")
            
    return resultados

def generar():
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    canales = extraer_profundo()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        f.write("# --- CANALES DETECTADOS POR RASTREO PROFUNDO ---\n")
        
        if canales:
            for c in canales:
                f.write(f"#EXTINF:-1, [FUTBOL] {c['n']}\n")
                f.write(f"{c['u']}|Referer={URL_BASE}/&User-Agent=Mozilla/5.0\n")
        else:
            f.write("# No se hallaron links. Es posible que los canales no hayan iniciado aún.\n")
            print("No se encontró nada en este ciclo.")

if __name__ == "__main__":
    generar()
