import re
from pathlib import Path
import pandas as pd

ENTRADA = Path("datos/posts_python_blog.csv")
SALIDA1 = Path("datos/posts_python_blog_procesado.csv")
SALIDA2 = Path("datos/top_palabras_titulos.csv")

STOPWORDS_ES = {"de","la","el","y","en","a","un","una","para","por","con","del","los","las"}
STOPWORDS_EN = {"the","and","to","of","in","for","on","with","a","an"}

def tokenizar(texto: str):
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ0-9\s-]", " ", texto)
    tokens = [t for t in texto.split() if len(t) >= 3]
    tokens = [t for t in tokens if t not in STOPWORDS_ES and t not in STOPWORDS_EN]
    return tokens

def main():
    if not ENTRADA.exists():
        raise FileNotFoundError("Primero ejecuta: python origen/scrape_posts.py")

    df = pd.read_csv(ENTRADA)

    df["len_titulo"] = df["titulo"].fillna("").astype(str).str.len()
    df.to_csv(SALIDA1, index=False, encoding="utf-8")

    all_tokens = []
    for t in df["titulo"].fillna("").astype(str):
        all_tokens.extend(tokenizar(t))

    freq = (
        pd.Series(all_tokens)
        .value_counts()
        .head(20)
        .reset_index()
        .rename(columns={"index": "palabra", 0: "conteo"})
    )
    freq.to_csv(SALIDA2, index=False, encoding="utf-8")

    print(f"OK: {SALIDA1}")
    print(f"OK: {SALIDA2}")

if __name__ == "__main__":
    main()



