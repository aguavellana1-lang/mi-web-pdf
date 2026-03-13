from flask import Flask, render_template, request, send_file
import PyPDF2
from pdf2image import convert_from_bytes
from PIL import Image
import io

app = Flask(__name__)

# HOME
@app.route("/")
def index():
    return render_template("index.html")

# =============================
# UNIR PDF
# =============================

@app.route("/unir_pdf", methods=["GET","POST"])
def unir_pdf():

    if request.method == "POST":

        files = request.files.getlist("pdfs")

        merger = PyPDF2.PdfMerger()

        for file in files:
            merger.append(file)

        output = io.BytesIO()
        merger.write(output)
        merger.close()

        output.seek(0)

        return send_file(
            output,
            download_name="unido.pdf",
            as_attachment=True
        )

    return render_template("unir_pdf.html")

# =============================
# DIVIDIR PDF
# =============================

@app.route("/dividir_pdf", methods=["GET","POST"])
def dividir_pdf():

    if request.method == "POST":

        file = request.files["pdf"]

        reader = PyPDF2.PdfReader(file)

        writer = PyPDF2.PdfWriter()

        page_number = int(request.form["pagina"])

        writer.add_page(reader.pages[page_number])

        output = io.BytesIO()

        writer.write(output)

        output.seek(0)

        return send_file(
            output,
            download_name="pagina.pdf",
            as_attachment=True
        )

    return render_template("dividir_pdf.html")

# =============================
# PDF → IMAGEN
# =============================

@app.route("/pdf_imagen", methods=["GET","POST"])
def pdf_imagen():

    if request.method == "POST":

        file = request.files["pdf"]

        images = convert_from_bytes(file.read())

        img_io = io.BytesIO()

        images[0].save(img_io, format="PNG")

        img_io.seek(0)

        return send_file(
            img_io,
            download_name="pagina.png",
            as_attachment=True
        )

    return render_template("pdf_imagen.html")

# =============================
# IMAGEN → PDF
# =============================

@app.route("/imagen_pdf", methods=["GET","POST"])
def imagen_pdf():

    if request.method == "POST":

        file = request.files["imagen"]

        image = Image.open(file)

        pdf_io = io.BytesIO()

        image.convert("RGB").save(pdf_io, format="PDF")

        pdf_io.seek(0)

        return send_file(
            pdf_io,
            download_name="imagen.pdf",
            as_attachment=True
        )

    return render_template("imagen_pdf.html")

# =============================
# ROTAR PDF
# =============================

@app.route("/rotar_pdf", methods=["GET","POST"])
def rotar_pdf():

    if request.method == "POST":

        file = request.files["pdf"]

        reader = PyPDF2.PdfReader(file)

        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            page.rotate(90)
            writer.add_page(page)

        output = io.BytesIO()

        writer.write(output)

        output.seek(0)

        return send_file(
            output,
            download_name="rotado.pdf",
            as_attachment=True
        )

    return render_template("rotar_pdf.html")

# =============================
# COMPRIMIR / REDUCIR
# =============================

@app.route("/comprimir_pdf", methods=["GET","POST"])
def comprimir_pdf():

    if request.method == "POST":

        file = request.files["pdf"]

        reader = PyPDF2.PdfReader(file)

        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)

        output = io.BytesIO()

        writer.write(output)

        output.seek(0)

        return send_file(
            output,
            download_name="comprimido.pdf",
            as_attachment=True
        )

    return render_template("comprimir_pdf.html")

# =============================

if __name__ == "__main__":
    app.run(debug=True)
