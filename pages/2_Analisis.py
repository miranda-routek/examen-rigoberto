import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_exam_data
from src.filters import render_analisis_filters

st.set_page_config(
    page_title="Análisis de Proyectos",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar los datos
@st.cache_data
def load_data():
    return load_exam_data()

df = load_data()

# Aplicar los filtros
df_filtrado = render_analisis_filters(df)

st.markdown("<h1 style='text-align: center;'>Visualizaciones y comparación</h1>", unsafe_allow_html=True)

# Gráfica del sactter plot
st.subheader("Avance vs Presupuesto (k$)")

fig = px.scatter(
    df_filtrado,
    x='BudgetThousands',
    y='PercentComplete',
    color='Category',
    hover_data=['ProjectName', 'Manager', 'State'],
    title=''
)

fig.update_layout(
    xaxis_title='BudgetThousands',
    yaxis_title='PercentComplete',
    height=600
)

st.plotly_chart(fig, use_container_width=True)
