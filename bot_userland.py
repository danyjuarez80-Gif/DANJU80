import requests
import os

# Archivo de salida
ARCHIVO = "lista_danju80.m3u"

# Usaremos una fuente que ya hace el trabajo pesado por nosotros
# Estas listas se actualizan constantemente y son compatibles con IPTV
FUENTES_IPTV = [
    "https://raw.githubusercontent.com/fabiosemper/m3u/main/deportes.m3u",
    "https://iptv-org.github.io/iptv/countries/mx.m3u"
]

PRIORIDAD = ["ESPN", "FOX SPORTS", "TUDN", "AZTECA", "TELEMUNDO", "UNIVISION"]

def actualizar_lista():
    print("--- Recuperando Canales de Fuentes Verificadas ---")
    nueva_lista = ["#EXTM3U"]
    
    for url in FUENTES_IPTV:
        try:
            print(f"Obteniendo canales de: {url}")
            r = requests.get(url, timeout=10).text
            lineas = r.split("\n")
            
            for i in range(len(lineas)):
                # Si la línea tiene el nombre del canal
                if "#EXTINF" in lineas[i]:
                    # Verificamos si es uno de nuestros canales prioritarios
                    if any(p in lineas[i].upper() for p in PRIORIDAD):
                        # Guardamos esa línea y la siguiente (que es el link m3u8)
                        nueva_lista.append(lineas[i])
                        nueva_lista.append(lineas[i+1])
                        print(f"✅ Canal encontrado: {lineas[i].split(',')[-1]}")
        except:
            continue
            
    if len(nueva_lista) > 1:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write("\n".join(nueva_lista))
        return True
    return False

if __name__ == "__main__":
    if actualizar_lista():
        print(f"\nÉXITO: Se creó la lista con canales deportivos.")
    else:
        print("\nERROR: No se pudieron obtener canales de las fuentes.")
