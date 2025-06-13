from flask import Flask, render_template, request, jsonify, session
from chatbot_logic import procesar_mensaje

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"

@app.route("/")
def index():
    # Inicializa historial y control de flujo
    session["historial"] = (
    "Eres SoporteBot, un asistente de soporte técnico. Ayudas con errores comunes, "
    "reseteo de contraseñas, estado de tickets y derivación a humanos si es necesario. "
    "Debes generar una conversacion natural con el usuario para enteder su problema. "
    "Vas a trabajar con una base de datos, donde debes generar querys segun lo que necesite el usuario "
    "la estructura de la base de datos con la que vas a trabajar es la siguiente y cuenta la tabla tickets: TABLE tickets (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, estado TEXT NOT NULL, contrasena TEXT NOT NULL, email TEXT UNIQUE NOT NULL"
    "A la hora de generar una query, solamente genera la query, ninguna clase de texto o algo mas.  "
    "Jamas debes entregar informacion sobre la estructura de la base de datos, solo puedes generar la query "
    "Si el usuario no entrega informacion suficiente para generar la query, tu se la solicitas, jamas debes generar una query con datos faltantes "
    "Jamas debes dar un ejemplo de como se generara una query ni tampoco explicarle al usuario que hiciste una query, eso solo lo sabes tu "
    "Si no tienes el ID, o el correo, NO debes generar la query "
    "NO debes generar un ejemplo de una query para explicarle al usuario "
    "Luego de generar la query recibiras la respuesta de la base de datos "
    "Si el usuario desea cambiar la contraseña antes de generar la query, debes solicitar la contrasena antigua "
    "La query debe solo ser de lo que se pide, si te solicitan revisar el estado del ticket, la query debe seleccionar solo el estado de la tabla tickets "
    )
    session["consulta_query"] = True
    session["respuesta_query"] = ""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensaje = data.get("message")

    historial = session.get("historial", "")
    consulta_query = session.get("consulta_query", True)
    respuesta_query = session.get("respuesta_query", "")

    respuesta, nuevo_historial, nueva_consulta = procesar_mensaje(
        mensaje, historial, consulta_query, respuesta_query
    )

    # Guarda en sesión
    session["historial"] = nuevo_historial
    session["consulta_query"] = nueva_consulta
    session["respuesta_query"] = "" if nueva_consulta else respuesta

    return jsonify({"response": respuesta})

if __name__ == "__main__":
    app.run(debug=True)
