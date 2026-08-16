import re
from pathlib import Path

SUBTITLE_PATTERN = re.compile(r"^\d+\r?\n\d{2}:\d{2}:\d{2},\d{3} --> ")


def limpiar_srt(entrada: Path, salida: Path) -> int:
    bloques = re.split(r"\r?\n\r?\n+", entrada.read_text(encoding="utf-8-sig").strip())
    limpios = []

    for bloque in bloques:
        lineas = bloque.splitlines()
        if len(lineas) < 3 or not SUBTITLE_PATTERN.match(bloque):
            continue

        dialogo = [
            linea
            for linea in lineas[2:]
            if linea.strip() and not re.fullmatch(r"<[^>]+>", linea.strip())
        ]
        if dialogo and not any("@" in linea or "First draft" in linea for linea in dialogo):
            limpios.append(" ".join(dialogo))

    salida.write_text("\n".join(limpios) + "\n", encoding="utf-8")
    return len(limpios)


if __name__ == "__main__":
    carpeta = Path(__file__).parent
    entrada = next(
        archivo
        for archivo in carpeta.glob("*.srt")
        if archivo.name != "subtitulos-limpios.srt"
    )
    salida = carpeta / "subtitulos-limpios.txt"
    cantidad = limpiar_srt(entrada, salida)
    print(f"Bloques conservados: {cantidad}")
