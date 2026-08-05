import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Optimum Home - Rutas de Campo", page_icon="🚗", layout="centered"
)

with st.sidebar:
  try:
    st.image("logo_optimum.png", use_container_width=True)
  except:
    st.title("🏢 Optimum Home")

  st.markdown("### Panel de Control de Campo")

  cerrador_activo = st.selectbox(
      "Seleccione su Usuario (Cerrador):",
      [
          "Seleccione...",
          "Carlos Vivas (Demo)",
          "Cerrador 1 - Houston North",
          "Cerrador 2 - Houston South",
      ],
  )

  st.markdown("---")
  st.info("Use los botones de navegación para trazar la ruta automática.")

st.title("📍 Planificador de Rutas - Houston")

if cerrador_activo == "Seleccione...":
  st.warning(
      "Por favor, seleccione su nombre en la barra lateral para ver su ruta"
      " asignada del día."
  )
else:
  st.success(f"¡Bienvenido, **{cerrador_activo}**! Tienes 5 citas asignadas hoy.")

  data_prueba = [
      {
          "nombre": "Renee C Butler & Stephen M Butler",
          "direccion": "611 Mosman Ct, Houston, TX",
          "telefono": "+17135550142",
      },
      {
          "nombre": "Oanh Pham & Ker Teh",
          "direccion": "11511 Sugarbush Ridge Ln, Houston, TX",
          "telefono": "+17135550189",
      },
      {
          "nombre": "Dora E Hogan & Louis Hogan",
          "direccion": "11518 Chesswood Dr, Houston, TX",
          "telefono": "+17135550234",
      },
      {
          "nombre": "Ramona H Brady & Dennis Brady",
          "direccion": "506 Bridge Crest Blvd, Houston, TX",
          "telefono": "+17135550378",
      },
      {
          "nombre": "Aurelio G Galvan",
          "direccion": "5503 Fair Forest Dr, Houston, TX",
          "telefono": "+17135550491",
      },
  ]

  df_rutas = pd.DataFrame(data_prueba)

  for index, row in df_rutas.iterrows():
    with st.container():
      st.markdown(f"### 🏠 Parada #{index + 1}: {row['nombre']}")
      st.markdown(f"**Dirección:** {row['direccion']}")
      st.markdown(f"**Teléfono:** {row['telefono']}")

      dir_url = row["direccion"].replace(" ", "+")
      link_gmaps = f"https://www.google.com/maps/dir/?api=1&destination={dir_url}"
      link_waze = f"https://waze.com/ul?q={dir_url}&navigate=yes"

      col_call, col_map, col_waze = st.columns(3)

      with col_call:
        st.markdown(
            f'<a href="tel:{row["telefono"]}" target="_self"><button'
            ' style="width:100%; background-color:#2e7d32; color:white;'
            ' border:none; padding:10px; border-radius:5px;'
            ' font-weight:bold;">📞 Llamar</button></a>',
            unsafe_allow_html=True,
        )

      with col_map:
        st.markdown(
            f'<a href="{link_gmaps}" target="_blank"><button style="width:100%;'
            " background-color:#1976d2; color:white; border:none; padding:10px;"
            ' border-radius:5px; font-weight:bold;">🗺️ Google'
            " Maps</button></a>",
            unsafe_allow_html=True,
        )

      with col_waze:
        st.markdown(
            f'<a href="{link_waze}" target="_blank"><button style="width:100%;'
            " background-color:#00acc1; color:white; border:none; padding:10px;"
            ' border-radius:5px; font-weight:bold;">🚗 Waze</button></a>',
            unsafe_allow_html=True,
        )

      st.markdown("---")
