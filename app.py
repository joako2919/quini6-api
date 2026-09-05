from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def inicio():
    return jsonify({
        "sorteo": 3405,
        "fecha": "02/09/2026",
        "tradicional": ["00", "05", "10", "22", "26", "45"],
        "segunda": ["02", "03", "16", "22", "24", "44"],
        "revancha": ["02", "07", "14", "25", "34", "38"],
        "siempre_sale": ["02", "05", "08", "10", "31", "38"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
