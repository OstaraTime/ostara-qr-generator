from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import tempfile
import os
import shutil
from latexcompiler import LC

from OstaraQRGen.QRgen import generate_cards

app = FastAPI()

def csv_to_tex(csv_path: str, tex_path: str, tmpdir):
    generate_cards(csv_path, tex_path, True, tmpdir)

def tex_to_pdf(tex_path: str, pdf_path: str, tmpdir):
#    with open(pdf_path, "wb") as f:
#        f.write(b"%PDF-1.4\nBUREK\n")

    LC.compile_document(tex_engine = 'lualatex',
        bib_engine = 'biber', # Value is not necessary
        no_bib = True,
        path = tex_path,
        folder_name = '.aux_files')

@app.post("/generate-pdf")
async def generate_pdf(file: UploadFile = File(...)):
    tmpdir = tempfile.mkdtemp()   # 👈 NOT a context manager

    csv_path = os.path.join(tmpdir, file.filename)
    tex_path = os.path.join(tmpdir, "output.tex")
    pdf_path = os.path.join(tmpdir, "output.pdf")

    with open(csv_path, "wb") as f:
        f.write(await file.read())

    csv_to_tex(csv_path, tex_path, tmpdir)
    tex_to_pdf(tex_path, pdf_path, tmpdir)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="output.pdf",
        background=BackgroundTask(shutil.rmtree, tmpdir)  # 👈 cleanup AFTER response
    )
