import requests
import re

# Archivos de salida
ARCHIVOS_SALIDA = ["Danju80.txt", "DANJU80", "system_cache.log"]
# ESTA ES LA CLAVE: Tu archivo actual en GitHub
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/Danju80.txt"

SITIOS_WEB = [
    "https://www.tvplusgratis2.com/",
    "https://futbol-libre.su/",
    "https://television.libre.futbol/tv7/",
    "https://tvlibr3.com/"
]

OBJETIVOS = ["ESPN", "FOX", "TUDN", "AZTECA", "CANAL", "TELE", "UNI", "WIN", "DIRECTV", "STAR"]

def run_process():
    print("🛡️ Cargando escudo de protección de datos...")
    
    # 1. CARGAR LO QUE YA TIENES (PARA NO PERDER AVANCES)
    base_datos = []
    try:
        r = requests.get(URL_RESCATE, timeout=10)
        if r.status_code == 200:
            # Filtramos para no tener líneas vacías y mantener el orden
            base_datos = [line.strip() for line in r.text.splitlines() if line.strip()]
            print(f"📦 Avance recuperado: {len(base_datos)//2} canales asegurados.")
        else:
            base_datos = ["#EXTM3U"]
    except:
        print("⚠️ No se pudo conectar con GitHub, usando base vacía.")
        base_datos = ["#EXTM3U"]

    if not base_datos or not base_datos[0].startswith("#EXTM3U"):
        base_datos = ["#EXTM3U"]

    # Guardamos una copia del texto actual para comparar rápido
    texto_actual = "\n".join(base_datos)
    nuevos = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    # 2. BUSCAR NUEVOS CANALES
    for source in SITIOS_WEB:
        try:
            res = requests.get(source, headers=headers, timeout=8)
            if res.status_code == 200:
                # Solo buscamos links de video reales (.m3u8 o .ts)
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(?:m3u8|ts)', res.text)
                
                for link in set(links):
                    if link not in texto_actual:
                        if any(obj.lower() in link.lower() for obj in OBJETIVOS):
                            base_datos.append(f'#EXTINF:-1, Canal_Nuevo_{link[-5:]}')
                            base_datos.append(link)
                            nuevos += 1
        except: continue

    # 3. GUARDAR TODO JUNTO (LO VIEJO + LO NUEVO)
    if nuevos > 0:
        resultado_final = "\n".join(base_datos)
        for file_name in ARCHIVOS_SALIDA:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(resultado_final)
        print(f"✅ ¡Éxito! Mantuvimos lo anterior y sumamos {nuevos} canales.")
    else:
        print("😴 No hubo nada nuevo, pero tu avance sigue intacto.")

if __name__ == "__main__":
    run_process()
