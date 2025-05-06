from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from io import BytesIO

def generate_movimentacao_pdf(movimentacao):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Definição de margens
    left_margin = 50
    right_margin = 50
    top_margin = 50
    bottom_margin = 50

    # Cabeçalho da página
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - top_margin, f"Movimentação de {movimentacao.tipo}")
    p.setLineWidth(1)
    p.line(left_margin, height - top_margin - 10, width - right_margin, height - top_margin - 10)

    # Seção de informações da movimentação
    p.setFont("Helvetica", 12)
    y = height - top_margin - 30
    p.drawString(left_margin, y, f"Código: {movimentacao.codigo}")
    y -= 20
    p.drawString(left_margin, y, f"Data: {movimentacao.data_movimentacao.strftime('%d/%m/%Y %H:%M')}")
    y -= 20
    if movimentacao.documento:
        p.drawString(left_margin, y, f"Documento: {movimentacao.documento or '-'}")
        y -= 20
    elif movimentacao.obra:
        p.drawString(left_margin, y, f"Obra: {movimentacao.obra}")
        y -= 20
        p.drawString(left_margin, y, f"Contrato: {movimentacao.obra.contrato}")
        y -= 20
    if movimentacao.realizado_por:
        p.drawString(left_margin, y, f"Registrada por: {movimentacao.realizado_por.get_full_name()}")
    else:
        p.drawString(left_margin, y, "Realizado por: -")
    y -= 20



    p.drawString(left_margin, y, f"Observações: {movimentacao.observacoes or '-'}")
    y -= 30  # espaço antes da tabela

    # Função para desenhar o cabeçalho da tabela
    def draw_table_header(y_pos):
        p.setFont("Helvetica-Bold", 12)
        p.drawString(left_margin, y_pos, "Cod.")
        p.drawString(left_margin + 50, y_pos, "Material")
        p.drawString(left_margin + 400, y_pos, "Quantidade")
        p.line(left_margin, y_pos - 5, width - right_margin, y_pos - 5)
        return y_pos - 20

    # Cabeçalho da tabela
    y = draw_table_header(y)

    # Corpo da tabela: itera sobre os itens da movimentação
    for item in movimentacao.itens.all():
        if y < bottom_margin + 40:
            p.showPage()
            y = height - top_margin
            y = draw_table_header(y)

        # Trunca o nome do material se for maior que 30 caracteres
        p.setFont("Helvetica", 12)
        material_nome = str(item.material.nome)
        if len(material_nome) > 50:
            material_nome = material_nome[:40] + "..."
        p.drawString(left_margin, y, str(item.material.id))
        p.drawString(left_margin + 50, y, material_nome)
        p.drawString(left_margin + 430, y, str(item.quantidade))
        y -= 20

    # Área para assinatura
    # Área para assinatura
    p.setFont("Helvetica", 12)
    if y < bottom_margin + 80:
        p.showPage()
        y = height - top_margin
    y -= 40
    signature_line_length = 250
    signature_x = (width - signature_line_length) / 2  # posição X centralizada
    p.line(signature_x, y, signature_x + signature_line_length, y)
    p.drawCentredString(width / 2, y - 20, "Assinatura do Responsável")

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
