from collections import Counter
from pathlib import Path

import spacy


def lematizar(entrada: Path, salida: Path) -> int:
    nlp = spacy.load("es_core_news_sm")
    texto = entrada.read_text(encoding="utf-8")
    lemas = [
        token.lemma_.lower()
        for token in nlp(texto)
        if token.is_alpha and not token.is_stop
    ]
    frecuencias = Counter(lemas)
    salida.write_text(
        "lema\tfrecuencia\n"
        + "\n".join(
            f"{lema}\t{frecuencia}"
            for lema, frecuencia in frecuencias.most_common()
        )
        + "\n",
        encoding="utf-8",
    )
    return len(lemas)


if __name__ == "__main__":
    carpeta = Path(__file__).parent
    total = lematizar(
        carpeta / "subtitulos-limpios.txt",
        carpeta / "lemas.tsv",
    )
    print(f"Tokens lematizados: {total}")
