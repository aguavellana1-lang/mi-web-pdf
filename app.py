from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# Página principal
@app.route("/")
def index():
    return render_template("index.html")


# Generar PDF desde formulario principal
@app.route("/generar", methods=["POST"])
def generar_pdf():
    nombre = request.form.get("nombre", "")
    empresa = request.form.get("empresa", "")
    mensaje = request.form.get("mensaje", "")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 750, f"Nombre: {nombre}")
    pdf.drawString(100, 730, f"Empresa: {empresa}")
    pdf.drawString(100, 710, f"Mensaje: {mensaje}")

    pdf.save()

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="documento.pdf")


# Página texto → PDF
@app.route("/texto")
def texto():
    return render_template("texto_pdf.html")


# Generar PDF desde texto
@app.route("/texto-pdf", methods=["POST"])
def texto_pdf():
    texto = request.form.get("texto", "")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    y = 750
    for linea in texto.split("\n"):
        pdf.drawString(100, y, linea)
        y -= 20

    pdf.save()

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="texto.pdf")


# Página generador de CV
@app.route("/cv")
def cv():
    return render_template("cv.html")


# Generar CV en PDF
@app.route("/generar-cv", methods=["POST"])
def generar_cv():
    nombre = request.form.get("nombre", "")
    profesion = request.form.get("profesion", "")
    experiencia = request.form.get("experiencia", "")
    habilidades = request.form.get("habilidades", "")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    y = 750

    pdf.drawString(100, y, f"Nombre: {nombre}")
    y -= 30

    pdf.drawString(100, y, f"Profesión: {profesion}")
    y -= 40

    pdf.drawString(100, y, "Experiencia:")
    y -= 20

    for linea in experiencia.split("\n"):
        pdf.drawString(120, y, linea)
        y -= 20

    y -= 20
    pdf.drawString(100, y, "Habilidades:")
    y -= 20

    for linea in habilidades.split("\n"):
        pdf.drawString(120, y, linea)
        y -= 20

    pdf.save()

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="cv.pdf")


if __name__ == "__main__":
    app.run(debug=True)
