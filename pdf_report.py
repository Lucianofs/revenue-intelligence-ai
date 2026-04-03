from reportlab.platypus import SimpleDocTemplate, Paragraph

def gerar_pdf(resumo):
    doc = SimpleDocTemplate("relatorio.pdf")

    content = []

    content.append(Paragraph("Relatório Executivo", None))
    content.append(Paragraph(resumo, None))

    doc.build(content)
