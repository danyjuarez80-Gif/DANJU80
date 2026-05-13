import requests
import re

# Nombres camuflados para que nadie sospeche
ARCHIVOS_SALIDA = ["Danju80.txt", "system_cache.log"]
# Link RAW para que el bot rescate lo que ya tenías guardado
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/Danju80.txt"

# Sitios donde el bot buscará links escondidos
SITIOS_WEB = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://televisionlibre.net/es/",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://www.tvplusgratis.com/"
]

# Canales que el bot tiene orden de capturar
OBJETIVOS = ["ESPN", "FOX SPORTS", "TUDN", "AZTECA 7", "CANAL 5", "TELEMUNDO", "UNIVISION", "LAS ESTRELLAS"]

def check_status(url):
    """Prueba si el link responde en menos de 2 segundos"""
    try:
        res = requests.head(url, timeout=2, allow_redirects=True)
        return res.status_code == 200
    except:
        return False

def run_process():
    print("🚀 Iniciando mantenimiento de logs de sistema...")
    
    final_data = []
    try:
        # Intentamos leer lo que ya existe para no borrarlo
        r_old = requests.get(URL_RESCATE, timeout=10)
        if r_old.status_code == 200:
            final_data = [l.strip() for l in r_old.text.splitlines() if l.strip()]
            print(f"📚 Base de datos cargada. Registros actuales: {len(final_data)//2}")
    except:
        final_data = ["#EXTM3U"]

    if not final_data or not final_data[0].startswith("#EXTM3U"):
        final_data = ["#EXTM3U"]
    
    initial_count = len(final_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Buscamos en cada sitio de la lista
    for source in SITIOS_WEB:
        try:
            print(f"🔍 Escaneando fuente: {source[:30]}...")
            res = requests.get(source, headers=headers, timeout=12)
            if res.status_code == 200:
                # Extraemos links m3u8 con expresiones regulares
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+m3u8', res.text)
                
                for link in set(links):
                    link_limpio = link.strip()
                    # Si el link es nuevo y coincide con lo que buscamos
                    if link_limpio not in "\n".join(
