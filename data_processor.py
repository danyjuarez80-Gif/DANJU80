import requests
import re

ARCHIVOS_SALIDA = ["Danju80.txt", "system_cache.log"]
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/Danju80.txt"

# AMPLIAMOS LAS FUENTES (Estas se actualizan mucho más seguido)
SITIOS_WEB = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://raw.githubusercontent.com/frol/iptv-playlist-mexico/master/mexico.m3u",
    "https://raw.githubusercontent.com/ruuand/iptvmx/main/playlist.m3u"
]

# Filtros más amplios para que no se le escape nada
OBJETIVOS = ["ESPN", "FOX", "TUDN", "AZTECA", "CANAL", "TELE", "UNI", "SKY", "PROMO"]

def run_process():
    print("🚀 MODO CAZADOR TOTAL ACTIVADO...")
    final_data = ["#EXTM3U"]
    
    # 1. Intentar rescatar lo que ya tienes
    try:
        r_old = requests.get(URL_RESCATE, timeout=5)
        if r_old.status_code == 200:
            final_data = [l.strip() for l in r_old.text.splitlines() if l.strip()]
    except: pass

    if not final_data or not final_data[0].startswith("#EXTM3U"):
        final_data = ["#EXTM3U"]
    
    count_antes = len(final_data)
    
    # 2. Buscar en todas las fuentes nuevas
    for source in SITIOS_WEB:
        try:
            print(f"🔍 Buscando en: {source[:40]}...")
            res = requests.get(source, timeout=8)
            if res.status_code == 200:
                # Buscamos links m3u8 y ts (que también funcionan en Roku/VLC)
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+(?:m3u8|ts)', res.text)
                
                for link in set(links):
                    if link not in "\n".join(final_data):
                        # Si el link tiene algo de lo que buscamos, adentro
                        if any(obj.lower() in link.lower() for obj in OBJETIVOS):
                            final_data.append(f'#EXTINF:-1, Canal_Update_{link[-5:]}')
                            final_data.append(link)
        except: continue

    # 3. GUARDAR TODO (Incluso si no hay cambios, para asegurar que el archivo exista)
    output_text = "\n".join(final_data)
    for file_name in ARCHIVOS_SALIDA:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(output_text)
            
    print(f"✅ Proceso finalizado. Total canales ahora: {len(final_data)//2}")
    print(f"✨ Se agregaron {(len(final_data)-count_antes)//2} canales en esta vuelta.")

if __name__ == "__main__":
    run_process()
