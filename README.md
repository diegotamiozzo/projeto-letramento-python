# Controle de Despesas Pessoais

Aplicação desenvolvida em **Python**, utilizando **Streamlit** para interface gráfica e **SQLite** como banco de dados local. O objetivo é oferecer uma solução simples, rápida e funcional para registrar, visualizar e analisar despesas pessoais.

---

## Funcionalidades

* Registrar despesas com:

  * data
  * categoria
  * valor
  * descrição
* Filtrar despesas por intervalo de datas
* Visualizar tabela completa dos registros
* Exibir total gasto no período
* Gráfico de gastos por categoria
* Identificação da categoria com maior gasto
* Exportação dos dados filtrados em CSV

---

## Estrutura do Projeto

```
projeto-letramento-python/
│
├── app.py               # Código principal da aplicação
├── start.sh             # Script de inicialização para deploy no Render
├── requirements.txt     # Dependências do projeto
└── .gitignore           # Arquivos e pastas ignorados pelo Git
```

> O arquivo **despesas.db** é criado automaticamente durante a execução local e é ignorado no Git.

---

## Instalação e Execução Local

1. Crie e ative um ambiente virtual:

```
python -m venv .venv
.venv\Scripts\activate      # Windows
```

2. Instale as dependências:

```
pip install -r requirements.txt
```

3. Execute a aplicação:

```
python -m streamlit run app.py
```

A interface será aberta no navegador padrão.

---

## Deploy no Render (grátis)

1. Suba os seguintes arquivos para o GitHub:

```
app.py
requirements.txt
start.sh
.gitignore
```

2. No Render:

   * New → Web Service
   * Conecte ao repositório
   * Defina o **Start Command**:

```
bash start.sh
```

3. Aguarde o deploy e acesse seu aplicativo online.

---

## Dependências

* Python 3.10+
* Streamlit
* Pandas
* SQLite3 (nativo do Python)

---

## Licença

Este projeto é fornecido para fins educacionais e pode ser modificado e distribuído livremente.

---

## Autor

Desenvolvido como parte do projeto final do curso de Letramento Digital em Python.
