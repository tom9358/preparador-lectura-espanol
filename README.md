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

## Selección de palabras

`cruzar_cefrlex.py` conserva los datos de ELELex sin convertirlos en una
clasificación oficial. `seleccionar_palabras.py` aplica una heurística:

- `B2/C1`: la palabra tiene como nivel mínimo observado B2 o C1.
- `B1 con evidencia B2/C1`: su nivel mínimo observado es B1, pero aparece en
  al menos dos documentos de B2 o C1.

El nivel mínimo observado es el primer nivel, de A1 a C1, donde ELELex registra
frecuencia positiva y presencia en al menos dos documentos. `nb_doc` cuenta
documentos, no apariciones. Una palabra ausente o con evidencia insuficiente
queda fuera de la selección; esto no significa que sea necesariamente difícil.
