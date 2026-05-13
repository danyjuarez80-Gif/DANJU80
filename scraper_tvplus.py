import asyncio
import re
from playwright.async_api import async_playwright

# Canales que quieres con su URL exacta en tvplusgratis2.com
CANALES_TVPLUS = [
    {"nombre": "ESPN",          "url": "https://www.tvplusgratis2.com/espn-en-vivo.html"},
    {"nombre": "ESPN 2",        "url": "https://www.tvplusgratis2.com/espn-2-en-vivo.html"},
    {"nombre": "ESPN Mexico",   "url": "https://www.tvplusgratis2.com/espn-mexico-en-vivo.html"},
    {"nombre": "Fox Deportes",  "url": "https://www.tvplusgratis2.com/fox-deportes-en-vivo.html"},
    {"nombre": "Fox Sports",    "url": "https://www.tvplusgratis2.com/fox-sports-en-vivo.html"},
    {"nombre": "Fox One",       "url": "https://www.tvplusgratis2.com/fox-one-en-vivo.html"},
    {"nombre": "TUDN",          "url": "https://www.tvplusgratis2.com/tudn-en-vivo.html"},
    {"nombre": "Univision",     "url": "https://www.tvplusgratis2.com/univision-en-vivo.html"},
    {"nombre": "UniMas",        "url": "https://www.tvplusgratis2.com/unimas-en-vivo.html"},
    {"nombre": "Telemundo",     "url": "https://www.tvplusgratis2.com/telemundo-en-vivo.html"},
    {"nombre": "beIN Sports",   "url": "https://www.tvplusgratis2.com/bein-sports-en-vivo.html"},
    {"nombre": "Champions TV",  "url": "https://www.tvplusgratis2.com/champions-league-en-vivo.html"},
    {"nombre": "Claro Sports",  "url": "https://www.tvplusgratis2.com/claro-sports-en-vivo.html"},
    {"nombre": "Caliente TV",   "url": "https://www.tvplusgratis2.com/caliente-tv-en-vivo.html"},
]

async def capturar_m3u8(page, canal):
    m3u8_url = None

    def interceptar(request):
        nonlocal m3u8_url
        if ".m3u8" in request.url and m3u8_url is None:
            m3u8_url = request.url

    page.on("request", interceptar)

    try:
        await page.goto(canal["url"], timeout=20000, wait_until="networkidle")
        await asyncio.sleep(5)  # Esperar que cargue el player
    except Exception as e:
        print(f"⚠️ Error cargando {canal['nombre']}: {e}")

    return m3u8_url

async def scrape_tvplus():
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()

        for canal in CANALES_TVPLUS:
            print(f"🔍 Buscando: {canal['nombre']}...")
            url = await capturar_m3u8(page, canal)
            if url:
                print(f"✅ {canal['nombre']}: {url}")
                resultados.append((canal["nombre"], url))
            else:
                print(f"❌ {canal['nombre']}: no encontrado")

        await browser.close()

    return resultados

if __name__ == "__main__":
    resultados = asyncio.run(scrape_tvplus())
    for nombre, url in resultados:
        print(f"{nombre} -> {url}")
