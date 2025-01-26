import flet as ft
import numpy_financial as npf
import pandas as pd
import numpy as np

def main(page: ft.Page):
    page.title = "Simulador de Empréstimos"
    page.padding = 20

    # Campos de entrada
    valor_emprestimo = ft.TextField(
        label="Valor do Empréstimo",
        hint_text="Ex: 10000",
        keyboard_type="number"
    )
    taxa_juros = ft.TextField(
        label="Taxa de Juros (%)",
        hint_text="Ex: 1.5",
        keyboard_type="number"
    )
    prazo_input = ft.TextField(
        label="Prazo (meses)",
        hint_text="Ex: 12",
        keyboard_type="number"
    )
    sistema_amortizacao = ft.Dropdown(
        label="Sistema de Amortização",
        options=[
            ft.dropdown.Option("SAC"),
            ft.dropdown.Option("Price")
        ],
        width=200
    )

    # Tabela para exibir os resultados (inicialmente escondida)
    resultados = ft.DataTable(
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

    def calcular(e):
        try:
            # Obter os valores dos campos
            valor = float(valor_emprestimo.value.replace(',', '.'))
            taxa = float(taxa_juros.value.replace(',', '.')) / 100 / 12  # Taxa mensal
            prazo = int(prazo_input.value)

            # Limpar resultados anteriores
            resultados.rows.clear()

            # Calcular as parcelas e criar um DataFrame para armazenar os dados
            if sistema_amortizacao.value == "SAC":
                amortizacao = valor / prazo
                saldo_devedor = valor
                novas_linhas = []

                for i in range(1, prazo + 1):
                    juros = saldo_devedor * taxa
                    parcela = amortizacao + juros
                    saldo_devedor -= amortizacao

                    novas_linhas.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"{i}")),
                                ft.DataCell(ft.Text(f"R$ {parcela:.2f}")),
                                ft.DataCell(ft.Text(f"R$ {juros:.2f}")),
                                ft.DataCell(ft.Text(f"R$ {amortizacao:.2f}")),
                                ft.DataCell(ft.Text(f"R$ {saldo_devedor:.2f}"))
                            ]
                        )
                    )

            else:  # Price
                parcela = npf.pmt(taxa, prazo, -valor)
                novas_linhas = []
                saldo_devedor = valor

                for i in range(1, prazo + 1):
                    juros = saldo_devedor * taxa
                    amortizacao = parcela - juros
                    saldo_devedor -= amortizacao

                    novas_linhas.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"{i}")),
                                ft.DataCell(ft.Text(f"R$ {parcela:.2f}")),
                                ft.DataCell(ft.Text(f"R$ {juros:.2f}")),
                                ft.DataCell(ft.Text(f"R$ {amortizacao:.2f}")),
                                ft.DataCell(ft.Text(f"R$ {saldo_devedor:.2f}"))
                            ]
                        )
                    )

            resultados.rows = novas_linhas
            resultados.visible = True
            page.update()

        except ValueError as e:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(
                        "Por favor, insira valores numéricos válidos."
                    ),
                    bgcolor=ft.colors.ERROR
                )
            )
            page.update()

    calcular_btn = ft.ElevatedButton(
        text="Calcular",
        on_click=calcular,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor={"": ft.colors.BLUE}
        )
    )

    # Organizando o layout
    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Simulador de Empréstimos",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                valor_emprestimo,
                taxa_juros,
                prazo_input,
                sistema_amortizacao,
                calcular_btn,
                resultados
            ],
            spacing=20
        )
    )

if __name__ == "__main__":
    ft.app(target=main)