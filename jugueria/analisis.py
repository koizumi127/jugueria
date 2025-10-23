import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard: Juguería Oriana",
    page_icon="🍓",
    layout="wide"  # Usa el ancho completo de la pantalla
)

# --- Barra Lateral (Inputs del Usuario) ---
with st.sidebar:
    st.image("https://i.imgur.com/g0h1k1S.png") # Un logo genérico de jugos
    st.title("🍓 Juguería Oriana")
    st.header("Ingresa tus Datos Mensuales (S/)")

    ingresos_ventas = st.number_input(
        "Ingresos por Ventas", 
        min_value=0.0, value=30000.0, step=100.0
    )

    st.subheader("Costos y Gastos Operativos")
    
    costo_insumos = st.number_input("1. Costo de Insumos (Variable)", min_value=0.0, value=12000.0, step=50.0)
    sueldo_personal = st.number_input("2. Sueldo de Personal (Fijo)", min_value=0.0, value=5600.0, step=50.0)
    alquiler_local = st.number_input("3. Alquiler del Local (Fijo)", min_value=0.0, value=3000.0, step=50.0)
    servicios = st.number_input("4. Servicios (Agua y Luz) (Fijo)", min_value=0.0, value=700.0, step=10.0)
    flete = st.number_input("5. Flete (Fijo)", min_value=0.0, value=160.0, step=10.0)
    mantenimiento = st.number_input("6. Mantenimiento (Fijo)", min_value=0.0, value=200.0, step=10.0)


# --- Cálculos Financieros ---
costos_fijos = sueldo_personal + alquiler_local + servicios + flete + mantenimiento
costos_variables = costo_insumos
total_gastos = costos_fijos + costos_variables
utilidad_neta = ingresos_ventas - total_gastos

if ingresos_ventas > 0:
    margen_neto = (utilidad_neta / ingresos_ventas) * 100
    margen_contribucion_pct = (ingresos_ventas - costos_variables) / ingresos_ventas
else:
    margen_neto = 0
    margen_contribucion_pct = 0

if margen_contribucion_pct > 0:
    punto_equilibrio = costos_fijos / margen_contribucion_pct
else:
    punto_equilibrio = costos_fijos  # Si no hay margen, el PE es al menos los costos fijos

# Preparar datos para el gráfico
data_gastos = {
    'Categoría': ['Insumos', 'Sueldos', 'Alquiler', 'Servicios', 'Flete', 'Mantenimiento'],
    'Monto (S/)': [costo_insumos, sueldo_personal, alquiler_local, servicios, flete, mantenimiento]
}
df_gastos = pd.DataFrame(data_gastos).sort_values(by='Monto (S/)', ascending=False)


# --- Página Principal (Dashboard con Pestañas) ---
st.title("📊 Dashboard de Análisis Financiero")
st.markdown(f"Análisis de rentabilidad para **Juguería Oriana**.")

# Pestañas
tab1, tab2 = st.tabs(["Resumen General (KPIs)", "Análisis de Gastos"])

# --- Pestaña 1: Resumen General ---
with tab1:
    st.header("Resultados Clave del Mes")
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Ingresos por Ventas", f"S/ {ingresos_ventas:,.2f}")
    col2.metric("🧾 Gastos Totales", f"S/ {total_gastos:,.2f}")
    col3.metric("✨ Utilidad Neta", f"S/ {utilidad_neta:,.2f}")
    
    st.markdown("---")
    
    st.header("Indicadores de Desempeño (KPIs)")
    
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        st.subheader("📈 Margen de Ganancia Neta")
        st.metric(label="Margen Neto", value=f"{margen_neto:.1f} %")
        st.info(f"Por cada S/ 100 de venta, te estás quedando con S/ {margen_neto:.1f} de ganancia pura.")

    with col_kpi2:
        st.subheader("🎯 Punto de Equilibrio")
        st.metric(label="Venta Mínima Requerida", value=f"S/ {punto_equilibrio:,.2f}")
        st.info(f"Necesitas vender al menos S/ {punto_equilibrio:,.2f} al mes solo para cubrir todos tus costos.")

    st.markdown("---")
    
    # Semáforo de Salud Financiera
    st.header("Salud Financiera")
    if utilidad_neta > 0:
        st.success(f"¡Felicidades! Estás generando ganancias. Tu utilidad es de S/ {utilidad_neta:,.2f}.")
    elif utilidad_neta == 0 or (utilidad_neta > -500 and utilidad_neta < 0): # Un pequeño margen de "break-even"
        st.warning(f"¡Cuidado! Estás en punto de equilibrio. Tus ingresos (S/ {ingresos_ventas:,.2f}) apenas cubren tus gastos (S/ {total_gastos:,.2f}).")
    else:
        st.error(f"¡Alerta! Estás perdiendo dinero. Tienes una pérdida de S/ {utilidad_neta:,.2f}.")

# --- Pestaña 2: Análisis de Gastos ---
with tab2:
    st.header("Desglose de Gastos Operativos")
    
    # Gráfico de Pastel (Dona) con Plotly
    fig_pie = px.pie(
        df_gastos,
        names='Categoría',
        values='Monto (S/)',
        title='Proporción de Gastos del Mes',
        hole=0.4, # Esto lo convierte en dona
        color_discrete_sequence=px.colors.sequential.RdBu # Paleta de colores
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Tabla de datos
    st.subheader("Tabla de Gastos")
    st.dataframe(df_gastos.set_index('Categoría').style.format("S/ {:,.2f}"), use_container_width=True)