import re
from pathlib import Path

import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://blog.python.org/"
OUT = Path("data/posts_python_blog.csv")

def limpiar_texto(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    resp = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    posts = []
    for h3 in soup.select("h3.post-title"):
        a = h3.select_one("a")
        if not a:
            continue
        titulo = limpiar_texto(a.get_text())
        link = (a.get("href") or "").strip()
        if titulo and link:
            posts.append({"titulo": titulo, "url": link})

    df = pd.DataFrame(posts).drop_duplicates()
    df.to_csv(OUT, index=False, encoding="utf-8")
    print(f"OK: {len(df)} posts guardados en {OUT}")

if __name__ == "__main__":
    main()
