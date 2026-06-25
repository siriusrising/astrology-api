from flask import Flask, request
import swisseph as swe

app = Flask(__name__)

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces"
]


def get_sign(longitude):
    return SIGNS[int(longitude // 30)]


@app.route("/")
def home():
    return {
        "status": "Swiss Ephemeris API",
        "message": "Running"
    }


@app.route("/chart")
def chart():

    year = int(request.args["year"])
    month = int(request.args["month"])
    day = int(request.args["day"])
    hour = int(request.args["hour"])
    minute = int(request.args["minute"])

    ut = hour + (minute / 60.0)

    jd = swe.julday(year, month, day, ut)

    sun = swe.calc_ut(jd, swe.SUN)[0][0]

    return {
        "sun": get_sign(sun),
        "sunLongitude": sun,
        "sunDegree": sun % 30
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
