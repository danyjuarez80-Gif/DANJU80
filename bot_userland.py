import requests
import re

# Nombres de tus archivos en el repo DANJU80
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def cazar_canales():
    enlaces = []
    # Usamos headers para que la web crea que somos un celular
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
        'Referer': URL_BASE + '/'
    }
    
    try:
        # 1. Buscamos los partidos activos
        r = requests.get(URL_BASE, headers=headers, timeout=15).text
        bloques = re.findall(r'href="(/embed/[^"]+)"', r)
        
        for path in set(bloques):
            # 2. Entramos a cada canal para sacar el link del video (m3u8)
            r_canal = requests.get(URL_BASE + path, headers=headers, timeout=10).text
            # Buscamos el archivo de video que se carga tras el clic
            match = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_canal)
            if not match:
                match = re.search(r'file:\s*"([^"]+\.m3u8[^"]*)"', r_canal)
            
            if match:
                link = match.group(1)
                nombre = path.replace("/embed/", "").replace("-", " ").upper()
                # Agregamos el Referer para que no se bloquee en tu app de IPTV
                enlaces.append(f"#EXTINF:-1, [FUTBOL] {nombre}\n{link}|Referer={URL_BASE}/&User-Agent=Mozilla/5.0")
    except Exception as e:
        print(f"Error: {e}")
    return enlaces

# Paso final: Unir con tus noticias de 'fijos.m3u'
try:
    with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
        base = f.read().strip()
except:
    base = "#EXTM3U"

nuevos = cazar_canales()

with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
    f.write(base + "\n\n")
    f.write("# --- CANALES DINÁMICOS DETECTADOS ---\n")
    if nuevos:
        f.write("\n".join(nuevos))
        print(f"¡Exito! Se encontraron {len(nuevos)} canales.")
    else:
        f.write("# No se hallaron links en este ciclo. Reintenta en 15 min.\n")
