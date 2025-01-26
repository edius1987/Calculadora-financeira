import flet as ft
import locale
import numpy_financial as npf
from datetime import datetime, timedelta
from fpdf import FPDF

# Configurar locale para pt-BR
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class MainApp:
    def __init__(self):
        self.current_tab = None
        
    def main(self, page: ft.Page):
        page.title = "Calculadora Financeira"
        page.padding = 20
        page.bgcolor = "#1d1313"
        page.theme_mode = ft.ThemeMode.DARK
        page.window_width = 1200
        page.window_height = 800
        
        def change_tab(e):
            tabs_content.content = tab_contents[e.control.selected_index]
            page.update()

        # Container para conteúdo das abas
        tabs_content = ft.Container(
            content=None,
            padding=20,
            bgcolor="#1d1313",
            border=ft.border.all(2, "#30c4c9"),
            border_radius=10,
            expand=True
        )

        # Criando as abas
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            on_change=change_tab,
            tabs=[
                ft.Tab(
                    text="Calculadora Financeira",
                    icon=ft.icons.CALCULATE,
                ),
                ft.Tab(
                    text="Simulador de Empréstimos",
                    icon=ft.icons.MONEY,
                ),
                ft.Tab(
                    text="Calculadora de Financiamento",
                    icon=ft.icons.ATTACH_MONEY,
                ),
                ft.Tab(
                    text="Ajuda e Instruções",
                    icon=ft.icons.HELP_OUTLINE,
                ),
            ],
        )

        # Conteúdo de cada aba
        tab_contents = [
            self.create_calculadora_tab(page),
            self.create_simulador_tab(page),
            self.create_financiamento_tab(page),
            self.create_help_tab(page)
        ]

        # Definir conteúdo inicial
        tabs_content.content = tab_contents[0]

        # Layout principal
        page.add(
            ft.Column([
                tabs,
                tabs_content
            ], expand=True)
        )

    def calcular_taxa_juros(self, prestacao, meses, valor_financiado, precisao=0.000001):
        j_min = 0
        j_max = 1
        j = (j_min + j_max) / 2

        while j_max - j_min > precisao:
            q0 = (((1 - (1 + j) ** -meses)) / j) * prestacao
            if q0 < valor_financiado:
                j_min = j
            else:
                j_max = j
            j = (j_min + j_max) / 2

        return j

    def calcular_prestacao(self, valor_financiado, taxa_juros, meses):
        prestacao = valor_financiado * (taxa_juros / (1 - (1 + taxa_juros) ** -meses))
        return prestacao

    def calcular_valor_financiado(self, prestacao, taxa_juros, meses):
        valor_financiado = prestacao * ((1 - (1 + taxa_juros) ** -meses) / taxa_juros)
        return valor_financiado

    def create_calculadora_tab(self, page):
        # Primeira calculadora (app1.py)
        def calcular(e):
            try:
                # Contando campos preenchidos
                campos_preenchidos = sum(1 for campo in [
                    valor_financiado.value,
                    meses.value,
                    prestacao.value,
                    taxa_juros.value
                ] if campo)

                if campos_preenchidos != 3:
                    resultado.value = "Erro: Preencha exatamente 3 campos para realizar o cálculo"
                    resultado.color = "#d22042"
                    resultado.visible = True
                    page.update()
                    return

                if valor_financiado.value and prestacao.value and meses.value:
                    vf = float(valor_financiado.value.replace(',', '.'))
                    m = int(meses.value)
                    p = float(prestacao.value.replace(',', '.'))
                    
                    taxa = self.calcular_taxa_juros(p, m, vf)
                    taxa_percentual = taxa * 100
                    
                    resultado.value = f"Taxa de juros mensal calculada: {taxa_percentual:.2f}%"
                    resultado.color = "#a3b808"
                    
                elif taxa_juros.value and prestacao.value and meses.value:
                    taxa = float(taxa_juros.value.replace(',', '.')) / 100
                    p = float(prestacao.value.replace(',', '.'))
                    m = int(meses.value)
                    
                    vf = self.calcular_valor_financiado(p, taxa, m)
                    
                    resultado.value = f"Valor financiado calculado: R$ {vf:.2f}"
                    resultado.color = "#a3b808"
                    
                elif valor_financiado.value and taxa_juros.value and meses.value:
                    vf = float(valor_financiado.value.replace(',', '.'))
                    taxa = float(taxa_juros.value.replace(',', '.')) / 100
                    m = int(meses.value)
                    
                    p = self.calcular_prestacao(vf, taxa, m)
                    
                    resultado.value = f"Valor da prestação calculado: R$ {p:.2f}"
                    resultado.color = "#a3b808"
                    
                resultado.visible = True
                    
            except ValueError:
                resultado.value = "Erro: Verifique se os valores inseridos são números válidos"
                resultado.color = "#d22042"
                resultado.visible = True
            except Exception as e:
                resultado.value = f"Erro no cálculo: {str(e)}"
                resultado.color = "#d22042"
                resultado.visible = True
                
            page.update()

        # Campos de entrada
        taxa_juros = ft.TextField(
            label="Taxa de Juros Mensal (%)",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        meses = ft.TextField(
            label="Número de Meses",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        prestacao = ft.TextField(
            label="Valor da Prestação (R$)",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        valor_financiado = ft.TextField(
            label="Valor Financiado (R$)",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )

        resultado = ft.Text(size=16, color="#a3b808", visible=False)

        calcular_button = ft.ElevatedButton(
            text="Calcular",
            on_click=calcular,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor={"": "#24b694"},
            ),
            height=45,
            width=300,
        )

        instrucoes = ft.Column([
            ft.Text("Instruções", size=20, weight="bold", color="#24b694"),
            ft.Text(
                "Preencha 3 campos e o quarto será calculado. Utilize o ponto como marcador decimal.",
                size=16, 
                color="#30c4c9"
            ),
            ft.Text(
                "Se tiver 4 campos preenchidos irá apresentar um erro. Basta retirar um deles.",
                size=16, 
                color="#30c4c9"
            ),
        ])

        return ft.Column([
            ft.Text(
                "Calculadora Financeira", 
                size=30, 
                weight="bold",
                color="#24b694"
            ),
            instrucoes,
            ft.Divider(height=20, color="transparent"),
            taxa_juros,
            meses,
            prestacao,
            valor_financiado,
            calcular_button,
            resultado
        ], scroll=ft.ScrollMode.AUTO, spacing=20)

    def create_simulador_tab(self, page):
        def calcular_emprestimo(valor, parcelas, taxa, tipo, data_primeira_parcela):
            taxa = taxa / 100
            resultados = []
            
            if tipo == "price":
                pmt = -npf.pmt(taxa, parcelas, valor)
                saldo = valor
                
                for i in range(1, parcelas + 1):
                    juros = saldo * taxa
                    amortizacao = pmt - juros
                    saldo = saldo - amortizacao
                    
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
                amortizacao = valor / parcelas
                saldo = valor
                
                for i in range(1, parcelas + 1):
                    juros = saldo * taxa
                    valor_parcela = amortizacao + juros
                    saldo = saldo - amortizacao
                    
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

        # Criar os botões antes da função calcular
        btn_download_pdf = ft.ElevatedButton(
            text="Baixar PDF",
            on_click=lambda e: self.gerar_pdf(resultados, parametros),
            visible=False,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor={"": "#a3b808"},
            ),
            height=45,
            width=300,
        )

        btn_download_csv = ft.ElevatedButton(
            text="Baixar CSV",
            on_click=lambda e: self.gerar_csv(resultados, parametros),
            visible=False,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor={"": "#a3b808"},
            ),
            height=45,
            width=300,
        )

        # Variáveis para armazenar resultados e parâmetros
        resultados = []
        parametros = {}

        def calcular(e):
            try:
                valor = float(valor_emprestimo.value.replace(".", "").replace(",", "."))
                parcelas = int(num_parcelas.value)
                taxa = float(taxa_juros.value.replace(",", "."))
                tipo = tipo_tabela.value
                
                data_primeira_parcela = datetime(
                    int(data_ano.value),
                    int(data_mes.value),
                    int(data_dia.value)
                )
                
                nonlocal resultados, parametros
                resultados = calcular_emprestimo(valor, parcelas, taxa, tipo, data_primeira_parcela)
                
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
                
                # Habilitar botões de download
                btn_download_pdf.visible = True
                btn_download_csv.visible = True
                
                # Atualizar parâmetros
                parametros = {
                    "valor": valor,
                    "parcelas": parcelas,
                    "taxa": taxa,
                    "tipo": tipo,
                    "data_primeira_parcela": data_primeira_parcela
                }
                
                page.update()
                
            except Exception as err:
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Por favor, verifique os valores informados"),
                        bgcolor="#d22042"
                    )
                )

        # Campos do simulador
        valor_emprestimo = ft.TextField(
            label="Valor do empréstimo",
            prefix_text="R$ ",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        num_parcelas = ft.TextField(
            label="Número de parcelas",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        taxa_juros = ft.TextField(
            label="Taxa de juros mensal (%)",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        tipo_tabela = ft.Dropdown(
            label="Sistema de amortização",
            options=[
                ft.dropdown.Option("price", "Tabela Price (parcelas fixas)"),
                ft.dropdown.Option("sac", "Tabela SAC (amortização constante)")
            ],
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        # Campos para data
        data_dia = ft.Dropdown(
            label="Dia",
            options=[ft.dropdown.Option(str(i).zfill(2)) for i in range(1, 32)],
            width=100,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        data_mes = ft.Dropdown(
            label="Mês",
            options=[ft.dropdown.Option(str(i).zfill(2)) for i in range(1, 13)],
            width=100,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        data_ano = ft.Dropdown(
            label="Ano",
            options=[ft.dropdown.Option(str(datetime.now().year + i)) for i in range(3)],
            width=100,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
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

        calcular_button = ft.ElevatedButton(
            text="Calcular",
            on_click=calcular,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor={"": "#24b694"},
            ),
            height=45,
            width=300,
        )

        return ft.Column([
            ft.Text(
                "Simulador de Empréstimos", 
                size=30,
                weight="bold",
                color="#24b694"
            ),
            ft.Row([valor_emprestimo, num_parcelas]),
            ft.Row([taxa_juros, tipo_tabela]),
            ft.Text("Data da primeira parcela:", size=16, color="#30c4c9"),
            ft.Row([data_dia, data_mes, data_ano]),
            ft.Row([
                calcular_button,
                btn_download_pdf,
                btn_download_csv
            ]),
            tabela_resultados
        ], scroll=ft.ScrollMode.AUTO, spacing=20)

    def create_financiamento_tab(self, page):
        def calcular(e):
            try:
                campos_preenchidos = sum(1 for campo in [
                    valor_presente.value,
                    taxa.value,
                    tempo.value,
                    valor_futuro.value
                ] if campo)

                if campos_preenchidos != 3:
                    resultado.value = "Erro: Preencha exatamente 3 campos para realizar o cálculo"
                    resultado.color = "#d22042"
                    resultado.visible = True
                    page.update()
                    return

                if valor_presente.value and taxa.value and tempo.value:
                    vp = float(valor_presente.value.replace(',', '.'))
                    t = int(tempo.value)
                    r = float(taxa.value.replace(',', '.')) / 100
                    
                    vf = vp * (1 + r) ** t
                    
                    resultado.value = f"Valor futuro calculado: R$ {vf:.2f}"
                    resultado.color = "#a3b808"
                    
                elif valor_presente.value and taxa.value and valor_futuro.value:
                    vp = float(valor_presente.value.replace(',', '.'))
                    r = float(taxa.value.replace(',', '.')) / 100
                    vf = float(valor_futuro.value.replace(',', '.'))
                    
                    t = round(log(vf/vp) / log(1 + r))
                    
                    resultado.value = f"Tempo calculado: {t} meses"
                    resultado.color = "#a3b808"
                    
                elif valor_presente.value and tempo.value and valor_futuro.value:
                    vp = float(valor_presente.value.replace(',', '.'))
                    t = int(tempo.value)
                    vf = float(valor_futuro.value.replace(',', '.'))
                    
                    r = (vf/vp) ** (1/t) - 1
                    
                    resultado.value = f"Taxa de juros calculada: {r*100:.2f}%"
                    resultado.color = "#a3b808"
                    
                resultado.visible = True
                    
            except ValueError:
                resultado.value = "Erro: Verifique se os valores inseridos são números válidos"
                resultado.color = "#d22042"
                resultado.visible = True
            except Exception as e:
                resultado.value = f"Erro no cálculo: {str(e)}"
                resultado.color = "#d22042"
                resultado.visible = True
                
            page.update()

        valor_presente = ft.TextField(
            label="Valor Presente",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        taxa = ft.TextField(
            label="Taxa de Juros (%)",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        tempo = ft.TextField(
            label="Tempo (meses)",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )
        
        valor_futuro = ft.TextField(
            label="Valor Futuro",
            width=300,
            border_color="#24b694",
            focused_border_color="#24b694",
            color="#30c4c9",
        )

        resultado = ft.Text(size=16, color="#a3b808", visible=False)

        calcular_button = ft.ElevatedButton(
            text="Calcular",
            on_click=calcular,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor={"": "#24b694"},
            ),
            height=45,
            width=300,
        )

        return ft.Column([
            ft.Text(
                "Financiamento com prestações fixas",
                size=30,
                weight="bold",
                color="#24b694"
            ),
            valor_presente,
            taxa,
            tempo,
            valor_futuro,
            calcular_button,
            resultado
        ], scroll=ft.ScrollMode.AUTO, spacing=20)

    def create_help_tab(self, page):
        try:
            with open('help.md', 'r', encoding='utf-8') as file:
                md_content = file.read()
        except Exception as e:
            md_content = "# Arquivo de ajuda não encontrado\n\nErro: " + str(e)

        return ft.Column([
            ft.Text(
                "Ajuda e Instruções",
                size=30,
                weight="bold",
                color="#24b694"
            ),
            ft.Markdown(
                md_content,
                selectable=True,
                extension_set="commonmark",
                on_tap_link=lambda e: page.launch_url(e.data),
                code_style=ft.TextStyle(
                    color="#30c4c9",
                    font_family="monospace"
                ),
            )
        ], scroll=ft.ScrollMode.AUTO)

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
        
        try:
            # Salvar PDF
            pdf.output("simulacao_emprestimo.pdf")
            # Abrir o arquivo após gerar
            import webbrowser
            webbrowser.open("simulacao_emprestimo.pdf")
        except Exception as e:
            print(f"Erro ao gerar PDF: {str(e)}")

    def gerar_csv(self, dados, parametros):
        """Gera arquivo CSV com os resultados da simulação"""
        import csv
        
        try:
            with open('simulacao_emprestimo.csv', 'w', newline='', encoding='utf-8') as file:
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
                for linha in dados:
                    writer.writerow([
                        linha['parcela'],
                        linha['data'],
                        locale.currency(linha['valor_parcela'], grouping=True),
                        locale.currency(linha['amortizacao'], grouping=True),
                        locale.currency(linha['juros'], grouping=True),
                        locale.currency(linha['saldo'], grouping=True)
                    ])
                
                # Totais
                total_valor = sum(r['valor_parcela'] for r in dados)
                total_amortizacao = sum(r['amortizacao'] for r in dados)
                total_juros = sum(r['juros'] for r in dados)
                
                writer.writerow([])  # Linha em branco
                writer.writerow([
                    'Totais',
                    '',
                    locale.currency(total_valor, grouping=True),
                    locale.currency(total_amortizacao, grouping=True),
                    locale.currency(total_juros, grouping=True),
                    ''
                ])

            # Abrir o arquivo após gerar
            import webbrowser
            webbrowser.open("simulacao_emprestimo.csv")
        except Exception as e:
            print(f"Erro ao gerar CSV: {str(e)}")

def main():
    app = MainApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main() 