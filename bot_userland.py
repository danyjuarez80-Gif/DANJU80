import requests
import re
import time

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"

def extraer_tv_plus():
    print("--- Escaneando TVPlusGratis2 ---")
    enlaces = []
    url_tvplus = "https://www.tvplusgratis2.com/"
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 11)'}
    
    try:
        r = requests.get(url_tvplus, headers=headers, timeout=15).text
        # Buscamos los cuadros de canales en la pagina principal
        canales = re.findall(r'href="(https://www.tvplusgratis2.com/[^"]+)"[^>]*>.*?<h2[^>]*>(.*?)</h2>', r, re.DOTALL)
        
        for link_canal, nombre in canales:
            nombre = nombre.strip().upper()
            # Filtramos para no traer cosas que no sean canales
            if "DMCA" in nombre or "CONTACTO" in nombre: continue
            
            print(f"Procesando: {nombre}...")
            time.sleep(2) # Pausa para no ser bloqueado por UserLand
            
            # Entramos al canal para buscar el reproductor
            r_int = requests.get(link_canal, headers=headers, timeout=10).text
            # Buscamos el m3u8 o el iframe del video
            m3u8 = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_int)
            if m3u8:
                link_final = m3u8.group(1)
                enlaces.append(f"#EXTINF:-1, [TV+] {nombre}\n{link_final}|Referer={url_tvplus}")
    except Exception as e:
        print(f"Error en TVPlus: {e}")
    return enlaces

def principal():
    # 1. Cargar canales fijos
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    # 2. Rastreo de Fútbol Libre (el que ya tenías)
    # Aqui va tu funcion anterior de futbol libre o puedes usar esta simplificada
    
    # 3. Rastreo de la nueva pagina
    nuevos_tvplus = extraer_tv_plus()

    # 4. Guardar todo
    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        f.write("# --- CANALES DE TV PLUS GRATIS ---\n")
        f.write("\n".join
