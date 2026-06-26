from flask import Flask, request
import swisseph as swe
from geopy.geocoders import Nominatim

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

geolocator = Nominatim(user_agent="astrology_api")


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

    city = request.args["city"]
    country = request.args["country"]

    location = geolocator.geocode(f"{city}, {country}")

    if location is None:
        return {
            "error": f"Could not find '{city}, {country}'"
        }, 400

    latitude = location.latitude
    longitude = location.longitude

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
        "pluto": swe.PLUTO,

        # Modern astrology points
        "chiron": swe.CHIRON,
        "north_node": swe.TRUE_NODE,
        "lilith": swe.MEAN_APOG
    }

    result = {}

    for name, planet in planets.items():

        lon = swe.calc_ut(jd, planet)[0][0]

        result[name] = {
            "sign": get_sign(lon),
            "degree": round(lon % 30, 4),
            "longitude": round(lon, 6)
        }
# South Node (opposite the North Node)

south_lon = (result["north_node"]["longitude"] + 180) % 360

result["south_node"] = {
    "sign": get_sign(south_lon),
    "degree": round(south_lon % 30, 4),
    "longitude": round(south_lon, 6)
}




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

    result["location"] = {
        "city": city,
        "country": country,
        "latitude": latitude,
        "longitude": longitude
    }

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
