import os
from flask import Flask, render_template, request
import math

app = Flask(__name__)


def parse_number(value):
    return float(value.strip().replace(",", "."))

def fmt(n):
    if n == int(n):
        return str(int(n))
    return str(round(n, 3))


def equation_text(a, b, c):
    text = f"{fmt(a)}x²"

    if b >= 0:
        text += f" + {fmt(b)}x"
    else:
        text += f" - {fmt(abs(b))}x"

    if c >= 0:
        text += f" + {fmt(c)}"
    else:
        text += f" - {fmt(abs(c))}"

    return text + " = 0"

@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    result = None
    values = {"a": "", "b": "", "c": ""}

    if request.method == "POST":
        values["a"] = request.form.get("a", "")
        values["b"] = request.form.get("b", "")
        values["c"] = request.form.get("c", "")

        try:
            if not values["a"].strip() or not values["b"].strip() or not values["c"].strip():
                errors.append("Wszystkie pola muszą być wypełnione.")
            else:
                a = parse_number(values["a"])
                b = parse_number(values["b"])
                c = parse_number(values["c"])

                if a == 0:
                    errors.append("To nie jest równanie kwadratowe, lecz liniowe!")
                else:
                    delta = b ** 2 - 4 * a * c

                    result = {
                        "a": a,
                        "b": b,
                        "c": c,
                        "equation": equation_text(a, b, c),
                        "delta": delta,
                        "delta_step1": f"Δ = {fmt(b)}² - 4·{fmt(a)}·{fmt(c)}",
                        "delta_step2": f"Δ = {fmt(b**2)} - {fmt(4*a*c)}",
                        "delta_step3": f"Δ = {fmt(delta)}"
                    }

                    if delta > 0:
                        x1 = (-b - math.sqrt(delta)) / (2 * a)
                        x2 = (-b + math.sqrt(delta)) / (2 * a)

                        result["message"] = "Równanie ma dwa rozwiązania."

                        result["x1"] = x1
                        result["x2"] = x2

                        result["x1_step1"] = f"x1 = (-({fmt(b)}) - √{fmt(delta)}) / ({fmt(2)}·{fmt(a)})"
                        result["x1_step2"] = f"x1 = ({fmt(-b)} - {fmt(math.sqrt(delta))}) / {fmt(2*a)}"
                        result["x1_step3"] = f"x1 = {fmt(x1)}"

                        result["x2_step1"] = f"x2 = (-({fmt(b)}) + √{fmt(delta)}) / ({fmt(2)}·{fmt(a)})"
                        result["x2_step2"] = f"x2 = ({fmt(-b)} + {fmt(math.sqrt(delta))}) / {fmt(2*a)}"
                        result["x2_step3"] = f"x2 = {fmt(x2)}"

                    elif delta == 0:
                        x0 = -b / (2 * a)

                        result["message"] = "Równanie ma jedno rozwiązanie."

                        result["x0"] = x0

                        result["x0_step1"] = f"x0 = -({fmt(b)}) / ({fmt(2)}·{fmt(a)})"
                        result["x0_step2"] = f"x0 = {fmt(-b)} / {fmt(2*a)}"
                        result["x0_step3"] = f"x0 = {fmt(x0)}"

                    else:
                        result["message"] = "Równanie nie ma rozwiązań rzeczywistych."

        except ValueError:
            errors.append("Współczynniki muszą być poprawnymi liczbami rzeczywistymi.")

    return render_template("form.html", errors=errors, values=values, result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
