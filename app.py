from flask import Flask, request
from kerykeion import AstrologicalSubject

app = Flask(__name__)

@app.route("/")
def home():

    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    day = int(request.args.get("day"))
    hour = int(request.args.get("hour"))
    minute = int(request.args.get("minute"))
    city = request.args.get("city")

    person = AstrologicalSubject(
        "Client",
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        city=city
    )

    return {
        "sun": str(person.sun.sign),
        "moon": str(person.moon.sign),
        "ascendant": str(person.first_house.sign)
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
