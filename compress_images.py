"""
Script de compression des images statiques du projet.
- Redimensionne a max selon le dossier
- Convertit en WebP qualite 82
- Garde les PNG avec transparence en PNG optimise
- Garde les memes noms de fichiers
"""
import os
import sys
from pathlib import Path
from PIL import Image

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

STATIC_IMAGES = Path(__file__).parent / "static" / "images"

MAX_SIZES = {
    "programme":   1000,
    "accueuil":    1000,
    "communaute":   800,
    "defis":        700,
    "default":      900,
}

WEBP_QUALITY = 82


def compress_image(path: Path, max_size: int) -> tuple:
    size_before = path.stat().st_size
    img = Image.open(path)

    w, h = img.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        new_size = (int(w * ratio), int(h * ratio))
        img = img.resize(new_size, Image.LANCZOS)
        print(f"  Redim: {w}x{h} -> {new_size[0]}x{new_size[1]}")

    has_alpha = (img.mode in ("RGBA", "LA") or
                 (img.mode == "P" and "transparency" in img.info))

    if has_alpha:
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        img.save(path, format="PNG", optimize=True)
    else:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        img.save(path, format="WEBP", quality=WEBP_QUALITY, method=6)

    size_after = path.stat().st_size
    return size_before, size_after


def main():
    total_before = 0
    total_after  = 0
    image_exts = {".png", ".jpg", ".jpeg", ".webp"}
    images = [f for f in STATIC_IMAGES.rglob("*")
              if f.is_file() and f.suffix.lower() in image_exts]

    print(f"=== Compression de {len(images)} image(s) ===\n")

    for img_path in sorted(images):
        folder = img_path.parent.name
        max_size = MAX_SIZES.get(folder, MAX_SIZES["default"])
        rel = img_path.relative_to(STATIC_IMAGES)
        print(f">> {rel}")

        try:
            before, after = compress_image(img_path, max_size)
            total_before += before
            total_after  += after
            gain = before - after
            pct  = (gain / before * 100) if before > 0 else 0
            sign = "-" if gain >= 0 else "+"
            print(f"   {before//1024} KB -> {after//1024} KB  ({sign}{abs(gain)//1024} KB, {sign}{abs(pct):.0f}%)\n")
        except Exception as e:
            print(f"   ERREUR: {e}\n")

    print("=" * 50)
    if total_before > 0:
        gain_total = total_before - total_after
        pct_total  = gain_total / total_before * 100
        print(f"TOTAL AVANT : {total_before//1024} KB")
        print(f"TOTAL APRES : {total_after//1024} KB")
        print(f"GAIN        : -{gain_total//1024} KB ({pct_total:.0f}% reduction)")


if __name__ == "__main__":
    main()
