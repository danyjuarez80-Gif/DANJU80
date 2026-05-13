import requests
import re

ARCHIVOS_SALIDA = ["Danju80.txt", "system_cache.log"]
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/Danju80.txt"

SITIOS_WEB = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://televisionlibre.net/es/",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

OBJETIVOS = ["ESPN", "FOX SPORTS", "TUDN", "AZTECA 7", "CANAL 5", "TELEMUNDO", "UNIVISION"]

def check_status(url):
    try:
        # Bajamos a 2 segundos la verificación de cada link
        res = requests.head(url, timeout=2, allow_redirects=True)
        return res.status_code == 200
    except:
        return False

def run_process():
    print("🚀 Mantenimiento rápido iniciado...")
    final_data = []
    
    try:
        # Carga rápida de la base actual
        r_old = requests.get(URL_RESCATE, timeout=5)
        if r_old.status_code == 200:
            final_data = [l.strip() for l in r_old.text.splitlines() if l.strip()]
    except:
        final_data = ["#EXTM3U"]

    if not final_data or not final_data[0].startswith("#EXTM3U"):
        final_data = ["#EXTM3U"]
    
    initial_count = len(final_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for source in SITIOS_WEB:
        try:
            # SI EL SITIO TARDA MÁS DE 5 SEGUNDOS, LO SALTAMOS
            res = requests.get(source, headers=headers, timeout=5)
            if res.status_code == 200:
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+m3u8', res.text)
                for link in set(links):
                    link_limpio = link.strip()
                    if link_limpio not in "\n".join(final_data):
                        if any(obj.lower() in link_limpio.lower() for obj in OBJETIVOS):
                            if check_status(link_limpio):
                                final_data.append(f'#EXTINF:-1, Sys_Entry_{link_limpio[-5:]}')
                                final_data.append(link_limpio)
        except:
            print(f"⚠️ Salto por lentitud: {source[:20]}")
            continue

    if len(final_data) > initial_count:
        output_text = "\n".join(final_data)
        for file_name in ARCHIVOS_SALIDA:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(output_text)
        print("✅ Guardado rápido completado.")
    else:
        print("😴 Sin cambios.")

if __name__ == "__main__":
    run_process()
