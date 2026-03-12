from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import io
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

app = Flask(__name__)

# HOME
@app.route("/")
def home():
    return render_template("index.html")


# TEXTO → PDF
@app.route("/texto")
def texto():
    return render_template("texto_pdf.html")

@app.route("/generar_pdf", methods=["POST"])
def generar_pdf():

    texto = request.form["texto"]

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    y = 750
    for linea in texto.split("\n"):
        pdf.drawString(100, y, linea)
        y -= 20

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="texto.pdf", mimetype="application/pdf")


# CV
@app.route("/cv")
def cv():
    return render_template("cv.html")


# FACTURA
@app.route("/factura")
def factura():
    return render_template("factura.html")


# NOTAS
@app.route("/notas")
def notas():
    return render_template("notas.html")


# TAREAS
@app.route("/tareas")
def tareas():
    return render_template("tareas.html")


# AGENDA
@app.route("/agenda")
def agenda():
    return render_template("agenda.html")


# UNIR PDF
@app.route("/unir-pdf")
def unir_pdf():
    return render_template("unir_pdf.html")

@app.route("/procesar_unir_pdf", methods=["POST"])
def procesar_unir_pdf():

    archivos = request.files.getlist("pdfs")

    merger = PdfMerger()

    for archivo in archivos:
        merger.append(archivo)

    buffer = io.BytesIO()
    merger.write(buffer)
    merger.close()

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="unidos.pdf", mimetype="application/pdf")


# DIVIDIR PDF
@app.route("/dividir-pdf")
def dividir_pdf():
    return render_template("dividir_pdf.html")

@app.route("/procesar_dividir_pdf", methods=["POST"])
def procesar_dividir_pdf():

    archivo = request.files["pdf"]

    reader = PdfReader(archivo)
    writer = PdfWriter()

    writer.add_page(reader.pages[0])

    buffer = io.BytesIO()
    writer.write(buffer)

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="pagina1.pdf", mimetype="application/pdf")


# IMAGEN → PDF
@app.route("/imagen-a-pdf")
def imagen_a_pdf():
    return render_template("imagen_pdf.html")

@app.route("/procesar_imagen_pdf", methods=["POST"])
def procesar_imagen_pdf():

    imagen = request.files["imagen"]

    img = Image.open(imagen)

    buffer = io.BytesIO()
    img.convert("RGB").save(buffer, format="PDF")

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="imagen.pdf", mimetype="application/pdf")


# PDF → IMAGEN (simulado simple)
@app.route("/pdf-a-imagen")
def pdf_a_imagen():
    return render_template("pdf_imagen.html")

@app.route("/procesar_pdf_imagen", methods=["POST"])
def procesar_pdf_imagen():

    pdf = request.files["pdf"]

    return "Herramienta en desarrollo"


if __name__ == "__main__":
    app.run()
