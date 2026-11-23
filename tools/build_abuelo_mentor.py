from pathlib import Path
import tempfile
import gdown
import pypdfium2 as pdfium
from PIL import Image

FILE_ID = "1s0317-i0MzXlVj9h3y23Kfymr7BloLA2"
EXPECTED = 20
OUT = Path("assets/mentor/abuelo")
OUT.mkdir(parents=True, exist_ok=True)

with tempfile.TemporaryDirectory() as td:
    pdf_path = Path(td) / "cuenta-abuelo-cuenta.pdf"
    result = gdown.download(id=FILE_ID, output=str(pdf_path), quiet=False)
    if not result or not pdf_path.exists() or pdf_path.stat().st_size < 100000:
        raise RuntimeError("No se pudo descargar el texto mentor desde Drive.")
    pdf = pdfium.PdfDocument(str(pdf_path))
    if len(pdf) != EXPECTED:
        raise RuntimeError(f"Se esperaban {EXPECTED} páginas y se obtuvieron {len(pdf)}.")
    for old in OUT.glob("page-*.jpg"):
        old.unlink()
    for i in range(len(pdf)):
        page = pdf[i]
        bmp = page.render(scale=1.8)
        im = bmp.to_pil().convert("RGB")
        if im.width > 1400:
            h = round(im.height * 1400 / im.width)
            im = im.resize((1400,h),Image.Resampling.LANCZOS)
        im.save(OUT / f"page-{i+1:02d}.jpg","JPEG",quality=88,optimize=True,progressive=True)
print("Generadas",EXPECTED,"páginas de Cuenta abuelo, cuenta")
