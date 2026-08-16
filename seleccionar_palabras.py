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
    """Selecciona B2/C1 y los B1 con evidencia en niveles superiores."""
    with entrada.open(encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.DictReader(archivo, delimiter="\t"))

    seleccionadas = []
    for fila in filas:
        fila["nivel_minimo_observado"] = nivel_minimo(fila)
        nivel = fila["nivel_minimo_observado"]
        evidencia_superior = any(
            float(fila[f"nb_doc@{superior}"] or 0) >= MIN_DOCUMENTOS
            for superior in ("b2", "c1")
        )
        if nivel in ("B2", "C1") or (nivel == "B1" and evidencia_superior):
            fila["motivo_seleccion"] = (
                "B2/C1"
                if nivel in ("B2", "C1")
                else "B1 con evidencia B2/C1"
            )
            seleccionadas.append(fila)

    columnas = [*filas[0].keys(), "motivo_seleccion"]
    with salida.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, delimiter="\t")
        escritor.writeheader()
        escritor.writerows(seleccionadas)


if __name__ == "__main__":
    carpeta = Path(__file__).parent
    seleccionar(carpeta / "lemas-cefr.tsv", carpeta / "palabras-dificiles.tsv")
    print("Lista creada: palabras-dificiles.tsv")
