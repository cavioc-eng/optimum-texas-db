import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Optimum Home - Rutas de Campo",
    page_icon="🚗",
    layout="centered",
)

st.sidebar.markdown("### 🚗 Panel de Control de Campo")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Carga de Rutas Diarias")

# Botón para que el administrador o call center suba el CSV del día
uploaded_file = st.sidebar.file_uploader(
    "Sube el archivo CSV del día:", type=["csv"]
)

if uploaded_file is not None:
  try:
    df = pd.read_csv(uploaded_file)
    # Validar que contenga las columnas requeridas
    required_cols = ["Cerrador", "Cliente", "Direccion", "Telefono", "Estatus"]
    if not all(col in df.columns for col in required_cols):
      st.error(
          "El archivo CSV no tiene el formato correcto. Debe contener las"
          " columnas: Cerrador, Cliente, Direccion, Telefono, Estatus."
      )
      st.stop()
  except Exception as e:
    st.error(f"Error al leer el archivo CSV: {e}")
    st.stop()
else:
  # Datos de prueba por defecto para evitar errores si no se ha subido archivo
  data = {
      "Cerrador": [
          "Carlos Vivas (Demo)",
          "Carlos Vivas (Demo)",
          "Cerrador 1 - Houston North",
          "Cerrador 1 - Houston North",
          "Cerrador 2 - Houston South",
      ],
      "Cliente": [
          "Distribuidora Los Andes",
          "Inversiones Coseinca",
          "Alpha Logistics Corp",
          "Lone Star Supply",
          "Gulf Coast Energy",
      ],
      "Direccion": [
          "Avenida Principal de Cabudare",
          "Centro Comercial Loma Linda",
          "12400 Westheimer Rd",
          "4500 Post Oak Pkwy",
          "900 Smith St",
      ],
      "Telefono": [
          "0412-5268823",
          "0426-0367843",
          "713-555-0198",
          "713-555-0245",
          "713-555-0312",
      ],
      "Estatus": [
          "Pendiente",
          "Pendiente",
          "Pendiente",
          "Completado",
          "Pendiente",
      ],
  }
  df = pd.DataFrame(data)
  st.sidebar.info(
      "💡 Usando datos de prueba. Sube el archivo CSV del día en el botón de"
      " arriba para actualizar las rutas."
  )

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
  st.markdown(f"### 📋 Visitas asignadas para: **{cerrador_activo}**")
  st.info(f"Total de clientes en ruta: {len(df_filtrado)}")

  # Mostrar la tabla limpia con los datos de las visitas
  st.dataframe(
      df_filtrado[["Cliente", "Direccion", "Telefono", "Estatus"]],
      use_container_width=True,
  )

  # Detalle interactivo por cliente
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
