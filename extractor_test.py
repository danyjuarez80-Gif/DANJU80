import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🔥 Iniciando Modo Agresivo (Intento 2)...")
        
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={"width": 360, "height": 740} # Simula pantalla exacta de celular
        )
        page = await context.new_page()
        
        todo_el_trafico = []

        # Capturar ABSOLUTAMENTE TODO lo que pida la página sin filtros
        page.on("request", lambda req: todo_el_trafico.append(f"[REQ] -> {req.url}"))
        page.on("response", lambda res: todo_el_trafico.append(f"[RES ({res.status})] -> {res.url} | MIME: {res.headers.get('content-type')}"))

        try:
            # 🛠️ METE AQUÍ TU URL REAL, PERRITO. Si dejas la de ejemplo va a volver a fallar
            url_a_probar = "https://TU-PAGINA-DE-STREAMING-AQUI.com" 
            
            await page.goto(url_a_probar, wait_until="load", timeout=60000)
            print(f"📡 Navegando en la boca del lobo: {url_a_probar}")
            await asyncio.sleep(5)

            # Intentar interactuar rudo con la página para activar reproductores flojos
            print("👇 Tirando clics en coordenadas locas para romper anuncios...")
            await page.mouse.click(180, 370) # Clic al centro de la pantalla simulada del cel
            await asyncio.sleep(3)
            await page.mouse.click(180, 370) # Segundo intento por si el primero abrió pop-up
            
            print("⏳ Esperando 15 segundos de reproducción de fondo...")
            await asyncio.sleep(15)

            # 📸 LA PRUEBA REINA: Tomar una foto de qué está viendo el robot
            await page.screenshot(path="pantalla_final.png")
            print("📸 Foto de la página guardada con éxito.")

        except Exception as e:
            print(f"❌ Tronó el proceso: {e}")
        finally:
            await browser.close()

        # Guardar todo el reporte de tráfico bruto
        with open("resultados_trafico.txt", "w", encoding="utf-8") as f:
            if todo_el_trafico:
                f.write(f"Tráfico total detectado: {len(todo_el_trafico)} peticiones.\n\n")
                for linea in todo_el_trafico:
                    f.write(linea + "\n")
            else:
                f.write("La página bloqueó por completo la salida de red del bot.\n")

if __name__ == "__main__":
    asyncio.run(run())
