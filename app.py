import streamlit as st
import supabase
import uuid
import time
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO

# Initialize Supabase client using secrets
supabase_client = supabase.create_client(st.secrets["secrets"]["NEXT_PUBLIC_SUPABASE_URL"], st.secrets["secrets"]["NEXT_PUBLIC_SUPABASE_ANON_KEY"])

# Situations list
situations = [
    "Esta es una situación de prueba, utiliza el deslizador para elegir cuál de los 2 agentes preferirías que te orientara/te diera un consejo/te ayudara en cada una de las siguientes situaciones",
    "¿Qué hago si quiero saber a quién contarle primero que voy a ser papá o mamá?",
    "¿Qué hago si no sé cómo avisarles a mis padres que tengo malas calificaciones?",
    "¿Qué hago si quiero cuidar bien a un bebé?",
    "¿Qué hago cuando necesito saber si está bien o no hacer trampa en un juego o negocio?",
    "¿Qué hago si veo a alguien copiando en un examen y no estoy seguro si debo avisarle al profesor?",
    "¿Qué hago si alguien se burla de mí?",
    "¿Qué hago si me siento triste y quiero saber si debería hablar con alguien de eso?",
    "¿Qué hago para saber si mis ideas de alguien son correctas o no?",
    "¿Qué hago si quiero saber si los gatos ven mejor que los perros en la oscuridad?",
    "¿Qué hago si no puedo dejar de hacer algo que creo me hace daño?",
    "¿Qué hago cuando necesito saber si es bueno pedir un consejo al momento de tomar decisiones importantes?",
    "¿Qué hago si quiero saber si es bueno o malo lo que pide una religión?",
    "¿Qué hago para saber qué hacer si alguien me ha golpeado y me duele?",
    "¿Qué hago si quiero saber cuál es el mejor jugador de fútbol del mundo?",
    "¿Qué hago si quiero saber si soy o no físicamente atractivo/a?",
    "¿Qué hago si quiero saber si debo decir que algún familiar o alguien cercano se comporta mal conmigo?",
    "¿Qué hago si me siento mal porque creo que le he hecho daño a alguien?",
    "¿Qué hago si quiero sembrar un árbol de mango en casa?",
    "¿Qué hago si quiero saber cuál es la mejor época para viajar a otro país?",
    "¿Qué hago si necesito saber si estar enamorado es bueno o no?",
    "¿Qué hago si quiero saber cuál es la mejor comida del mundo?",
    "¿Qué hago si me invitan a consumir drogas o alcohol?",
    "¿Qué hago si quiero saber el año exacto en que inventaron el bombillo?",
    "¿Qué hago si quiero saber cuál es el nombre exacto de Shakira?",
    "¿Qué hago si quiero saber si Dios existe o no?",
    "¿Qué hago si quiero preparar un pastel de chocolate?",
    "¿Qué hago si quiero vengarme de alguien?",
    "¿Qué hago si quiero saber cuál es el mejor momento del año para ir a la playa?",
    "¿Qué hago si quiero saber qué sentido tiene mi vida?",
    "¿Qué hago si me siento alegre y quiero saber si debería hablar con alguien de eso?"
]

# Function to get current situation
def get_current_situation(situation_index):
    return situations[situation_index] if situation_index < len(situations) else "FINISHED"

# Function to save questionnaire data to Supabase
def save_questionnaire_data(data):
    try:
        response = supabase_client.table("respuestas").insert({
            "consentimiento": data["consentimiento"],
            "name": data["data.name"],
            "birthdate": data["data.birthdate"],
            "devices": data["data.devices"],
            "tech_time": data["data.tech"],
            "socio_stratum": data["data.socioStratum"],
            "ai_knowledge": data["ai.knowledge"],
            "ai_trust_epistemic": data["ai.trust.epistemic"],
            "ai_trust_social": data["ai.trust.social"],
            "human_trust_epistemic": data["human.trust.epistemic"],
            "human_trust_social": data["human.trust.social"]
        }).execute()
        return response.data[0]["id"]
    except Exception as e:
        st.error(f"Error saving questionnaire data: {str(e)}")
        return None

# Function to save situation response to Supabase
def save_situation_response(participant_id, situation_index, response_time, slider_value):
    result = f"{slider_value} - {response_time}"
    supabase_client.table("situationresponses").insert({
        "participant_id": participant_id,
        "situation_index": situation_index,
        "response": result
    }).execute()

# Initialize session state
if "screen" not in st.session_state:
    st.session_state.screen = "questionnaire"
    st.session_state.situation_index = 0
    st.session_state.participant_id = None
    st.session_state.start_time = None
    st.session_state.button_clicked = False

# CSS for styling
st.markdown("""
    <style>
    .main {
        padding: 20px;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        margin-top: 20px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stSlider {
        width: 60%;
        margin: 20px auto;
    }
    .slider-label {
        font-weight: bold;
        display: inline-block;
        width: 50px;
        text-align: center;
        vertical-align: middle;
        line-height: 40px; /* Match slider height */
    }
    .situation-text {
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .loading-button {
        background-color: grey !important;
        color: white !important;
        cursor: not-allowed !important;
    }
    .image-container img {
        width: 100px;
        height: auto;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Main app logic
def main():
    if st.session_state.screen == "questionnaire":
        st.header("Encuesta de Toma de Decisiones")
        st.markdown("""
            Muchas gracias por participar en el proyecto del Doctorado en Psicología acerca de decisiones emocionales y morales e Inteligencia Artificial. El presente cuestionario busca conocer sus datos sociodemográficos y forma de contacto, con el fin de generar un perfil completo de los participantes en el estudio. Agradecemos diligenciar todo el cuestionario. Por favor responda con la mayor fidelidad posible a su situación y tómese el tiempo que necesite para hacerlo.

            El cuestionario fue diseñado para una duración aproximada de quince minutos de realización con el objetivo de tener múltiples variables que permitan un análisis completo en conjunto con una prueba psicométrica que será aplicada a cada participante con el fin de identificar sus decisiones ante preguntas específicas.

            Esta actividad se realiza como marco de un ejercicio académico con el fin de generar una evaluación y relación entre variables y los niveles de toma de decisión de los participantes según situaciones específicas.

            De nuevo muchas gracias por la información brindada, es de gran utilidad para mejorar el conocimiento sobre posibles efectos del aprendizaje tecnológico en los participantes. Si desea conocer más información al respecto o desea contactar a el investigador principal, no dude en comunicarse a los siguientes datos de contacto:

            **Johan Sebastián Galindez Acosta**  
            Celular: +57 3103817021  
            Correo: johangalac@unisabana.edu.co

            Toda la información aquí consolidada se manejará bajo principios de confidencialidad y anonimato. Los datos se codificarán para que sea imposible el manejo por parte de terceros ajenos al estudio. Si usted está de acuerdo con participar por favor diligencie la encuesta adjunta. Recuerde que en cualquier momento puede decidir si continúa o se retira de participar en el estudio sin ningún tipo de sanción o perjuicio.
        """)

        consent = st.selectbox("¿Acepta participar en la recolección de datos anteriormente descrita?", ["Sí", "No"], key="consent")
        st.subheader("Por favor complete el siguiente cuestionario")
        name = st.text_input("Nombres y apellidos", key="name")
        birthdate = st.date_input("Fecha de nacimiento", min_value=datetime(1900, 1, 1), key="birthdate")
        
        devices_options = [
            "Smartphones", "Computadoras portátiles", "Tablet", "Smart TV", "Consolas de videojuegos",
            "Asistentes de voz", "Dispositivos de streaming", "Altavoces Bluetooth", "Cámaras de seguridad inteligentes",
            "Wearables", "Impresoras multifunción", "Dispositivos de realidad virtual (VR)", "Dispositivos de cocina inteligente",
            "Cámaras digitales y videocámaras", "Dispositivos de domótica", "Auriculares inalámbricos"
        ]
        devices = st.multiselect("¿Qué dispositivos tecnológicos tienen en casa? (Seleccione todos los que correspondan)", devices_options, key="devices")
        
        tech_time = st.selectbox("¿Cuánto tiempo suele pasar utilizando tecnología en el día?", 
                                 ["1 a 2 horas", "3 a 4 horas", "5 a 7 horas", "8 horas o más", "No sabe"], key="tech_time")
        socioeconomic = st.selectbox("Estrato socioeconómico de su vivienda", 
                                    ["1", "2", "3", "4", "5", "6", "7", "Sin estrato"], key="socioeconomic")
        
        st.markdown("Responda las siguientes preguntas teniendo en cuenta que 1 es poco o nada y 5 es mucho")
        ai_knowledge = st.selectbox("¿Qué tanto conocimiento tienes acerca de Inteligencia Artificial?", [1, 2, 3, 4, 5], key="ai_knowledge")
        ai_trust_epistemic = st.selectbox("¿Qué tanto confías en que la Inteligencia Artificial puede darte buenas respuestas cuando se trata de información o conocimientos (como explicarte algo, ayudarte a estudiar o resolver un problema)?", 
                                          [1, 2, 3, 4, 5], key="ai_trust_epistemic")
        ai_trust_social = st.selectbox("¿Qué tanto confías en que la Inteligencia Artificial puede ayudarte en situaciones personales o emocionales (como darte consejos, apoyarte o entender cómo te sientes)?", 
                                       [1, 2, 3, 4, 5], key="ai_trust_social")
        human_trust_epistemic = st.selectbox("¿Qué tanto confías en que otras personas (amigos, profesores, profesionales) pueden darte buenas respuestas cuando se trata de información o conocimientos (como explicarte algo, ayudarte a estudiar o resolver un problema)?", 
                                             [1, 2, 3, 4, 5], key="human_trust_epistemic")
        human_trust_social = st.selectbox("¿Qué tanto confías en que otras personas (amigos, profesores, profesionales) pueden ayudarte en situaciones personales o emocionales (como darte consejos, apoyarte o entender cómo te sientes)?", 
                                          [1, 2, 3, 4, 5], key="human_trust_social")

        if not st.session_state.button_clicked:
            if st.button("Siguiente", key="questionnaire_submit"):
                st.session_state.button_clicked = True
                if consent == "No":
                    st.error("Debe aceptar participar para continuar.")
                    st.session_state.button_clicked = False
                    return
                if not name or not birthdate:
                    st.error("Por favor complete todos los campos obligatorios.")
                    st.session_state.button_clicked = False
                    return
                data = {
                    "consentimiento": consent,
                    "data.name": name,
                    "data.birthdate": birthdate.strftime("%Y-%m-%d"),
                    "data.devices": len(devices),
                    "data.tech": tech_time,
                    "data.socioStratum": socioeconomic,
                    "ai.knowledge": ai_knowledge,
                    "ai.trust.epistemic": ai_trust_epistemic,
                    "ai.trust.social": ai_trust_social,
                    "human.trust.epistemic": human_trust_epistemic,
                    "human.trust.social": human_trust_social
                }
                participant_id = save_questionnaire_data(data)
                if participant_id:
                    st.session_state.participant_id = participant_id
                    st.session_state.screen = "screen_1"
                    st.session_state.button_clicked = False
                    st.rerun()
        else:
            st.markdown('<button class="loading-button" disabled>Cargando</button>', unsafe_allow_html=True)

    elif st.session_state.screen == "screen_1":
        st.header("Estos son los agentes que puedes seleccionar para que te orienten en las próximas situaciones")
        response = requests.get("https://raw.githubusercontent.com/SebastianFullStack/images/main/IA.png")
        img = Image.open(BytesIO(response.content))
        st.image(img, caption="Imagen IA", use_column_width=True)
        if not st.session_state.button_clicked:
            if st.button("Siguiente", key="screen_1_next"):
                st.session_state.button_clicked = True
                st.session_state.screen = "screen_2"
                st.session_state.button_clicked = False
                st.rerun()
        else:
            st.markdown('<button class="loading-button" disabled>Cargando</button>', unsafe_allow_html=True)

    elif st.session_state.screen == "screen_2":
        st.header("Estos son los agentes que puedes seleccionar para que te orienten en las próximas situaciones")
        response = requests.get("https://raw.githubusercontent.com/SebastianFullStack/images/main/Humano.png")
        img = Image.open(BytesIO(response.content))
        st.image(img, caption="Imagen Humano", use_column_width=True)
        if not st.session_state.button_clicked:
            if st.button("Siguiente", key="screen_2_next"):
                st.session_state.button_clicked = True
                st.session_state.screen = "screen_3"
                st.session_state.start_time = time.time()
                st.session_state.button_clicked = False
                st.rerun()
        else:
            st.markdown('<button class="loading-button" disabled>Cargando</button>', unsafe_allow_html=True)

    elif st.session_state.screen == "screen_3":
        situation = get_current_situation(st.session_state.situation_index)
        if situation == "FINISHED":
            st.markdown("<h3>¡Gracias por participar! Tus respuestas han sido guardadas, puedes cerrar esta página.</h3>", unsafe_allow_html=True)
            return
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            response = requests.get("https://raw.githubusercontent.com/SebastianFullStack/images/main/IA.png")
            img_ai = Image.open(BytesIO(response.content))
            st.image(img_ai, caption="Imagen IA", use_column_width=False)
            st.markdown("<span class='slider-label'>IA</span>", unsafe_allow_html=True)
        with col3:
            response = requests.get("https://raw.githubusercontent.com/SebastianFullStack/images/main/Humano.png")
            img_human = Image.open(BytesIO(response.content))
            st.image(img_human, caption="Imagen Humano", use_column_width=False)
            st.markdown("<span class='slider-label'>Humano</span>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div class='situation-text'>{situation}</div>", unsafe_allow_html=True)
            slider_col1, slider_col2, slider_col3 = st.columns([1, 3, 1])
            with slider_col2:
                slider_value = st.slider("", 0, 100, 50, key="decision_slider")
        
        if not st.session_state.button_clicked:
            if st.button("Siguiente", key="situation_submit"):
                st.session_state.button_clicked = True
                end_time = time.time()
                response_time = end_time - st.session_state.start_time
                save_situation_response(st.session_state.participant_id, st.session_state.situation_index, response_time, slider_value)
                st.session_state.situation_index += 1
                st.session_state.start_time = time.time()
                st.session_state.button_clicked = False
                st.rerun()
        else:
            st.markdown('<button class="loading-button" disabled>Cargando</button>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
