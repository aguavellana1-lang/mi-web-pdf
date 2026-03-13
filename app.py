from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
from pdf2image import convert_from_bytes
import io

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# UNIR PDF
@app.route("/unir-pdf", methods=["GET","POST"])
def unir_pdf():

    if request.method == "POST":

        archivos = request.files.getlist("pdfs")

        merger = PdfMerger()

        for pdf in archivos:
            merger.append(pdf)

        salida = "unido.pdf"
        merger.write(salida)
        merger.close()

        return send_file(salida, as_attachment=True)

    return render_template("unir_pdf.html")


# DIVIDIR PDF
@app.route("/dividir-pdf", methods=["GET","POST"])
def dividir_pdf():

    if request.method == "POST":

        archivo = request.files["pdf"]
        pagina = int(request.form["pagina"])

        reader = PdfReader(archivo)
        writer = PdfWriter()

        writer.add_page(reader.pages[pagina-1])

        salida = "pagina.pdf"

        with open(salida,"wb") as f:
            writer.write(f)

        return send_file(salida, as_attachment=True)

    return render_template("dividir_pdf.html")


# IMAGEN A PDF
@app.route("/imagen-pdf", methods=["GET","POST"])
def imagen_pdf():

    if request.method == "POST":

        archivo = request.files["imagen"]

        imagen = Image.open(archivo).convert("RGB")

        salida = "imagen.pdf"

        imagen.save(salida)

        return send_file(salida, as_attachment=True)

    return render_template("imagen_pdf.html")


# PDF A IMAGEN
@app.route("/pdf-imagen", methods=["GET","POST"])
def pdf_imagen():

    if request.method == "POST":

        archivo = request.files["pdf"]

        paginas = convert_from_bytes(archivo.read())

        imagen = paginas[0]

        buffer = io.BytesIO()
        imagen.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="image/png",
            as_attachment=True,
            download_name="pagina.png"
        )

    return render_template("pdf_imagen.html")


if __name__ == "__main__":
    app.run(debug=True)
