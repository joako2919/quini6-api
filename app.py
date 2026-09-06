from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

URL = "https://quiniya.com.ar/sorteos/ultimo"


@app.route("/")
def inicio():
    try:
        response = requests.get(
            URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        texto = soup.get_text(" ", strip=True)

        sorteo_match = re.search(
            r"Sorteo\s*(?:N[°º]?\s*)?(\d{4})",
            texto,
            re.IGNORECASE
        )

        fecha_match = re.search(
            r"\b(\d{1,2}/\d{1,2}/\d{4})\b",
            texto
        )

        def extraer(inicio, fin=None):
            if fin:
                patron = inicio + r"(.*?)" + fin
            else:
                patron = inicio + r"(.*)"

            match = re.search(
                patron,
                texto,
                re.IGNORECASE | re.DOTALL
            )

            if not match:
                return []

            numeros = re.findall(r"\b\d{1,2}\b", match.group(1))
            numeros = [n.zfill(2) for n in numeros[:6]]
            return sorted(numeros, key=int)

        tradicional = extraer(
            r"Tradicional",
            r"(?:La\s+Segunda|Segunda)"
        )

        segunda = extraer(
            r"(?:La\s+Segunda|Segunda)",
            r"Revancha"
        )

        revancha = extraer(
            r"Revancha",
            r"Siempre\s+Sale"
        )

        siempre_sale = extraer(
            r"Siempre\s+Sale"
        )

        if not sorteo_match:
            raise ValueError("No se pudo encontrar el número de sorteo")

        return jsonify({
            "sorteo": int(sorteo_match.group(1)),
            "fecha": fecha_match.group(1) if fecha_match else None,
            "tradicional": tradicional,
            "segunda": segunda,
            "revancha": revancha,
            "siempre_sale": siempre_sale
        })

    except Exception as e:
        return jsonify({
            "error": "No se pudieron obtener los resultados",
            "detalle": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
