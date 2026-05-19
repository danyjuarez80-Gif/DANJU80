import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🔥 Iniciando Operación Terco en ESPN Premium...")
        
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={"width": 360, "height": 740}
        )
        page = await context.new_page()
        
        links_video = []

        # El interceptor se queda activo todo el tiempo atrapando lo que caiga
        def revisar_trafico(res):
            url = res.url
            ct = res.headers.get('content-type', '').lower()
            if any(ext in url.lower() for ext in [".m3u8", ".ts", ".mpd", "playlist"]):
                if not any(banned in url for banned in ["google", "analytics", "facebook", "doubleclick"]):
                    links_video.append(f"[VIDEO] -> {url}")
            elif "mpegurl" in ct or "video/mp2t" in ct:
                links_video.append(f"[MIME VIDEO] -> {url}")

        page.on("response", revisar_trafico)

        try:
            url_target = "https://tvlibr3.com/en-vivo/espn-premium/"
            print(f"📡 Conectando a: {url_target}")
            await page.goto(url_target, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)

            # 1. Forzamos el clic en la Opción 1 para asegurar que monte el reproductor
            print("👇 Activando Opción 1...")
            opcion = page.locator("text=/Opción 1/i").first
            if await opcion.is_visible():
                await opcion.click()
            await asyncio.sleep(5) # Esperamos a que cargue el reproductor negro

            # 2. EL CICLO TERCO: Picar, esperar, volver a picar en el centro del reproductor
            # Coordenadas (180, 300) que es justo donde sale el botón de Play en la foto
            for intento in range(1, 5):
                print(f"👆 Ponchando el reproductor - Intento #{intento}...")
                await page.mouse.click(180, 300)
                
                print(f"⏳ Esperando 8 segundos a que pase el comercial o reaccione...")
                await asyncio.sleep(8)

            # 3. Guardia final: Nos quedamos 20 segundos quietos escuchando si el video ya fluye
            print("📡 Dejando el receptor abierto para pescar el m3u8 de fondo...")
            await asyncio.sleep(20)

            # Tomamos foto para ver si el triángulo de Play ya se quitó
            await page.screenshot(path="pantalla_final.png")
            print("📸 Foto final guardada.")

        except Exception as e:
            print(f"❌ Tronó el intento: {e}")
        finally:
            await browser.close()

        # Guardar resultados
        with open("resultados_trafico.txt", "w", encoding="utf-8") as f:
            if links_video:
                f.write(f"¡A HUEVO! La terquedad funcionó. Enlaces encontrados:\n\n")
                for link in set(links_video):
                    f.write(link + "\n")
            else:
                f.write("Ni con la racha de clics soltó el video. Esos comerciales están durísimos.\n")

if __name__ == "__main__":
    asyncio.run(run())
