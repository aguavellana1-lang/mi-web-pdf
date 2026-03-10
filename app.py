from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import io
import os

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/generar", methods=["POST"])
def generar_pdf():
    nombre = request.form["nombre"]
    empresa = request.form["empresa"]
    mensaje = request.form["mensaje"]

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 750, f"Documento generado para: {nombre}")
    pdf.drawString(100, 720, f"Empresa: {empresa}")
    pdf.drawString(100, 690, f"Mensaje: {mensaje}")

    pdf.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="documento.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
