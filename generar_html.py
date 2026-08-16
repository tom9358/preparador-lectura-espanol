import csv
import html
from pathlib import Path


NIVELES = ("C1", "B2", "B1")


def generar_html(entrada: Path, salida: Path) -> None:
    """Genera una página de estudio con las palabras y sus contextos."""
    with entrada.open(encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.DictReader(archivo, delimiter="\t"))

    secciones = []
    for nivel in NIVELES:
        nivel_filas = [
            fila
            for fila in filas
            if fila["nivel_minimo_observado"] == nivel
        ]
        nivel_filas.sort(key=lambda fila: int(fila["frecuencia_texto"]), reverse=True)
        tarjetas = []
        for fila in nivel_filas:
            contextos = [
                html.escape(contexto)
                for contexto in fila["contextos"].split(" || ")
                if contexto
            ]
            tarjetas.append(
                f"""
                <article class="tarjeta" data-lema="{html.escape(fila["lema"])}"
                  onclick="alternarEstado(this, event)" tabindex="0">
                  <h3>{html.escape(fila["lema"])}
                    <small>{fila["frecuencia_texto"]} apariciones</small>
                  </h3>
                  <details><summary>SRT ({len(contextos)})</summary>
                  {"".join(f"<p>{contexto}</p>" for contexto in contextos)}
                  </details>
                  <details class="tatoeba" data-lema="{html.escape(fila["lema"])}">
                    <summary>Tatoeba</summary>
                    <div class="tatoeba-results">Abrir para cargar ejemplos.</div>
                  </details>
                </article>
                """
            )
        secciones.append(
            f"<section><h2>{nivel} ({len(nivel_filas)})</h2>"
            + "".join(tarjetas)
            + "</section>"
        )

    documento = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Vocabulario difícil</title>
  <style>
    body {{ font: 16px system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; color: #222; }}
    article {{ border: 1px solid #ddd; border-radius: 8px; padding: .7rem 1rem; margin: .5rem 0; }}
    h2 {{ border-bottom: 2px solid #555; padding-bottom: .3rem; margin-top: 2rem; }}
    h3 {{ margin: 0 0 .5rem; }}
    small {{ color: #666; font-weight: normal; margin-left: .5rem; }}
    p {{ background: #f5f5f5; padding: .5rem; border-radius: 4px; }}
    article.tarjeta > details {{ margin: .45rem 0 .45rem 1rem; }}
    details details {{ margin: .35rem 0 .35rem 1rem; }}
    article.conocida {{ background: #e8f5e9; border-color: #66bb6a; opacity: .75; }}
    article.conocida h3 {{ text-decoration: line-through; }}
    article.tarjeta {{ cursor: pointer; }}
    article.tarjeta:focus {{ outline: 2px solid #90caf9; }}
    article.tarjeta.conocida {{ background: #e8f5e9; border-color: #66bb6a; opacity: .75; }}
    header {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; }}
    button.reset {{ border: 1px solid #ccc; border-radius: 999px; background: transparent; color: #666; cursor: pointer; padding: .35rem .7rem; }}
    button.reset:hover {{ background: #f5f5f5; color: #222; }}
    footer {{ margin: 2rem 0; color: #777; font-size: .85rem; text-align: center; }}
  </style>
  <script>
    const ESTADOS = 'palabras-conocidas';

    function actualizarEstado(tarjeta) {{
      const conocida = JSON.parse(localStorage.getItem(ESTADOS) || '{{}}');
      const lema = tarjeta.dataset.lema;
      const activa = Boolean(conocida[lema]);
      tarjeta.classList.toggle('conocida', activa);
      tarjeta.title = activa ? 'Marcar como pendiente' : 'Marcar como conocida';
    }}

    function alternarEstado(tarjeta, event) {{
      if (event.target.closest('details')) return;
      const conocida = JSON.parse(localStorage.getItem(ESTADOS) || '{{}}');
      const lema = tarjeta.dataset.lema;
      conocida[lema] = !conocida[lema];
      localStorage.setItem(ESTADOS, JSON.stringify(conocida));
      actualizarEstado(tarjeta);
    }}

    function reiniciarEstados() {{
      localStorage.removeItem(ESTADOS);
      document.querySelectorAll('.tarjeta').forEach(actualizarEstado);
    }}

    document.addEventListener('DOMContentLoaded', () => {{
      document.querySelectorAll('.tarjeta').forEach(actualizarEstado);
    }});

    async function cargarTatoeba(detalle) {{
      if (detalle.dataset.cargado) return;
      const lema = detalle.dataset.lema;
      const resultados = detalle.querySelector('.tatoeba-results');
      for (const idioma of ['nld', 'eng']) {{
        const params = new URLSearchParams({{
          q: lema, lang: 'spa', sort: 'relevance',
          'showtrans:lang': idioma, limit: '10'
        }});
        const respuesta = await fetch(
          'https://api.tatoeba.org/v1/sentences?' + params
        );
        const datos = await respuesta.json();
        const ejemplos = (datos.data || []).filter(
          frase => frase.translations && frase.translations.length
        );
        if (!ejemplos.length) continue;
        resultados.innerHTML = ejemplos.map(frase => {{
          const traducciones = frase.translations.flat()
            .filter(traduccion => traduccion.lang === idioma)
            .map(traduccion => `<p>${{traduccion.text}}</p>`).join('');
          return `<details><summary>${{frase.text}}</summary>
            ${{traducciones}}</details>`;
        }}).join('');
        detalle.dataset.cargado = 'true';
        return;
      }}
      resultados.textContent = 'No hay ejemplos con traducción disponible.';
      detalle.dataset.cargado = 'true';
    }}

    document.addEventListener('toggle', event => {{
      if (event.target.matches('.tatoeba') && event.target.open) {{
        cargarTatoeba(event.target);
      }}
    }}, true);
  </script>
</head>
<body>
  <header>
    <h1>Vocabulario difícil</h1>
    <button class="reset" onclick="reiniciarEstados()">Reiniciar progreso</button>
  </header>
  {"".join(secciones)}
  <footer><a href="https://github.com/tom9358/preparador-lectura-espanol">Proyecto y README en GitHub</a></footer>
</body>
</html>
"""
    salida.write_text(documento, encoding="utf-8")


if __name__ == "__main__":
    carpeta = Path(__file__).parent
    generar_html(
        carpeta / "palabras-dificiles.tsv",
        carpeta / "index.html",
    )
    print("Vista creada: index.html")
