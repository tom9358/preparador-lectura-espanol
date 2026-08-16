import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


API = "https://api.tatoeba.org/v1/sentences"


def consultar(lema: str, idioma: str) -> list[dict[str, str]]:
    parametros = (
        f"q={urlencode({'q': lema})[2:]}"
        f"&lang=spa&sort=relevance&showtrans:lang={idioma}&limit=10"
    )
    with urlopen(f"{API}?{parametros}", timeout=30) as respuesta:
        datos = json.load(respuesta)

    ejemplos = []
    for frase in datos.get("data", []):
        traducciones = frase.get("translations", [])
        if traducciones and isinstance(traducciones[0], list):
            traducciones = traducciones[0]
        textos = [t["text"] for t in traducciones if t.get("lang") == idioma]
        if textos:
            ejemplos.append({"es": frase["text"], "traducciones": textos})
    return ejemplos


def obtener(palabras: Path, salida: Path) -> None:
    """Obtiene ejemplos Tatoeba, priorizando neerlandés y usando inglés como reserva."""
    resultado = {}
    with palabras.open(encoding="utf-8-sig", newline="") as archivo:
        lemas = [fila["lema"] for fila in csv.DictReader(archivo, delimiter="\t")]
    for lema in lemas:
        ejemplos = consultar(lema, "nld")
        idioma = "nld"
        if not ejemplos:
            ejemplos = consultar(lema, "eng")
            idioma = "eng"
        resultado[lema] = {"idioma": idioma, "ejemplos": ejemplos}
    salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    carpeta = Path(__file__).parent
    obtener(carpeta / "palabras-dificiles.tsv", carpeta / "tatoeba.json")
    print("Ejemplos creados: tatoeba.json")
