"""
Gera os PDFs de exemplo do Relatório de Indisponibilidade (TCE-MG):
1. relatorio_limiar.pdf      — Relatório por Limiar (com QR Code de autenticação)
2. relatorio_diario_admin.pdf — Relatório Diário do Administrador (sem QR Code)
"""

import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

# ---------- Dados de exemplo ----------
DATA_REFERENCIA = "23 de janeiro de 2026"
DIRETOR_NOME = "José Antônio Ferreira"
DIRETOR_CARGO = "Diretoria de Tecnologia da Informação"
CODIGO_VERIFICADOR = "0000001"
CODIGO_USUARIO = "000000123"
URL_AUTENTICACAO = "https://indisponibilidade.tce.mg.gov.br/autenticar"

SISTEMAS_LIMIAR = [
    {
        "nome": "E-TCE",
        "periodos": [("23/01/2026 11:35", "23/01/2026 13:35", "120 minutos")],
        "total": "120 minutos",
    },
    {
        "nome": "Consulta Processual",
        "periodos": [
            ("23/01/2026 14:00", "23/01/2026 15:00", "60 minutos"),
            ("23/01/2026 17:00", "23/01/2026 18:15", "75 minutos"),
        ],
        "total": "135 minutos",
    },
]

SISTEMAS_DIARIO = SISTEMAS_LIMIAR + [
    {
        "nome": "Portal de Serviços",
        "periodos": [("23/01/2026 11:35", "23/01/2026 12:20", "45 minutos")],
        "total": "45 minutos",
        "hierarquia": "E-TCE, Consulta Processual",
    },
    {
        "nome": "SIGESP",
        "periodos": [("23/01/2026 09:10", "23/01/2026 09:30", "20 minutos")],
        "total": "20 minutos",
        "hierarquia": None,
    },
]

# Adiciona hierarquia aos sistemas do limiar também (para exibição opcional)
SISTEMAS_LIMIAR[0]["hierarquia"] = None
SISTEMAS_LIMIAR[1]["hierarquia"] = None


# ---------- Estilos ----------
styles = getSampleStyleSheet()

style_org = ParagraphStyle(
    "Org", parent=styles["Normal"], fontSize=15, leading=18,
    fontName="Helvetica-Bold", alignment=TA_LEFT, textColor=colors.HexColor("#1f2937"),
)
style_org_sub = ParagraphStyle(
    "OrgSub", parent=styles["Normal"], fontSize=15, leading=18,
    fontName="Helvetica-Bold", alignment=TA_LEFT, textColor=colors.HexColor("#1f2937"),
)
style_title = ParagraphStyle(
    "Title", parent=styles["Normal"], fontSize=18, leading=22,
    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceBefore=18, spaceAfter=18,
    textColor=colors.HexColor("#111827"),
)
style_intro = ParagraphStyle(
    "Intro", parent=styles["Normal"], fontSize=10.5, leading=15,
    alignment=TA_LEFT, textColor=colors.HexColor("#374151"), spaceAfter=16,
)
style_sistema_nome = ParagraphStyle(
    "SistemaNome", parent=styles["Normal"], fontSize=12, leading=15,
    fontName="Helvetica-Bold", textColor=colors.HexColor("#111827"), spaceBefore=14, spaceAfter=2,
)
style_hierarquia = ParagraphStyle(
    "Hierarquia", parent=styles["Normal"], fontSize=8.5, leading=11,
    fontName="Helvetica-Oblique", textColor=colors.HexColor("#6b7280"), spaceAfter=6,
)
style_assinatura_nome = ParagraphStyle(
    "AssinaturaNome", parent=styles["Normal"], fontSize=10.5, leading=14,
    fontName="Helvetica-BoldOblique", textColor=colors.HexColor("#111827"),
)
style_assinatura_cargo = ParagraphStyle(
    "AssinaturaCargo", parent=styles["Normal"], fontSize=9.5, leading=13,
    fontName="Helvetica-Oblique", textColor=colors.HexColor("#4b5563"),
)
style_auth_text = ParagraphStyle(
    "AuthText", parent=styles["Normal"], fontSize=8, leading=11,
    textColor=colors.HexColor("#4b5563"),
)
style_parcial = ParagraphStyle(
    "Parcial", parent=styles["Normal"], fontSize=10, leading=13,
    fontName="Helvetica-BoldOblique", textColor=colors.HexColor("#9f580a"),
    alignment=TA_CENTER, spaceAfter=14,
)


def gerar_qrcode_buffer(data):
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#111827", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def tabela_periodos(periodos, total):
    data = [["Hora de Início", "Hora de Término", "Tempo de\nIndisponibilidade"]]
    for ini, fim, tempo in periodos:
        data.append([ini, fim, tempo])
    data.append(["Indisponibilidade total do dia", "", total])

    n_rows = len(data)
    col_widths = [55 * mm, 55 * mm, 45 * mm]

    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    style_cmds = [
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#374151")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f4f6")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        # Linha de total: mescla as duas primeiras colunas, destaca fundo
        ("SPAN", (0, n_rows - 1), (1, n_rows - 1)),
        ("BACKGROUND", (0, n_rows - 1), (-1, n_rows - 1), colors.HexColor("#f9fafb")),
        ("FONTNAME", (0, n_rows - 1), (-1, n_rows - 1), "Helvetica-Bold"),
        ("TEXTCOLOR", (2, n_rows - 1), (2, n_rows - 1), colors.HexColor("#c81e1e")),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def construir_documento(caminho_saida, sistemas, incluir_autenticacao, parcial=False):
    doc = SimpleDocTemplate(
        caminho_saida, pagesize=A4,
        topMargin=22 * mm, bottomMargin=20 * mm,
        leftMargin=22 * mm, rightMargin=22 * mm,
    )
    story = []

    # Cabeçalho institucional (texto, sem logo real — placeholder)
    header_data = [[
        Paragraph("<b>TCE</b>", ParagraphStyle("LogoPlaceholder", parent=styles["Normal"],
                  fontSize=13, alignment=TA_CENTER, textColor=colors.white)),
        Paragraph("Tribunal de Contas do Estado de<br/>Minas Gerais", style_org_sub),
    ]]
    header_table = Table(header_data, colWidths=[16 * mm, 140 * mm])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#c81e1e")),
        ("BOX", (0, 0), (0, 0), 0, colors.white),
        ("TOPPADDING", (0, 0), (0, 0), 10),
        ("BOTTOMPADDING", (0, 0), (0, 0), 10),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e5e7eb")))
    story.append(Spacer(1, 10))

    titulo = "Indisponibilidade Técnica dos Sistemas"
    if parcial:
        titulo += " (Parcial)"
    story.append(Paragraph(titulo, style_title))

    if parcial:
        story.append(Paragraph(
            "⚠ RELATÓRIO PARCIAL — Gerado sob demanda, reflete o status até o momento da emissão.",
            style_parcial
        ))

    intro = (
        f"Declaro, para os devidos fins, a indisponibilidade dos sistemas listados abaixo, "
        f"ao longo do dia <b>{DATA_REFERENCIA}</b>."
        if not parcial else
        f"Declaro, para os devidos fins, a indisponibilidade dos sistemas listados abaixo, "
        f"registrada até o momento da emissão deste relatório no dia <b>{DATA_REFERENCIA}</b>."
    )
    story.append(Paragraph(intro, style_intro))

    for sistema in sistemas:
        story.append(Paragraph(sistema["nome"], style_sistema_nome))
        if sistema.get("hierarquia"):
            story.append(Paragraph(f"Hierarquia (pai): {sistema['hierarquia']}", style_hierarquia))
        story.append(tabela_periodos(sistema["periodos"], sistema["total"]))

    story.append(Spacer(1, 28))
    story.append(Paragraph(DIRETOR_NOME, style_assinatura_nome))
    story.append(Paragraph(DIRETOR_CARGO, style_assinatura_cargo))

    story.append(Spacer(1, 22))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e5e7eb")))
    story.append(Spacer(1, 12))

    if incluir_autenticacao:
        qr_buf = gerar_qrcode_buffer(
            f"{URL_AUTENTICACAO}?verificador={CODIGO_VERIFICADOR}&usuario={CODIGO_USUARIO}"
        )
        qr_img = Image(qr_buf, width=22 * mm, height=22 * mm)
        auth_text = Paragraph(
            f"A autenticidade deste documento pode ser conferida no site "
            f"<b>{URL_AUTENTICACAO}</b>, informando o código verificador "
            f"<b>{CODIGO_VERIFICADOR}</b> e o código do usuário <b>{CODIGO_USUARIO}</b>.",
            style_auth_text
        )
        auth_table = Table([[qr_img, auth_text]], colWidths=[26 * mm, 130 * mm])
        auth_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(auth_table)
    else:
        story.append(Paragraph(
            "Relatório de uso interno do Administrador de Sistemas — não requer autenticação por QR Code.",
            style_auth_text
        ))

    doc.build(story)


if __name__ == "__main__":
    # 1) Relatório por Limiar — com QR Code
    construir_documento(
        "/tmp/relatorio_pdf/relatorio_limiar.pdf",
        SISTEMAS_LIMIAR,
        incluir_autenticacao=True,
        parcial=False,
    )

    # 2) Relatório Diário do Administrador — sem QR Code, todos os sistemas
    construir_documento(
        "/tmp/relatorio_pdf/relatorio_diario_admin.pdf",
        SISTEMAS_DIARIO,
        incluir_autenticacao=False,
        parcial=False,
    )

    # 3) Relatório Parcial do Administrador — sem QR Code, indicado como parcial
    construir_documento(
        "/tmp/relatorio_pdf/relatorio_parcial_admin.pdf",
        SISTEMAS_DIARIO[:2],
        incluir_autenticacao=False,
        parcial=True,
    )

    print("PDFs gerados com sucesso.")
