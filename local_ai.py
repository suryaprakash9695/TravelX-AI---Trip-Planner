import requests
import random
import time

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_itinerary(source, destination, start_date, end_date, no_of_day):

    styles = [
        "luxury travel style",
        "budget-friendly travel",
        "adventure-focused trip",
        "family-friendly trip",
        "solo traveler itinerary",
        "local culture focused trip"
    ]

    style = random.choice(styles)
    seed = random.randint(1000, 9999)

    prompt = f"""
You are a professional travel planner.

Generate a UNIQUE and DIFFERENT {no_of_day}-day itinerary.
Trip Style: {style}
Seed: {seed}

Trip Details:
From: {source}
To: {destination}
Dates: {start_date} to {end_date}

Rules:
- Use Morning / Afternoon / Evening
- Mention real places
- Include local food
- Mention approximate budget in INR
- DO NOT repeat previous itineraries
"""

    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.9,
            "top_p": 0.95,
            "num_predict": 400
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()
        data = response.json()

        return data.get("response", "").strip()

    except Exception as e:
        print("Ollama Error:", e)
        return None
