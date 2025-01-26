import flet as ft

def main(page: ft.Page):
    page.title = "Simulador de Empréstimos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def calcular_emprestimo(e):
        valor_emprestimo = float(txt1.value.replace(",", "."))
        num_parcelas = int(txt2.value)
        tipo_parcelas = comboEspecial3.value
        taxa_juros = float(txt4.value.replace(",", "."))
        indice_correcao = comboIndice5.value
        data_primeira_parcela = f"{comboDataDia6.value}/{comboDataMes6.value}/{comboDataAno6.value}"

        resultado.value = (
            f"Valor do empréstimo: {valor_emprestimo}\n"
            f"Número de parcelas: {num_parcelas}\n"
            f"Tipo de parcelas: {tipo_parcelas}\n"
            f"Taxa de juros: {taxa_juros}\n"
            f"Índice de correção: {indice_correcao}\n"
            f"Data da primeira parcela: {data_primeira_parcela}"
        )
        resultado.update()

    txt1 = ft.TextField(label="1. Valor do empréstimo:", value="0,00", width=200)
    txt2 = ft.TextField(label="2. Número de parcelas:", value="0", width=200)
    
    comboEspecial3 = ft.Dropdown(
        label="3. Tipo de parcelas:",
        options=[
            ft.dropdown.Option("Fixas (Tabela Price)"),
            ft.dropdown.Option("Decrescentes (Tabela SAC)"),
        ],
        width=200
    )
    
    comboJuros4 = ft.Dropdown(
        label="4. Valor da taxa de juros:",
        options=[
            ft.dropdown.Option("ao mês"),
            ft.dropdown.Option("ao ano"),
        ],
        width=200
    )
    
    txt4 = ft.TextField(label="", value="0,00", width=100)
    
    comboIndice5 = ft.Dropdown(
        label="5. Índice de correção monetária:",
        options=[
            ft.dropdown.Option("Nenhum"),
            ft.dropdown.Option("Dólar - Taxa de câmbio livre de venda"),
            ft.dropdown.Option("IGP-DI - Índice Geral de Preços"),
            ft.dropdown.Option("IGP-M - Índ. Geral de Preços do Mercado"),
            ft.dropdown.Option("IPCA - Índ. Preços ao Consumidor Amplo"),
            ft.dropdown.Option("Selic - Taxa básica de juros da economia"),
        ],
        width=200
    )
    
    comboDataAno6 = ft.Dropdown(
        label="6. Data da primeira parcela:",
        options=[
            ft.dropdown.Option("2024"),
            ft.dropdown.Option("2025"),
            ft.dropdown.Option("2026"),
        ],
        width=100
    )
    
    comboDataMes6 = ft.Dropdown(
        options=[ft.dropdown.Option(str(i)) for i in range(1, 13)],
        width=100
    )
    
    comboDataDia6 = ft.Dropdown(
        options=[ft.dropdown.Option(str(i)) for i in range(1, 32)],
        width=100
    )
    
    btnContinuar = ft.ElevatedButton(
        text="Continuar",
        on_click=calcular_emprestimo
    )
    
    resultado = ft.Text(value="", width=400)

    page.add(
        ft.Text("Simulador de Empréstimos", size=24, weight="bold"),
        ft.Text("Calcula amortizações e juros de um empréstimo."),
        ft.Text(
            "Esta tabela pode ser usada para fins de comparação com o que lhe é "
            "informado no momento do empréstimo."
        ),
        ft.Text("Parâmetros:", weight="bold"),
        txt1,
        txt2,
        comboEspecial3,
        ft.Row([comboJuros4, txt4]),
        comboIndice5,
        ft.Row([comboDataAno6, comboDataMes6, comboDataDia6]),
        btnContinuar,
        resultado
    )


ft.app(target=main)
