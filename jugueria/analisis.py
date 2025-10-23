import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard: Juguería Oriana",
    page_icon="🍓",
    layout="wide"  # Usa el ancho completo de la pantalla
)

# --- 2. Barra Lateral (Inputs del Usuario) ---
with st.sidebar:
    # Usamos el logo de tu ejemplo
    st.image("https://i.imgur.com/g0h1k1S.png")
    st.title("🍓 Juguería Oriana")
    st.header("Simulador Financiero (S/)")
    st.caption("Modifica los valores para ver el impacto en tiempo real.")

    ingresos_ventas = st.number_input(
        "Ingresos por Ventas (Mensual)",
        min_value=0.0,
        # Dato de tu P&L 
        value=30000.0,
        step=100.0,
        help="Total de ventas brutas del mes."
    )

    st.subheader("Costos y Gastos Operativos")
    
    # --- Costos Variables ---
    costo_insumos = st.number_input(
        "1. Costo de Insumos (Variable)",
        min_value=0.0,
        # Dato de tu P&L 
        value=12000.0,
        step=50.0,
        help="Costo de frutas, pan, azúcar, etc. [cite: 120]"
    )
    
    # --- Costos Fijos ---
    sueldo_personal = st.number_input(
        "2. Sueldo de Personal (Fijo)",
        min_value=0.0,
        # Dato de tu P&L 
        value=5600.0,
        step=50.0,
        help="Pago total a los 4 trabajadores (4 x S/1400 mensual, según P&L) [cite: 97, 159]"
    )
    alquiler_local = st.number_input(
        "3. Alquiler del Local (Fijo)",
        min_value=0.0,
        # Dato de tu P&L 
        value=3000.0,
        step=50.0
    )
    servicios = st.number_input(
        "4. Servicios (Agua y Luz) (Fijo)",
        min_value=0.0,
        # Dato de tu P&L 
        value=700.0,
        step=10.0
    )
    flete = st.number_input(
        "5. Flete (Fijo)",
        min_value=0.0,
        # Dato de tu P&L 
        value=160.0,
        step=10.0,
        help="Transporte de insumos (S/40 semanal x 4 semanas) [cite: 195]"
    )
    mantenimiento = st.number_input(
        "6. Mantenimiento (Fijo)",
        min_value=0.0,
        # Dato de tu P&L 
        value=200.0,
        step=10.0
    )
    # ¡Importante! Agregado desde tu P&L 
    depreciacion = st.number_input(
        "7. Depreciación (Fijo)",
        min_value=0.0,
        # Dato de tu P&L 
        value=250.0,
        step=10.0,
        help="Gasto no monetario por desgaste de activos (equipos, muebles) [cite: 124]"
    )

# --- 3. Cálculos Financieros ---

# Gastos de Administración
gastos_admin = alquiler_local + servicios + mantenimiento + depreciacion
# Gastos de Venta
gastos_venta = flete + sueldo_personal

# Costos Fijos y Variables
costos_fijos = gastos_admin + gastos_venta
costos_variables = costo_insumos
total_gastos_operativos = costos_fijos + costos_variables

# Utilidades
utilidad_bruta = ingresos_ventas - costo_insumos
utilidad_operativa = utilidad_bruta - (gastos_venta + gastos_admin) # Es lo mismo que (Ingresos - Total Gastos)

# KPIs
if ingresos_ventas > 0:
    # Margen Bruto (tu doc lo calcula en 60%) [cite: 102]
    margen_bruto_pct = (utilidad_bruta / ingresos_ventas)
    # Margen Operativo (tu doc lo calcula en 26.97%) [cite: 110]
    margen_operativo_pct = (utilidad_operativa / ingresos_ventas)
    # Margen de Contribución (para Punto de Equilibrio)
    margen_contribucion_pct = (ingresos_ventas - costos_variables) / ingresos_ventas
else:
    margen_bruto_pct = 0
    margen_operativo_pct = 0
    margen_contribucion_pct = 0

# Punto de Equilibrio (Break-Even Point)
if margen_contribucion_pct > 0:
    punto_equilibrio = costos_fijos / margen_contribucion_pct
else:
    # Si no hay margen, el PE es al menos los costos fijos
    punto_equilibrio = costos_fijos 

# Preparar datos para el gráfico de gastos
data_gastos = {
    'Categoría': [
        'Insumos (Variable)', 
        'Sueldos', 
        'Alquiler', 
        'Servicios', 
        'Flete', 
        'Mantenimiento', 
        'Depreciación'
    ],
    'Monto (S/)': [
        costo_insumos, 
        sueldo_personal, 
        alquiler_local, 
        servicios, 
        flete, 
        mantenimiento, 
        depreciacion
    ]
}
df_gastos = pd.DataFrame(data_gastos).sort_values(by='Monto (S/)', ascending=False)


# --- 4. Página Principal (Dashboard con Pestañas) ---
st.title("📊 Dashboard de Análisis Financiero")
st.markdown(f"Análisis de rentabilidad mensual para **Juguería Oriana**.")

# Pestañas
tab1, tab2, tab3 = st.tabs([
    "📈 Resumen de Rentabilidad", 
    "💸 Análisis de Gastos", 
    "🎯 Punto de Equilibrio"
])

# --- Pestaña 1: Resumen de Rentabilidad ---
with tab1:
    st.header("Estado de Resultados (P&L)")
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Ingresos por Ventas", f"S/ {ingresos_ventas:,.2f}")
    col2.metric("🧾 Gastos Operativos Totales", f"S/ {total_gastos_operativos:,.2f}")
    col3.metric("✨ Utilidad Operativa (EBIT)", f"S/ {utilidad_operativa:,.2f}")
    
    st.markdown("---")
    
    st.header("Indicadores de Margen")
    
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        # Gráfico de "velocímetro" para el Margen Bruto
        fig_mg = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = margen_bruto_pct * 100,
            title = {'text': "Margen Bruto"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            number = {'suffix': "%"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "rgba(58, 112, 189, 0.8)"},
                'steps' : [
                     {'range': [0, 20], 'color': "#F08080"},
                     {'range': [20, 50], 'color': "#FFFACD"},
                     {'range': [50, 100], 'color': "#90EE90"}
                ],
            }
        ))
        fig_mg.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=0))
        st.plotly_chart(fig_mg, use_container_width=True)
        st.info(f"Por cada S/ 1.00 de venta, te quedan S/ {margen_bruto_pct:.2f} después de pagar los insumos.")

    with col_kpi2:
        # Gráfico de "velocímetro" para el Margen Operativo
        fig_mo = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = margen_operativo_pct * 100,
            title = {'text': "Margen Operativo (Rentabilidad Real)"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            number = {'suffix': "%"},
            gauge = {
                'axis': {'range': [0, 50]}, # Más realista para rentabilidad neta
                'bar': {'color': "rgba(0, 128, 0, 0.8)"},
                'steps' : [
                     {'range': [0, 10], 'color': "#F08080"},
                     {'range': [10, 25], 'color': "#FFFACD"},
                     {'range': [25, 50], 'color': "#90EE90"}
                ],
            }
        ))
        fig_mo.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=0))
        st.plotly_chart(fig_mo, use_container_width=True)
        st.info(f"Por cada S/ 1.00 de venta, tu ganancia neta (operativa) es de S/ {margen_operativo_pct:.2f} después de pagar TODO.")

# --- Pestaña 2: Análisis de Gastos ---
with tab2:
    st.header("Desglose de Gastos Operativos")
    
    # Gráfico de Pastel (Dona) con Plotly
    fig_pie = px.pie(
        df_gastos,
        names='Categoría',
        values='Monto (S/)',
        title=f'Proporción de Gastos (Total: S/ {total_gastos_operativos:,.2f})',
        hole=0.4, # Esto lo convierte en dona
        # Paleta de colores más "frutal" y elegante
        color_discrete_sequence=px.colors.diverging.Spectral
    )
    fig_pie.update_traces(
        textposition='outside', 
        textinfo='percent+label', 
        pull=[0.05 if c == 'Insumos (Variable)' else 0 for c in df_gastos['Categoría']] # Destaca Insumos
    )
    fig_pie.update_layout(showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.warning(
        f"**Análisis:** El **{df_gastos.iloc[0]['Categoría']}** representa el "
        f"**{(df_gastos.iloc[0]['Monto (S/)'] / total_gastos_operativos) * 100:,.1f}%** de tus gastos operativos totales. "
        "Es el punto principal para enfocar el control de costos."
    )
    
    # Tabla de datos
    st.subheader("Tabla de Gastos")
    st.dataframe(
        df_gastos.set_index('Categoría').style.format("S/ {:,.2f}"), 
        use_container_width=True
    )

# --- Pestaña 3: Punto de Equilibrio ---
with tab3:
    st.header("🎯 Punto de Equilibrio (Break-Even Point)")
    st.markdown("El Punto de Equilibrio es la **cantidad mínima que necesitas vender** solo para cubrir todos tus costos (fijos y variables). No ganas ni pierdes dinero.")
    
    st.metric(
        label="Venta Mínima Requerida para Cubrir Costos", 
        value=f"S/ {punto_equilibrio:,.2f}"
    )

    # Semáforo de Salud Financiera
    if utilidad_operativa > 0:
        st.success(f"¡Felicidades! Estás vendiendo S/ {ingresos_ventas - punto_equilibrio:,.2f} por encima de tu punto de equilibrio. Tu ganancia es de S/ {utilidad_operativa:,.2f}.")
    elif utilidad_operativa > -200: # Un pequeño margen
        st.warning(f"¡Cuidado! Estás en el límite. Tus ingresos (S/ {ingresos_ventas:,.2f}) apenas cubren tus costos (S/ {total_gastos_operativos:,.2f}).")
    else:
        st.error(f"¡Alerta! Estás por debajo del punto de equilibrio. Tienes una pérdida de S/ {utilidad_operativa:,.2f}.")
    
    st.markdown("---")
    
    # Gráfico de Punto de Equilibrio
    st.subheader("Gráfico de Punto de Equilibrio")
    
    # Creamos un rango de ventas para graficar
    max_ventas = max(ingresos_ventas * 1.5, punto_equilibrio * 1.5)
    ventas_hipoteticas = pd.Series(range(0, int(max_ventas), 1000))
    
    df_pe = pd.DataFrame({
        'Ventas': ventas_hipoteticas,
        'Costos Totales': costos_fijos + (ventas_hipoteticas * (1 - margen_contribucion_pct)),
        'Costos Fijos': costos_fijos
    })
    
    fig_pe = go.Figure()

    # 1. Línea de Costos Fijos (Horizontal)
    fig_pe.add_trace(go.Scatter(
        x=df_pe['Ventas'], y=df_pe['Costos Fijos'], 
        mode='lines', name='Costos Fijos', line=dict(color='red', dash='dash')
    ))
    
    # 2. Línea de Costos Totales (Inicia en Costos Fijos)
    fig_pe.add_trace(go.Scatter(
        x=df_pe['Ventas'], y=df_pe['Costos Totales'], 
        mode='lines', name='Costos Totales', line=dict(color='orange')
    ))
    
    # 3. Línea de Ingresos (Línea de 45 grados)
    fig_pe.add_trace(go.Scatter(
        x=df_pe['Ventas'], y=df_pe['Ventas'], 
        mode='lines', name='Ingresos (Ventas)', line=dict(color='green')
    ))
    
    # 4. Punto de Equilibrio (Intersección)
    fig_pe.add_trace(go.Scatter(
        x=[punto_equilibrio], y=[punto_equilibrio], 
        mode='markers', name='Punto de Equilibrio', 
        marker=dict(color='blue', size=12, symbol='star')
    ))
    
    # Zonas de Pérdida y Ganancia
    fig_pe.add_vrect(
        x0=0, x1=punto_equilibrio, 
        fillcolor="red", opacity=0.1, line_width=0, 
        annotation_text="Pérdida", annotation_position="top left"
    )
    fig_pe.add_vrect(
        x0=punto_equilibrio, x1=max_ventas, 
        fillcolor="green", opacity=0.1, line_width=0,
        annotation_text="Ganancia", annotation_position="top right"
    )

    fig_pe.update_layout(
        title='Ventas vs. Costos',
        xaxis_title='Ingresos por Ventas (S/)',
        yaxis_title='Monto (S/)'
    )
    
    st.plotly_chart(fig_pe, use_container_width=True)
