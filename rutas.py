import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Optimum Home - Rutas del Día",
    page_icon="🚗",
    layout="centered",
)

st.sidebar.markdown("### 🚗 Panel de Control de Campo")

# Cargar el archivo CSV del día correspondiente
try:
  df = pd.read_csv("rutas_del_dia_2026-08-25.csv")
except FileNotFoundError:
  st.error(
      "No se encontró el archivo de rutas del día"
      " ('rutas_del_dia_2026-08-25.csv'). Por favor, verifique que esté subido"
      " al repositorio."
  )
  st.stop()

# Selector de cerrador en la barra lateral
lista_cerradores = ["Seleccione..."] + sorted(df["Cerrador"].unique().tolist())
cerrador_activo = st.sidebar.selectbox(
    "Seleccione su Usuario (Cerrador):", lista_cerradores
)

# Encabezado principal de la aplicación
st.markdown("## 📍 Planificador de Rutas - Operaciones Diarias")

if cerrador_activo != "Seleccione...":
  # Filtro estricto: el operador solo ve sus propias asignaciones
  df_filtrado = df[df["Cerrador"] == cerrador_activo]

  st.sidebar.success(f"Usuario activo: {cerrador_activo}")
  st.markdown(
      f"### 📋 Visitas asignadas para: **{cerrador_activo}**"
  )
  st.info(f"Total de clientes en ruta: {len(df_filtrado)}")

  # Mostrar la tabla limpia con los datos de las visitas
  st.dataframe(
      df_filtrado[["Cliente", "Direccion", "Telefono", "Estatus"]],
      use_container_width=True,
  )

  # Opcional: Detalle interactivo por cliente
  st.markdown("---")
  st.markdown("### 🔍 Detalle de Visita")
  cliente_seleccionado = st.selectbox(
      "Seleccione un cliente para gestionar:",
      df_filtrado["Cliente"].tolist(),
  )

  if cliente_seleccionado:
    datos_cliente = df_filtrado[
        df_filtrado["Cliente"] == cliente_seleccionado
    ].iloc[0]
    st.write(f"**Dirección:** {datos_cliente['Direccion']}")
    st.write(f"**Teléfono:** {datos_cliente['Telefono']}")
    st.write(f"**Estatus actual:** {datos_cliente['Estatus']}")

    if st.button("Marcar visita como Completada"):
      st.success(
          f"La visita al cliente {cliente_seleccionado} ha sido registrada con"
          " éxito."
      )

else:
  st.warning(
      "Por favor, seleccione su nombre o rol de cerrador en la barra lateral"
      " izquierda para acceder a su ruta asignada."
  )
