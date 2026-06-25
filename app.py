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
        "status": "online",
        "message": "Swiss Ephemeris API running"
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

    planets = {
        "sun": swe.SUN,
        "moon": swe.MOON,
        "mercury": swe.MERCURY,
        "venus": swe.VENUS,
        "mars": swe.MARS,
        "jupiter": swe.JUPITER,
        "saturn": swe.SATURN,
        "uranus": swe.URANUS,
        "neptune": swe.NEPTUNE,
        "pluto": swe.PLUTO
    }

    result = {}

    for name, planet in planets.items():

        longitude = swe.calc_ut(jd, planet)[0][0]

        result[name] = {
            "sign": get_sign(longitude),
            "degree": round(longitude % 30, 4),
            "longitude": round(longitude, 6)
        }

    #
    # ASCENDANT + MIDHEAVEN
    #

    latitude = float(request.args["lat"])
    longitude = float(request.args["lon"])

    houses = swe.houses_ex(
        jd,
        latitude,
        longitude,
        b'P'
    )

    asc = houses[1][0]
    mc = houses[1][1]

    result["ascendant"] = {
        "sign": get_sign(asc),
        "degree": round(asc % 30, 4),
        "longitude": round(asc, 6)
    }

    result["midheaven"] = {
        "sign": get_sign(mc),
        "degree": round(mc % 30, 4),
        "longitude": round(mc, 6)
    }

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
