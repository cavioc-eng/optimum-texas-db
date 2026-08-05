import urllib.parse
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(
    page_title="Optimum Home - Rutas de Campo",
    page_icon="🚗",
    layout="centered",
)

# --- LOGOTIPO OFICIAL DE LA EMPRESA ---
try:
  st.sidebar.image("logo_optimum.png", use_container_width=True)
except Exception:
  st.sidebar.markdown("### 🏠 OPTIMUM HOME")

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
        "lat",
        "lon",
    ]
    if not all(col in df.columns for col in required_cols):
      st.error(
          "El archivo CSV debe contener las columnas: Cerrador, Hora, Cliente,"
          " Direccion, Telefono, Estatus, lat, lon."
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
      "Hora": ["09:00 AM", "02:30 PM", "11:30 AM"],  # Desordenadas a propósito
      "Cliente": [
          "Distribuidora Los Andes",
          "Comercial Lara C.A.",
          "Inversiones Coseinca",
      ],
      "Direccion": [
          "Avenida Principal de Cabudare",
          "Avenida Venezuela Barquisimeto",
          "Centro Comercial Loma Linda",
      ],
      "Telefono": ["0412-5268823", "0412-1112233", "0426-0367843"],
      "Estatus": ["Pendiente", "Pendiente", "Pendiente"],
      "lat": [10.0890, 10.0670, 10.0750],
      "lon": [-69.2930, -69.3220, -69.3120],
  }
  df = pd.DataFrame(data)
  st.sidebar.info(
      "💡 Usando datos de prueba. Sube tu CSV para actualizar las rutas."
  )

lista_cerradores = ["Seleccione..."] + sorted(df["Cerrador"].unique().tolist())
cerrador_activo = st.sidebar.selectbox(
    "Seleccione su Usuario (Cerrador):", lista_cerradores
)

st.markdown(
    """
    <div style="background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%); padding: 15px; border-radius: 8px; color: white; margin-bottom: 20px;">
        <h2 style="margin: 0; font-size: 24px;">📍 Optimum Home - Planificador de Rutas</h2>
        <p style="margin: 5px 0 0 0; font-size: 14px;">Control operativo y navegación inteligente para cerradores</p>
    </div>
""",
    unsafe_allow_html=True,
)

if cerrador_activo != "Seleccione...":
  df_filtrado = df[df["Cerrador"] == cerrador_activo].copy()

  # --- ORDENAMIENTO CRONOLÓGICO EXACTO POR HORA ---
  if "Hora" in df_filtrado.columns:
    try:
      df_filtrado["temp_hora"] = pd.to_datetime(
          df_filtrado["Hora"], format="%I:%M %p"
      )
      df_filtrado = df_filtrado.sort_values(by="temp_hora")
      df_filtrado = df_filtrado.drop(columns=["temp_hora"])
    except Exception:
      df_filtrado = df_filtrado.sort_values(by="Hora")

  # Asignar secuencia numérica 1, 2, 3...
  df_filtrado = df_filtrado.reset_index(drop=True)
  df_filtrado["Secuencia"] = range(1, len(df_filtrado) + 1)

  st.sidebar.success(f"Usuario activo: {cerrador_activo}")
  st.markdown(f"### 📋 Visitas asignadas para: **{cerrador_activo}**")
  st.info(
      "🕒 Tus citas están ordenadas cronológicamente de la más temprana a la"
      " más tardía."
  )
  st.info(f"Total de clientes en ruta: {len(df_filtrado)}")

  # --- MAPA INTERACTIVO CON SECUENCIA NUMÉRICA ---
  st.markdown("### 🗺️ Secuencia de Ruta en el Mapa")
  st.write(
      "Los números en el mapa indican el orden exacto en el que debes visitar"
      " cada parada:"
  )

  if "lat" in df_filtrado.columns and "lon" in df_filtrado.columns:
    lat_centro = df_filtrado["lat"].mean()
    lon_centro = df_filtrado["lon"].mean()

    # Capa de puntos (círculos)
    layer_scatter = pdk.Layer(
        "ScatterplotLayer",
        data=df_filtrado,
        get_position=["lon", "lat"],
        get_fill_color=[30, 58, 138, 200],  # Azul corporativo
        get_radius=300,
        pickable=True,
    )

    # Capa de texto (números de secuencia 1, 2, 3...)
    layer_text = pdk.Layer(
        "TextLayer",
        data=df_filtrado,
        get_position=["lon", "lat"],
        get_text="Secuencia",
        get_color=[255, 255, 255],
        get_size=18,
        get_alignment_baseline="'center'",
        get_text_anchor="'middle'",
    )

    view_state = pdk.ViewState(
        latitude=lat_centro, longitude=lon_centro, zoom=12, pitch=0
    )

    r = pdk.Deck(
        layers=[layer_scatter, layer_text],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Parada #{Secuencia}</b><br>Cliente: {Cliente}<br>Hora:"
            " {Hora}",
            "style": {"backgroundColor": "#1E3A8A", "color": "white"},
        },
    )
    st.pydeck_chart(r)

  st.markdown("---")

  # --- TABLA DE RESUMEN CON SECUENCIA ---
  st.markdown("### 📋 Listado de Paradas")
  st.dataframe(
      df_filtrado[["Secuencia", "Hora", "Cliente", "Direccion", "Telefono", "Estatus"]],
      use_container_width=True,
  )

  # --- DETALLE Y NAVEGACIÓN GPS ---
  st.markdown("---")
  st.markdown("### 🔍 Detalle de Visita y Navegación Individual")
  cliente_opciones = [
      f"Parada {row.Secuencia} - {row.Cliente} ({row.Hora})"
      for row in df_filtrado.itertuples()
  ]
  seleccion_str = st.selectbox(
      "Seleccione un cliente para gestionar:", cliente_opciones
  )

  if seleccion_str:
    idx_sel = cliente_opciones.index(seleccion_str)
    datos_cliente = df_filtrado.iloc[idx_sel]

    st.write(f"**Parada número:** {datos_cliente['Secuencia']}")
    st.write(f"**Hora de la cita:** {datos_cliente['Hora']}")
    st.write(f"**Cliente:** {datos_cliente['Cliente']}")
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
          f"La visita al cliente {datos_cliente['Cliente']} ha sido registrada"
          " con éxito."
      )

else:
  st.warning(
      "Por favor, seleccione su nombre o rol de cerrador en la barra lateral"
      " izquierda para acceder a su ruta asignada."
  )
