from flask import Flask
from kerykeion import AstrologicalSubject

app = Flask(__name__)

@app.route("/")
def home():

    person = AstrologicalSubject(
        "Test",
        year=1957,
        month=1,
        day=20,
        hour=9,
        minute=0,
        city="Glasgow"
    )

    return {
        "sun": str(person.sun.sign),
        "moon": str(person.moon.sign),
        "ascendant": str(person.first_house.sign)
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
