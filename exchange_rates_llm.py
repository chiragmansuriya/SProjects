import os
import google.generativeai as genai
import json
import requests
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")

model = genai.GenerativeModel('gemini-1.5-flash')

user_input = input("Enter currency for convert (For Ex. USD to INR): ")

prompt = """
You are provided with an Exchange Rates API endpoint and a user prompt.
The API endpoint is: "https://api.exchangeratesapi.io/v1/convert?access_key={EXCHANGERATE_API_KEY}&from=GBP&to=JPY&amount=25"

The user has asked: {input}

Based on the user's prompt, please convert it into the correct API request format by identifying the "base" and "symbols" parameters. Provide the final JSON in the format:
{{
  "base": "BASE_CURRENCY",
  "symbols": "TARGET_CURRENCY"
  "amount": "AMOUNT"
}}
Only output the JSON format.
""".format(input=user_input, EXCHANGERATE_API_KEY=EXCHANGERATE_API_KEY)

response = model.generate_content(prompt)

# Extract the actual text from the 'parts' field
generated_text = response.candidates[0].content.parts[0].text
if generated_text.find('{'):
    start_index = generated_text.find('{')
    last_index = generated_text.find('}')
    generated_text = generated_text[start_index:last_index+1]

# Try to parse the generated text as JSON
try:
    json_response = json.loads(generated_text)
    base_currency = json_response.get("base")
    target_currency = json_response.get("symbols")
    amount = json_response.get("amount")


    url = f"https://api.exchangeratesapi.io/v1/latest?access_key={EXCHANGERATE_API_KEY}&symbols={base_currency},{target_currency}"
    response_exchange = requests.get(url)

    if response_exchange.status_code == 200:
        data = response_exchange.json()
        base_currency_rate = data['rates'][base_currency]
        target_currency_rate = data['rates'][target_currency]

        # convert to_currency into 1 from_currency_rate
        target_currency_rate_one = target_currency_rate / base_currency_rate
        target_current_rate = target_currency_rate_one * float(amount)
        print("Converted Currency Amount: ", round(target_current_rate,2))
    else:
        print("Failed to get exchange rates. Status code:", response_exchange.status_code)

except Exception as e:
    print("Error: ", e)
