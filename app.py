from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "9c133adc04bde5e8249b9dd2554e9bf2"

search_history = []

@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = None

    if request.method == "POST":

        city = request.form["city"]

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)

        data = response.json()

        if response.status_code == 200:

            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "icon": data["weather"][0]["icon"],
                "sunrise": datetime.fromtimestamp(
                    data["sys"]["sunrise"]
                ).strftime("%I:%M %p"),
                "sunset": datetime.fromtimestamp(
                    data["sys"]["sunset"]
                ).strftime("%I:%M %p")
            }

            if city not in search_history:
                search_history.insert(0, city)

            if len(search_history) > 5:
                search_history.pop()

        else:
            error = "City not found!"

    return render_template(
        "index.html",
        weather=weather,
        error=error,
        history=search_history
    )

if __name__ == "__main__":
    app.run(debug=True)