import flet as ft

def calcular_taxa_juros(prestacao, meses, valor_financiado, precisao=0.000001):
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

def calcular_prestacao(valor_financiado, taxa_juros, meses):
    prestacao = valor_financiado * (taxa_juros / (1 - (1 + taxa_juros) ** -meses))
    return prestacao

def calcular_valor_financiado(prestacao, taxa_juros, meses):
    valor_financiado = prestacao * ((1 - (1 + taxa_juros) ** -meses) / taxa_juros)
    return valor_financiado

def main(page: ft.Page):
    page.title = "Calculadora de Financiamento"
    page.padding = 20
    page.bgcolor = "#1d1313"  # Fundo escuro

    # Criando o cabeçalho com instruções
    titulo = ft.Text("Calculadora de Financiamento", size=24, weight="bold", color="#24b694")
    instrucoes = ft.Column([
        ft.Text("Instruções", size=20, weight="bold", color="#24b694"),
        ft.Text("Preencha 3 campos e o quarto será calculado. Utilize o ponto como marcador decimal.",
               size=16, color="#30c4c9"),
        ft.Text("Se tiver 4 campos preenchidos irá apresentar um erro. Basta retirar um deles.",
               size=16, color="#30c4c9"),
    ])

    # Modificando os campos de entrada na ordem solicitada
    taxa_juros_input = ft.TextField(
        label="Taxa de Juros Mensal (%)",
        width=300,
        keyboard_type="number",
        hint_text="Ex: 1.99",
        border_color="#24b694",
        focused_border_color="#24b694",
        color="#30c4c9",
    )
    
    meses_input = ft.TextField(
        label="Número de Meses",
        width=300,
        keyboard_type="number",
        hint_text="Ex: 12",
        border_color="#24b694",
        focused_border_color="#24b694",
        color="#30c4c9",
    )
    
    prestacao_input = ft.TextField(
        label="Valor da Prestação (R$)",
        width=300,
        keyboard_type="number",
        hint_text="Ex: 261.50",
        border_color="#24b694",
        focused_border_color="#24b694",
        color="#30c4c9",
    )
    
    valor_financiado_input = ft.TextField(
        label="Valor Financiado (R$)",
        width=300,
        keyboard_type="number",
        hint_text="Ex: 2000.00",
        border_color="#24b694",
        focused_border_color="#24b694",
        color="#30c4c9",
    )
    
    resultado = ft.Text(size=16, color="#a3b808")

    def calcular(e):
        try:
            # Contando campos preenchidos
            campos_preenchidos = sum(1 for campo in [
                valor_financiado_input.value,
                meses_input.value,
                prestacao_input.value,
                taxa_juros_input.value
            ] if campo)

            if campos_preenchidos != 3:
                resultado.value = "Erro: Preencha exatamente 3 campos para realizar o cálculo"
                resultado.visible = True
                page.update()
                return

            if valor_financiado_input.value and prestacao_input.value and meses_input.value:
                valor_financiado = float(valor_financiado_input.value.replace(',', '.'))
                meses = int(meses_input.value)
                prestacao = float(prestacao_input.value.replace(',', '.'))
                
                taxa_juros = calcular_taxa_juros(prestacao, meses, valor_financiado)
                taxa_juros_percentual = taxa_juros * 100
                
                resultado.value = f"Taxa de juros mensal calculada: {taxa_juros_percentual:.2f}%"
                
            elif taxa_juros_input.value and prestacao_input.value and meses_input.value:
                taxa_juros = float(taxa_juros_input.value.replace(',', '.')) / 100
                prestacao = float(prestacao_input.value.replace(',', '.'))
                meses = int(meses_input.value)
                
                valor_financiado = calcular_valor_financiado(prestacao, taxa_juros, meses)
                
                resultado.value = f"Valor financiado calculado: R$ {valor_financiado:.2f}"
                
            elif valor_financiado_input.value and taxa_juros_input.value and meses_input.value:
                valor_financiado = float(valor_financiado_input.value.replace(',', '.'))
                taxa_juros = float(taxa_juros_input.value.replace(',', '.')) / 100
                meses = int(meses_input.value)
                
                prestacao = calcular_prestacao(valor_financiado, taxa_juros, meses)
                
                resultado.value = f"Valor da prestação calculado: R$ {prestacao:.2f}"
                
            resultado.visible = True
                
        except ValueError as e:
            resultado.value = "Erro: Verifique se os valores inseridos são números válidos"
            resultado.color = "#d22042"  # Vermelho para erro
            resultado.visible = True
        except Exception as e:
            resultado.value = f"Erro no cálculo: {str(e)}"
            resultado.color = "#d22042"  # Vermelho para erro
            resultado.visible = True
            
        page.update()

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

    # Organizando o layout
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    titulo,
                    instrucoes,
                    ft.Divider(height=20, color="transparent"),
                    taxa_juros_input,
                    meses_input,
                    prestacao_input,
                    valor_financiado_input,
                    calcular_button,
                    resultado,
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )
    )

ft.app(target=main)
