import requests
import re

# Los tres archivos que mantenemos al cien
ARCHIVOS_SALIDA = ["Danju80.txt", "DANJU80", "system_cache.log"]
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/Danju80.txt"

SITIOS_WEB = [
    "https://www.tvplusgratis2.com/",
    "https://futbol-libre.su/",
    "https://television.libre.futbol/tv7/",
    "https://tvlibr3.com/"
]

# Filtros de búsqueda
OBJETIVOS = ["ESPN", "FOX", "TUDN", "AZTECA", "CANAL", "TELE", "UNI", "WIN", "DIRECTV", "STAR"]

def run_process():
    print("🎯 Buscando links reales de video...")
    final_data = []
    
    try:
        r_old = requests.get(URL_RESCATE, timeout=5)
        if r_old.status_code == 200:
            final_data = [l.strip() for l in r_old.text.splitlines() if l.strip()]
    except:
        final_data = ["#EXTM3U"]

    if not final_data or not final_data[0].startswith("#EXTM3U"):
        final_data = ["#EXTM3U"]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    nuevos_encontrados = 0
    
    for source in SITIOS_WEB:
        try:
            res = requests.get(source, headers=headers, timeout=8)
            if res.status_code == 200:
                # CAMBIO CLAVE: Solo buscamos archivos que terminen en .m3u8 o .ts
                # Quitamos la captura de páginas genéricas
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(?:m3u8|ts)', res.text)
                
                for link in set(links):
                    link_limpio = link.strip()
                    if link_limpio not in "\n".join(final_data):
                        # Verificamos que sea de los canales que quieres
                        if any(obj.lower() in link_limpio.lower() for obj in OBJETIVOS):
                            final_data.append(f'#EXTINF:-1, Canal_Real_{link_limpio[-8:-5]}')
                            final_data.append(link_limpio)
                            nuevos_encontrados += 1
        except: continue

    # Solo guardamos si encontramos algo que valga la pena
    output_text = "\n".join(final_data)
    for file_name in ARCHIVOS_SALIDA:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(output_text)
            
    print(f"✅ Proceso terminado. Se agregaron {nuevos_encontrados} links de video reales.")

if __name__ == "__main__":
    run_process()
