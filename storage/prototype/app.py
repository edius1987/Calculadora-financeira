import flet as ft
from flet import (
    Page,
    Text,
    TextField,
    ElevatedButton,
    Column,
    Row,
    Container,
    ListView,
    IconButton,
    icons,
    colors,
    TextButton,
)
import math
from fpdf import FPDF
from datetime import datetime

class CalculadoraFinanceira:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = "Calculadora Financeira"
        self.page.padding = 20
        self.page.bgcolor = "#1d1313"  # Cor de fundo escura
        
        # Títulos
        self.titulo = Text(
            "Financiamento com prestações fixas",
            size=30,
            weight="bold",
            color="#24b694"
        )
        self.subtitulo = Text(
            "Simule o financiamento com prestações fixas",
            size=20,
            color="#30c4c9"
        )
        
        # Campos de entrada com labels
        self.t_label = Text("Tempo", size=18, weight="bold", color="#24b694")
        self.s_label = Text("Taxa de Juros (%)", size=18, weight="bold", color="#24b694")
        self.vp_label = Text("Valor Presente", size=18, weight="bold", color="#24b694")
        self.vf_label = Text("Valor Futuro", size=18, weight="bold", color="#24b694")
        
        self.t = TextField(
            width=400,
            border_color="#30c4c9",
            focused_border_color="#24b694",
            bgcolor="#1d1313",
            color="#ffffff"
        )
        self.s = TextField(
            width=400,
            border_color="#30c4c9",
            focused_border_color="#24b694",
            bgcolor="#1d1313",
            color="#ffffff"
        )
        self.vp = TextField(
            width=400,
            border_color="#30c4c9",
            focused_border_color="#24b694",
            bgcolor="#1d1313",
            color="#ffffff"
        )
        self.vf = TextField(
            width=400,
            border_color="#30c4c9",
            focused_border_color="#24b694",
            bgcolor="#1d1313",
            color="#ffffff"
        )
        
        # Mensagem de erro
        self.error_text = Text("", color="#d22042")
        
        # Lista de resultados
        self.resultados = []
        self.lista_resultados = ListView(
            expand=1,
            spacing=10,
            height=200,
            width=400
        )
        
        # Botões
        self.btn_calcular = ElevatedButton(
            "Calcular",
            on_click=lambda e: self.calcula(False),
            bgcolor="#24b694",
            color="#ffffff"
        )
        self.btn_vu = ElevatedButton(
            "Calcular VU",
            on_click=lambda e: self.calcula(True),
            bgcolor="#24b694",
            color="#ffffff"
        )
        self.btn_pdf = ElevatedButton(
            "Gerar PDF",
            on_click=self.gerar_pdf,
            disabled=True,
            bgcolor="#a3b808",
            color="#ffffff"
        )
        
        # Instruções
        self.instrucoes = Container(
            content=Column([
                Text("Instruções", size=24, weight="bold", color="#24b694"),
                Text(
                    "Preencha 3 campos e o quarto será calculado. Utilize o ponto como marcador decimal.",
                    size=16,
                    color="#ffffff"
                ),
                Text(
                    "Se tiver 4 campos preenchidos irá apresentar um erro. Basta retirar um deles.",
                    size=16,
                    color="#ffffff"
                ),
                Text(
                    "Para calcular o valor presente uniforme não preencha o campo do valor presente.",
                    size=16,
                    color="#ffffff"
                ),
            ]),
            bgcolor="#1d1313",
            padding=20,
            border=ft.border.all(2, "#30c4c9"),
            border_radius=10
        )
        
        # Layout
        self.page.add(
            self.titulo,
            self.subtitulo,
            Column([
                self.t_label,
                self.t,
                self.s_label,
                self.s,
                self.vp_label,
                self.vp,
                self.vf_label,
                self.vf,
            ], spacing=10),
            Row([self.btn_calcular, self.btn_vu]),
            self.error_text,
            Text("Resultados Salvos:", size=20, weight="bold", color="#24b694"),
            self.lista_resultados,
            self.btn_pdf,
            self.instrucoes
        )

    def valida(self, vf, s, t, vp):
        try:
            if vf: float(vf)
            if s: float(s)
            if t: int(t)
            if vp: float(vp)
            return True
        except ValueError:
            return False

    def calcula(self, VU):
        s = self.s.value.replace(",", ".")
        t = self.t.value
        vp = self.vp.value.replace(",", ".")
        vf = self.vf.value.replace(",", ".")
        
        tipo = None
        
        if not vf and s and t and vp:
            tipo = "vf"
            vf = "0"
        elif vf and not s and t and vp:
            tipo = "s"
            s = "0"
        elif vf and s and not t and vp:
            tipo = "t"
            t = "0"
        elif vf and s and t and not vp:
            tipo = "vp"
            vp = "0"
            
        if self.valida(vf, s, t, vp):
            vf = float(vf)
            vp = float(vp)
            s = float(s)/100
            t = int(t)
            result = 0
            
            if tipo == "vf":
                result = vp * math.pow((1+s), t)
            elif tipo == "vp":
                if VU:
                    result = vf / (math.pow(1+s, t) - 1)
                else:
                    result = vf / (math.pow(1+s, t))
            elif tipo == "t":
                result = math.ceil(math.log(vf/vp)/math.log(1+s))
            elif tipo == "s":
                result = (math.pow(vf/vp, 1/t) - 1) * 100
                
            if tipo is None:
                self.error_text.value = "Você está com 4 variáveis, por favor retire uma delas!"
            else:
                resultado_texto = f"{tipo.upper()}: {result:.2f}"
                self.adicionar_resultado(resultado_texto)
                if tipo == "vf": self.vf.value = f"{result:.2f}"
                elif tipo == "vp": self.vp.value = f"{result:.2f}"
                elif tipo == "t": self.t.value = f"{result:.0f}"
                elif tipo == "s": self.s.value = f"{result:.2f}"
                self.error_text.value = ""
        else:
            self.error_text.value = "Algum(ns) dos campos está(ão) inválido(s), por favor verificar!"
            
        self.page.update()

    def adicionar_resultado(self, resultado):
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        container = Container(
            content=Row([
                Text(f"{agora} - {resultado}", color="#ffffff"),
                IconButton(
                    icon=icons.DELETE,
                    icon_color="#d22042",
                    on_click=lambda e, res=resultado: self.remover_resultado(e, res)
                )
            ]),
            bgcolor="#24b694",
            padding=10,
            border_radius=5
        )
        self.resultados.append({
            'tempo': self.t.value,
            'taxa': self.s.value,
            'valor_presente': self.vp.value,
            'valor_futuro': self.vf.value,
            'resultado': resultado
        })
        self.lista_resultados.controls.append(container)
        self.btn_pdf.disabled = False
        self.page.update()

    def remover_resultado(self, e, resultado):
        for control in self.lista_resultados.controls:
            if resultado in control.content.controls[0].value:
                self.lista_resultados.controls.remove(control)
                self.resultados.remove(resultado)
                break
        
        if not self.resultados:
            self.btn_pdf.disabled = True
            
        self.page.update()

    def gerar_pdf(self, e):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=16)
        
        # Título
        pdf.cell(200, 10, txt="Financiamento com prestações fixas", ln=1, align="C")
        pdf.cell(200, 10, txt="Simulação de financiamento com prestações fixas", ln=1, align="C")
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=1, align="L")
        
        # Cabeçalho da tabela
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, "Tempo", 1)
        pdf.cell(40, 10, "Taxa (%)", 1)
        pdf.cell(40, 10, "Valor Presente", 1)
        pdf.cell(40, 10, "Valor Futuro", 1)
        pdf.cell(30, 10, "Resultado", 1, ln=1)
        
        # Dados da tabela
        pdf.set_font("Arial", size=10)
        for res in self.resultados:
            pdf.cell(40, 10, str(res['tempo']), 1)
            pdf.cell(40, 10, str(res['taxa']), 1)
            pdf.cell(40, 10, str(res['valor_presente']), 1)
            pdf.cell(40, 10, str(res['valor_futuro']), 1)
            pdf.cell(30, 10, str(res['resultado']), 1, ln=1)
            
        pdf.output("resultados_financeiros.pdf")
        
def main(page: Page):
    CalculadoraFinanceira(page)

if __name__ == "__main__":
    ft.app(target=main)
