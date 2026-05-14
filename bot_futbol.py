import requests
import re

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def bot_extractor():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Referer': URL_BASE
    }
    enlaces_encontrados = []
    
    with requests.Session() as s:
        try:
            # 1. Obtener la home para sacar los IDs de los canales
            r_home = s.get(URL_BASE, headers=headers, timeout=15)
            # Buscamos patrones como /embed/?r=... o similares que usa la web
            ids_canales = re.findall(r'href="(/embed/[^"]+)"', r_home.text)
            
            for path in set(ids_canales):
                url_canal = URL_BASE + path
                # 2. Entrar a la subpágina del canal
                r_canal = s.get(url_canal, headers=headers, timeout=10)
                
                # 3. EL CLAVO: Buscamos el iframe o el script que carga el m3u8
                # Buscamos dentro de variables JS como 'window.atob' o 'source: "..."'
                # Muchos de estos sitios encriptan el link en Base64 o lo sirven vía AJAX
                match = re.search(r'(https?://[\w\.\-/]+\.m3u8[^"]*)', r_canal.text)
                
                if match:
                    link_m3u8 = match.group(1)
                    nombre = path.split('/')[-1].replace('-', ' ').upper()
                    enlaces_encontrados.append({"n": nombre, "u": link_m3u8})
                    
        except Exception as e:
            print(f"Error: {e}")
            
    return enlaces_encontrados

def actualizar_lista():
    # Leer tus fijos (el PASO 1 que hicimos)
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    canales = bot_extractor()

    # Generar el archivo final combinando todo
    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        f.write("# --- CANALES DINÁMICOS DETECTADOS ---\n")
        if canales:
            for c in canales:
                f.write(f"#EXTINF:-1, [FUTBOL] {c['n']}\n")
                # El Referer es OBLIGATORIO en el link para que no de 403 Forbidden
                f.write(f"{c['u']}|Referer={URL_BASE}/\n")
        else:
            f.write("# No se hallaron links en este ciclo. Reintenta en 15 min.\n")

if __name__ == "__main__":
    actualizar_lista()
