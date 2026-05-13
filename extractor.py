import requests
import os
import re
from playwright.sync_api import sync_playwright

# Configuración de URLs
URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE = "https://www.tvplusgratis2.com/"

def es_m3u8(url):
    filtros = ["google", "ads", "analytics", "facebook", "mp4", "log", "pixel"]
    return ".m3u8" in url and len(url) > 50 and not any(x in url.lower() for x in filtros)

def ejecutar():
    lineas_finales = []
    ultimo_num = 70
    
    # 1. CARGAR LISTA ACTUAL PARA MANTENER TUS CANALES MANUALES
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        content = r.text if r.status_code == 200 else ""
        if not content and os.path.exists("DANJU80"):
            with open("DANJU80", "r", encoding="utf-8") as f: content = f.read()
        
        for l in content.splitlines():
            if "#EXTM3U" not in l and l.strip():
                lineas_finales.append(l.strip())
                # Buscar el número más alto para seguir la cuenta
                if "noticia" in l.lower():
                    nums = re.findall(r'\d+', l)
                    if nums:
                        n = int(nums[-1])
                        if n > ultimo_num: ultimo_num = n
    except: pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Linux; Android 10; SM-G960F)")
        page = context.new_page()

        # 2. AUTO-DESCUBRIMIENTO DE CANALES
        print("🕵️ Escaneando la web en busca de canales...")
        try:
            page.goto(URL_BASE, timeout=60000, wait_until="networkidle")
