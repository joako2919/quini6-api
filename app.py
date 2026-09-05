from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "API de Quini 6 funcionando"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
