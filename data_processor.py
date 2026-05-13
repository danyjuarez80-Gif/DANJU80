import requests
import re

# Definimos los dos nombres que quieres mantener actualizados
# Agregamos DANJU80 a la lista de salida
ARCHIVOS_SALIDA = ["Danju80.txt", "DANJU80", "system_cache.log"]

# Usamos el .txt como fuente de rescate para no perder nada
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/Danju80.txt"

SITIOS_WEB = [
    "https://www.tvplusgratis2.com/",
    "https://futbol-libre.su/",
    "https://television.libre.futbol/tv7/",
    "https://tvlibr3.com/"
]

OBJETIVOS = ["ESPN", "FOX", "TUDN", "AZTECA", "CANAL", "TELE", "UNI", "WIN", "DIRECTV", "STAR"]

def run_process():
    print("🚀 Iniciando actualización doble (TXT y RAW)...")
    final_data = []
    
    # IMPORTANTE: Cargamos lo que ya tienes para NO borrar nada
    try:
        r_old = requests.get(URL_RESCATE, timeout=5)
        if r_old.status_code == 200:
            # Filtramos líneas vacías y guardamos lo que ya existe
            final_data = [l.strip() for l in r_old.text.splitlines() if l.strip()]
            print(f"📚 Base actual cargada: {len(final_data)//2} canales preservados.")
    except:
        print("⚠️ No se pudo rescatar la lista anterior, empezando de cero.")
        final_data = ["#EXTM3U"]

    if not final_data or not final_data[0].startswith("#EXTM3U"):
        final_data = ["#EXTM3U"]
    
    count_antes = len(final_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for source in SITIOS_WEB:
        try:
            res = requests.get(source, headers=headers, timeout=6)
            if res.status_code == 200:
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+(?:m3u8|ts)', res.text)
                for link in set(links):
                    link_limpio = link.strip()
                    # Solo agregamos si el link NO existe ya en la lista
                    if link_limpio not in "\n".join(final_data):
                        if any(obj.lower() in link_limpio.lower() for obj in OBJETIVOS):
                            final_data.append(f'#EXTINF:-1, Canal_Auto_{link_limpio[-5:]}')
                            final_data.append(link_limpio)
        except: continue

    # Escribimos el resultado en TODOS los archivos de la lista ARCHIVOS_SALIDA
    output_text = "\n".join(final_data)
    for file_name in ARCHIVOS_SALIDA:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(output_text)
            
    print(f"✅ ¡Hecho! {len(final_data)//2} canales guardados en Danju80.txt y DANJU80.")

if __name__ == "__main__":
    run_process()
