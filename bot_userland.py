import requests
import re

ARCHIVO = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def extraccion_medula():
    print("--- INICIANDO EXTRACCIÓN DE MÉDULA (CANAL POR CANAL) ---")
    enlaces = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6)',
        'Referer': URL_BASE
    }

    try:
        # 1. Buscamos el script que contiene la base de datos de canales
        print(f"Escaneando estructura de {URL_BASE}...")
        r = requests.get(URL_BASE, headers=headers, timeout=15).text
        
        # Esta regex busca patrones de enlaces internos de partidos/canales
        canales = re.findall(r'href="(https://futbollibre\.ec/embed/[^"]+)"', r)
        
        if not canales:
            # Intento alternativo con rutas relativas
            canales = [URL_BASE + c for c in re.findall(r'href="(/embed/[^"]+)"', r)]

        print(f"Se detectaron {len(canales)} canales potenciales.")

        for url_canal in list(set(canales)):
            nombre = url_canal.split('/')[-1].replace('-', ' ').upper()
            print(f"[*] Analizando tráfico interno de: {nombre}...")
            
            try:
                # Entramos a la página del canal para buscar el flujo real
                r_canal = requests.get(url_canal, headers={'Referer': URL_BASE}, timeout=10).text
                # El truco de Jhon Doe: buscar el m3u8 dentro de los parámetros de carga
                match = re.search(r'source:\s*"([^"]+)"', r_canal.replace('\\/', '/'))
                
                if match:
                    link = match.group(1)
                    enlaces.append(f"#EXTINF:-1, [FULL-SCAN] {nombre}\n{link}|Referer={URL_BASE}/")
                    print(f"    ✅ Canal capturado con éxito.")
                else:
                    print(f"    ❌ El canal {nombre} está protegido por token dinámico.")
            except:
                continue

    except Exception as e:
        print(f"Falla en la matriz: {e}")
        
    return enlaces

if __name__ == "__main__":
    lista = extraccion_medula()
    if lista:
        # Mantenemos los de IPTV-org y sumamos los nuevos
        with open(ARCHIVO, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(lista))
        print(f"\nSe añadieron {len(lista)} canales nuevos a la lista.")
    else:
        print("\nNo se pudo extraer contenido nuevo de las páginas deportivas.")
