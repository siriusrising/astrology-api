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
        "sun": person.sun.sign,
        "moon": person.moon.sign
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
