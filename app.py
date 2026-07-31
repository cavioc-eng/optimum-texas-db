import glob
import os
import pandas as pd
import streamlit as st

# Configuración de la página web
st.set_page_config(
    page_title="Optimum Home - Portal de Consulta", page_icon="🏢", layout="wide"
)

# Cargar y unir automáticamente las partes de la base de datos de forma robusta
if "df" not in st.session_state:
  current_dir = os.path.dirname(os.path.abspath(__file__))
  pattern = os.path.join(current_dir, "parte_*.csv")
  archivos_partes = sorted(glob.glob(pattern))

  if archivos_partes:
    df_list = [pd.read_csv(f, low_memory=False) for f in archivos_partes]
    st.session_state.df = pd.concat(df_list, ignore_index=True)
  else:
    st.session_state.df = pd.DataFrame(
        columns=[
            "first_name",
            "last_name",
            "city",
            "address1",
            "email",
            "clean_phone",
        ]
    )

# Control de Sesión y Autenticación
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
  st.session_state.rol = None

if not st.session_state.autenticado:
  st.title("🔒 Optimum Home - Acceso Restringido")
  st.markdown("Ingrese su contraseña autorizada para acceder al sistema.")

  with st.form("login_form"):
    password_ingresada = st.text_input("Contraseña de Acceso", type="password")
    submit = st.form_submit_button("Ingresar al Sistema")

    if submit:
      if password_ingresada == "optimum2026":
        st.session_state.autenticado = True
        st.session_state.rol = "Agente"
        st.rerun()
      elif password_ingresada == "coseinca2026":
        st.session_state.autenticado = True
        st.session_state.rol = "Admin"
        st.rerun()
      else:
        st.error(
            "Contraseña incorrecta. Verifique sus credenciales de acceso."
        )
else:
  st.sidebar.title("Panel de Control")
  st.sidebar.write(f"**Rol activo:** {st.session_state.rol}")
  if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.rol = None
    st.rerun()

  st.title("🏢 Optimum Home - Consulta de Base de Datos Texas")

  if st.session_state.rol == "Agente":
    st.info(
        "Modo Agente Activo: Utilice los filtros para consultar la"
        " disponibilidad y datos de los prospectos en tiempo real."
    )

    col1, col2 = st.columns(2)
    with col1:
      filtro_ciudad = st.text_input("Filtrar por Ciudad (Ej: Houston, Katy):")
    with col2:
      filtro_busqueda = st.text_input(
          "Buscar por Dirección, Nombre o Teléfono:"
      )

    df_filtrado = st.session_state.df.copy()

    if filtro_ciudad:
      df_filtrado = df_filtrado[
          df_filtrado["city"]
          .astype(str)
          .str.contains(filtro_ciudad, case=False, na=False)
      ]

    if filtro_busqueda:
      mask = (
          df_filtrado.astype(str)
          .apply(
              lambda col: col.str.contains(
                  filtro_busqueda, case=False, na=False
              )
          )
          .any(axis=1)
      )
      df_filtrado = df_filtrado[mask]

    st.write(f"**Registros encontrados:** {len(df_filtrado)}")
    st.dataframe(df_filtrado, use_container_width=True)

  elif st.session_state.rol == "Admin":
    st.success(
        "Modo Administrador: Acceso total de gestión y actualización de datos."
    )

    tab1, tab2 = st.tabs(["🔍 Consultar y Exportar", "➕ Agregar Nuevo Registro"])

    with tab1:
      filtro_admin = st.text_input("Búsqueda general (Admin):")
      df_admin = st.session_state.df.copy()
      if filtro_admin:
        mask = (
            df_admin.astype(str)
            .apply(
                lambda col: col.str.contains(
                    filtro_admin, case=False, na=False
                )
            )
            .any(axis=1)
        )
        df_admin = df_admin[mask]

      st.dataframe(df_admin, use_container_width=True)

      csv_export = df_admin.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="📥 Descargar Base Depurada (Solo Admin)",
          data=csv_export,
          file_name="Master_Texas_Actualizado.csv",
          mime="text/csv",
      )

    with tab2:
      st.subheader("Incorporar nuevo prospecto a la base de datos central")
      with st.form("form_nuevo"):
        f_name = st.text_input("Nombre")
        l_name = st.text_input("Apellido")
        city_in = st.text_input("Ciudad")
        addr_in = st.text_input("Dirección")
        phone_in = st.text_input("Teléfono")
        email_in = st.text_input("Correo electrónico")

        guardar_btn = st.form_submit_button("Guardar en el Sistema")

        if guardar_btn:
          nuevo_registro = {
              "first_name": f_name,
              "last_name": l_name,
              "city": city_in,
              "address1": addr_in,
              "email": email_in,
              "clean_phone": phone_in,
          }
          nuevo_df = pd.DataFrame([nuevo_registro])
          st.session_state.df = pd.concat(
              [st.session_state.df, nuevo_df], ignore_index=True
          )
          st.success("¡El registro se ha incorporado exitosamente!")
