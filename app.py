from flask import Flask
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


@app.route("/")
def home():
    return {
        "status": "Swiss Ephemeris loaded"
    }


@app.route("/sun")
def sun():

    # 20 Jan 1957 09:00 UT
    jd = swe.julday(1957, 1, 20, 9.0)

    longitude = swe.calc_ut(jd, swe.SUN)[0][0]

    sign = SIGNS[int(longitude // 30)]

    degree = longitude % 30

    return {
        "longitude": longitude,
        "sign": sign,
        "degree": degree
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
