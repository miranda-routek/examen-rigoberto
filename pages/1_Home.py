import streamlit as st
import pandas as pd
from src.data_loader import load_exam_data
from src.filters import render_home_filters

# Configuración de la página
st.set_page_config(
    page_title="Home - Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos
@st.cache_data
def load_data():
    return load_exam_data()

df = load_data()

# Aplicar filtros desde el módulo
df_filtrado = render_home_filters(df)

# Contenido de Home
st.markdown("<h1 style='text-align: center;'>Dashboard principal de proyectos</h1>", unsafe_allow_html=True)

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Proyectos", len(df_filtrado))

with col2:
    avance_promedio = df_filtrado['PercentComplete'].mean()
    st.metric("Promedio avance (%)", f"{avance_promedio:.1f}")

with col3:
    managers_unicos = df_filtrado['Manager'].nunique()
    st.metric("Managers únicos", managers_unicos)

with col4:
    presupuesto_medio = df_filtrado['BudgetThousands'].mean()
    st.metric("Presupuesto medio", f"${presupuesto_medio:.1f}K")

st.markdown("---")

# Mostrar los datos 
df_mostrar = df_filtrado.reset_index(drop=True)
df_mostrar.index.name = ''
st.dataframe(
    df_mostrar,
    use_container_width=True,
    hide_index=False
)
