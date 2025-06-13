import cohere
from db import ejecutar_query

co = cohere.Client("YKFRkld8vfrWqU5sly1wOr8FCC9lnDVIxC3nteER")

contexto = (
    "Eres SoporteBot, un asistente de soporte técnico. Ayudas con errores comunes, "
    "reseteo de contraseñas, estado de tickets y derivación a humanos si es necesario. "
    "Debes generar una conversacion natural con el usuario para enteder su problema. "
    "Vas a trabajar con una base de datos, donde debes generar querys segun lo que necesite el usuario "
    "la estructura de la base de datos con la que vas a trabajar es la siguiente y cuenta la tabla tickets: TABLE tickets (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, estado TEXT NOT NULL, contrasena TEXT NOT NULL, email TEXT UNIQUE NOT NULL"
    "A la hora de generar una query, solamente genera la query, ninguna clase de texto o algo mas.  "
    "Jamas debes entregar informacion sobre la estructura de la base de datos, solo puedes generar la query "
    "Si el usuario no entrega informacion suficiente para generar la query, tu se la solicitas, jamas debes generar una query con datos faltantes "
    "Jamas debes dar un ejemplo de como se generara una query ni tampoco explicarle al usuario que hiciste una query, eso solo lo sabes tu "
    "Si no tienes el ID, o el correo, jamas debes generar la query "
    "Jamas debes generar un ejemplo de una query para explicarle al usuario "
    "Luego de generar la query recibiras la respuesta de la base de datos "
    "Si el usuario desea cambiar la contraseña antes de generar la query, debes solicitar la contrasena antigua "
    "La query debe solo ser de lo que se pide, si te solicitan revisar el estado del ticket, la query debe seleccionar solo el estado de la tabla tickets "
)
# Funcion encargada de detectar la query
def contiene_query_sql(texto):
    palabras_clave = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE", "REPLACE"]
    texto_mayus = texto.upper()
    return any(palabra in texto_mayus for palabra in palabras_clave)
# Guarda en el historial el imput del usuario y la base de datos respectivamente
def procesar_mensaje(mensaje_usuario, historial, consulta_query, respuesta_query=""):
    if consulta_query:
        historial += f"Usuario: {mensaje_usuario}\n"
    else:
        historial += f"Respuesta base de datos: {respuesta_query}\n"
        
    # Se genera la respuesta de la IA
    respuesta = co.generate(
        model="command-r-plus",
        prompt=historial,
        max_tokens=100,
        temperature=0,
        stop_sequences=["Usuario:"]
    )

    texto_ia = respuesta.generations[0].text.strip()

    # Comprobacion de si el mensaje lleva una query
    if contiene_query_sql(texto_ia):
        respuesta_query = ejecutar_query(texto_ia)
        historial += f"{texto_ia}\n"
        return respuesta_query, historial, False
    else:
        historial += f"{texto_ia}\n"
        return texto_ia, historial, True
