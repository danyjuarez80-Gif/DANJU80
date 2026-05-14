import requests
import re
import time

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"

def cazar_futbol_libre():
    print("--- Escaneando Fútbol Libre ---")
    enlaces = []
    url_base = "https://futbollibre.ec"
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'}
    try:
        r = requests.get(url_base, headers=headers, timeout=10).text
        bloques = re.findall(r'href="(/embed/[^"]+)"', r)
        for path in set(bloques):
            time.sleep(3) # Pausa para evitar bloqueos en el celular
            r_canal = requests.get(url_base + path, headers=headers, timeout=10).text
            match = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_canal)
            if match:
                link = match.group(1)
                nombre = path.replace("/embed/", "").replace("-", " ").upper()
                enlaces.append(f"#EXTINF:-1, [FUTBOL] {nombre}\n{link}|Referer={url_base}/")
                print(f"¡Cazado!: {nombre}")
    except: pass
    return enlaces

def extraer_tv_plus():
    print("--- Escaneando TVPlusGratis2 ---")
    enlaces = []
    url_tvplus = "https://www.tvplusgratis2.com/"
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 11)'}
    try:
        r = requests.get(url_tvplus, headers=headers, timeout=10).text
        canales = re.findall(r'href="(https://www.tvplusgratis2.com/[^"]+)"[^>]*>.*?<h2[^>]*>(.*?)</h2>', r, re.DOTALL)
        for link_canal, nombre in canales:
            nombre = nombre.strip().upper()
            if any(x in nombre for x in ["DMCA", "CONTACTO", "POLITICA"]): continue
            time.sleep(2)
            r_int = requests.get(link_canal, headers=headers, timeout=10).text
            m3u8 = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_int)
            if m3u8:
                enlaces.append(f"#EXTINF:-1, [TV+] {nombre}\n{m3u8.group(1)}|Referer={url_tvplus}")
                print(f"¡Cazado!: {nombre}")
    except: pass
    return enlaces

def principal():
    # 1. Cargar canales de noticias (fijos)
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    # 2. Ejecutar ambos rastreos
    links_futbol = cazar_futbol_libre()
    links_tvplus = extraer_tv_plus()

    # 3. Guardar todo en el archivo final
    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        
        if links_futbol:
            f.write("# --- CANALES DE FUTBOL LIBRE ---\n")
            f.write("\n".join(links_futbol) + "\n\n")
            
        if links_tvplus:
            f.write("# --- CANALES DE TV PLUS GRATIS ---\n")
            f.write("\n".join(links_tvplus) + "\n")
        
        print(f"Éxito: {len(links_futbol)} de Fútbol y {len(links_tvplus)} de TVPlus guardados.")

if __name__ == "__main__":
    principal()
