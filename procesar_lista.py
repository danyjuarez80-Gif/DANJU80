import re
import os

# SEGURO: Si el archivo no existe o está corrupto, frenamos
if not os.path.exists('completa.m3u'):
    print('Error: El archivo completa.m3u no existe.')
    exit(1)

tamano = os.path.getsize('completa.m3u')
print(f'Tamaño del archivo descargado: {tamano} bytes')

if tamano < 10240:
    print('Error crítico: Descarga corrupta o rechazada por Dropbox.')
    exit(1)

# Creamos las cabeceras estándar
with open('tv.m3u', 'w', encoding='utf-8') as f: f.write('#EXTM3U\n')
with open('peliculas.m3u', 'w', encoding='utf-8') as f: f.write('#EXTM3U\n')
with open('series.m3u', 'w', encoding='utf-8') as f: f.write('#EXTM3U\n')

with open('completa.m3u', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

current_extinf = None
enlaces_procesados = 0

for line in lines:
    line_strip = line.strip()
    if not line_strip:
        continue
    
    if line_strip.startswith('#EXTINF:'):
        current_extinf = line_strip
            
    elif line_strip.startswith('http'):
        if current_extinf:
            enlaces_procesados += 1
            match_name = re.search(r',([^,]*)$', current_extinf)
            match_duration = re.search(r'^#EXTINF:(\s*[-]?\d+)', current_extinf)
            
            duracion = match_duration.group(1) if match_duration else '-1'
            nombre = match_name.group(1).strip() if match_name else 'Contenido Sin Nombre'
            
            if '/movie/' in line_strip:
                linea_limpia = f'#EXTINF:{duracion},{nombre}\n'
                with open('peliculas.m3u', 'a', encoding='utf-8') as f_out:
                    f_out.write(linea_limpia + line_strip + '\n')
                    
            elif '/series/' in line_strip:
                linea_limpia = f'#EXTINF:{duracion},{nombre}\n'
                with open('series.m3u', 'a', encoding='utf-8') as f_out:
                    f_out.write(linea_limpia + line_strip + '\n')
                    
            else:
                match_group = re.search(r'group-title=\"([^\"]+)\"', current_extinf)
                if match_group:
                    categoria = match_group.group(1)
                    linea_tv = f'#EXTINF:{duracion} group-title=\"{categoria}\",{nombre}\n'
                else:
                    linea_tv = f'#EXTINF:{duracion},{nombre}\n'
                    
                with open('tv.m3u', 'a', encoding='utf-8') as f_out:
                    f_out.write(linea_tv + line_strip + '\n')
                    
            current_extinf = None

print(f'Proceso terminado con éxito. Se procesaron {enlaces_procesados} enlaces.')
if enlaces_procesados == 0:
    print('Error: No se encontraron enlaces válidos.')
    exit(1)
