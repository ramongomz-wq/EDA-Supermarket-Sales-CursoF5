import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Supermarket Sales · EDA",
    page_icon="🐼",
    layout="wide"
)

st.markdown("""
<style>

/* Colores de los cuatro KPI secundarios */
.st-key-kpi_transacciones {
    background-color: #146C63;
}

.st-key-kpi_cogs {
    background-color: #395983;
}

.st-key-kpi_ingreso {
    background-color: #57388C;
}

.st-key-kpi_rating {
    background-color: #86522F;
}

/* Diseño común de las cuatro tarjetas */
:is(
    .st-key-kpi_transacciones,
    .st-key-kpi_cogs,
    .st-key-kpi_ingreso,
    .st-key-kpi_rating
) {
    padding: 18px;
    border-radius: 12px;
    text-align: center;
}

/* Centrar las etiquetas */
:is(
    .st-key-kpi_transacciones,
    .st-key-kpi_cogs,
    .st-key-kpi_ingreso,
    .st-key-kpi_rating
) [data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    width: 100%;
}

/* Tamaño y color de las etiquetas */
:is(
    .st-key-kpi_transacciones,
    .st-key-kpi_cogs,
    .st-key-kpi_ingreso,
    .st-key-kpi_rating
) [data-testid="stMetricLabel"] p {
    color: white !important;
    font-size: 1rem !important;
    font-weight: 600;
}

/* Tamaño y color de los valores */
:is(
    .st-key-kpi_transacciones,
    .st-key-kpi_cogs,
    .st-key-kpi_ingreso,
    .st-key-kpi_rating
) [data-testid="stMetricValue"] {
    color: white !important;
    font-size: 1.8rem !important;
    text-align: center;
}

/* Tarjeta principal */
.st-key-kpi_facturacion {
    background-color: #17324D;
    padding: 24px;
    border-radius: 12px;
    text-align: center;
}

/* Centrar el contenido del KPI */
.st-key-kpi_facturacion [data-testid="stMetric"] {
    text-align: center;
}

/* Centrar la etiqueta */
.st-key-kpi_facturacion [data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    width: 100%;
}

/* Tamaño y color de FACTURACIÓN TOTAL */
.st-key-kpi_facturacion [data-testid="stMetricLabel"] p {
    color: white !important;
    font-size: 1.4rem !important;
    font-weight: 700;
}

/* Valor numérico */
.st-key-kpi_facturacion [data-testid="stMetricValue"] {
    color: white;
    font-size: 3rem;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


df = pd.read_csv("data/supermarket_sales.csv")

# ============================================================
# FILTROS INTERACTIVOS
# ============================================================

# Preparar las fechas
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

st.sidebar.header("🔎 Filtros del dashboard")

# Filtro de ciudades
ciudades = st.sidebar.multiselect(
    "Ciudad",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

# Filtro de líneas de producto
productos = st.sidebar.multiselect(
    "Línea de producto",
    options=sorted(df["Product line"].unique()),
    default=sorted(df["Product line"].unique())
)

# Filtro de fechas
fecha_min = df["Date"].min().date()
fecha_max = df["Date"].max().date()

periodo = st.sidebar.date_input(
    "Periodo",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max,
    format="DD/MM/YYYY"
)

# Esperar a que se seleccionen las dos fechas
if len(periodo) != 2:
    st.info("Selecciona una fecha inicial y otra final.")
    st.stop()

fecha_inicio, fecha_fin = periodo

# Aplicar todos los filtros al DataFrame
df = df.loc[
    df["City"].isin(ciudades)
    & df["Product line"].isin(productos)
    & df["Date"].between(
        pd.Timestamp(fecha_inicio),
        pd.Timestamp(fecha_fin)
    )
].copy()

# Comprobar que hay datos
if df.empty:
    st.warning("No hay registros para los filtros seleccionados.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
df["Mes"] = df["Date"].dt.to_period("M")

st.title("📊 Supermarket Sales")
st.subheader("Análisis exploratorio de ventas · Primer trimestre de 2019")
st.write("Dashboard interactivo desarrollado con Python y Streamlit.")

st.write("Primeras filas del dataset:")
st.dataframe(
    df.head(),
    column_config={
        "Date": st.column_config.DatetimeColumn(
            "Fecha",
            format="DD/MM/YYYY"
        )
    }
)

facturacion_total = df["Total"].sum()
numero_transacciones = df["Invoice ID"].nunique()
cogs_medio = df["cogs"].mean()
ingreso_bruto_total = df["gross income"].sum()
rating_medio = df["Rating"].mean()

# st.metric(
#     label="Facturación total",
#     value=f"{facturacion_total:,.2f}"
# )

# st.metric(
#     label="Número de transacciones",
#     value=numero_transacciones
# )

# col1, col2 = st.columns(2)

# with col1:
#     st.metric("Facturación total", f"{facturacion_total:,.2f}")

# with col2:
#     st.metric("Número de transacciones", numero_transacciones)

# Tarjeta principal: facturación total
with st.container(key="kpi_facturacion"):
    st.metric(
        "FACTURACIÓN TOTAL",
        f"{facturacion_total:,.2f}"
    )

# Cuatro KPI secundarios
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(key="kpi_transacciones"):
        st.metric("TRANSACCIONES", f"{numero_transacciones:,}")

with col2:
    with st.container(key="kpi_cogs"):
        st.metric("Coste medio de Bienes", f"{cogs_medio:,.2f}")

with col3:
    with st.container(key="kpi_ingreso"):
        st.metric("INGRESO BRUTO", f"{ingreso_bruto_total:,.2f}")

with col4:
    with st.container(key="kpi_rating"):
        st.metric("RATING MEDIO", f"{rating_medio:.2f}")


# ============================================================
# PREPARACIÓN DE LOS DATOS
# ============================================================

df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
df["Mes"] = df["Date"].dt.to_period("M")

colores_ciudades = {
    "Yangon": "#D97706",
    "Naypyitaw": "#146C63",
    "Mandalay": "#17324D"
}

nombres_meses = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo"
}


# ============================================================
# FILA SUPERIOR: DOS COLUMNAS
# ============================================================

col1, col2 = st.columns(2, gap="medium")

# ------------------------------------------------------------
# IZQUIERDA: EVOLUCIÓN MENSUAL
# ------------------------------------------------------------

with col1:

    st.subheader("Facturación y transacciones mensuales")

    ventas_mensuales = df.groupby("Mes").agg(
        facturacion=("Total", "sum"),
        transacciones=("Invoice ID", "nunique")
    )

    ventas_mensuales["ticket_medio"] = (
        ventas_mensuales["facturacion"] /
        ventas_mensuales["transacciones"]
    )

    meses = [
        nombres_meses[mes.month]
        for mes in ventas_mensuales.index
    ]

    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.bar(
        meses,
        ventas_mensuales["facturacion"],
        color="#17324D",
        alpha=0.85
    )

    ax1.set_ylabel("Facturación registrada")

    # Segundo eje: transacciones
    ax2 = ax1.twinx()

    ax2.plot(
        meses,
        ventas_mensuales["transacciones"],
        color="#D97706",
        marker="o",
        linewidth=3
    )

    # ax2.set_ylim(400, 520)
    # ax2.set_yticks(range(400, 521, 20))

    # Escala dinámica según las transacciones filtradas
    max_transacciones = ventas_mensuales["transacciones"].max()

    ax2.set_ylim(0, max(10, max_transacciones * 1.2))

    ax2.set_ylabel("Transacciones")

    # Ticket medio en el interior de las barras
    for i, ticket in enumerate(ventas_mensuales["ticket_medio"]):

        altura = ventas_mensuales["facturacion"].iloc[i]

        ax1.text(
            i,
            altura / 2,
            f"Ticket medio:\n{ticket:,.2f}",
            ha="center",
            va="center",
            fontsize=9,
            color="white",
            bbox=dict(
                boxstyle="round,pad=0.4",
                facecolor="#4F7F45",
                edgecolor="white"
            )
        )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "El eje de transacciones comienza en 400; "
        "la escala amplifica visualmente las diferencias."
    )


# ------------------------------------------------------------
# DERECHA: FACTURACIÓN POR PRODUCTO
# ------------------------------------------------------------

with col2:

    st.subheader("Facturación por línea de producto")

    ventas_productos = (
        df.groupby("Product line")["Total"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        x=ventas_productos.values,
        y=ventas_productos.index,
        color="#146C63",
        ax=ax
    )

    ax.set_xlabel("Facturación registrada")
    ax.set_ylabel("Línea de producto")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# FILA INFERIOR: DOS COLUMNAS
# ============================================================

col3, col4 = st.columns(2, gap="medium")

# ------------------------------------------------------------
# IZQUIERDA: FACTURACIÓN POR CIUDAD
# ------------------------------------------------------------

with col3:

    st.subheader("Distribución de facturación por ciudad")

    ventas_ciudad = df.groupby("City")["Total"].sum()

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.pie(
        ventas_ciudad,
        labels=ventas_ciudad.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=[
            colores_ciudades[ciudad]
            for ciudad in ventas_ciudad.index
        ],
        textprops={"fontsize": 11, "color": "#334155"},
        wedgeprops={
            "edgecolor": "white",
            "linewidth": 2
        }
    )

    ax.axis("equal")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ------------------------------------------------------------
# DERECHA: RATING MEDIO POR CIUDAD
# ------------------------------------------------------------

with col4:

    st.subheader("Valoración media por ciudad")

    rating_ciudad = (
        df.groupby("City")["Rating"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(7, 5))

    sns.barplot(
        x=rating_ciudad.values,
        y=rating_ciudad.index,
        hue=rating_ciudad.index,
        palette=colores_ciudades,
        legend=False,
        ax=ax
    )

    ax.set_xlim(5, 10)
    ax.set_xticks([5, 6, 7, 8, 9, 10])
    ax.set_xlabel("Rating medio")
    ax.set_ylabel("Ciudad")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# TABLA INFERIOR: FACTURACIÓN MENSUAL POR CIUDAD
# ============================================================

st.subheader("Facturación mensual por ciudad")

tabla_mes_ciudad = df.pivot_table(
    index="Mes",
    columns="City",
    values="Total",
    aggfunc="sum"
)

tabla_mes_ciudad.index = [
    nombres_meses[mes.month]
    for mes in tabla_mes_ciudad.index
]

tabla_mes_ciudad.index.name = "Mes"

st.dataframe(
    tabla_mes_ciudad.style.format("{:,.2f}"),
    width="stretch"
)
