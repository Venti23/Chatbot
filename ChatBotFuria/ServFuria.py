from flask import Flask, request, jsonify, render_template
import os, json

app = Flask(__name__, template_folder="templates")


with open("./perguntas/perguntas.json", "r", encoding="utf-8") as f:
    perguntas = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "").strip()

    if msg.isdigit() and msg in perguntas:
        caminho = os.path.join(base_dir, "dados", f"{msg}.json")
        if os.path.exists(caminho):
            with open("./perguntas/perguntas.json", "r", encoding="utf-8") as f:
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
        menu = "\n".join([f"{num}. {perg}" for num, perg in perguntas.items()])
        saudacao = (
            "Olá! Eu sou o PanteraBot 🐾\n"
            "Digite o número de uma das opções abaixo para saber mais:\n\n" + menu
        )
        return jsonify({"response": saudacao, "pergunta": None})

if __name__ == "__main__":
    app.run(debug=True)
