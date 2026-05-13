import requests
import re

# Archivos donde se guardará la lista
ARCHIVOS_SALIDA = ["Danju80.txt", "system_cache.log"]
# Link para no perder lo que ya tenías
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/Danju80.txt"

# Fuentes de canales rápidas
SITIOS_WEB = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

# Lo que quieres buscar
OBJETIVOS = ["ESPN", "FOX SPORTS", "TUDN", "AZTECA 7", "CANAL 5", "TELEMUNDO", "UNIVISION"]

def run_process():
    print("⚡ MODO FLASH ACTIVADO...")
    final_data = ["#EXTM3U"]
    
    try:
        # Recuperamos lo anterior MUY rápido
        r_old = requests.get(URL_RESCATE, timeout=3)
        if r_old.status_code == 200:
            final_data = [l.strip() for l in r_old.text.splitlines() if l.strip()]
    except: pass

    if not final_data or not final_data[0].startswith("#EXTM3U"):
        final_data = ["#EXTM3U"]
    
    initial_count = len(final_data)
    
    # Escaneo veloz
    for source in SITIOS_WEB:
        try:
            res = requests.get(source, timeout=4)
            if res.status_code == 200:
                # Buscamos los links m3u8 sin probarlos (para no perder tiempo)
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+m3u8', res.text)
                for link in set(links):
                    if link not in "\n".join(final_data):
                        if any(obj.lower() in link.lower() for obj in OBJETIVOS):
                            final_data.append(f'#EXTINF:-1, Canal_{link[-5:]}')
                            final_data.append(link)
        except: continue

    # GUARDADO FORZOSO
    output_text = "\n".join(final_data)
    for file_name in ARCHIVOS_SALIDA:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(output_text)
    print(f"🚀 Guardado completado. Total líneas: {len(final_data)}")

if __name__ == "__main__":
    run_process()
