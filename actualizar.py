import requests
import re

# Nombres de tus archivos en el repo
ARCHIVOS_SALIDA = ["DANJU80", "lista_dany.m3u"]

# Canales fijos que SIEMPRE deben estar (Links estables)
CANALES_FIJOS = [
    {"n": "Azteca 7 HD", "u": "https://televisa-latam-azteca7-1-mx.samsung.wurl.com/manifest/playlist.m3u8"},
    {"n": "Telemundo", "u": "https://telemundo-usa-east-1-mx.samsung.wurl.com/manifest/playlist.m3u8"},
    {"n": "NASA TV (Prueba)", "u": "https://ntv1.akamaized.net/hls/live/2014049/NASA-NTV1/master.m3u8"}
]

def ejecutar():
    print("🚀 Iniciando actualización...")
    
    # 1. Empezamos la lista limpia para evitar errores de VLC
    lineas = ["#EXTM3U"]
    
    # 2. Agregamos los canales fijos
    for c in CANALES_FIJOS:
        lineas.append(f'#EXTINF:-1 group-title="FIJOS", {c["n"]}')
        lineas.append(c["u"])
    
    # 3. Intentamos buscar en una fuente externa de respaldo
    try:
        r = requests.get("https://iptv-org.github.io/iptv/countries/mx.m3u", timeout=10)
        if r.status_code == 200:
            # Solo buscamos canales específicos para no saturar tu lista
            for canal in ["ESPN", "FOX", "TUDN", "Canal 5"]:
                matches = re.findall(rf'#EXTINF:.*{canal}.*\n(http.*)', r.text, re.IGNORECASE)
                for link in matches[:2]: # Máximo 2 links por canal
                    lineas.append(f'#EXTINF:-1 group-title="AUTO", {canal}')
                    lineas.append(link.strip())
    except Exception as e:
        print(f"⚠️ No se pudo conectar a la fuente externa: {e}")

    texto_final = "\n".join(lineas)

    # 4. GUARDADO: Escribir en los dos archivos que usas
    for nombre_archivo in ARCHIVOS_SALIDA:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(texto_final)
            print(f"✅ Archivo {nombre_archivo} guardado con éxito.")

if __name__ == "__main__":
    ejecutar()
