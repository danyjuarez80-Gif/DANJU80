import requests
import re

ARCHIVOS_SALIDA = ["DANJU80", "lista_dany.m3u"]
# Tu link para rescatar lo que ya hay en el repo
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

# Listas de donde el bot va a "robar" links frescos
FUENTES_EXTERNAS = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://iptv-org.github.io/iptv/categories/movies.m3u"
]

# Palabras clave de los canales que quieres que el bot pesque
BUSQUEDA_OBJETIVO = [
    "ESPN", "FOX SPORTS", "TUDN", "AZTECA 7", "CANAL 5", 
    "LAS ESTRELLAS", "TELEMUNDO", "UNIVISION", "HBO", "WARNER"
]

def ejecutar():
    print("🕵️ El bot está saliendo a buscar canales...")
    
    # 1. PASO SAGRADO: Recuperar tus canales actuales
    lineas_finales = []
    try:
        r_old = requests.get(URL_RESCATE, timeout=10)
        if r_old.status_code == 200:
            lineas_finales = [l.strip() for l in r_old.text.splitlines() if l.strip()]
            print(f"📚 Tus {len(lineas_finales)} canales actuales están a salvo.")
    except:
        lineas_finales = ["#EXTM3U"]

    if not lineas_finales: lineas_finales = ["#EXTM3U"]

    # 2. BUSQUEDA MASIVA
    for url_fuente in FUENTES_EXTERNAS:
        try:
            print(f"📡 Rastreando fuente: {url_fuente.split('/')[-1]}")
            res = requests.get(url_fuente, timeout=15)
            if res.status_code == 200:
                contenido_fuente = res.text
                
                for objetivo in BUSQUEDA_OBJETIVO:
                    # Buscamos el canal y su link m3u8
                    matches = re.findall(rf'#EXTINF:.*{objetivo}.*\n(http.*)', contenido_fuente, re.IGNORECASE)
                    
                    for link in matches[:3]: # Traer máximo 3 opciones por canal
                        link_limpio = link.strip()
                        # Solo agregamos si no lo tenemos ya repetido
                        if link_limpio not in "\n".join(lineas_finales):
                            lineas_finales.append(f'#EXTINF:-1 group-title="CAZADOS", {objetivo} (Auto)')
                            lineas_finales.append(link_limpio)
        except:
            continue

    # 3. GUARDADO FINAL
    texto_final = "\n".join(lineas_finales)
    for nombre in ARCHIVOS_SALIDA:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto_final)
    
    print(f"✅ ¡Chamba terminada! Lista actualizada en GitHub.")

if __name__ == "__main__":
    ejecutar()
