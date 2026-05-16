def limpiar_lista_m3u(lineas_m3u):
    """
    Recibe una lista de líneas del archivo M3U original
    y regresa únicamente los canales en vivo, eliminando VOD (Películas/Series).
    """
    lineas_filtradas = []
    skip_next = False
    
    # Aseguramos la cabecera obligatoria
    if lineas_m3u and lineas_m3u[0].startswith("#EXTM3U"):
        lineas_filtradas.append(lineas_m3u[0])
    
    for i in range(1, len(lineas_m3u)):
        linea = lineas_m3u[i].strip()
        
        # Si la línea anterior fue un canal válido, metemos su URL correspondiente
        if skip_next:
            if linea.startswith("http"):
                lineas_filtradas.append(linea)
            skip_next = False
            continue
            
        if linea.startswith("#EXTINF"):
            linea_lower = linea.lower()
            
            # Revisamos la URL que viene justo abajo para detectar si es VOD
            url_abajo = ""
            if i + 1 < len(lineas_m3u):
                url_abajo = lineas_m3u[i + 1].lower()
            
            # Criterios para detectar Películas o Series de Xtream Codes y archivos pesados
            es_vod = (
                "/movie/" in url_abajo or 
                "/series/" in url_abajo or 
                ".mp4" in url_abajo or 
                ".mkv" in url_abajo or
                'group-title="películas"' in linea_lower or
                'group-title="series"' in linea_lower or
                'group-title="vod"' in linea_lower
            )
            
            # Si NO es película ni serie, dejamos pasar el tag y activamos bandera para meter la URL abajo
            if not es_vod:
                lineas_filtradas.append(linea)
                skip_next = True
                
    return lineas_filtradas

# --- EJEMPLO DE CÓMO INTEGRARLO EN TU FLUJO ---
# mapeo_de_lineas = contenido_original_m3u.splitlines()
# lineas_limpias = limpiar_lista_m3u(mapeo_de_lineas)
# 
# with open("lista_canales_en_vivo.m3u", "w", encoding="utf-8") as f:
#     f.write("\n".join(lineas_limpias))
