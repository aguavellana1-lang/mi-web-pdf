from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# PAGINA PRINCIPAL
@app.route("/")
def home():
    return render_template("index.html")


# TEXTO A PDF
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

    return send_file(
        buffer,
        as_attachment=True,
        download_name="texto.pdf",
        mimetype="application/pdf"
    )


# CV A PDF
@app.route("/cv")
def cv():
    return render_template("cv.html")


@app.route("/generar_cv", methods=["POST"])
def generar_cv():

    nombre = request.form["nombre"]
    email = request.form["email"]
    experiencia = request.form["experiencia"]

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(100, 750, nombre)

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 710, f"Email: {email}")

    y = 670
    for linea in experiencia.split("\n"):
        pdf.drawString(100, y, linea)
        y -= 20

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="cv.pdf",
        mimetype="application/pdf"
    )


# FACTURA PDF
@app.route("/factura")
def factura():
    return render_template("factura.html")


@app.route("/generar_factura", methods=["POST"])
def generar_factura():

    cliente = request.form["cliente"]
    producto = request.form["producto"]
    precio = request.form["precio"]

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(100, 750, "Factura")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 710, f"Cliente: {cliente}")
    pdf.drawString(100, 680, f"Producto: {producto}")
    pdf.drawString(100, 650, f"Precio: {precio}")

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="factura.pdf",
        mimetype="application/pdf"
    )


# NOTAS A PDF
@app.route("/notas")
def notas():
    return render_template("notas.html")


@app.route("/generar_notas", methods=["POST"])
def generar_notas():

    nota = request.form["nota"]

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    y = 750
    for linea in nota.split("\n"):
        pdf.drawString(100, y, linea)
        y -= 20

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="notas.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run()
