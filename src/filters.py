import streamlit as st
import pandas as pd


def render_home_filters(df):
    st.sidebar.header("Filtros")
    
    # Estado
    estados = sorted(df['State'].unique().tolist())
    estados_seleccionados = st.sidebar.multiselect(
        "Estado",
        estados,
        default=estados
    )
    
    # Categoría
    categorias = sorted(df['Category'].unique().tolist())
    categorias_seleccionadas = st.sidebar.multiselect(
        "Categoría",
        categorias,
        default=categorias
    )
    
    # Avance mínimo
    avance_minimo = st.sidebar.slider(
        "Avance mínimo (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )
    
    # Manager
    managers = sorted(df['Manager'].unique().tolist())
    managers_seleccionados = st.sidebar.multiselect(
        "Manager",
        managers,
        default=managers
    )
    
    # Aplicar los filtros al dataframe
    df_filtrado = df.copy()
    
    if estados_seleccionados:
        df_filtrado = df_filtrado[df_filtrado['State'].isin(estados_seleccionados)]
    
    if categorias_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado['Category'].isin(categorias_seleccionadas)]
    
    df_filtrado = df_filtrado[df_filtrado['PercentComplete'] >= avance_minimo]
    
    if managers_seleccionados:
        df_filtrado = df_filtrado[df_filtrado['Manager'].isin(managers_seleccionados)]
    
    return df_filtrado


def render_analisis_filters(df):
    """Renderiza los filtros de la página Analisis y retorna el dataframe filtrado."""
    st.sidebar.header("Filtros")
    
    # Manager
    st.sidebar.write("Selecciona Manager")
    managers = sorted(df['Manager'].unique().tolist())
    managers_seleccionados = st.sidebar.multiselect(
        "Manager",
        managers,
        default=managers,
        label_visibility="collapsed"
    )
    
    # Categoría
    st.sidebar.write("Filtra por categoría")
    categorias = sorted(df['Category'].unique().tolist())
    categorias_seleccionadas = st.sidebar.multiselect(
        "Categoría",
        categorias,
        default=categorias,
        label_visibility="collapsed"
    )
    
    # Aplicar filtros al dataframe
    df_filtrado = df.copy()
    
    if managers_seleccionados:
        df_filtrado = df_filtrado[df_filtrado['Manager'].isin(managers_seleccionados)]
    
    if categorias_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado['Category'].isin(categorias_seleccionadas)]
    
    return df_filtrado
