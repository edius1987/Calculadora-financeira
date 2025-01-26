import flet as ft
import numpy_financial as npf
from fpdf import FPDF
from datetime import datetime
import locale

# Configurar localização para formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Cores do tema
CORES = {
    "background": "#1d1313",
    "primary": "#24b694",
    "secondary": "#d22042",
    "accent1": "#a3b808",
    "accent2": "#30c4c9"
}

def main(page: ft.Page):
    page.title = "Simulador de Empréstimos"
    page.padding = 20
    page.bgcolor = CORES["background"]
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(
        primary=CORES["primary"],
        secondary=CORES["secondary"]
    ))

    def criar_pdf(dados_simulacao):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        
        # Cabeçalho
        pdf.cell(0, 10, "Simulação de Empréstimo", ln=True, align='C')
        pdf.ln(10)
        
        # Dados do empréstimo
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Valor do empréstimo: R$ {dados_simulacao['valor']:,.2f}", ln=True)
        pdf.cell(0, 10, f"Taxa de juros: {dados_simulacao['taxa']*1200:.2f}% ao mês", ln=True)
        pdf.cell(0, 10, f"Prazo: {dados_simulacao['prazo']} meses", ln=True)
        pdf.cell(0, 10, f"Sistema: {dados_simulacao['sistema']}", ln=True)
        pdf.cell(0, 10, f"Data primeira parcela: {dados_simulacao['data']}", ln=True)
        pdf.ln(10)
        
        # Tabela
        pdf.set_font("Arial", "B", 10)
        colunas = ['Período', 'Parcela', 'Juros', 'Amortização', 'Saldo']
        larguras = [20, 35, 35, 35, 35]
        
        for i, coluna in enumerate(colunas):
            pdf.cell(larguras[i], 10, coluna, 1)
        pdf.ln()
        
        pdf.set_font("Arial", "", 10)
        for linha in dados_simulacao['tabela']:
            for i, valor in enumerate(linha):
                pdf.cell(larguras[i], 10, str(valor), 1)
            pdf.ln()
        
        # Salvar PDF
        nome_arquivo = f"simulacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(nome_arquivo)
        return nome_arquivo

    def calcular_simulacao(e):
        try:
            valor = float(txt1.value.replace(".", "").replace(",", "."))
            prazo = int(txt2.value)
            sistema = comboEspecial3.value
            taxa = float(txt4.value.replace(",", ".")) / 100 / 12
            
            # Validar data
            try:
                data = f"{comboDataDia6.value}/{comboDataMes6.value}/{comboDataAno6.value}"
                datetime.strptime(data, "%d/%m/%Y")
            except (ValueError, AttributeError):
                raise ValueError("Data inválida")
            
            # Limpar tabela anterior
            tabela_resultados.rows.clear()
            
            dados_simulacao = {
                'valor': valor,
                'taxa': taxa,
                'prazo': prazo,
                'sistema': sistema,
                'data': data,
                'tabela': []
            }

            if sistema == "Decrescentes (Tabela SAC)":
                amortizacao = valor / prazo
                saldo_devedor = valor
                
                for i in range(1, prazo + 1):
                    juros = saldo_devedor * taxa
                    parcela = amortizacao + juros
                    saldo_devedor -= amortizacao
                    
                    dados_simulacao['tabela'].append([
                        f"{i}",
                        f"R$ {parcela:,.2f}",
                        f"R$ {juros:,.2f}",
                        f"R$ {amortizacao:,.2f}",
                        f"R$ {saldo_devedor:,.2f}"
                    ])
                    
                    tabela_resultados.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"{i}")),
                                ft.DataCell(ft.Text(f"R$ {parcela:,.2f}")),
                                ft.DataCell(ft.Text(f"R$ {juros:,.2f}")),
                                ft.DataCell(ft.Text(f"R$ {amortizacao:,.2f}")),
                                ft.DataCell(ft.Text(f"R$ {saldo_devedor:,.2f}"))
                            ]
                        )
                    )
            else:  # Price
                parcela = npf.pmt(taxa, prazo, -valor)
                saldo_devedor = valor
                
                for i in range(1, prazo + 1):
                    juros = saldo_devedor * taxa
                    amortizacao = parcela - juros
                    saldo_devedor -= amortizacao
                    
                    dados_simulacao['tabela'].append([
                        f"{i}",
                        f"R$ {parcela:,.2f}",
                        f"R$ {juros:,.2f}",
                        f"R$ {amortizacao:,.2f}",
                        f"R$ {saldo_devedor:,.2f}"
                    ])
                    
                    tabela_resultados.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"{i}")),
                                ft.DataCell(ft.Text(f"R$ {parcela:,.2f}")),
                                ft.DataCell(ft.Text(f"R$ {juros:,.2f}")),
                                ft.DataCell(ft.Text(f"R$ {amortizacao:,.2f}")),
                                ft.DataCell(ft.Text(f"R$ {saldo_devedor:,.2f}"))
                            ]
                        )
                    )

            tabela_resultados.visible = True
            btn_exportar.visible = True
            
            # Armazenar dados para exportação
            btn_exportar.data = dados_simulacao
            
            page.update()

        except ValueError:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Por favor, insira valores válidos."),
                    bgcolor=CORES["secondary"]
                )
            )

    def exportar_pdf(e):
        if hasattr(btn_exportar, 'data'):
            try:
                arquivo = criar_pdf(btn_exportar.data)
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"PDF salvo como: {arquivo}"),
                        bgcolor=CORES["primary"]
                    )
                )
            except Exception as err:
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"Erro ao gerar PDF: {str(err)}"),
                        bgcolor=CORES["secondary"]
                    )
                )

    # Componentes da interface
    txt1 = ft.TextField(
        label="1. Valor do empréstimo:",
        value="0,00",
        width=200,
        bgcolor=CORES["accent2"]
    )
    
    txt2 = ft.TextField(
        label="2. Número de parcelas:",
        value="0",
        width=200,
        bgcolor=CORES["accent2"]
    )
    
    comboEspecial3 = ft.Dropdown(
        label="3. Tipo de parcelas:",
        options=[
            ft.dropdown.Option("Fixas (Tabela Price)"),
            ft.dropdown.Option("Decrescentes (Tabela SAC)"),
        ],
        width=200,
        bgcolor=CORES["accent2"]
    )
    
    txt4 = ft.TextField(
        label="4. Taxa de juros (% ao mês):",
        value="0,00",
        width=200,
        bgcolor=CORES["accent2"]
    )

    comboDataAno6 = ft.Dropdown(
        label="6. Data da primeira parcela:",
        options=[
            ft.dropdown.Option(str(year)) 
            for year in range(datetime.now().year, datetime.now().year + 3)
        ],
        width=100,
        bgcolor=CORES["accent2"]
    )

    comboDataMes6 = ft.Dropdown(
        options=[ft.dropdown.Option(str(i).zfill(2)) for i in range(1, 13)],
        width=100,
        bgcolor=CORES["accent2"]
    )

    comboDataDia6 = ft.Dropdown(
        options=[ft.dropdown.Option(str(i).zfill(2)) for i in range(1, 32)],
        width=100,
        bgcolor=CORES["accent2"]
    )

    tabela_resultados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Período")),
            ft.DataColumn(ft.Text("Parcela")),
            ft.DataColumn(ft.Text("Juros")),
            ft.DataColumn(ft.Text("Amortização")),
            ft.DataColumn(ft.Text("Saldo Devedor"))
        ],
        rows=[],
        visible=False
    )

    btn_calcular = ft.ElevatedButton(
        text="Calcular",
        on_click=calcular_simulacao,
        style=ft.ButtonStyle(
            bgcolor={"": CORES["primary"]},
            color={"": "white"}
        )
    )

    btn_exportar = ft.ElevatedButton(
        text="Exportar PDF",
        on_click=exportar_pdf,
        visible=False,
        style=ft.ButtonStyle(
            bgcolor={"": CORES["accent1"]},
            color={"": "white"}
        )
    )

    # Layout
    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Simulador de Empréstimos",
                    size=24,
                    weight="bold",
                    color=CORES["primary"]
                ),
                ft.Text(
                    "Calcule amortizações e juros do seu empréstimo",
                    color="white"
                ),
                txt1,
                txt2,
                comboEspecial3,
                txt4,
                ft.Row(
                    [
                        comboDataAno6,
                        comboDataMes6,
                        comboDataDia6
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Row([btn_calcular, btn_exportar]),
                tabela_resultados
            ],
            spacing=20
        )
    )

if __name__ == "__main__":
    ft.app(target=main) 