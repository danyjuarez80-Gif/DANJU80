import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🔥 Iniciando Extractor de Canales en tvlibr3.com...")
        
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={"width": 360, "height": 740}
        )
        page = await context.new_page()
        
        links_video = []

        # Capturador especializado: Solo guarda si encuentra indicios de video real
        def revisar_trafico(res):
            url = res.url
            ct = res.headers.get('content-type', '').lower()
            # Buscamos m3u8, ts, o respuestas de tipo stream/mpegurl
            if any(ext in url for ext in [".m3u8", ".ts", "playlist.m3u8", "master.m3u8"]):
                links_video.append(f"[DIRECTO] -> {url}")
            elif "mpegurl" in ct or "video/mp2t" in ct or "application/x-mpegurl" in ct:
                links_video.append(f"[MIME: {ct}] -> {url}")

        page.on("response", revisar_trafico)

        try:
            # 1. Entramos directo a la página
            await page.goto("https://tvlibr3.com/", wait_until="load", timeout=60000)
            await asyncio.sleep(5)

            # 2. SELECCIÓN DE CANAL: Buscamos el primer enlace de canal disponible y le picamos
            print("📡 Buscando un canal para abrir...")
            # Buscamos elementos que apunten a transmisiones (generalmente contienen la agenda o logos)
            enlaces = await page.locator("a").all_urls()
            canal_url = None
            for url in enlaces:
                if "agenda" not in url and url != "https://tvlibr3.com/":
                    canal_url = url
                    break
            
            if canal_url:
                print(f"📺 Entrando al canal: {canal_url}")
                await page.goto(canal_url, wait_until="load", timeout=60000)
                await asyncio.sleep(5)
            else:
                print("⚠️ No se detectó sub-enlace, intentando interactuar en la pantalla actual...")

            # 3. EL TRUCO DEL PLAY: Simulamos clics agresivos donde suele estar el reproductor
            print("👆 Botoneando el reproductor para forzar el flujo m3u8...")
            # Clic en el centro de la pantalla para activar el reproductor y comernos el primer anuncio
            await page.mouse.click(180, 350)
            await asyncio.sleep(3)
            
            # Segundo clic en el mismo punto (por si el primero fue un pop-up invisible)
            await page.mouse.click(180, 350)
            print("⏳ Esperando 20 segundos para recolectar el flujo de video...")
            await asyncio.sleep(20)

            # Tomamos foto para verificar si se abrió el reproductor o se quedó en publicidad
            await page.screenshot(path="pantalla_final.png")

        except Exception as e:
            print(f"❌ Error en la ejecución: {e}")
        finally:
            await browser.close()

        # Guardar solo los enlaces limpios de IPTV que se pescaron
        with open("resultados_trafico.txt", "w", encoding="utf-8") as f:
            if links_video:
                f.write(f"¡PUM! Se encontraron {len(links_video)} enlaces de video activos:\n\n")
                for link in set(links_video):
                    f.write(link + "\n")
            else:
                f.write("No se capturó ningún flujo m3u8/ts. El reproductor no se activó correctamente.\n")

if __name__ == "__main__":
    asyncio.run(run())
