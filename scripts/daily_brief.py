import os

import anthropic
import dotenv
import requests


dotenv.load_dotenv()



city_name = "Netanya"
country_code = "IL"
priorities = ["Workout after work", "Improve myself atleast 1% by stuying", "Eat a healthy meal after workout"]

try:
    request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={os.getenv('OPENWEATHER_API_KEY')}")
    weather_data = request.json()
    client=anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="You are my daily assistant, you will provide me with the current weather in celsius, a short motivitional quote based on the weather, list my 3 priorities for the day and suggest a focus for the day based on my priorities. Keep the response concise and non robotic.",
        messages=[{
            "role": "user",
            "content": f"Use the weather data from {weather_data['weather'][0]['description']}, time:{weather_data['dt']}, my daily priorities are {priorities} - This will be my daily brief."
        }]
)
    print(message.content[0].text)
except Exception as e:
    print(f"An error occurred: {e}")