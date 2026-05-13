import requests
import re

# Archivos de salida garantizados
ARCHIVOS_SALIDA = ["Danju80.txt", "DANJU80", "system_cache.log"]
# Fuente de rescate para NO borrar tu avance
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/Danju80.txt"

SITIOS_WEB = [
    "https://www.tvplusgratis2.com/",
    "https://futbol-libre.su/",
    "https://television.libre.futbol/tv7/",
    "https://tvlibr3.com/"
]

OBJETIVOS = ["ESPN", "FOX", "TUDN", "AZTECA", "CANAL", "TELE", "UNI", "WIN", "DIRECTV", "STAR"]

def run_process():
    print("🛡️ Asegurando canales y manteniendo avances...")
    base_datos = []
    
    # 1. Recuperar lo que ya tienes
    try:
        r = requests.get(URL_RESCATE, timeout=10)
        if r.status_code == 200:
            base_datos = [line.strip() for line in r.text.splitlines() if line.strip()]
            print(f"📦 Avance recuperado: {len(base_datos)//2} canales.")
        else: base_datos = ["#EXTM3U"]
    except: base_datos = ["#EXTM3U"]

    if not base_datos or not base_datos[0].startswith("#EXTM3U"):
        base_datos = ["#EXTM3U"]

    texto_actual = "\n".join(base_datos)
    nuevos = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    # 2. Búsqueda flexible (Magia mejorada)
    for source in SITIOS_WEB:
        try:
            res = requests.get(source, headers=headers, timeout=8)
            if res.status_code == 200:
                # Buscamos enlaces que contengan tus palabras clave aunque no tengan extensión
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', res.text)
                
                for link in set(links):
                    link_limpio = link.strip().rstrip('/')
                    if link_limpio not in texto_actual:
                        # Si el link tiene el nombre de un canal que quieres
                        if any(obj.lower() in link_limpio.lower() for obj in OBJETIVOS):
                            base_datos.append(f'#EXTINF:-1, Canal_Encontrado_{link_limpio[-5:]}')
                            base_datos.append(link_limpio)
                            nuevos += 1
        except: continue

    # 3. Guardado forzoso
    resultado_final = "\n".join(base_datos)
    for file_name in ARCHIVOS_SALIDA:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(resultado_final)
    print(f"✅ Finalizado. Se sumaron {nuevos} enlaces a tu historial.")

if __name__ == "__main__":
    run_process()
