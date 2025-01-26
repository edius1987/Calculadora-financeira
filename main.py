import flet as ft
import markdown
import locale
from datetime import datetime
from fpdf import FPDF
import math

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

    def create_calculadora_tab(self, page):
        # Primeira calculadora
        return ft.Column([
            ft.Text("Calculadora Financeira", 
                   size=30, 
                   weight="bold",
                   color="#24b694"),
            self.create_calculadora_content(page)
        ], scroll=ft.ScrollMode.AUTO)

    def create_calculadora_content(self, page):
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

        resultado = ft.Text(size=16, color="#a3b808")

        def calcular(e):
            # Lógica de cálculo aqui
            resultado.value = "Cálculo realizado!"
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

        return ft.Column([
            taxa_juros,
            meses,
            prestacao,
            valor_financiado,
            calcular_button,
            resultado
        ], spacing=20)

    def create_simulador_tab(self, page):
        return ft.Column([
            ft.Text("Simulador de Empréstimos", 
                   size=30,
                   weight="bold",
                   color="#24b694"),
            self.create_simulador_content(page)
        ], scroll=ft.ScrollMode.AUTO)

    def create_simulador_content(self, page):
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

        return ft.Column([
            valor_emprestimo,
            num_parcelas,
            taxa_juros,
        ], spacing=20)

    def create_financiamento_tab(self, page):
        return ft.Column([
            ft.Text("Calculadora de Financiamento",
                   size=30,
                   weight="bold",
                   color="#24b694"),
            self.create_financiamento_content(page)
        ], scroll=ft.ScrollMode.AUTO)

    def create_financiamento_content(self, page):
        # Campos do financiamento
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

        return ft.Column([
            valor_presente,
            taxa,
            tempo,
        ], spacing=20)

    def create_help_tab(self, page):
        try:
            with open('help.md', 'r', encoding='utf-8') as file:
                md_content = file.read()
        except:
            md_content = "# Arquivo de ajuda não encontrado"

        return ft.Column([
            ft.Text("Ajuda e Instruções",
                   size=30,
                   weight="bold",
                   color="#24b694"),
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

def main():
    app = MainApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main() 