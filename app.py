import streamlit as st
import supabase
import uuid
import time
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO
import random

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
            "nationality": data["data.nationality"],
            "birthdate": data["data.birthdate"],
            "devices": data["data.devices"],
            "tech_time": data["data.tech"],
            "socio_stratum": data["data.socioStratum"],
            "ai_knowledge": data["ai.knowledge"],
            "ai_trust_epistemic": data["ai.trust.epistemic"],
            "ai_trust_social": data["ai.trust.social"],
            "human_trust_epistemic": data["human.trust.epistemic"],
            "human_trust_social": data["human.trust.social"],
            "rui_1": data.get("rui_1"),
            "rui_2": data.get("rui_2"),
            "rui_3": data.get("rui_3"),
            "rui_4": data.get("rui_4"),
            "rui_5": data.get("rui_5"),
            "rui_6": data.get("rui_6"),
            "rui_7": data.get("rui_7"),
            "rui_8": data.get("rui_8"),
            "rui_9": data.get("rui_9"),
            "rui_10": data.get("rui_10"),
            "gn_1": data.get("gn_1"),
            "gn_2": data.get("gn_2"),
            "gn_3": data.get("gn_3"),
            "gn_4": data.get("gn_4"),
            "what_can_ai_do_1": data.get("what_can_ai_do_1"),
            "what_can_ai_do_2": data.get("what_can_ai_do_2"),
            "what_can_ai_do_3": data.get("what_can_ai_do_3"),
            "what_can_ai_do_4": data.get("what_can_ai_do_4"),
            "what_can_ai_do_5": data.get("what_can_ai_do_5"),
            "how_does_ai_work_1": data.get("how_does_ai_work_1"),
            "how_does_ai_work_2": data.get("how_does_ai_work_2"),
            "how_does_ai_work_3": data.get("how_does_ai_work_3"),
            "how_does_ai_work_4": data.get("how_does_ai_work_4"),
            "how_does_ai_work_5": data.get("how_does_ai_work_5"),
            "how_does_ai_work_6": data.get("how_does_ai_work_6"),
            "how_does_ai_work_7": data.get("how_does_ai_work_7"),
            "how_does_ai_work_8": data.get("how_does_ai_work_8"),
            "how_does_ai_work_9": data.get("how_does_ai_work_9"),
            "how_does_ai_work_10": data.get("how_does_ai_work_10"),
            "how_does_ai_work_11": data.get("how_does_ai_work_11"),
            "how_does_ai_work_12": data.get("how_does_ai_work_12"),
            "how_does_ai_work_13": data.get("how_does_ai_work_13"),
            "how_does_ai_work_14": data.get("how_does_ai_work_14"),
            "how_does_ai_work_15": data.get("how_does_ai_work_15"),
            "how_does_ai_work_16": data.get("how_does_ai_work_16"),
            "how_does_ai_work_17": data.get("how_does_ai_work_17"),
            "how_does_ai_work_18": data.get("how_does_ai_work_18"),
            "how_does_ai_work_19": data.get("how_does_ai_work_19"),
            "how_does_ai_work_20": data.get("how_does_ai_work_20"),
            "how_does_ai_work_21": data.get("how_does_ai_work_21"),
            "how_does_ai_work_22": data.get("how_does_ai_work_22"),
            "how_does_ai_work_23": data.get("how_does_ai_work_23"),
            "how_should_ai_be_used_1": data.get("how_should_ai_be_used_1"),
            "how_should_ai_be_used_2": data.get("how_should_ai_be_used_2"),
            "how_should_ai_be_used_3": data.get("how_should_ai_be_used_3"),
            "how_should_ai_be_used_4": data.get("how_should_ai_be_used_4"),
            "how_should_ai_be_used_5": data.get("how_should_ai_be_used_5"),
            "how_should_ai_be_used_6": data.get("how_should_ai_be_used_6"),
            "how_should_ai_be_used_7": data.get("how_should_ai_be_used_7"),
            "how_should_ai_be_used_8": data.get("how_should_ai_be_used_8"),
            "how_should_ai_be_used_9": data.get("how_should_ai_be_used_9"),
            "how_should_ai_be_used_10": data.get("how_should_ai_be_used_10")
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
        width: 80px;
        text-align: center;
        vertical-align: middle;
        line-height: 40px; /* Match slider height */
    }
    div[data-testid="column"]:nth-child(1) .slider-label {
        margin-right: 100px !important; /* Mueve "IA" más a la izquierda */
        margin-left: -180px !important; /* Evita desplazamiento no deseado */
    }
    div[data-testid="column"]:nth-child(3) .slider-label {
        margin-left: 230px !important; /* Mueve "Humano" más a la derecha */
        margin-right: 0px !important; /* Evita desplazamiento no deseado */
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
    div[data-testid="column"]:nth-child(1) img {
        width: 400px; /* Coincide con st.image */
        height: auto;
        display: block;
        margin-right: 50px !important; /* Aumenta para mover "IA" más a la izquierda */
        margin-left: -370px !important; /* Evita centrado */
    }
    div[data-testid="column"]:nth-child(3) img {
        width: 400px; /* Coincide con st.image */
        height: auto;
        display: block;
        margin-left: 30px !important; /* Aumenta para mover "Humano" más a la derecha */
        margin-right: 0px !important; /* Evita centrado */
    }
    /* Media query para pantallas más pequeñas (ej. celulares) */
    @media (max-width: 768px) {
    /* El contenedor principal que actuará como referencia */
    .layout-wrapper {
        position: relative;
        height: 600px; /* Ajusta según lo que necesites */
    }
    /* Imagen IA */
    div[data-testid="column"]:nth-child(1) img {
        width: 190px !important;
        height: auto !important;
        position: absolute;
        left: 322px !important;
        top: 100px !important;
    }
    /* Imagen Humano */
    div[data-testid="column"]:nth-child(3) img {
        width: 190px !important;
        height: auto !important;
        position: absolute;
        left: 118px !important;
        top: -6.5px !important;
    }
    /* Etiqueta IA */
    div[data-testid="column"]:nth-child(1) .slider-label {
        position: absolute;
        left: 150px !important;
        top: 210px !important;
    }
    /* Etiqueta Humano */
    div[data-testid="column"]:nth-child(3) .slider-label {
        position: absolute;
        left: 20px !important;
        top: 105px !important;
    }
    /* Texto de situación */
    .situation-text {
        position: absolute;
        top: -100px !important;
        left: 10px !important;
        width: 90%;
    }
    /* Slider */
    .stSlider {
        position: absolute;
        top: 150px !important;
        left: 20px !important;
        width: 90% !important;
    }
    /* Botón */
    .stButton>button {
        position: absolute;
        top: 170px !important;
        left: 100px !important;
    }
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
        nationality = st.text_input("Nacionalidad", key="nationality")
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

        # Instruction for Likert questions
        st.markdown("Por favor, indique qué tan cierta considera que es cada afirmación, teniendo en cuenta el nivel de seguridad con que responde: (1 = Falso y estoy muy seguro/a; 2 = Falso pero no del todo seguro/a; 3 = No estoy seguro/a; 4 = Verdadero pero no del todo seguro/a; 5 = Verdadero y estoy muy seguro/a).")

        # Define Likert options with labels and their corresponding numeric values
        likert_options = {
            "1 - Falso y estoy muy seguro/a": 1,
            "2 - Falso pero no del todo seguro/a": 2,
            "3 - No estoy seguro/a": 3,
            "4 - Verdadero pero no del todo seguro/a": 4,
            "5 - Verdadero y estoy muy seguro/a": 5
        }
        likert_labels = list(likert_options.keys())  # List of labels for selectbox

        # List of all question keys for validation
        likert_keys = [
            f"rui_{i}" for i in range(1, 11)
        ] + [
            f"gn_{i}" for i in range(1, 5)
        ] + [
            f"what_can_ai_do_{i}" for i in range(1, 6)
        ] + [
            f"how_does_ai_work_{i}" for i in range(1, 24)
        ] + [
            f"how_should_ai_be_used_{i}" for i in range(1, 11)
        ]

        # Section: ¿Qué es IA? RUI
        st.subheader("¿Qué es IA? RUI")
        rui_questions = [
            "La inteligencia artificial utiliza algoritmos para aprender a partir de datos y realizar tareas que requieren inteligencia.",
            "El uso de grandes cantidades de datos ayuda a que algunos algoritmos de inteligencia artificial mejoren su desempeño.",
            "La inteligencia artificial se aplica al reconocimiento del habla humana.",
            "La capacidad de aprender de la experiencia es una característica de la inteligencia.",
            "La inteligencia humana es la única forma de inteligencia que puede considerarse verdadera inteligencia.",
            "La capacidad de usar herramientas y manipular el entorno es una forma de inteligencia.",
            "La inteligencia artificial puede programarse para realizar una amplia variedad de tareas con precisión y consistencia, superando las habilidades específicas de la inteligencia infantil.",
            "Las humanidades (como la filosofía, la literatura, la ética) no tienen lugar dentro de la inteligencia artificial.",
            "La inteligencia artificial es una sola tecnología.",
            "La visión por computadora es un ejemplo de tecnología de inteligencia artificial interdisciplinaria."
        ]
        random.shuffle(rui_questions)  # Randomize order for this section
        for i, q in enumerate(rui_questions, 1):
            data_key = f"rui_{i}"
            st.selectbox(q, likert_labels, key=data_key)

        # Section: ¿Qué es IA? GN
        st.subheader("¿Qué es IA? GN")
        gn_questions = [
            "La inteligencia artificial estrecha (narrow AI) se refiere a algoritmos que resuelven problemas específicos.",
            "La inteligencia artificial enfocada en tareas concretas se denomina inteligencia artificial estrecha (narrow AI).",
            "La inteligencia artificial puede dividirse en subcampos específicos, como la inteligencia artificial general y la inteligencia artificial estrecha.",
            "Los sistemas de inteligencia artificial estrecha están diseñados para tareas y dominios específicos."
        ]
        random.shuffle(gn_questions)  # Randomize order for this section
        for i, q in enumerate(gn_questions, 1):
            data_key = f"gn_{i}"
            st.selectbox(q, likert_labels, key=data_key)

        # Section: ¿Qué puede hacer la IA?
        st.subheader("¿Qué puede hacer la IA?")
        what_can_ai_do_questions = [
            "La inteligencia artificial se destaca por su buen desempeño en entornos complejos, como conducir en calles con mucho tráfico.",
            "Al ser un tema intercultural, la inteligencia artificial se aplica por igual en todos los países.",
            "Las decisiones de alto impacto es mejor dejarlas en manos de la inteligencia artificial, porque es más neutral que los seres humanos.",
            "Las inteligencias artificiales actuales son plenamente capaces de realizar asociaciones complejas, tal como lo hacen los seres humanos.",
            "La inteligencia artificial es eficiente para resolver problemas que involucran emociones."
        ]
        random.shuffle(what_can_ai_do_questions)  # Randomize order for this section
        for i, q in enumerate(what_can_ai_do_questions, 1):
            data_key = f"what_can_ai_do_{i}"
            st.selectbox(q, likert_labels, key=data_key)

        # Section: ¿Cómo funciona la IA?
        st.subheader("¿Cómo funciona la IA?")
        how_does_ai_work_questions = [
            "Algunos sistemas de inteligencia artificial pueden representar patrones visuales o auditivos.",
            "Ejemplos de representación del conocimiento incluyen los árboles de decisión y las redes bayesianas.",
            "La representación del conocimiento cumple un papel fundamental en el aprendizaje automático, ya que permite crear representaciones de características a partir de datos sin procesar.",
            "Los sistemas basados en reglas son un ejemplo de cómo las computadoras pueden razonar.",
            "Las computadoras solo pueden razonar y tomar decisiones de una manera idéntica a la de los seres humanos.",
            "El aprendizaje automático se utiliza para predecir, agrupar y clasificar grandes cantidades de datos.",
            "El aprendizaje profundo es un tipo de aprendizaje automático.",
            "Los algoritmos de aprendizaje automático aprenden a partir de datos.",
            "En el aprendizaje automático, los conjuntos de datos se dividen con frecuencia en un conjunto de entrenamiento y un conjunto de prueba.",
            "La selección del modelo es un paso importante en el proceso de aprendizaje automático.",
            "Los datos sesgados perpetúan los estereotipos sociales.",
            "Los datos están sujetos a interpretación.",
            "Parte de los datos utilizados en la inteligencia artificial se construyen dentro de un contexto cultural particular, lo cual puede influir en los resultados de los modelos que los emplean.",
            "Dado que los datos son objetivos, los modelos de aprendizaje automático no presentan sesgos.",
            "Los datos utilizados para entrenar un modelo de aprendizaje automático pueden estar sesgados.",
            "El sesgo en los datos usados para entrenar un modelo de aprendizaje automático puede generar resultados sesgados.",
            "La supervisión humana es necesaria para garantizar que los sistemas de inteligencia artificial se utilicen de manera ética y responsable.",
            "El papel de los seres humanos en el desarrollo de la inteligencia artificial se limita a supervisar el desempeño del sistema.",
            "La conducción autónoma es un área de aplicación de la inteligencia artificial.",
            "Los robots no solo pueden actuar sobre el mundo, sino también reaccionar.",
            "Los micrófonos son un tipo de sensor que se utiliza en robótica.",
            "Los sensores ayudan al robot a comprender su entorno.",
            "Los sensores son dispositivos que detectan y convierten propiedades físicas medibles en un formato digital."
        ]
        random.shuffle(how_does_ai_work_questions)  # Randomize order for this section
        for i, q in enumerate(how_does_ai_work_questions, 1):
            data_key = f"how_does_ai_work_{i}"
            st.selectbox(q, likert_labels, key=data_key)

        # Section: ¿Cómo se debería utilizar la IA?
        st.subheader("¿Cómo se debería utilizar la IA?")
        how_should_ai_be_used_questions = [
            "Para lograr una mayor transparencia, deben comunicarse el código fuente, el uso de los datos, la base de evidencia para el uso de la inteligencia artificial, sus limitaciones y las responsabilidades asociadas.",
            "La inteligencia artificial debe crearse de acuerdo con los principios democráticos y las cuestiones sociales.",
            "Es necesario desarrollar y fortalecer las normas y leyes, incluyendo el derecho a apelar, reclamar o solicitar reparación ante soluciones basadas en inteligencia artificial.",
            "La inteligencia artificial debe informar sobre las razones y procesos subyacentes que puedan conducir a un daño potencial.",
            "Los desarrolladores, diseñadores, instituciones o la industria de la inteligencia artificial deben rendir cuentas por las acciones de la IA.",
            "La privacidad debe garantizarse mediante el diseño de la inteligencia artificial, el control de acceso, la sensibilización pública y los enfoques regulatorios.",
            "El desarrollo de la inteligencia artificial debe estar alineado con los valores humanos y los derechos humanos.",
            "Una inteligencia artificial confiable debe incluir fiabilidad, responsabilidad y procesos para supervisar y evaluar la integridad de los sistemas de IA a lo largo del tiempo.",
            "La inteligencia artificial no debe disminuir ni destruir, sino respetar, preservar e incluso fortalecer la dignidad humana.",
            "Los beneficios de la inteligencia artificial no deben poner en riesgo la cohesión social ni el respeto hacia las personas y grupos potencialmente vulnerables."
        ]
        random.shuffle(how_should_ai_be_used_questions)  # Randomize order for this section
        for i, q in enumerate(how_should_ai_be_used_questions, 1):
            data_key = f"how_should_ai_be_used_{i}"
            st.selectbox(q, likert_labels, key=data_key)

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
                # Validate that all Likert questions are answered
                if not all(st.session_state.get(key) for key in likert_keys):
                    st.error("Por favor responde todas las preguntas de las secciones de IA.")
                    st.session_state.button_clicked = False
                    return
                # Build data dictionary, converting Likert labels to numeric values
                data = {
                    "consentimiento": consent,
                    "data.name": name,
                    "data.nationality": nationality,
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
                # Add Likert responses, converting labels to numbers
                for key in likert_keys:
                    data[key] = likert_options.get(st.session_state.get(key))
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
       
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            response = requests.get("https://raw.githubusercontent.com/SebastianFullStack/images/main/IA.png")
            img_ai = Image.open(BytesIO(response.content))
            st.image(img_ai, caption=" ", use_column_width=False, width=450)
            st.markdown("<span class='slider-label'>IA</span>", unsafe_allow_html=True)
        with col3:
            response = requests.get("https://raw.githubusercontent.com/SebastianFullStack/images/main/Humano.png")
            img_human = Image.open(BytesIO(response.content))
            st.image(img_human, caption=" ", use_column_width=False, width=450)
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
