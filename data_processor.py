import requests
import re

# Archivos de salida ninja
ARCHIVOS_SALIDA = ["Danju80.txt", "system_cache.log"]
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/Danju80.txt"

# TUS PÁGINAS SELECCIONADAS
SITIOS_WEB = [
    "https://www.tvplusgratis2.com/",
    "https://futbol-libre.su/",
    "https://television.libre.futbol/tv7/",
    "https://tvlibr3.com/"
]

# Filtros para capturar lo mejor
OBJETIVOS = ["ESPN", "FOX", "TUDN", "AZTECA", "CANAL", "TELE", "UNI", "WIN", "DIRECTV", "STAR"]

def run_process():
    print("🪄 Ejecutando magia en tus fuentes personales...")
    final_data = ["#EXTM3U"]
    
    # 1. Recuperar base actual
    try:
        r_old = requests.get(URL_RESCATE, timeout=5)
        if r_old.status_code == 200:
            final_data = [l.strip() for l in r_old.text.splitlines() if l.strip()]
    except: pass

    if not final_data or not final_data[0].startswith("#EXTM3U"):
        final_data = ["#EXTM3U"]
    
    count_antes = len(final_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 2. Escaneo profundo en tus sitios
    for source in SITIOS_WEB:
        try:
            print(f"📡 Escaneando: {source}")
            # Tiempo límite de 6 segundos por sitio para no fallar
            res = requests.get(source, headers=headers, timeout=6)
            if res.status_code == 200:
                # Buscamos links de video directo
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+(?:m3u8|ts)', res.text)
                
                for link in set(links):
                    link_limpio = link.strip()
                    if link_limpio not in "\n".join(final_data):
                        # Si coincide con deportes o tus canales
                        if any(obj.lower() in link_limpio.lower() for obj in OBJETIVOS):
                            print(f"✨ ¡Cazado!: {link_limpio[-30:]}")
                            final_data.append(f'#EXTINF:-1, Magia_{link_limpio[-5:]}')
                            final_data.append(link_limpio)
        except Exception as e:
            print(f"⚠️ Salto {source} por lentitud.")
            continue

    # 3. GUARDADO TOTAL
    output_text = "\n".join(final_data)
    for file_name in ARCHIVOS_SALIDA:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(output_text)
            
    print(f"✅ Magia terminada. Total canales: {len(final_data)//2}")
    print(f"📈 Nuevos agregados: {(len(final_data)-count_antes)//2}")

if __name__ == "__main__":
    run_process()
