import asyncio
import re
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🚀 DESATANDO MAGIA: Extracción de código fuente en ESPN Premium...")
        
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={"width": 360, "height": 740}
        )
        page = await context.new_page()
        
        links_encontrados = set()

        # Interceptor de red de respaldo
        def revisar_red(res):
            url = res.url
            if any(ext in url.lower() for ext in [".m3u8", ".ts", "playlist.m3u8"]):
                if not any(b in url for b in ["google", "analytics"]):
                    links_encontrados.add(f"[RED] -> {url}")

        page.on("response", revisar_red)

        try:
            url_target = "https://tvlibr3.com/en-vivo/espn-premium/"
            print(f"📡 Conectando a la fuente: {url_target}")
            
            # Cargamos la página base
            await page.goto(url_target, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(7)

            # 🛠️ MAGIA 1: Raspar el HTML de todos los marcos (iframes) ocultos
            print("🕵️ Escaneando iframes internos...")
            marcos = page.frames
            print(f"📋 Se detectaron {len(marcos)} estructuras internas.")
            
            for i, marco in enumerate(marcos):
                try:
                    html_interno = await marco.content()
                    
                    # Buscamos patrones de video (.m3u8, .ts, .mpd) grabados en texto plano
                    enlaces_m3u8 = re.findall(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', html_interno)
                    enlaces_ts = re.findall(r'(https?://[^\s"\']+\.ts[^\s"\']*)', html_interno)
                    
                    for link in enlaces_m3u8 + enlaces_ts:
                        if "bestleague" in link or "stream" in link or "live" in link:
                            links_encontrados.add(f"[TEXTO-IFRAME-{i}] -> {link}")
                except Exception:
                    continue

            # 🛠️ MAGIA 2: Extraer variables de JavaScript cargadas en memoria
            print("🧠 Extrayendo scripts de reproducción...")
            scripts = await page.locator("script").all_inner_texts()
            for script in scripts:
                enlaces_js = re.findall(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', script)
                for link in enlaces_js:
                    links_encontrados.add(f"[JS-VARIABLE] -> {link}")

            # Tomamos una foto solo para ver el estado de la carga
            await page.screenshot(path="pantalla_final.png")

        except Exception as e:
            print(f"❌ Tronó el descifrado: {e}")
        finally:
            await browser.close()

        # Guardar el reporte final
        with open("resultados_trafico.txt", "w", encoding="utf-8") as f:
            if links_encontrados:
                f.write(f"¡PUM! Rompimos el blindaje. Enlaces IPTV extraídos:\n\n")
                for link in links_encontrados:
                    f.write(link + "\n")
            else:
                f.write("El código fuente viene encriptado u oculto por tokens dinámicos.\n")

if __name__ == "__main__":
    asyncio.run(run())
