from flask import Flask, request, jsonify, render_template
from together import Together
import os
from dotenv import load_dotenv
from flask_cors import CORS
import json

# Função que lê o próximo jogo da FURIA
def get_proximo_jogo():
    try:
        with open("data/jogos.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            jogo = data["proximo_jogo"]
            return (f"A FURIA joga contra {jogo['adversario']} no dia {jogo['data']} às {jogo['horario']}, "
                    f"pelo campeonato {jogo['campeonato']}.")
    except:
        return "Não consegui encontrar informações sobre o próximo jogo no momento 😢"

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Permite que o front acesse a API

# Inicializa o cliente Together com a chave da API
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")  # Renderiza o front-end

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Mensagem vazia"}), 400

        # Detecta se o usuário quer saber sobre o próximo jogo
        if "próximo jogo" in user_message.lower() or "quando a furia joga" in user_message.lower():
            info_jogo = get_proximo_jogo()
            user_message = f"{info_jogo}\n\n{user_message}"

        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages = [
                {"role": "system", "content": (
                    "Você é o **PanteraBot**, um chatbot carismático, fanático pelo time de CS:GO da FURIA. "
                    "Seu objetivo é conversar com fãs, responder com emoção, orgulho do time, e usar gírias como 'panterinha', 'bala', 'rush B', 'jogo sujo', 'monstro', 'mandou bem', etc. "
                    "Fale como um torcedor empolgado, tipo streamer ou narrador de CS. "
                    "Inclua curiosidades sobre a FURIA se for relevante. "
                    "Se o usuário pedir algo fora de contexto, responda de forma engraçada ou puxe o assunto de volta pro time. "
                    "Nunca diga que é apenas um assistente de IA, e nunca fale como se fosse um sistema genérico. "
                    "Seja direto, informal, criativo e divertido."
                )},
                {"role": "user", "content": user_message}
            ]
        )

        bot_message = response.choices[0].message.content
        return jsonify({"response": bot_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
