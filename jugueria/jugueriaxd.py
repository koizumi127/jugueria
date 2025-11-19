import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="SGF - Juguería Oriana",
    page_icon="🥝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (Para los colores de la marca) ---
st.markdown("""
    <style>
    .main { background-color: #f9fafb; }
    .stMetric { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .css-1aumxhk { background-color: #1f2937; color: white; } /* Sidebar */
    h1, h2, h3 { color: #111827; }
    .highlight-green { color: #166534; font-weight: bold; }
    .highlight-orange { color: #ea580c; font-weight: bold; }
    .highlight-red { color: #dc2626; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS MAESTROS (OCTUBRE 2025) ---
# Estos son los datos finales corregidos y cuadrados
KPI_OCT = {
    "ventas": 33898.50,
    "costo_venta": 18046.00,
    "utilidad_bruta": 15852.50,
    "gastos_op": 4060.00,
    "utilidad_neta": 11792.50,
    "eficiencia": 11.98,  # %
    "margen_neto": 34.79, # %
    "caja": 11992.50
}

# --- SIDEBAR DE NAVEGACIÓN ---
with st.sidebar:
    st.title("🥝 ORIANA")
    st.caption("SISTEMA DE GESTIÓN FINANCIERA")
    st.markdown("---")
    
    menu = st.radio(
        "Menú Principal",
        ["Dashboard General", "Estados Financieros", "Gestión de Riesgos", "Ciclo Contable", "Recomendaciones", "Registro Diario"],
        index=0
    )
    
    st.markdown("---")
    st.info("📅 Periodo: Octubre 2025\n\n🟢 Estado: Informal (NRUS Pendiente)")

# --- LÓGICA DE VISTAS ---

# 1. DASHBOARD
if menu == "Dashboard General":
    st.header("📊 Resumen Gerencial (Octubre 2025)")
    
    # KPIs ROW
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ventas Totales", f"S/. {KPI_OCT['ventas']:,.2f}", "-20% vs Sept")
    col2.metric("Utilidad Neta", f"S/. {KPI_OCT['utilidad_neta']:,.2f}", "34.8% Margen")
    col3.metric("Eficiencia Gastos", f"{KPI_OCT['eficiencia']}%", "Nivel Óptimo")
    col4.metric("Caja Disponible", f"S/. {KPI_OCT['caja']:,.2f}", "Alta Liquidez")

    st.markdown("---")

    # GRÁFICOS
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Evolución Comparativa (Sept vs Oct)")
        # Datos para el gráfico
        data_evo = pd.DataFrame({
            "Concepto": ["Ventas", "Ventas", "Utilidad Neta", "Utilidad Neta"],
            "Mes": ["Septiembre", "Octubre", "Septiembre", "Octubre"],
            "Monto": [42638.50, 33898.50, 13703.50, 11792.50]
        })
        fig_bar = px.bar(data_evo, x="Concepto", y="Monto", color="Mes", barmode="group",
                         color_discrete_map={"Septiembre": "#9ca3af", "Octubre": "#ea580c"},
                         text_auto='.2s')
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("Destino de Ingresos (Oct)")
        # Datos Donut
        labels = ['Costo Venta (Insumos)', 'Utilidad Neta', 'Gastos Op. (Fijos)']
        values = [KPI_OCT['costo_venta'], KPI_OCT['utilidad_neta'], KPI_OCT['gastos_op']]
        colors = ['#f97316', '#16a34a', '#374151']
        
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=colors)])
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.caption("El 53% de los ingresos se destina a costos directos de producción.")


# 2. ESTADOS FINANCIEROS
elif menu == "Estados Financieros":
    st.header("📑 Estados Financieros Integrales")
    
    tab1, tab2 = st.tabs(["Estado de Resultados", "Balance General"])
    
    with tab1:
        st.subheader("Estado de Resultados (Septiembre vs Octubre)")
        
        # DataFrame ER
        data_er = {
            "Concepto": [
                "(+) Ventas Totales", 
                "(-) Costo de Ventas (Insumos + Sueldos)", 
                "(=) UTILIDAD BRUTA", 
                "(-) Gastos Operativos (Alquiler, Luz, Flete)", 
                "(=) UTILIDAD OPERATIVA", 
                "(-) Impuestos (Nota NIC 12)", 
                "(=) GANANCIA NETA"
            ],
            "Septiembre": [42638.50, -24675.00, 17963.50, -4260.00, 13703.50, 0.00, 13703.50],
            "Octubre": [33898.50, -18046.00, 15852.50, -4060.00, 11792.50, 0.00, 11792.50],
            "Var %": ["-20%", "-27%", "-12%", "-5%", "-14%", "-", "-14%"]
        }
        df_er = pd.DataFrame(data_er)
        
        # Formato visual de tabla
        st.dataframe(
            df_er.style.format({
                "Septiembre": "S/. {:,.2f}", 
                "Octubre": "S/. {:,.2f}"
            }).apply(lambda x: ['background: #dcfce7; font-weight: bold' if "GANANCIA" in v else '' for v in x], axis=1),
            use_container_width=True,
            hide_index=True
        )
        
        st.warning("⚠️ **Nota NIC 12:** No se incluyen provisiones de impuestos debido a la condición de informalidad actual. La utilidad incluye el ahorro fiscal.")

    with tab2:
        st.subheader("Estado de Situación Financiera")
        
        col_act, col_pas = st.columns(2)
        
        with col_act:
            st.markdown("### ACTIVOS")
            data_act = {
                "Rubro": ["Efectivo y Equivalentes", "Inventarios", "Activos Fijos (Muebles)", "TOTAL ACTIVOS"],
                "Octubre": [11992.50, 992.00, 3000.00, 15984.50]
            }
            df_act = pd.DataFrame(data_act)
            st.table(df_act.style.format({"Octubre": "S/. {:,.2f}"}))
            
        with col_pas:
            st.markdown("### PASIVO Y PATRIMONIO")
            data_pas = {
                "Rubro": ["Proveedores", "Capital Social", "Resultados Acumulados (Ajustado)", "Ganancia del Periodo", "TOTAL PAS + PAT"],
                "Octubre": [1860.00, 5000.00, -2668.00, 11792.50, 15984.50]
            }
            df_pas = pd.DataFrame(data_pas)
            st.table(df_pas.style.format({"Octubre": "S/. {:,.2f}"}))
            
        st.info("ℹ️ **Nota:** El saldo negativo en 'Resultados Acumulados' refleja el ajuste contable por los retiros de utilidades realizados por los propietarios en periodos anteriores (S/. 16k aprox).")


# 3. GESTIÓN DE RIESGOS
elif menu == "Gestión de Riesgos":
    st.header("⚠️ Matriz de Riesgos y Plan de Acción")
    
    riesgos = [
        {"ID": "R01", "Riesgo": "Mezcla de Finanzas (Retiros desordenados)", "Nivel": "CRÍTICO", "Solución": "Asignar 'Sueldo Gerencial' y prohibir retiros de caja."},
        {"ID": "R02", "Riesgo": "Contingencia Fiscal (Informalidad)", "Nivel": "ALTO", "Solución": "Formalización gradual vía NRUS (S/ 50 mensual)."},
        {"ID": "R03", "Riesgo": "Mermas de Insumos", "Nivel": "MEDIO", "Solución": "Implementar Kardex PEPS y compras just-in-time."},
        {"ID": "R04", "Riesgo": "Exceso de Liquidez Ociosa", "Nivel": "MEDIO", "Solución": "Invertir excedente en cuenta de ahorros alto rendimiento."}
    ]
    
    df_riesgos = pd.DataFrame(riesgos)
    
    def color_risk(val):
        color = '#fee2e2' if val == 'CRÍTICO' or val == 'ALTO' else '#fef3c7'
        return f'background-color: {color}; color: black; font-weight: bold'

    st.dataframe(df_riesgos.style.applymap(color_risk, subset=['Nivel']), use_container_width=True)


# 4. CICLO CONTABLE
elif menu == "Ciclo Contable":
    st.header("🔄 Propuesta de Ciclo Contable para MYPE")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2910/2910791.png", width=200) # Icono generico
    
    with col2:
        st.markdown("""
        ### Flujo de Información Financiera
        
        1.  **📥 Recolección (Input):** Centralización diaria de tickets de venta y notas de pedido.
        2.  **📝 Registro (Procesamiento):** Ingreso en el aplicativo clasificando Ingresos (Efectivo/Yape) y Salidas.
        3.  **⚖️ Conciliación (Control):** Arqueo de Caja diario. *(Saldo Inicial + Ventas - Gastos = Dinero Físico)*.
        4.  **📊 Reporte (Output):** Generación automática de Estado de Resultados a fin de mes.
        """)


# 5. RECOMENDACIONES
elif menu == "Recomendaciones":
    st.header("💡 Plan de Acción y Mejora")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ Recomendaciones Financieras")
        st.markdown("""
        * **Mantener estructura de costos:** La eficiencia operativa del 12% es clave. No elevar costos fijos sin asegurar ventas.
        * **Invertir excedentes:** Usar los S/ 11k de caja para comprar activos productivos (congeladoras) o ampliar la oferta.
        """)
        
    with col2:
        st.warning("🚀 Recomendaciones Operativas")
        st.markdown("""
        * **Formalización NRUS:** Urgente para evitar multas y acceder a crédito bancario.
        * **Disciplina de Caja:** Establecer un día fijo al mes para el reparto de utilidades, eliminando el "gasteo" diario.
        """)


# 6. REGISTRO DIARIO
elif menu == "Registro Diario":
    st.header("📝 Módulo de Registro Diario (Simulador)")
    
    with st.form("my_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            fecha = st.date_input("Fecha de Operación")
            tipo = st.selectbox("Tipo", ["🟢 Ingreso (Venta)", "🔴 Egreso (Insumos)", "🔴 Egreso (Gasto Fijo)"])
        
        with col_b:
            concepto = st.text_input("Concepto", placeholder="Ej. Venta del turno mañana")
            monto = st.number_input("Monto (S/.)", min_value=0.0, format="%.2f")
            
        medio = st.radio("Medio de Pago", ["Efectivo", "Yape / Plin"], horizontal=True)
        
        submitted = st.form_submit_button("💾 Registrar Operación")
        
        if submitted:
            st.toast(f"✅ Operación registrada correctamente: {concepto} - S/. {monto}")
            st.balloons()

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #6b7280;'>Sistema desarrollado por el Equipo 3 - Administración Financiera 2025</div>", unsafe_allow_html=True)