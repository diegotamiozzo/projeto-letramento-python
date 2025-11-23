import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ------------------------------------------------
# FUNÇÕES DO BANCO DE DADOS
# ------------------------------------------------

def criar_tabela():
    conn = sqlite3.connect("despesas.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            categoria TEXT,
            valor REAL,
            descricao TEXT
        )
    """)
    conn.commit()
    conn.close()


def adicionar_despesa(data, categoria, valor, descricao):
    conn = sqlite3.connect("despesas.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO despesas (data, categoria, valor, descricao) VALUES (?, ?, ?, ?)",
        (data, categoria, valor, descricao)
    )
    conn.commit()
    conn.close()


def listar_todas():
    conn = sqlite3.connect("despesas.db")
    df = pd.read_sql_query("SELECT * FROM despesas ORDER BY id DESC", conn)
    conn.close()
    return df


def listar_despesas(inicio=None, fim=None):
    conn = sqlite3.connect("despesas.db")
    query = "SELECT * FROM despesas"

    if inicio and fim:
        query += f" WHERE date(data) BETWEEN '{inicio}' AND '{fim}'"

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def atualizar_despesa(id_, data, categoria, valor, descricao):
    conn = sqlite3.connect("despesas.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE despesas 
        SET data = ?, categoria = ?, valor = ?, descricao = ?
        WHERE id = ?
    """, (data, categoria, valor, descricao, id_))
    conn.commit()
    conn.close()


def excluir_despesa(id_):
    conn = sqlite3.connect("despesas.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM despesas WHERE id = ?", (id_,))
    conn.commit()
    conn.close()


# ------------------------------------------------
# INTERFACE
# ------------------------------------------------

st.set_page_config(page_title="Controle de Despesas")
st.title("Controle de Despesas Pessoais")

criar_tabela()

menu = ["Adicionar Despesa", "Relatórios", "Gerenciar (CRUD)"]
escolha = st.sidebar.selectbox("Menu", menu)

# ------------------------------------------------
# ADICIONAR
# ------------------------------------------------

if escolha == "Adicionar Despesa":
    st.header("Adicionar Despesa")

    # Definimos a lista de categorias
    lista_categorias = [
        "Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", 
        "Água", "Luz", "Telefone", "Internet", "Educação", "Outros"
    ]
    
    # Adicionamos a opção "placeholder" no início da lista
    opcoes_combo = ["Selecione uma categoria..."] + lista_categorias

    # Usamos clear_on_submit=True para limpar após sucesso
    with st.form("form_adicionar_despesa", clear_on_submit=True):
        
        data = st.date_input("Data")
        
        # O selectbox agora começa com a opção inválida
        categoria = st.selectbox("Categoria", options=opcoes_combo)
        
        valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
        descricao = st.text_input("Descrição")

        submitted = st.form_submit_button("Salvar Despesa")

        if submitted:
            # VALIDAÇÃO: Impede salvar se o usuário não mudou a categoria
            if categoria == "Selecione uma categoria...":
                st.warning(" Por favor, escolha uma categoria válida antes de salvar.")
            elif valor == 0:
                st.warning(" O valor da despesa não pode ser zero.")
            else:
                # Se tudo estiver ok, salva
                adicionar_despesa(str(data), categoria, valor, descricao)
                import time
                success_box = st.empty()  
                success_box.success("Despesa registrada com sucesso!")

                time.sleep(2)  # espera 2 segundos
                success_box.empty()  # remove a mensagem


# ------------------------------------------------
# RODAPÉ
# ------------------------------------------------
    st.write("---")
    st.markdown("<center><b>Desenvolvido por Diego Tamiozzo</b></center>", unsafe_allow_html=True)

# ------------------------------------------------
# RELATÓRIOS
# ------------------------------------------------

elif escolha == "Relatórios":
    st.header("Relatórios")

    col1, col2 = st.columns(2)
    inicio = col1.date_input("Data Inicial")
    fim = col2.date_input("Data Final")

    df = listar_despesas(str(inicio), str(fim))

    st.subheader("Despesas Registradas")
    st.dataframe(df)

    if not df.empty:
        total = df["valor"].sum()
        st.write(f"Total gasto no período: R$ {total:.2f}")

        st.subheader("Gastos por Categoria")
        por_categoria = df.groupby("categoria")["valor"].sum()
        st.bar_chart(por_categoria)

        maior_categoria = por_categoria.idxmax()
        st.write(f"Categoria com maior gasto: {maior_categoria}")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar CSV",
            data=csv,
            file_name="despesas.csv",
            mime="text/csv"
        )

# ------------------------------------------------
# GERENCIAMENTO (CRUD)
# ------------------------------------------------

elif escolha == "Gerenciar (CRUD)":
    st.header("Gerenciar Despesas (CRUD)")

    df = listar_todas()
    st.dataframe(df)

    if not df.empty:
        ids = df["id"].tolist()
        id_escolhido = st.selectbox("Selecione o ID para editar ou excluir:", ids)

        linha = df[df["id"] == id_escolhido].iloc[0]

        st.subheader("Editar Despesa")

        # Nota: Aqui não usamos st.form pois queremos ver as alterações em tempo real ou precisamos de lógica mais complexa
        nova_data = st.date_input("Data", datetime.strptime(linha["data"], "%Y-%m-%d"))
        nova_categoria = st.selectbox("Categoria", 
                                      ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", 
                                       "Água", "Luz", "Telefone", "Internet", "Educação", "Outros"],
                                      index=["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", 
                                             "Água", "Luz", "Telefone", "Internet", "Educação", "Outros"].index(linha["categoria"])
                                      )
        novo_valor = st.number_input("Valor (R$)", value=float(linha["valor"]))
        nova_descricao = st.text_input("Descrição", linha["descricao"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Salvar Alterações"):
                atualizar_despesa(id_escolhido, str(nova_data), nova_categoria, novo_valor, nova_descricao)
                st.success("Despesa atualizada com sucesso.")
                st.rerun() # Recarrega para atualizar a tabela

        with col2:
            if st.button("Excluir", type="primary"):
                excluir_despesa(id_escolhido)
                st.error("Despesa excluída.")
                st.rerun()

