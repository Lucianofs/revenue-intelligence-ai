from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def gerar_pdf(relatorio):
    doc = SimpleDocTemplate("relatorio.pdf")
    styles = getSampleStyleSheet()

    content = []

    for linha in relatorio.split("\n"):
        content.append(Paragraph(linha, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)
