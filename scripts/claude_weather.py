# Day 9 - Trying to create Claude API calls on your own
import os
from dotenv import load_dotenv
import anthropic
import requests

load_dotenv()

city_name = "Netanya"
country_code = "IL"
request = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={os.getenv('OPENWEATHER_API_KEY')}"
)
if request.status_code == 200:
    data = request.json()
    kelvin_degrees = data["main"]["temp"]
    celsius_degrees = kelvin_degrees - 273.15
    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="""You are a weather assistant that provides the current time and temperature in Celsius and gives a brief description of the weather conditions.""",
            messages=[
                {
                    "role": "user",
                    "content": f"City {city_name}, weather data: {data['weather'][0]['description']}, time:{data['dt']}, {celsius_degrees:.2f}°C",
                }
            ],
        )
        print(message.content[0].text)
    except Exception as e:
        print("Error communicating with Claude API: ", e)
else:
    print("Error fetching weather data: ", request.status_code)