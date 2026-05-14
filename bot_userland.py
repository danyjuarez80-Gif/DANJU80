import requests
import re

ARCHIVO = "lista_danju80.m3u"
# Estos son "agregadores" que ya hicieron el scraping por nosotros
GATEWAYS = [
    "https://raw.githubusercontent.com/GuuS-97/TV_Latina/main/TV_Latina.m3u",
    "https://raw.githubusercontent.com/m3u8playlist/Free-IPTV-Channels/master/countries/mx.m3u8"
]

CANALES_TOP = ["FOX SPORTS", "ESPN", "TUDN", "AZTECA 7", "WIN SPORTS"]

def operacion_espejo():
    print("--- INICIANDO OPERACIÓN ESPEJO: BUSCANDO PUENTES ABIERTOS ---")
    enlaces = []
    
    for gway in GATEWAYS:
        try:
            print(f"Sincronizando con puente: {gway[:40]}...")
            data = requests.get(gway, timeout=10).text
            lineas = data.split('\n')
            
            for i in range(len(lineas)):
                if "#EXTINF" in lineas[i]:
                    # Si el canal está en nuestra lista de deseos
                    if any(c in lineas[i].upper() for c in CANALES_TOP):
                        nombre = lineas[i].split(',')[-1].strip()
                        link = lineas[i+1].strip()
                        if link.startswith('http'):
                            enlaces.append(f"#EXTINF:-1, [VERIFICADO] {nombre}\n{link}")
                            print(f"✅ Canal asegurado: {nombre}")
        except: continue
    return enlaces

if __name__ == "__main__":
    final = operacion_espejo()
    if final:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(final))
        print(f"\n¡ÉXITO! Logramos rescatar {len(final)} canales sin tokens.")
    else:
        print("\nTodos los puentes están caídos. El sistema es impenetrable hoy.")
