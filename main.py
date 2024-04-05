import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import re



st.title("Termómetro de Crédito Hipotecario")

st.markdown("""
> "Crédito... es el único testimonio perdurable a la confianza del hombre en el hombre."
""")




# Información de los bancos
bancos = {
    "BBVA": {
        "Plazo": "240 meses",
        "Monto máximo": "$15.000.000",
        "TEA": "7,5%",
        "Link": "https://www.bbva.com.ar/personas/productos/creditos-hipotecarios/comprar/permanente-pesos.html",
    },
    "Hipotecario UVA": {
        "Plazo": "360 meses",
        "Monto máximo": "$20.000.000",
        "TEA": "13,5%",
        "Link": "https://www.hipotecario.com.ar/personas/creditos-hipotecarios/adquisicion/",
    },
    "Provincia": {
        "Plazo": "Hasta 30 años",
        "Monto máximo": "$8.000.000",
        "TEA": "140,5%",
        "Link": "https://www.bancoprovincia.com.ar/CDN/Get/A5388_Banca_Personal_tasas_costos_condiciones_vigentes",
    },
}


df_prestamos = pd.DataFrame(bancos).T

url = "https://www.bbva.com.ar/personas/productos/creditos-hipotecarios/comprar/permanente-pesos.html"
response = requests.get(url)
html_content = response.text
# tasa_bbva = re.findall(r"(\d+,\d+)", html_content)[0]
tasa_bbva='117,13%'

df_prestamos.loc["BBVA", "TEA"] = tasa_bbva

# mejor tasa
tasa_minima = df_prestamos["TEA"].min()


st.write(f"""
<span style="color: green; font-weight: bold;">**Tasa mínima:** {tasa_minima}</span>
""", unsafe_allow_html=True)



st.table(df_prestamos)


st.markdown("""
**Información obtenida en:** https://www.argentina.gob.ar/tema/vivienda/creditos#1
""")

st.markdown("""## Simular:
""")
monto_prestamo = st.number_input("Monto ", min_value=1000, max_value=5000000000)
tasa_interes = st.number_input("Tasa de interés anual", min_value=1, max_value=10000)
plazo_anios = st.number_input("Plazo del préstamo (años)", min_value=1, max_value=50)


cuota_mensual = (monto_prestamo * tasa_interes / 12) / (1 - (1 + tasa_interes / 12)**(-plazo_anios * 12))

amortizacion_total = cuota_mensual * plazo_anios * 12

interes_total = amortizacion_total - monto_prestamo



st.write("Cuota mensual estimada: $", cuota_mensual)
st.write("Amortización total: $", amortizacion_total)
st.write("Interés total: $", interes_total)

# Gráfico amortización

if st.checkbox("Mostrar gráfico "):
    meses = np.arange(1, plazo_anios * 12 + 1)
    amortizacion_acumulada = np.cumsum(cuota_mensual)

    fig, ax = plt.subplots()
    ax.plot(meses, amortizacion_acumulada, label="Amortización acumulada")
    ax.plot(meses, monto_prestamo * np.ones(len(meses)), label="Saldo pendiente")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Monto ($)")
    ax.legend()
    st.pyplot(fig)
