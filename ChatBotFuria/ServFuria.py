from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__, template_folder="Templates")

# Caminho absoluto para o diretório base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho para perguntas.json
caminho_perguntas = os.path.join(base_dir, "perguntas", "perguntas.json")
with open(caminho_perguntas, "r", encoding="utf-8") as f:
    perguntas = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "").strip()

    if msg.isdigit() and msg in perguntas:
        # Caminho para o arquivo da resposta
        caminho_dados = os.path.join(base_dir, "perguntas", "dados", f"{msg}.json")

        if os.path.exists(caminho_dados):
            with open(caminho_dados, "r", encoding="utf-8") as f:
                conteudo = json.load(f)
                return jsonify({
                    "response": conteudo["resposta"],
                    "pergunta": conteudo["pergunta"]
                })
        else:
            return jsonify({
                "response": "Essa opção não existe. Tente outro número!",
                "pergunta": None
            })
    else:
        # Mensagem padrão + menu
        menu = "\n".join([f"{num}. {texto}" for num, texto in perguntas.items()])
        saudacao = (
            "Olá! Eu sou o PanteraBot 🐾\n"
            "Digite o número de uma das opções abaixo para saber mais:\n\n" + menu
        )
        return jsonify({"response": saudacao, "pergunta": None})

if __name__ == "__main__":
    app.run(debug=True)
