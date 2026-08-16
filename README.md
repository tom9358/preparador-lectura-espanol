# Preparador de lectura en español

Herramienta para preparar la lectura en español mediante lemas, niveles CEFR
y vocabulario especializado.

## Flujo

1. Limpia los subtítulos:

   ```powershell
   uv run python limpiar_subtitulos.py
   ```

2. Lematiza el texto y guarda los contextos:

   ```powershell
   uv run python lematizar.py
   ```

3. Cruza los lemas con ELELex:

   ```powershell
   uv run python cruzar_cefrlex.py
   ```

4. Selecciona B2/C1 y los B1 con evidencia en niveles superiores:

   ```powershell
   uv run python seleccionar_palabras.py
   ```

5. Genera la vista para estudiar:

   ```powershell
   uv run python generar_html.py
   ```

La vista resultante es `vocabulario-dificil.html`.
