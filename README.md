# Preparador de lectura

Prepara una lectura o una película en otro idioma: extrae vocabulario,
lo lematiza, lo relaciona con niveles CEFR y muestra ejemplos con contexto.
La vista HTML permite marcar las palabras ya conocidas.

Este repositorio usa subtítulos de la película *Encanto* como ejemplo. El mismo
flujo puede adaptarse a otros textos, idiomas y recursos léxicos; por ejemplo,
una persona china aprendiendo sueco puede usar textos suecos, un modelo
spaCy sueco y una lista CEFR sueca.

## Ejemplo: preparar una película

Coloca el archivo `.srt` y `ejemplo-encanto/limpiar_subtitulos.py` juntos en
una carpeta. El script elimina numeración, tiempos y metadatos, y conserva
solo los diálogos:

```powershell
uv run python limpiar_subtitulos.py
```

El resultado es `subtitulos-limpios.txt`. Este paso es opcional si ya tienes
texto limpio, pero resulta útil para preparar vocabulario antes de ver una
película.

## Flujo de análisis

Desde la raíz del proyecto:

```powershell
uv run python lematizar.py
uv run python cruzar_cefrlex.py
uv run python seleccionar_palabras.py
uv run python generar_html.py
```

El resultado es `vocabulario-dificil.html`. Ábrelo en un navegador; el progreso
se guarda localmente y los ejemplos de Tatoeba se cargan desde el navegador.

## Estado actual

Es un prototipo: varias decisiones todavía están **hardcoded** para el ejemplo
español. En particular, los nombres de archivo, el modelo `es_core_news_sm`,
los niveles `A1`–`C1`, las columnas de ELELex, los umbrales de selección y los
idiomas `spa`, `nld` y `eng` de Tatoeba. Para reutilizarlo en otro caso hay que
modificar esos valores y adaptar los scripts; todavía no existe una
configuración general por proyecto o por idioma.

## Adaptar el proyecto

1. Sustituye `subtitulos-limpios.txt` por el texto que quieras estudiar.
2. Cambia el modelo de spaCy en `pyproject.toml` por el idioma de destino
   (`es_core_news_sm`, `sv_core_news_sm`, etc.).
3. Ajusta las columnas y los niveles de `ELELex.tsv` al recurso léxico de ese
   idioma. Si su formato es diferente, adapta `cruzar_cefrlex.py`.
4. Configura `generar_html.py` y Tatoeba con los códigos ISO del idioma de
   aprendizaje y de la traducción.

## Fuente de ELELex

`ELELex.tsv` procede de **ELELex: a CEFR-graded lexical resource for
Spanish**, disponible para descarga en:

<https://cental.uclouvain.be/cefrlex/elelex/download/>

ELELex es específico para español. Para otro idioma hay que sustituirlo por
un recurso léxico CEFR compatible y adaptar `cruzar_cefrlex.py` a sus columnas,
niveles y condiciones de licencia. Consulta también la publicación o
instrucciones de citación de la fuente original si redistribuyes sus datos.

Los niveles calculados son heurísticos, no clasificaciones oficiales. La
licencia MIT cubre el código propio. Comprueba por separado las licencias de
los subtítulos, corpus, modelos y ejemplos que redistribuyas.

## Licencia

Código del proyecto: MIT. Véase `LICENSE`. Para citarlo, consulta
`CITATION.cff`.
