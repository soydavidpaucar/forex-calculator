import streamlit as st

def calcular_posicion_forex(balance, riesgo_porcentaje, comision_por_lote, stop_loss_pips, valor_pip=10):
    riesgo_decimal = riesgo_porcentaje / 100
    riesgo_total = round(balance * riesgo_decimal, 2)

    def calcular_riesgo_real(lotes):
        return (stop_loss_pips * valor_pip * lotes) + (comision_por_lote * lotes)

    lotes_inicial = riesgo_total / (stop_loss_pips * valor_pip)
    lotes = lotes_inicial

    while calcular_riesgo_real(lotes) > riesgo_total:
        lotes -= 0.01

    lotes = round(lotes, 2)
    comision_total = round(comision_por_lote * lotes, 2)
    riesgo_por_pip = round(lotes * valor_pip, 2)
    riesgo_total_final = round(calcular_riesgo_real(lotes), 2)

    return lotes, comision_total, riesgo_por_pip, riesgo_total_final

# Configuración de la página
st.set_page_config(layout="wide")

# Título centrado y grande
st.markdown("<h1 style='text-align: center; color: #1E88E5; font-size: 3rem;'>Calculadora de Posición para Forex</h1>", unsafe_allow_html=True)

# Crear tres columnas para centrar el contenido
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Inputs con valores por defecto
    balance = st.number_input("Balance de la cuenta ($):", value=100000.0, step=1000.0)
    riesgo_porcentaje = st.number_input("Riesgo (%):", value=1.0, step=0.1)
    comision_por_lote = st.number_input("Comisión por lote ($):", value=4.0, step=0.1)
    stop_loss_pips = st.number_input("Stop Loss (pips):", value=9.5, step=0.1)

    if st.button("Calcular", use_container_width=True):
        lotes, comision_total, riesgo_por_pip, riesgo_total_final = calcular_posicion_forex(
            balance, riesgo_porcentaje, comision_por_lote, stop_loss_pips
        )

        # Contenedor para los resultados con estilo mejorado
        st.markdown("""
        <style>
        .result-box {
            font-size: 24px;
            text-align: center;
            padding: 15px;
            margin: 10px;
            background-color: #1E88E5;
            color: white;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Resultados formateados con 2 decimales y estilo visible
        st.markdown(f"<div class='result-box'>Tamaño de la posición: {lotes:.2f} lotes</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>Comisión total: ${comision_total:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>Riesgo por pip: ${riesgo_por_pip:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>Riesgo total (incluyendo comisión): ${riesgo_total_final:.2f}</div>", unsafe_allow_html=True)