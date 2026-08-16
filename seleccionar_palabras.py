import csv
from pathlib import Path

NIVELES = ("a1", "a2", "b1", "b2", "c1")
MIN_DOCUMENTOS = 2


def nivel_minimo(fila: dict[str, str]) -> str:
    for nivel in NIVELES:
        if (
            float(fila[f"level_freq@{nivel}"] or 0) > 0
            and float(fila[f"nb_doc@{nivel}"] or 0) >= MIN_DOCUMENTOS
        ):
            return nivel.upper()
    return "sin_datos"


def seleccionar(entrada: Path, salida: Path) -> None:
    with entrada.open(encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.DictReader(archivo, delimiter="\t"))

    for fila in filas:
        fila["nivel_minimo_observado"] = nivel_minimo(fila)

    columnas = [*filas[0].keys()]
    with salida.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, delimiter="\t")
        escritor.writeheader()
        escritor.writerows(filas)


if __name__ == "__main__":
    carpeta = Path(__file__).parent
    seleccionar(carpeta / "lemas-cefr.tsv", carpeta / "palabras-seleccionadas.tsv")
    print("Lista creada: palabras-seleccionadas.tsv")
