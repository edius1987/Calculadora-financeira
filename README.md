# Calculadora Financeira

Uma aplicação multiplataforma para cálculos financeiros desenvolvida com Python e Flet. A calculadora oferece diferentes funcionalidades para simulações financeiras, incluindo cálculo de valor futuro, simulação de empréstimos e financiamentos.

## Funcionalidades

- **Valor Futuro de um Capital**
  - Cálculo de juros compostos
  - Valor presente e futuro
  - Taxa de juros
  - Período em meses

- **Simulador de Empréstimos**
  - Tabela Price (parcelas fixas)
  - Tabela SAC (amortização constante)
  - Geração de relatórios em PDF
  - Exportação de dados em CSV
  - Visualização detalhada das parcelas

- **Financiamento com Prestações Fixas**
  - Cálculo de prestações
  - Simulação de diferentes cenários
  - Análise de taxas de juros

## Tecnologias Utilizadas

- Python 3.x
- Flet (Framework UI)
- FPDF (Geração de PDF)
- NumPy Financial
- Locale (Formatação monetária)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/calculadora-financeira.git
cd calculadora-financeira
```

2. Instale as dependências:
```bash
poetry init
```

3. Execute a aplicação:
```bash
poetry run flet run main.py
```

Para rodar no poetry como aplicativo web use o comando:

```poetry run flet run -w app.py```

## Como Usar

### Valor Futuro de um Capital
- Preencha 3 dos 4 campos disponíveis
- O campo não preenchido será calculado automaticamente
- Use ponto como separador decimal
- Os campos são:
  - Taxa de juros mensal (%)
  - Número de meses
  - Valor presente
  - Valor futuro

### Simulador de Empréstimos
- Preencha todos os campos solicitados
- Escolha o sistema de amortização (Price ou SAC)
- Defina a data da primeira parcela
- Visualize a tabela completa de parcelas
- Exporte os resultados em PDF ou CSV

### Financiamento com Prestações Fixas
- Similar ao cálculo de valor futuro
- Preencha 3 campos para calcular o quarto
- Ideal para simular diferentes cenários de financiamento

## Recursos Adicionais

- Interface intuitiva e responsiva
- Temas dark mode
- Exportação de dados em múltiplos formatos
- Cálculos precisos usando bibliotecas financeiras

## Contribuindo

1. Faça um fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Seu Nome - [@edius_ferreira](https://twitter.com/edius_ferreira)

Link do Projeto: [https://github.com/seu-usuario/calculadora-financeira](https://github.com/seu-usuario/calculadora-financeira)

## Referências

- [Python Flet - Introdução](https://www.usandopy.com/pt/curso-de-python-flet/python-flet-introducao-ao-python-flet/)
- [Flutter With Python](https://dev.to/ankushsinghgandhi/building-cross-platform-apps-with-flutter-and-python-a-short-guide-using-flet-epa)
- [Flet Documentation](https://flet.dev/)
