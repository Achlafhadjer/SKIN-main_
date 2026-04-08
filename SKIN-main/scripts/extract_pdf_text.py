"""Extrait le texte des PDF du projet (exigences prof) vers des fichiers .txt."""
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    raise SystemExit("Installez pypdf : pip install pypdf") from None

ROOT = Path(__file__).resolve().parents[1]
NAMES = [
    "Feuille de route_Mini-Projet_Deep Learning 2026.pdf",
    "Projet_WAMS_2025.pdf",
]


def main() -> None:
    for name in NAMES:
        pdf = ROOT / name
        if not pdf.is_file():
            print("Absent:", pdf.name)
            continue
        reader = PdfReader(str(pdf))
        parts = []
        for i, page in enumerate(reader.pages):
            t = page.extract_text() or ""
            parts.append(f"--- Page {i + 1} ---\n{t}")
        out = ROOT / (pdf.stem + "_extracted.txt")
        out.write_text("\n".join(parts), encoding="utf-8")
        print("OK", out.relative_to(ROOT), f"({len(reader.pages)} pages)")


if __name__ == "__main__":
    main()
