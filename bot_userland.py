import requests
import re
import os
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

ARCHIVO = "lista_danju80.m3u"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Configuración de fuentes y sus patrones de extracción
FUENTES = [
    {
        "nombre": "FutbolLibre TV", 
        "url": "https://futbolslibre-tv.co/", 
        "regex_canales": r'href="(https?://futbolslibre-tv\.co/(?:tyc-sports|directv-sports|tnt-sports|tv-publica|fox-sports|espn-premium|deportv|tudn|golperu)/)"',
        "regex_reproductores": r'href="(https?://[^"]+/(?:vivo/canales|global1|canal|tycsports-sd|canales)\.php\?[^"]+)"'
    },
    {
        "nombre": "Pirlo TV",
        "url": "https://www.pirlotv3.sale/",
        "regex_canales": r'href="(/canal\.php\?id=[^"]+)"',
        "regex_reproductores": None # En Pirlo el canal.php ya es el reproductor
    }
]

def obtener_html(url, referer=None):
    headers = {'User-Agent': USER_AGENT}
    if referer:
        headers['Referer'] = referer
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        # print(f"  [!] Error en {url}: {e}")
        return None

def extraer_m3u8(url_embed, referer):
    html = obtener_html(url_embed, referer)
    if not html:
        return None
    
    # Patrones comunes de enlaces m3u8
    patrones = [
        r'var playbackURL\s*=\s*"([^"]+)"',
        r'source:\s*"([^"]+)"',
        r'file:\s*"([^"]+)"',
        r'hls:\s*"([^"]+)"',
        r'["\'](https?://[^"\']+\.m3u8[^"\']*)["\']'
    ]
    
    for patron in patrones:
        match = re.search(patron, html)
        if match:
            link = match.group(1).replace('\\/', '/')
            if '.m3u8' in link:
                return link
    return None

def procesar_fuente_futbollibre(url_canal, fuente):
    nombre = url_canal.strip('/').split('/')[-1].replace('-', ' ').upper()
    html_canal = obtener_html(url_canal, fuente['url'])
    if not html_canal: return None
    
    reproductores = re.findall(fuente['regex_reproductores'], html_canal)
    for url_rep in reproductores:
        m3u8 = extraer_m3u8(url_rep, url_canal)
        if m3u8:
            return f"#EXTINF:-1, [FULL-SCAN] {nombre}\n{m3u8}|Referer={url_rep}"
    return None

def procesar_fuente_pirlo(url_relativa, fuente):
    url_canal = urljoin(fuente['url'], url_relativa)
    nombre = url_relativa.split('=')[-1].upper()
    m3u8 = extraer_m3u8(url_canal, fuente['url'])
    if m3u8:
        return f"#EXTINF:-1, [PIRLO] {nombre}\n{m3u8}|Referer={fuente['url']}"
    return None

def ejecutar():
    print("--- INICIANDO EXTRACCIÓN MULTI-FUENTE ---")
    enlaces_totales = []
    
    for fuente in FUENTES:
        print(f"[*] Escaneando: {fuente['nombre']}...")
        html_inicio = obtener_html(fuente['url'])
        if not html_inicio: continue
        
        items = list(set(re.findall(fuente['regex_canales'], html_inicio)))
        print(f"    Encontrados {len(items)} posibles canales.")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            if fuente['nombre'] == "FutbolLibre TV":
                resultados = list(executor.map(lambda x: procesar_fuente_futbollibre(x, fuente), items))
            else:
                resultados = list(executor.map(lambda x: procesar_fuente_pirlo(x, fuente), items))
                
        validos = [r for r in resultados if r]
        print(f"    ✅ Capturados con éxito: {len(validos)}")
        enlaces_totales.extend(validos)

    if enlaces_totales:
        modo = "a" if os.path.exists(ARCHIVO) else "w"
        with open(ARCHIVO, modo, encoding="utf-8") as f:
            if modo == "w": f.write("#EXTM3U\n")
            f.write("\n" + "\n".join(enlaces_totales) + "\n")
        print(f"\n[FIN] Se guardaron {len(enlaces_totales)} canales en {ARCHIVO}.")
    else:
        print("\n[!] No se encontró contenido nuevo.")

if __name__ == "__main__":
    ejecutar()
