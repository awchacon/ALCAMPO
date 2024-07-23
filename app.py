import streamlit as st
import requests
import json
import base64
from PIL import Image

#### streamlit run .\app.py

# Configuración de la página
st.set_page_config(page_title="Mi ALCAMPO", page_icon="static/images/logo.png", layout="centered")

# Cargar el archivo CSS
def load_css():
    with open("static/styles/styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Título principal
st.markdown("<h1 class='center-text'>ALCAMPO</h1>", unsafe_allow_html=True)
st.write("")

# Menú de opciones
selected = st.selectbox(
    "Menú",
    ["Inicio", "Consultas", "Analytics"]
)

# Función HomePage
def HomePage():
    file_ = open("static/images/logo.png", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<div class="centered-content"><img src="data:image/gif;base64,{data_url}" alt="main gif" class="centered-image"></div>',
        unsafe_allow_html=True,
    )
    st.markdown("<h2 class='center-text'>¡Bienvenidos a AppALCAMPO!</h2>", unsafe_allow_html=True)
    st.write("Disfruta de nuestras funcionalidades y características (Consultas y Looker).")

# Función para generar consultas
def mostrar_consultas():
    st.markdown("<div class='container centered-content'><div class='contenido'>", unsafe_allow_html=True)
    st.title('Generador de Consultas SQL')

    # Recuadros para ingresar el nombre y la descripción
    name = st.text_input('Nombre').upper()  # Convertir el nombre a mayúsculas automáticamente
    description = st.text_input('Descripción')

    # Campo para ingresar la consulta desde la cláusula FROM
    from_clause = st.text_area('Ingrese la parte de la consulta SQL desde FROM', height=200)

    # Concatenar la parte fija con la entrada del usuario
    sql_query = f'SELECT generate_uuid() AS id_alerta, unique_transaction_id AS unique_transaction_id, store_number AS numero_tienda, transaction_datetime AS fecha, terminal AS numero_caja, operator_number AS numero_de_cajera, importe_ticket AS importe_ticket, null AS articulo, null AS importe_articulo, "{name}" AS tipo_alerta FROM {from_clause}'

    st.markdown('Consulta completa generada')
    st.code(sql_query, language='sql')

    # Botón para aceptar
    if st.button('Aceptar'):
        # Validar entradas
        if not from_clause:
            st.error('El campo de la parte de la consulta SQL desde FROM es obligatorio.')
        else:
            # st.write('Consulta generada:')
            # st.code(sql_query, language='sql')

            # Crear el payload para la solicitud POST
            payload = {
                "name": name,
                "description": description,
                "code": sql_query
            }

            try:
                with st.spinner('Enviando consulta...'):
                    # Realizar la solicitud POST
                    response = requests.post(
                        'https://europe-southwest1-firm-star-429208-k0.cloudfunctions.net/alert_validation_v1',
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(payload)  # Convertir el diccionario a JSON
                    )
                    
                    # Mostrar la respuesta de la solicitud
                    if response.status_code == 200:
                        st.success('Consulta enviada exitosamente!')
                        st.write('Respuesta del servidor:')
                        st.json(response.json())  # Muestra el contenido JSON de la respuesta
                    elif response.status_code == 400:
                        st.error('Error al enviar la consulta: 400 (Bad Request)')
                        try:
                            st.write('Respuesta del servidor:')
                            st.json(response.json())  # Muestra el contenido JSON de la respuesta en caso de error
                        except json.JSONDecodeError:
                            st.write(response.text)  # Muestra el texto de la respuesta si no es JSON
                    else:
                        st.error(f'Error al enviar la consulta: {response.status_code}')
                        try:
                            st.write('Respuesta del servidor:')
                            st.json(response.json())  # Muestra el contenido JSON de la respuesta en caso de error
                        except json.JSONDecodeError:
                            st.write(response.text)  # Muestra el texto de la respuesta si no es JSON
            except requests.RequestException as e:
                st.error(f'Error al enviar la consulta: {e}')
    st.markdown("</div></div>", unsafe_allow_html=True)

# Función para mostrar la página de looker
def mostrar_looker():
    st.markdown("<div class='container centered-content'><div class='contenido'>", unsafe_allow_html=True)
    st.title("Looker")
    #st.write("Aquí se mostrará el contenido de Looker")

    # Enlace del iframe de Looker Studio
    looker_iframe = """
    <iframe width="100%" height="550" src="https://lookerstudio.google.com/embed/reporting/c5480342-44a1-4f38-bb34-d2d037598c3c/page/p_3dwuhm857c" frameborder="0" style="border:0" allowfullscreen></iframe>
    """
    st.markdown(looker_iframe, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# Navegación entre las opciones del menú
if selected == "Inicio":
    HomePage()
elif selected == "Consultas":
    mostrar_consultas()
elif selected == "Analytics":
    mostrar_looker()
