import requests
import os
import re
from playwright.sync_api import sync_playwright

# Configuración de URLs
URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE = "https://www.tvplusgratis2.com/"

def es_m3u8(url):
    """ Filtra solo los enlaces de video reales, ignorando basura publicitaria """
    filtros = ["google", "ads", "analytics", "facebook", "mp4", "log", "pixel"]
    return ".m3u8" in url and len(url) > 50 and not any(x in url.lower() for x in filtros)

def ejecutar():
    # 1. LEER ARCHIVO ACTUAL PARA MANTENER TUS MANUALES Y BUSCAR EL ÚLTIMO NÚMERO
    lineas_finales = []
    ultimo_num = 70
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        content = r.text if r.status_code == 200 else ""
        if not content and os.path.exists("DANJU80"):
            with open("DANJU80", "r", encoding="utf-8") as f: content = f.read()

        for linea in content.splitlines():
            if "noticia" in linea.lower():
                # Buscamos el número más alto en tus líneas actuales
                nums = re.findall(r'\d+', linea)
                if nums:
                    n = int(nums[-1])
                    if n > ultimo_num: ultimo_num = n
            # Guardamos la línea (si es #EXTM3U la saltamos para no duplicar el encabezado luego)
            if "#EXTM3U" not in linea:
                lineas_finales.append(linea)
    except Exception as e:
        print(f"⚠️ Error leyendo base: {e}")

    with sync_playwright() as p:
        # Lanzamos el navegador con identidad de celular
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            extra_http_headers={"Referer": URL_BASE}
        )
        page = context.new_page()

        links_vivos = []
        # Capturamos el tráfico de red como lo hace Web Video Caster
        page.on("request", lambda req: links_vivos.append(req.url) if es_m3u8(req.url) else None)

        try:
            nombre_canal = "noticia" 
            print(f"📡 Buscando enlace fresco para {nombre_canal}...")
            
            # Cambia esta URL por el canal que quieras rastrear hoy
            page.goto(f"{URL_BASE}tudn-en-vivo.html", timeout=60000, wait_until="networkidle")
            
            # ESPERA DE PACIENCIA: 15 segundos para que cargue el video y suelte el link
            page.wait_for_timeout(15000) 
            
            # Simulamos un clic para activar el reproductor si está pausado
            page.mouse.click(300, 300)
            page.wait_for_timeout(5000)

            if links_vivos:
                # Tomamos el link más reciente y le inyectamos las credenciales (Referer)
                raw_link = links_vivos[-1].split("'")[0].split('"')[0]
                # ESTA ES LA CLAVE: El reproductor ahora dirá que viene de la web original
                nuevo_link = f"{raw_link}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                
                print(f"✅ Link capturado con Referer!")

                # BUSCAR SI EL CANAL YA EXISTE PARA ACTUALIZARLO
                encontrado = False
                for i, linea in enumerate(lineas_finales):
                    if f"{nombre_canal} {ultimo_num}" in linea:
                        if i + 1 < len(lineas_finales):
                            lineas_finales[i+1] = nuevo_link
                            encontrado = True
                            print(f"🔄 Actualizado: {nombre_canal} {ultimo_num}")
                            break
                
                # SI ES TOTALMENTE NUEVO, CREARLO
                if not encontrado:
                    ultimo_num += 1
                    lineas_finales.append(f'#EXTINF:-1 group-title="TV",{nombre_canal} {ultimo_num}')
                    lineas_finales.append(nuevo_link)
                    print(f"➕ Agregado nuevo: {nombre_canal} {ultimo_num}")
            else:
                print("❌ No se detectó tráfico m3u8. Prueba con otro canal.")

        except Exception as e:
            print(f"⚠️ Error en el proceso: {e}")
        
        browser.close()

    # 3. GUARDADO FINAL LIMPIO
    # Unimos el encabezado con todas las líneas (manuales + automáticas actualizadas)
    resultado = ["#EXTM3U"] + [l for l in lineas_finales if l.strip()]
    
    contenido_final = "\n".join(resultado)

    # Escribimos los archivos
    for archivo in ["DANJU80", "lista_dany.m3u"]:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido_final)
    
    print("🚀 Proceso terminado con éxito.")

if __name__ == "__main__":
    ejecutar()
