import streamlit as st
import pandas as pd



st.title("Simulador de Crédito Hipotecario")

st.markdown("""
> "Crédito... es el único testimonio perdurable a la confianza del hombre en el hombre."
""")


monto_prestamo = st.number_input("Monto del préstamo", min_value=100000, max_value=5000000)
tasa_interes = st.number_input("Tasa de interés anual", min_value=0.01, max_value=0.20)
plazo_anios = st.number_input("Plazo del préstamo (años)", min_value=1, max_value=30)


cuota_mensual = (monto_prestamo * tasa_interes / 12) / (1 - (1 + tasa_interes / 12)**(-plazo_anios * 12))

amortizacion_total = cuota_mensual * plazo_anios * 12

interes_total = amortizacion_total - monto_prestamo



st.write("Cuota mensual estimada: $", cuota_mensual)
st.write("Amortización total: $", amortizacion_total)
st.write("Interés total: $", interes_total)

# Gráfico amortización (opcional)

if st.checkbox("Mostrar gráfico de amortización"):
    meses = np.arange(1, plazo_anios * 12 + 1)
    amortizacion_acumulada = np.cumsum(cuota_mensual)

    fig, ax = plt.subplots()
    ax.plot(meses, amortizacion_acumulada, label="Amortización acumulada")
    ax.plot(meses, monto_prestamo * np.ones(len(meses)), label="Saldo pendiente")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Monto ($)")
    ax.legend()
    st.pyplot(fig)
