import csv
import html
import json
from pathlib import Path


NIVELES = ("C1", "B2", "B1")


def generar_html(entrada: Path, tatoeba: Path, salida: Path) -> None:
    """Genera una página de estudio con las palabras y sus contextos."""
    with entrada.open(encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.DictReader(archivo, delimiter="\t"))
    ejemplos_tatoeba = json.loads(tatoeba.read_text(encoding="utf-8"))

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
                <article>
                  <h3>{html.escape(fila["lema"])}
                    <small>{fila["frecuencia_texto"]} apariciones</small>
                  </h3>
                  <details>
                    <summary>Ver contexto</summary>
                    <details><summary>SRT ({len(contextos)})</summary>
                    {"".join(f"<p>{contexto}</p>" for contexto in contextos)}
                    </details>
                    {tatoeba_html(ejemplos_tatoeba.get(fila["lema"], {}))}
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
  </style>
</head>
<body>
  <h1>Vocabulario difícil</h1>
  {"".join(secciones)}
</body>
</html>
"""
    salida.write_text(documento, encoding="utf-8")


def tatoeba_html(datos: dict) -> str:
    ejemplos = datos.get("ejemplos", [])
    idioma = datos.get("idioma", "")
    contenido = []
    for ejemplo in ejemplos:
        traducciones = "".join(
            f"<p>{html.escape(traduccion)}</p>"
            for traduccion in ejemplo["traducciones"]
        )
        contenido.append(
            f"<details><summary>{html.escape(ejemplo['es'])}</summary>"
            f"<details><summary>Traducciones ({idioma})</summary>{traducciones}</details></details>"
        )
    return f"<details><summary>Tatoeba ({len(ejemplos)})</summary>{''.join(contenido)}</details>"


if __name__ == "__main__":
    carpeta = Path(__file__).parent
    generar_html(
        carpeta / "palabras-dificiles.tsv",
        carpeta / "tatoeba.json",
        carpeta / "vocabulario-dificil.html",
    )
    print("Vista creada: vocabulario-dificil.html")
