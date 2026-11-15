from pathlib import Path
import shutil
import tempfile

import gdown
import pypdfium2 as pdfium
from PIL import Image

FILE_ID = "1RouGLbjVSyNqfeMxpRS_y_XsISObvQWW"
EXPECTED_PAGES = 20
OUT = Path("assets/mentor/hambre")
OUT.mkdir(parents=True, exist_ok=True)

with tempfile.TemporaryDirectory() as td:
    pdf_path = Path(td) / "quien-tiene-hambre.pdf"
    result = gdown.download(id=FILE_ID, output=str(pdf_path), quiet=False)
    if not result or not pdf_path.exists() or pdf_path.stat().st_size < 100000:
        raise RuntimeError("No se pudo descargar el PDF de Drive.")

    pdf = pdfium.PdfDocument(str(pdf_path))
    if len(pdf) != EXPECTED_PAGES:
        raise RuntimeError(f"Se esperaban {EXPECTED_PAGES} páginas y se obtuvieron {len(pdf)}.")

    for old in OUT.glob("page-*.jpg"):
        old.unlink()

    for i in range(len(pdf)):
        page = pdf[i]
        bitmap = page.render(scale=1.85)
        im = bitmap.to_pil().convert("RGB")
        # Calidad suficiente para proyección y dos páginas en pantalla.
        if im.width > 1400:
            h = round(im.height * 1400 / im.width)
            im = im.resize((1400, h), Image.Resampling.LANCZOS)
        out = OUT / f"page-{i+1:02d}.jpg"
        im.save(out, "JPEG", quality=88, optimize=True, progressive=True)

print(f"Generadas {EXPECTED_PAGES} páginas en {OUT}")
