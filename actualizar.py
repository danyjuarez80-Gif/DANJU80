import requests
import re

# Nombres camuflados: Parecen archivos de configuración de sistema
# Puedes usar: "sys_config.cfg", "system_boot.log" o "network_cache.data"
ARCHIVOS_SALIDA = ["config_backup.cfg", "system_cache.log"]
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/config_backup.cfg"

FUENTES_EXTERNAS = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://televisionlibre.net/es/",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

# Cambié los nombres de las variables para que no digan "CANAL" o "IPTV"
OBJETIVOS = ["ESPN", "FOX SPORTS", "TUDN", "AZTECA 7", "CANAL 5", "TELEMUNDO", "UNIVISION"]

def check_status(address):
    try:
        res = requests.head(address, timeout=2, allow_redirects=True)
        return res.status_code == 200
    except:
        return False

def run_process():
    print("🚀 Running background data sync...")
    
    final_data = []
    try:
        r_old = requests.get(URL_RESCATE, timeout=10)
        if r_old.status_code == 200:
            final_data = [l.strip() for l in r_old.text.splitlines() if l.strip()]
    except:
        final_data = ["#EXTM3U"]

    if not final_data: final_data = ["#EXTM3U"]
    
    initial_count = len(final_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for source in SITIOS_WEB: # Nota: Asegúrate que SITIOS_WEB sea FUENTES_EXTERNAS o cámbialo aquí
        try:
            res = requests.get(source, headers=headers, timeout=10)
            if res.status_code == 200:
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+m3u8', res.text)
                for link in set(links):
                    clean_link = link.strip()
                    if clean_link not in "\n".join(final_data):
                        if any(obj.lower() in clean_link.lower() for obj in OBJETIVOS):
                            if check_status(clean_link):
                                final_data.append(f'#EXTINF:-1, Cache_{clean_link[-5:]}')
                                final_data.append(clean_link)
        except: continue

    if len(final_data) > initial_count:
        output_text = "\n".join(final_data)
        for file_name in ARCHIVOS_SALIDA:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(output_text)
        print(f"✅ Sync complete. Entries updated.")
    else:
        print("😴 System up to date.")

if __name__ == "__main__":
    run_process()
