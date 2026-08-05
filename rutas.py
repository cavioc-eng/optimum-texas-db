import urllib.parse
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Optimum Home - Rutas del Día",
    page_icon="🚗",
    layout="centered",
)

st.sidebar.markdown("### 🚗 Panel de Control de Campo")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Carga de Rutas Diarias")

uploaded_file = st.sidebar.file_uploader(
    "Sube el archivo CSV del día:", type=["csv"]
)

if uploaded_file is not None:
  try:
    df = pd.read_csv(uploaded_file)
    required_cols = [
        "Cerrador",
        "Hora",
        "Cliente",
        "Direccion",
        "Telefono",
        "Estatus",
    ]
    if not all(col in df.columns for col in required_cols):
      st.error(
          "El archivo CSV debe contener las columnas: Cerrador, Hora, Cliente,"
          " Direccion, Telefono, Estatus."
      )
      st.stop()
  except Exception as e:
    st.error(f"Error al leer el archivo CSV: {e}")
    st.stop()
else:
  data = {
      "Cerrador": [
          "Carlos Vivas (Demo)",
          "Carlos Vivas (Demo)",
          "Carlos Vivas (Demo)",
      ],
      "Hora": ["09:00 AM", "11:30 AM", "02:30 PM"],
      "Cliente": [
          "Distribuidora Los Andes",
          "Inversiones Coseinca",
          "Comercial Lara C.A.",
      ],
      "Direccion": [
          "Avenida Principal de Cabudare",
          "Centro Comercial Loma Linda",
          "Avenida Venezuela Barquisimeto",
      ],
      "Telefono": ["0412-5268823", "0426-0367843", "0412-1112233"],
      "Estatus": ["Pendiente", "Pendiente", "Pendiente"],
  }
  df = pd.DataFrame(data)
  st.sidebar.info(
      "💡 Usando datos de prueba con horario. Sube tu CSV para actualizar."
  )

lista_cerradores = ["Seleccione..."] + sorted(df["Cerrador"].unique().tolist())
cerrador_activo = st.sidebar.selectbox(
    "Seleccione su Usuario (Cerrador):", lista_cerradores
)

st.markdown("## 📍 Planificador de Rutas - Operaciones Diarias")

if cerrador_activo != "Seleccione...":
  df_filtrado = df[df["Cerrador"] == cerrador_activo]

  if "Hora" in df_filtrado.columns:
    df_filtrado = df_filtrado.sort_values(by="Hora")

  st.sidebar.success(f"Usuario activo: {cerrador_activo}")
  st.markdown(f"### 📋 Visitas asignadas para: **{cerrador_activo}**")
  st.info(
      "🕒 Tus citas están ordenadas automáticamente desde la hora más temprana"
      " para optimizar tu recorrido."
  )
  st.info(f"Total de clientes en ruta: {len(df_filtrado)}")

  st.dataframe(
      df_filtrado[["Hora", "Cliente", "Direccion", "Telefono", "Estatus"]],
      use_container_width=True,
  )

  st.markdown("---")
  st.markdown("### 🔍 Detalle de Visita y Navegación")
  cliente_seleccionado = st.selectbox(
      "Seleccione un cliente para gestionar:",
      df_filtrado["Cliente"].tolist(),
  )

  if cliente_seleccionado:
    datos_cliente = df_filtrado[
        df_filtrado["Cliente"] == cliente_seleccionado
    ].iloc[0]
    st.write(f"**Hora de la cita:** {datos_cliente['Hora']}")
    st.write(f"**Dirección:** {datos_cliente['Direccion']}")
    st.write(f"**Teléfono:** {datos_cliente['Telefono']}")
    st.write(f"**Estatus actual:** {datos_cliente['Estatus']}")

    direccion_encoded = urllib.parse.quote(str(datos_cliente["Direccion"]))
    url_gmaps = (
        f"https://www.google.com/maps/search/?api=1&query={direccion_encoded}"
    )
    url_waze = f"https://waze.com/ul?q={direccion_encoded}&navigate=yes"

    st.markdown("##### Abrir aplicación de ruta:")
    col1, col2 = st.columns(2)
    with col1:
      st.link_button("🗺️ Google Maps", url_gmaps, use_container_width=True)
    with col2:
      st.link_button("🚗 Waze", url_waze, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
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
