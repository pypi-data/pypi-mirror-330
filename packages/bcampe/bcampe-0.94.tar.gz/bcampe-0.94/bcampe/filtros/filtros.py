import streamlit as st
import pandas as pd
from bcampe.estilos import show_warning

def criar_multiselect(colunas, dataframe, rename_columns=None, custom_placeholders=None):
    """
    Cria múltiplos multiselects dinamicamente com base nas colunas e dataframe fornecidos.
    Se um dicionário de renomeação for fornecido, ele renomeia as colunas conforme especificado.
    Se um dicionário de placeholders personalizados for fornecido, ele substitui o texto padrão do placeholder para cada coluna.
    """
    filtros = {}
    
    for coluna in colunas:
        # Renomeia a coluna se um nome de renomeação for fornecido
        nome_coluna = rename_columns.get(coluna, coluna) if rename_columns else coluna
        
        # Verifica se há um placeholder personalizado para a coluna, senão usa o padrão
        placeholder = custom_placeholders.get(coluna, f"Selecione uma {nome_coluna.replace('_', ' ')}") if custom_placeholders else f"Selecione uma {nome_coluna.replace('_', ' ')}"
        
        filtros[coluna] = st.multiselect(
            label=f"{nome_coluna.replace('_', ' ').title()}:",
            options=sorted(map(str, dataframe[coluna].unique().tolist())),
            placeholder=placeholder,
            key=coluna
        )
    
    return filtros
def inicializar_sessao(data_inicio, data_fim, filtros):
    """ Inicializa session_state com as chaves corretas dos filtros """
    if 'data_inicial' not in st.session_state:
        st.session_state['data_inicial'] = data_inicio
    if 'data_final' not in st.session_state:
        st.session_state['data_final'] = data_fim
    
    # Inicializa os filtros na session_state, se ainda não existirem
    for filtro in filtros.keys():
        if filtro not in st.session_state:
            st.session_state[filtro] = []

def resetar_filtros(filtros, data_inicio, data_fim):
    """ Reseta para o estado inicial """
    st.session_state['data_inicial'] = data_inicio  # Data original mínima
    st.session_state['data_final'] = data_fim       # Data original máxima
    for filtro in filtros.keys():  # Limpa as chaves dos filtros
        st.session_state[filtro] = []

def filtrar_dados(df, data_inicial, data_final, filtros, coluna_data):
    """
    Filtra os dados do DataFrame com base em um intervalo de datas e filtros específicos.

    Parâmetros:
    - df: DataFrame original.
    - data_inicial: Data mínima do filtro.
    - data_final: Data máxima do filtro.
    - filtros: Dicionário onde as chaves são nomes das colunas e os valores são listas de valores permitidos.
    - coluna_data: Nome da coluna que contém as datas para o filtro.

    Retorna:
    - df_filtrado: DataFrame filtrado conforme os critérios aplicados.
    """

    df_filtrado = df.copy()

    # Conversão das datas para datetime
    inicio = pd.to_datetime(data_inicial)
    fim = pd.to_datetime(data_final) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    # Verifica se a coluna de data existe no DataFrame
    if coluna_data not in df_filtrado.columns:
        st.error(f"A coluna '{coluna_data}' não existe no DataFrame.")
        st.stop()

    # Filtra o DataFrame pelo intervalo de datas
    df_filtrado = df_filtrado[(df_filtrado[coluna_data] >= inicio) & (df_filtrado[coluna_data] <= fim)]

    # Aplica filtros adicionais com base no dicionário de filtros
    for coluna, valores in filtros.items():
        if coluna in df_filtrado.columns and valores:  # Verifica se há valores para filtrar
            df_filtrado = df_filtrado[df_filtrado[coluna].astype(str).isin(valores)]

    # Verifica se o DataFrame filtrado está vazio
    if df_filtrado.empty:
        show_warning()
    st.session_state.df_filtrado = df_filtrado

    return df_filtrado

def converter_filtros(nomes_variaveis):
    """
    converte a lista em dicionario    
    Parâmetros:
    nomes_variaveis (list): Lista contendo os nomes das variáveis que serão usadas para os filtros.
    
    Retorno:
    dict: Dicionário com os filtros inicializados.
    """
    filtros = {}
    for nome in nomes_variaveis:
        filtros[nome] = st.session_state.get(nome, [])
    return filtros