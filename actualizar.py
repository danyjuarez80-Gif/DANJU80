import requests
import re

ARCHIVOS_SALIDA = ["DANJU80", "lista_dany.m3u"]
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

SITIOS_WEB = [
    "https://www.tvplusgratis.com/",
    "https://televisionlibre.net/es/",
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

BUSQUEDA_OBJETIVO = ["ESPN", "FOX SPORTS", "TUDN", "AZTECA 7", "CANAL 5", "TELEMUNDO", "UNIVISION"]

def esta_vivo(url):
    try:
        # Verificación rápida de 2 segundos
        res = requests.head(url, timeout=2, allow_redirects=True)
        return res.status_code == 200
    except:
        return False

def ejecutar():
    print("🚀 Iniciando búsqueda inteligente...")
    
    # 1. Recuperar lo que ya tienes
    lineas_finales = []
    try:
        r_old = requests.get(URL_RESCATE, timeout=10)
        if r_old.status_code == 200:
            lineas_finales = [l.strip() for l in r_old.text.splitlines() if l.strip()]
            print(f"📚 Canales actuales cargados: {len(lineas_finales)//2}")
    except:
        lineas_finales = ["#EXTM3U"]

    if not lineas_finales: lineas_finales = ["#EXTM3U"]
    
    conteo_inicial = len(lineas_finales)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 2. Cazar en la web
    for sitio in SITIOS_WEB:
        try:
            res = requests.get(sitio, headers=headers, timeout=10)
            if res.status_code == 200:
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+m3u8', res.text)
                for link in set(links):
                    link_limpio = link.strip()
                    if link_limpio not in "\n".join(lineas_finales):
                        if any(obj.lower() in link_limpio.lower() for obj in BUSQUEDA_OBJETIVO):
                            if esta_vivo(link_limpio):
                                print(f"✨ ¡Nuevo y vivo!: {link_limpio[:40]}")
                                lineas_finales.append(f'#EXTINF:-1 group-title="AUTO_CAZA", Canal Nuevo')
                                lineas_finales.append(link_limpio)
        except: continue

    # 3. VERIFICACIÓN DE CAMBIOS: ¿Realmente encontramos algo?
    if len(lineas_finales) > conteo_inicial:
        print(f"✅ Se encontraron { (len(lineas_finales) - conteo_inicial) // 2 } canales nuevos.")
        texto_final = "\n".join(lineas_finales)
        for nombre in ARCHIVOS_SALIDA:
            with open(nombre, "w", encoding="utf-8") as f:
                f.write(texto_final)
    else:
        print("😴 No hay nada nuevo. Proceso terminado sin guardar para ahorrar minutos.")

if __name__ == "__main__":
    ejecutar()
