import flet as ft
import numpy_financial as npf
from fpdf import FPDF
from datetime import datetime, timedelta
import locale

# Configurar locale para formatação de moeda em pt-BR
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class SimuladorEmprestimos:
    def __init__(self):
        pass
        
    def calcular_emprestimo(self, valor, parcelas, taxa, tipo, data_primeira_parcela):
        """
        Calcula as parcelas do empréstimo
        valor: valor do empréstimo
        parcelas: número de parcelas
        taxa: taxa de juros mensal (em %)
        tipo: 'price' para Tabela Price ou 'sac' para Tabela SAC
        data_primeira_parcela: data da primeira parcela
        """
        taxa = taxa / 100  # Converter taxa para decimal
        resultados = []
        
        if tipo == "price":
            # Cálculo Tabela Price
            pmt = -npf.pmt(taxa, parcelas, valor)
            saldo = valor
            
            for i in range(1, parcelas + 1):
                juros = saldo * taxa
                amortizacao = pmt - juros
                saldo = saldo - amortizacao
                
                # Calcula a data da parcela
                data_parcela = data_primeira_parcela + timedelta(days=30 * (i-1))
                
                resultados.append({
                    "parcela": i,
                    "valor_parcela": pmt,
                    "amortizacao": amortizacao,
                    "juros": juros,
                    "saldo": max(0, saldo),
                    "data": data_parcela.strftime("%d/%m/%Y")
                })
                
        else:  # SAC
            # Cálculo Tabela SAC
            amortizacao = valor / parcelas
            saldo = valor
            
            for i in range(1, parcelas + 1):
                juros = saldo * taxa
                valor_parcela = amortizacao + juros
                saldo = saldo - amortizacao
                
                # Calcula a data da parcela
                data_parcela = data_primeira_parcela + timedelta(days=30 * (i-1))
                
                resultados.append({
                    "parcela": i,
                    "valor_parcela": valor_parcela,
                    "amortizacao": amortizacao,
                    "juros": juros,
                    "saldo": max(0, saldo),
                    "data": data_parcela.strftime("%d/%m/%Y")
                })
        
        return resultados

    def gerar_pdf(self, dados, parametros):
        """Gera relatório PDF com os resultados da simulação"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        
        # Título
        pdf.cell(0, 10, "Simulação de Empréstimo", ln=True, align="C")
        pdf.ln(10)
        
        # Parâmetros
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Parâmetros do cálculo:", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Valor do empréstimo: {locale.currency(parametros['valor'], grouping=True)}", ln=True)
        pdf.cell(0, 10, f"Número de parcelas: {parametros['parcelas']}", ln=True)
        pdf.cell(0, 10, f"Taxa de juros: {parametros['taxa']}% ao mês", ln=True)
        pdf.cell(0, 10, f"Sistema: {'Tabela Price' if parametros['tipo'] == 'price' else 'Tabela SAC'}", ln=True)
        pdf.cell(0, 10, f"Data primeira parcela: {parametros['data_primeira_parcela'].strftime('%d/%m/%Y')}", ln=True)
        pdf.ln(10)
        
        # Tabela de resultados
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Resultados:", ln=True)
        
        # Cabeçalho da tabela
        headers = ["Parcela", "Data", "Valor", "Amortização", "Juros", "Saldo"]
        col_width = 32
        
        for header in headers:
            pdf.cell(col_width, 10, header, 1)
        pdf.ln()
        
        # Dados da tabela
        pdf.set_font("Arial", "", 10)
        total_valor = 0
        total_amortizacao = 0
        total_juros = 0
        
        for linha in dados:
            pdf.cell(col_width, 10, f"{linha['parcela']}", 1)
            pdf.cell(col_width, 10, f"{linha['data']}", 1)
            pdf.cell(col_width, 10, f"{locale.currency(linha['valor_parcela'], grouping=True)}", 1)
            pdf.cell(col_width, 10, f"{locale.currency(linha['amortizacao'], grouping=True)}", 1)
            pdf.cell(col_width, 10, f"{locale.currency(linha['juros'], grouping=True)}", 1)
            pdf.cell(col_width, 10, f"{locale.currency(linha['saldo'], grouping=True)}", 1)
            pdf.ln()
            
            total_valor += linha['valor_parcela']
            total_amortizacao += linha['amortizacao']
            total_juros += linha['juros']
        
        # Linha de totais
        pdf.set_font("Arial", "B", 10)
        pdf.cell(col_width, 10, "Totais", 1)
        pdf.cell(col_width, 10, "", 1)
        pdf.cell(col_width, 10, locale.currency(total_valor, grouping=True), 1)
        pdf.cell(col_width, 10, locale.currency(total_amortizacao, grouping=True), 1)
        pdf.cell(col_width, 10, locale.currency(total_juros, grouping=True), 1)
        pdf.cell(col_width, 10, "", 1)
        
        # Salvar PDF
        pdf.output("simulacao_emprestimo.pdf")

    def gerar_csv(self, dados, parametros):
        """Gera arquivo CSV com os resultados da simulação"""
        import csv
        
        with open('simulacao_emprestimo.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Cabeçalho com parâmetros
            writer.writerow(['Parâmetros do cálculo'])
            writer.writerow(['Valor do empréstimo', locale.currency(parametros['valor'], grouping=True)])
            writer.writerow(['Número de parcelas', parametros['parcelas']])
            writer.writerow(['Taxa de juros', f"{parametros['taxa']}% ao mês"])
            writer.writerow(['Sistema', 'Tabela Price' if parametros['tipo'] == 'price' else 'Tabela SAC'])
            writer.writerow(['Data primeira parcela', parametros['data_primeira_parcela'].strftime('%d/%m/%Y')])
            writer.writerow([])  # Linha em branco
            
            # Cabeçalho da tabela
            writer.writerow(['Parcela', 'Data', 'Valor', 'Amortização', 'Juros', 'Saldo'])
            
            # Dados
            total_valor = 0
            total_amortizacao = 0
            total_juros = 0
            
            for linha in dados:
                writer.writerow([
                    linha['parcela'],
                    linha['data'],
                    locale.currency(linha['valor_parcela'], grouping=True),
                    locale.currency(linha['amortizacao'], grouping=True),
                    locale.currency(linha['juros'], grouping=True),
                    locale.currency(linha['saldo'], grouping=True)
                ])
                total_valor += linha['valor_parcela']
                total_amortizacao += linha['amortizacao']
                total_juros += linha['juros']
            
            # Linha de totais
            writer.writerow([
                'Totais',
                '',
                locale.currency(total_valor, grouping=True),
                locale.currency(total_amortizacao, grouping=True),
                locale.currency(total_juros, grouping=True),
                ''
            ])

    def main_page(self, page: ft.Page):
        page.title = "Simulador de Empréstimos"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.width = 1000
        page.window.height = 800
        page.scroll = ft.ScrollMode.AUTO
        
        # Campos de entrada
        valor_emprestimo = ft.TextField(
            label="Valor do empréstimo",
            prefix_text="R$ ",
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        num_parcelas = ft.TextField(
            label="Número de parcelas",
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        taxa_juros = ft.TextField(
            label="Taxa de juros mensal (%)",
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        tipo_tabela = ft.Dropdown(
            label="Sistema de amortização",
            options=[
                ft.dropdown.Option("price", "Tabela Price (parcelas fixas)"),
                ft.dropdown.Option("sac", "Tabela SAC (amortização constante)")
            ],
            width=300
        )
        
        # Campos para data
        data_dia = ft.Dropdown(
            label="Dia",
            options=[ft.dropdown.Option(str(i).zfill(2)) for i in range(1, 32)],
            width=100
        )
        
        data_mes = ft.Dropdown(
            label="Mês",
            options=[ft.dropdown.Option(str(i).zfill(2)) for i in range(1, 13)],
            width=100
        )
        
        data_ano = ft.Dropdown(
            label="Ano",
            options=[ft.dropdown.Option(str(datetime.now().year + i)) for i in range(3)],
            width=100
        )
        
        # Tabela de resultados
        tabela_resultados = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Parcela")),
                ft.DataColumn(ft.Text("Data")),
                ft.DataColumn(ft.Text("Valor")),
                ft.DataColumn(ft.Text("Amortização")),
                ft.DataColumn(ft.Text("Juros")),
                ft.DataColumn(ft.Text("Saldo"))
            ],
            rows=[]
        )

        def calcular(e):
            try:
                valor = float(valor_emprestimo.value.replace(".", "").replace(",", "."))
                parcelas = int(num_parcelas.value)
                taxa = float(taxa_juros.value.replace(",", "."))
                tipo = tipo_tabela.value
                
                # Criar data da primeira parcela
                data_primeira_parcela = datetime(
                    int(data_ano.value),
                    int(data_mes.value),
                    int(data_dia.value)
                )
                
                resultados = self.calcular_emprestimo(valor, parcelas, taxa, tipo, data_primeira_parcela)
                
                # Atualizar tabela
                tabela_resultados.rows.clear()
                for r in resultados:
                    tabela_resultados.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"{r['parcela']}")),
                                ft.DataCell(ft.Text(r['data'])),
                                ft.DataCell(ft.Text(locale.currency(r['valor_parcela'], grouping=True))),
                                ft.DataCell(ft.Text(locale.currency(r['amortizacao'], grouping=True))),
                                ft.DataCell(ft.Text(locale.currency(r['juros'], grouping=True))),
                                ft.DataCell(ft.Text(locale.currency(r['saldo'], grouping=True)))
                            ]
                        )
                    )
                
                # Calcular totais
                total_valor = sum(r['valor_parcela'] for r in resultados)
                total_amortizacao = sum(r['amortizacao'] for r in resultados)
                total_juros = sum(r['juros'] for r in resultados)
                
                # Adicionar linha de totais
                tabela_resultados.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("Totais", weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text("")),
                            ft.DataCell(ft.Text(locale.currency(total_valor, grouping=True), weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(locale.currency(total_amortizacao, grouping=True), weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(locale.currency(total_juros, grouping=True), weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(""))
                        ],
                        color=ft.colors.SURFACE_VARIANT
                    )
                )
                
                # Gerar PDF e habilitar botões de download
                parametros = {
                    "valor": valor,
                    "parcelas": parcelas,
                    "taxa": taxa,
                    "tipo": tipo,
                    "data_primeira_parcela": data_primeira_parcela
                }
                self.gerar_pdf(resultados, parametros)
                self.gerar_csv(resultados, parametros)
                
                # Habilitar botões de download
                btn_download_pdf.visible = True
                btn_download_csv.visible = True
                page.update()
                
            except Exception as err:
                print(f"Erro: {err}")
                page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Por favor, verifique os valores informados"))
                )

        def download_pdf(e):
            try:
                import os
                import webbrowser
                if os.path.exists("simulacao_emprestimo.pdf"):
                    # Usar webbrowser ao invés de launch_url
                    webbrowser.open("simulacao_emprestimo.pdf")
            except Exception as err:
                print(f"Erro ao abrir PDF: {err}")

        def download_csv(e):
            try:
                import os
                import webbrowser
                if os.path.exists("simulacao_emprestimo.csv"):
                    # Usar webbrowser ao invés de launch_url
                    webbrowser.open("simulacao_emprestimo.csv")
            except Exception as err:
                print(f"Erro ao abrir CSV: {err}")

        # Botões
        btn_calcular = ft.ElevatedButton(
            text="Calcular",
            on_click=calcular,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: ft.colors.WHITE},
                bgcolor={ft.ControlState.DEFAULT: ft.Colors.BLUE_500}
            )
        )

        btn_download_pdf = ft.ElevatedButton(
            text="Baixar PDF",
            on_click=download_pdf,
            visible=False,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: ft.colors.WHITE},
                bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREEN_500}
            )
        )

        btn_download_csv = ft.ElevatedButton(
            text="Baixar CSV",
            on_click=download_csv,
            visible=False,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: ft.colors.WHITE},
                bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREEN_500}
            )
        )

        # Layout
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Simulador de Empréstimos", size=30, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([valor_emprestimo, num_parcelas]),
                            ft.Row([taxa_juros, tipo_tabela]),
                            ft.Text("Data da primeira parcela:", size=16),
                            ft.Row([data_dia, data_mes, data_ano]),
                            ft.Row([
                                btn_calcular,
                                btn_download_pdf,
                                btn_download_csv
                            ]),
                        ]),
                        padding=20,
                        bgcolor=ft.Colors.ON_SURFACE_VARIANT,
                        border_radius=10
                    ),
                    ft.ListView(
                        controls=[tabela_resultados],
                        expand=True,
                        spacing=10,
                        padding=20,
                    )
                ]),
                padding=20
            )
        )

    def run(self):
        ft.app(target=self.main_page)

if __name__ == "__main__":
    app = SimuladorEmprestimos()
    app.run() 