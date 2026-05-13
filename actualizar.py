import requests
import re

ARCHIVOS_SALIDA = ["DANJU80", "lista_dany.m3u"]
URL_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    print("🚀 Iniciando actualización segura...")
    
    # 1. RECUPERAR: Leemos lo que ya tienes para NO borrarlo
    lineas_finales = []
    try:
        r_old = requests.get(URL_RAW, timeout=10)
        if r_old.status_code == 200:
            lineas_finales = [l.strip() for l in r_old.text.splitlines() if l.strip()]
            print(f"📚 Recuperados {len(lineas_finales)} canales previos.")
        else:
            lineas_finales = ["#EXTM3U"]
    except:
        lineas_finales = ["#EXTM3U"]

    # 2. CANALES FIJOS (Si no están ya, los agrega)
    canales_fijos = [
        {"n": "Azteca 7 HD", "u": "https://televisa-latam-azteca7-1-mx.samsung.wurl.com/manifest/playlist.m3u8"},
        {"n": "Telemundo", "u": "https://telemundo-usa-east-1-mx.samsung.wurl.com/manifest/playlist.m3u8"}
    ]

    for c in canales_fijos:
        if c["u"] not in "\n".join(lineas_finales):
            lineas_finales.append(f'#EXTINF:-1 group-title="FIJOS", {c["n"]}')
            lineas_finales.append(c["u"])

    # 3. BUSCAR NUEVOS (Sin borrar los anteriores)
    try:
        r = requests.get("https://iptv-org.github.io/iptv/countries/mx.m3u", timeout=10)
        if r.status_code == 200:
            for busqueda in ["ESPN", "FOX", "TUDN"]:
                matches = re.findall(rf'#EXTINF:.*{busqueda}.*\n(http.*)', r.text, re.IGNORECASE)
                for link in matches[:1]:
                    if link.strip() not in "\n".join(lineas_finales):
                        lineas_finales.append(f'#EXTINF:-1 group-title="AUTO", {busqueda}')
                        lineas_finales.append(link.strip())
    except: pass

    # 4. GUARDADO FINAL
    texto_final = "\n".join(lineas_finales)
    for nombre in ARCHIVOS_SALIDA:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto_final)
    
    print("✅ Lista actualizada sin borrar tus canales.")

if __name__ == "__main__":
    ejecutar()
