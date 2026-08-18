"""
Ajoute loading="lazy" sur toutes les balises <img> des templates,
SAUF les images hero (au-dessus de la ligne de flottaison).
"""
import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

# Mots-clés dans le src = image above-the-fold (ne pas lazy-loader)
ABOVE_FOLD = ["hero-accueil", "hero-img"]

def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    count = 0

    def replacer(m):
        nonlocal count
        tag = m.group(0)
        # Skip si loading= déjà présent
        if "loading=" in tag:
            return tag
        # Skip si image hero
        if any(kw in tag for kw in ABOVE_FOLD):
            return tag
        count += 1
        # Insère loading="lazy" avant la fermeture de la balise
        tag = tag.rstrip(">").rstrip()
        if tag.endswith("/"):
            tag = tag[:-1].rstrip()
        return tag + ' loading="lazy">'

    new_text = re.sub(r"<img\b[^>]*>", replacer, text, flags=re.DOTALL)

    if count > 0:
        path.write_text(new_text, encoding="utf-8")

    return count


def main():
    total = 0
    for tpl in sorted(TEMPLATES_DIR.rglob("*.html")):
        n = process_file(tpl)
        if n > 0:
            rel = tpl.relative_to(TEMPLATES_DIR)
            print(f"  {rel}: +{n} loading=lazy")
            total += n

    print(f"\nTotal: {total} images avec loading=lazy ajoute")


if __name__ == "__main__":
    main()
