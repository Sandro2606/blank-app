import pandas as pd
import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://apis.digital.gob.cl/fl/feriados"

st.title("Análisis de Feriados - API Digital.gob.cl")

@st.cache_data
def cargar_datos_json(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  
        datos_json = response.json()  
        df = pd.DataFrame(datos_json)  
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()

df = cargar_datos_json(url)

if not df.empty:
    st.subheader("Datos cargados")
    st.dataframe(df)

    
    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])  
        df["año"] = df["fecha"].dt.year
        df["mes"] = df["fecha"].dt.month_name()
        df["día"] = df["fecha"].dt.day_name()

    st.sidebar.title("Filtros")
    año_seleccionado = st.sidebar.multiselect("Selecciona Año(s)", options=sorted(df["año"].unique()), default=sorted(df["año"].unique()))
    tipo_seleccionado = st.sidebar.multiselect("Selecciona Tipo(s) de Feriado", options=df["tipo"].unique(), default=df["tipo"].unique())

    df_filtrado = df[(df["año"].isin(año_seleccionado)) & (df["tipo"].isin(tipo_seleccionado))]

    st.write(f"Mostrando {len(df_filtrado)} feriados después de aplicar los filtros.")
    st.dataframe(df_filtrado)

    st.subheader("Gráficos")
    st.write("A continuación, se presentan visualizaciones basadas en los datos filtrados:")

    # Gráfico 1: Conteo de feriados por tipo
    if "tipo" in df_filtrado.columns:
        fig1, ax1 = plt.subplots()
        sns.countplot(
            y=df_filtrado["tipo"],
            order=df_filtrado["tipo"].value_counts().index,
            ax=ax1,
            hue=df_filtrado["tipo"],
            palette="viridis",
            legend=False
        )
        ax1.set_title("Conteo de Feriados por Tipo")
        st.pyplot(fig1)

    # Gráfico 2: Conteo de feriados por año
    if "año" in df_filtrado.columns:
        fig2, ax2 = plt.subplots()
        sns.countplot(
            x=df_filtrado["año"],
            hue=df_filtrado["año"],
            ax=ax2,
            palette="dark:Blue",
            legend=False
        )
        ax2.set_title("Conteo de Feriados por Año")
        st.pyplot(fig2)

    # Gráfico 3: Feriados por mes
    if "mes" in df_filtrado.columns:
        fig3, ax3 = plt.subplots()
        sns.countplot(
            y=df_filtrado["mes"],
            order=df_filtrado["mes"].value_counts().index,
            ax=ax3,
            hue=df_filtrado["mes"],
            palette="coolwarm",
            legend=False
        )
        ax3.set_title("Feriados por Mes")
        st.pyplot(fig3)

    # Gráfico 4: Proporción de feriados por tipo
    if "tipo" in df_filtrado.columns:
        tipo_counts = df_filtrado["tipo"].value_counts()
        fig4, ax4 = plt.subplots()
        ax4.pie(tipo_counts, labels=tipo_counts.index, autopct="%1.1f%%", colors=sns.color_palette("pastel"))
        ax4.set_title("Proporción de Feriados por Tipo")
        st.pyplot(fig4)

    # Gráfico 5: Frecuencia de feriados por día de la semana
    if "día" in df_filtrado.columns:
        fig5, ax5 = plt.subplots()
        sns.countplot(
            y=df_filtrado["día"],
            order=df_filtrado["día"].value_counts().index,
            ax=ax5,
            hue=df_filtrado["día"],
            palette="Set2",
            legend=False
        )
        ax5.set_title("Feriados por Día de la Semana")
        st.pyplot(fig5)

    st.subheader("Análisis Estadístico")
    st.write("A continuación, se presentan análisis estadísticos basados en los datos filtrados:")

    # Análisis 1: Número total de feriados
    st.write("1. Número total de feriados:")
    st.write(len(df_filtrado))

    # Análisis 2: Conteo de feriados por tipo
    if "tipo" in df_filtrado.columns:
        st.write("2. Conteo de feriados por tipo:")
        st.write(df_filtrado["tipo"].value_counts())

    # Análisis 3: Primer y último feriado registrado
    if "fecha" in df_filtrado.columns:
        st.write("3. Primer y último feriado registrado:")
        st.write(f"- Primer feriado: {df_filtrado['fecha'].min()}")
        st.write(f"- Último feriado: {df_filtrado['fecha'].max()}")

    # Análisis 4: Tipo de feriado más frecuente
    if "tipo" in df_filtrado.columns:
        st.write("4. Tipo de feriado más frecuente:")
        st.write(df_filtrado["tipo"].mode()[0])

    # Análisis 5: Mes con más feriados
    if "mes" in df_filtrado.columns:
        st.write("5. Mes con más feriados:")
        st.write(df_filtrado["mes"].value_counts().idxmax())
else:
    st.error("No se pudieron cargar los datos.")
