import csv
from pathlib import Path

NIVELES = ("a1", "a2", "b1", "b2", "c1")


def cargar_elelex(ruta: Path) -> dict[str, dict[str, float]]:
    datos = {}
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        for fila in csv.DictReader(archivo, delimiter="\t"):
            palabra = fila["word"].strip().lower()
            registro = datos.setdefault(
                palabra,
                {f"level_freq@{nivel}": 0.0 for nivel in NIVELES}
                | {f"nb_doc@{nivel}": 0.0 for nivel in NIVELES},
            )
            for nivel in NIVELES:
                for prefijo in ("level_freq", "nb_doc"):
                    columna = f"{prefijo}@{nivel}"
                    registro[columna] = max(
                        registro[columna], float(fila[columna] or 0)
                    )
    return datos


def enriquecer(lemas: Path, elelex: Path, salida: Path) -> None:
    datos = cargar_elelex(elelex)
    columnas = [
        "lema",
        "frecuencia_texto",
        "contextos",
        "elelex_encontrado",
        *(
            columna
            for nivel in NIVELES
            for columna in (f"level_freq@{nivel}", f"nb_doc@{nivel}")
        ),
    ]
    with lemas.open(encoding="utf-8-sig", newline="") as entrada, salida.open(
        "w", encoding="utf-8", newline=""
    ) as salida_archivo:
        lector = csv.DictReader(entrada, delimiter="\t")
        escritor = csv.DictWriter(salida_archivo, fieldnames=columnas, delimiter="\t")
        escritor.writeheader()
        for fila in lector:
            registro = datos.get(fila["lema"])
            salida_fila = {
                "lema": fila["lema"],
                "frecuencia_texto": fila["frecuencia"],
                "contextos": fila["contextos"],
                "elelex_encontrado": "sí" if registro else "no",
            }
            for nivel in NIVELES:
                for prefijo in ("level_freq", "nb_doc"):
                    columna = f"{prefijo}@{nivel}"
                    salida_fila[columna] = (
                        f"{registro[columna]:g}" if registro else ""
                    )
            escritor.writerow(salida_fila)


if __name__ == "__main__":
    carpeta = Path(__file__).parent
    enriquecer(
        carpeta / "lemas.tsv",
        carpeta / "ELELex.tsv",
        carpeta / "lemas-cefr.tsv",
    )
    print("Informe creado: lemas-cefr.tsv")
