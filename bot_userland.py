import requests
import re
import time

ARCHIVO = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def escaneo_quirurgico():
    print("--- INICIANDO ESCANEO PROFUNDO: CANAL POR CANAL ---")
    enlaces = []
    sesion = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6)',
        'Referer': URL_BASE
    }

    try:
        # 1. Obtenemos todos los links de la página principal
        print(f"Obteniendo lista de objetivos en {URL_BASE}...")
        home = sesion.get(URL_BASE, headers=headers, timeout=10).text
        # Buscamos patrones de canales (ej: href="/embed/espn-1")
        rutas_canales = re.findall(r'href="(/embed/[^"]+)"', home)
        # Eliminamos duplicados
        rutas_canales = list(set(rutas_canales))
        
        print(f"Se encontraron {len(rutas_canales)} objetivos. Iniciando infiltración individual...")

        for ruta in rutas_canales:
            nombre_canal = ruta.split('/')[-1].replace('-', ' ').upper()
            url_canal = URL_BASE + ruta
            print(f"[*] Entrando a: {nombre_canal}...")
            
            try:
                # 2. ENTRADA AL CANAL: Simulamos que el humano entró a la página del canal
                # Esperamos un segundo para no alertar al anti-bot
                time.sleep(1)
                html_canal = sesion.get(url_canal, headers=headers, timeout=7).text
                
                # 3. BÚSQUEDA DEL REPRODUCTOR: Buscamos el iframe o script que carga el video
                # Buscamos cualquier cosa que termine en .m3u8 pero limpiando el 'escape' \/
                # como lo haría un sniffer de tráfico
                html_limpio = html_canal.replace('\\/', '/')
                match = re.search(r'["\'](http[^"\']+\.m3u8[^"\']*)["\']', html_limpio)
                
                if match:
                    link_vulnerable = match.group(1).split('"')[0].split("'")[0]
                    # Agregamos el Referer de la página del canal para que no se corte
                    formato = f"#EXTINF:-1, [DEEP-SCAN] {nombre_canal}\n{link_vulnerable}|Referer={url_canal}"
                    enlaces.append(formato)
                    print(f"    ✅ ¡SISTEMA VULNERADO! Link capturado en {nombre_canal}")
                else:
                    print(f"    ❌ No se detectó flujo abierto en {nombre_canal}. (Posible token dinámico)")
            
            except Exception as e:
                print(f"    ⚠️ Error al escanear {nombre_canal}: {e}")
                continue

    except Exception as e:
        print(f"Falla crítica en el escaneo: {e}")
        
    return enlaces

if __name__ == "__main__":
    lista_final = escaneo_quirurgico()
    if lista_final:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(lista_final))
        print(f"\nOperación finalizada. Se extrajeron {len(lista_final)} canales reales.")
    else:
        print("\nEl escaneo profundo no encontró brechas de seguridad hoy.")
