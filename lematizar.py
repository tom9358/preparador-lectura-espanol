from collections import Counter, defaultdict
from pathlib import Path

import spacy


def lematizar(entrada: Path, salida: Path) -> int:
    nlp = spacy.load("es_core_news_sm")
    texto = entrada.read_text(encoding="utf-8")
    lemas = []
    contextos = defaultdict(list)
    for frase in texto.splitlines():
        doc = nlp(frase)
        for token in doc:
            if token.is_alpha and not token.is_stop:
                lema = token.lemma_.lower()
                lemas.append(lema)
                if frase.strip() and frase.strip() not in contextos[lema]:
                    contextos[lema].append(frase.strip())
    frecuencias = Counter(lemas)
    salida.write_text(
        "lema\tfrecuencia\tcontextos\n"
        + "\n".join(
            f"{lema}\t{frecuencia}\t{' || '.join(contextos[lema])}"
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
