import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🔥 Iniciando Extracción Avanzada en ESPN Premium...")
        
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={"width": 360, "height": 740}
        )
        page = await context.new_page()
        
        links_video = []

        # Rastreador de flujos multimedia activos
        def revisar_trafico(res):
            url = res.url
            ct = res.headers.get('content-type', '').lower()
            # Capturamos formatos m3u8, ts, mpd o tipos MIME de video comunes en IPTV
            if any(ext in url.lower() for ext in [".m3u8", ".ts", ".mpd", "chunk", "playlist"]):
                if not any(banned in url for banned in ["google", "analytics", "facebook"]):
                    links_video.append(f"[VIDEO] -> {url}")
            elif "mpegurl" in ct or "video/mp2t" in ct or "video/webm" in ct:
                links_video.append(f"[MIME VIDEO] -> {url} | ({ct})")

        page.on("response", revisar_trafico)

        try:
            # URL real que me pasaste en la captura
            url_target = "https://tvlibr3.com/en-vivo/espn-premium/"
            print(f"📡 Conectando a la transmisión: {url_target}")
            
            await page.goto(url_target, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)

            # --- TRUCO: Forzar la activación de las opciones en amarillo ---
            print("👇 Buscando los botones de opciones (Opción 1, Opción 2, Opción 3)...")
            
            # Intentamos hacer clic en los elementos que contienen texto de opciones o botones
            opciones = await page.locator("text=/Opción/i").all()
            print(f"📋 Se encontraron {len(opciones)} botones de opción potenciales.")
            
            # Le damos clic a las primeras 3 opciones dejando pausas para romper anuncios
            for i, opcion in enumerate(opciones[:3]):
                try:
                    print(f"👆 Activando Opción {i+1}...")
                    await opcion.click(timeout=5000)
                    await asyncio.sleep(4)
                    # Un clic extra al centro por si aparece un "Play" flotante interno
                    await page.mouse.click(180, 300)
                    await asyncio.sleep(3)
                except Exception:
                    continue

            # Revisar si el video se metió dentro de algún iframe (reproductor externo escondido)
            print("🕵️ Investigando marcos ocultos (iframes)...")
            for frame in page.frames:
                try:
                    # Si el iframe tiene un botón de play interno, intentamos presionarlo
                    play_button = await frame.locator("button, video, .play, #play").first
                    if await play_button.is_visible():
                        await play_button.click(timeout=3000)
                        print(f"▶️ Se activó un reproductor oculto en el marco: {frame.url[:50]}...")
                except Exception:
                    continue

            print("⏳ Absorbiendo tráfico de la transmisión por 25 segundos...")
            await asyncio.sleep(25)

            # Guardamos la foto final para verificar qué se quedó cargando
            await page.screenshot(path="pantalla_final.png")
            print("📸 Captura de pantalla final guardada.")

        except Exception as e:
            print(f"❌ Ocurrió un error en el proceso: {e}")
        finally:
            await browser.close()

        # Generar el reporte final de enlaces limpios
        with open("resultados_trafico.txt", "w", encoding="utf-8") as f:
            if links_video:
                f.write(f"¡TRAFICO CAPTURADO CON ÉXITO! Canales IPTV encontrados:\n\n")
                for link in set(links_video):
                    f.write(link + "\n")
            else:
                f.write("No se detectó ningún flujo de video directo en las opciones probadas.\n")

if __name__ == "__main__":
    asyncio.run(run())
