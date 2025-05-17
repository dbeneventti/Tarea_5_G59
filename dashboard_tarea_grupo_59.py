import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import date

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Dashboard Ventas - Grupo 59</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Equipo: Juan Osorio, Javiera Inda, Diego Beneventti, Andrea Angulo</h4>", unsafe_allow_html=True)

# Cargar datos
df = pd.read_csv("https://raw.githubusercontent.com/dbeneventti/Tarea_5_G59/main/data.csv", parse_dates=["Date"])

# Filtros
with st.expander("Filtros", expanded=False):
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        ciudades_sel = st.multiselect("Ciudad", df["City"].unique(), default=df["City"].unique())
    with col2:
        generos_sel = st.multiselect("Género", df["Gender"].unique(), default=df["Gender"].unique())
    with col3:
        pagos_sel = st.multiselect("Pago", df["Payment"].unique(), default=df["Payment"].unique())
    with col4:
        productos_sel = st.multiselect("Producto", df["Product line"].unique(), default=df["Product line"].unique())
    with col5:
        clientes_sel = st.multiselect("Cliente", df["Customer type"].unique(), default=df["Customer type"].unique())
    with col6:
        branch_sel = st.multiselect("Sucursal (Branch)", df["Branch"].unique(), default=df["Branch"].unique())
    with col7:
        fecha_min = df["Date"].min().date()
        fecha_max = df["Date"].max().date()
        fecha_inicio, fecha_fin = st.slider("Fecha", min_value=fecha_min, max_value=fecha_max, value=(fecha_min, fecha_max), format="DD/MM/YYYY")

# Aplicar filtros
df_filtrado = df[
    (df["City"].isin(ciudades_sel)) &
    (df["Gender"].isin(generos_sel)) &
    (df["Payment"].isin(pagos_sel)) &
    (df["Product line"].isin(productos_sel)) &
    (df["Customer type"].isin(clientes_sel)) &
    (df["Branch"].isin(branch_sel)) &
    (df["Date"].dt.date >= fecha_inicio) &
    (df["Date"].dt.date <= fecha_fin)
]


product_lines = sorted(df["Product line"].unique())
colors_set2 = sns.color_palette("Set2", n_colors=len(product_lines))
product_color_map = dict(zip(product_lines, colors_set2))

col1, col2, col3 = st.columns(3)

with col1:
    ventas_diarias = df_filtrado.groupby("Date")["Total"].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=ventas_diarias, x="Date", y="Total", marker="o", ax=ax1)
    ax1.set_title("Ventas Totales por Fecha", loc="center")
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel("Total")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with col2:
    ventas_ciudad = df_filtrado.groupby("City")["Total"].sum().sort_values().reset_index()
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=ventas_ciudad, y="City", x="Total", palette="pastel", ax=ax2)
    ax2.set_title("Ventas Totales por Ciudad", loc="center")
    ax2.set_xlabel("Total Ventas")
    ax2.set_ylabel("Ciudad")

    for bar in ax2.patches:
        bar.set_edgecolor("black")
        bar.set_linewidth(1)

    st.pyplot(fig2)

with col3:
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    color_order = df_filtrado["Product line"].dropna().unique()
    palette = [product_color_map[pl] for pl in color_order]

    sns.barplot(
        data=df_filtrado,
        x="Product line",
        y="Total",
        estimator=sum,
        errorbar=None,
        palette=palette,
        ax=ax3
    )
    ax3.set_title("Ingresos por Línea de Producto", loc="center")
    ax3.set_ylabel("Total Ventas")
    ax3.set_xlabel("")
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90)

    for bar in ax3.patches:
        bar.set_edgecolor("black")
        bar.set_linewidth(1)

    st.pyplot(fig3)


col4, col5, col6 = st.columns(3)

with col4:
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.histplot(
        df_filtrado["Rating"], 
        bins=20, 
        color="skyblue", 
        edgecolor="black", 
        stat="density", 
        ax=ax4
    )
    sns.kdeplot(df_filtrado["Rating"], color="red", linewidth=2, ax=ax4)
    ax4.set_title("Distribución de Calificaciones de Clientes", loc="center")
    ax4.set_xlabel("Calificación")
    ax4.set_ylabel("Densidad")
    ax4.set_xlim(df_filtrado["Rating"].min(), df_filtrado["Rating"].max())
    ax4.grid(False)
    st.pyplot(fig4)

    # Boxplot como complemento
    fig_box, ax_box = plt.subplots(figsize=(6, 0.5))
    sns.boxplot(x=df_filtrado["Rating"], ax=ax_box, color="skyblue", fliersize=3, linewidth=1, boxprops=dict(edgecolor="black"))
    ax_box.set_xlabel("Calificación")
    ax_box.set_yticks([])
    st.pyplot(fig_box)


with col5:
    total_spend = df_filtrado.groupby("Customer type")["Total"].sum().reset_index()
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    sns.barplot(
        data=total_spend,
        x="Customer type",
        y="Total",
        palette="Set3",
        ax=ax5
    )
    ax5.set_title("Gasto Total por Tipo de Cliente", loc="center")
    ax5.set_ylabel("Gasto Total")
    
    for i, row in total_spend.iterrows():
        ax5.text(i, row["Total"] + 100, f"{row['Total']:.2f}", ha='center')

    for bar in ax5.patches:
        bar.set_edgecolor("black")
        bar.set_linewidth(1)

    st.pyplot(fig5)

with col6:
    fig6, ax6 = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df_filtrado, x="cogs", y="gross income", hue="Branch", alpha=0.7, ax=ax6)
    ax6.set_title("COGS vs. Ingreso Bruto", loc="center")
    ax6.set_xlabel("COGS")
    ax6.set_ylabel("Ingreso Bruto")
    ax6.grid(False)
    st.pyplot(fig6)




col7, col8, col9 = st.columns(3)


with col7:
    payment_counts = df_filtrado['Payment'].value_counts().reset_index()
    payment_counts.columns = ['Método de Pago', 'Frecuencia']
    fig7, ax7 = plt.subplots(figsize=(6, 4))
    sns.barplot(
        data=payment_counts,
        x='Frecuencia',
        y='Método de Pago',
        palette='Set2',
        ax=ax7
    )
    ax7.set_title('Métodos de Pago Preferidos', loc="center")

    for bar in ax7.patches:
        bar.set_edgecolor("black")
        bar.set_linewidth(1)

    st.pyplot(fig7)


with col8:
    numeric_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
    df_numeric = df_filtrado[numeric_cols]
    correlation_matrix = df_numeric.corr()
    fig8, ax8 = plt.subplots(figsize=(6, 4))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, square=True, ax=ax8)
    ax8.set_title("Matriz de Correlación", loc="center")
    st.pyplot(fig8)

with col9:
    income_by_branch_product = df_filtrado.groupby(['Branch', 'Product line'])['gross income'].sum().reset_index()
    branch_totals = income_by_branch_product.groupby('Branch')['gross income'].sum()
    income_by_branch_product['Porcentaje'] = income_by_branch_product.apply(
        lambda row: row['gross income'] / branch_totals[row['Branch']] * 100, axis=1
    )
    pivot_values = income_by_branch_product.pivot(index='Branch', columns='Product line', values='gross income').fillna(0)
    percent_values = income_by_branch_product.pivot(index='Branch', columns='Product line', values='Porcentaje').fillna(0)

    fig9, ax9 = plt.subplots(figsize=(6, 4))
    bottom = [0] * len(pivot_values)
    x = range(len(pivot_values))

    for idx, column in enumerate(pivot_values.columns):
        values = pivot_values[column].values
        color = product_color_map.get(column, "gray")
        bars = ax9.bar(x, values, bottom=bottom, label=column, color=color)

        for i, bar in enumerate(bars):
            height = bar.get_height()
            if height > 0:
                pct = percent_values[column].iloc[i]
                ax9.text(bar.get_x() + bar.get_width()/2, bottom[i] + height/2,
                         f"{pct:.1f}%", ha='center', va='center', fontsize=8)

        bottom = [bottom[i] + values[i] for i in range(len(values))]

    ax9.set_xticks(x)
    ax9.set_xticklabels(pivot_values.index)
    ax9.set_title('Ingreso Bruto por Sucursal y Producto (%)', loc="center")
    ax9.set_ylabel("Ingreso Bruto Total")
    ax9.legend(title='Línea de Producto', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig9)


