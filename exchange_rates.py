import os
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()
EXCHANGE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")

today = date.today()
d1 = today.strftime("%Y-%m-%d")

from_currency = (input("Enter From Current (For Ex. USD, INR): ")).upper()
to_currency = (input("Enter To Currency (For Ex. JPY): ")).upper()
amount = float(input("Enter amount (Quantity): "))

url =f"https://api.exchangeratesapi.io/v1/latest?access_key={EXCHANGE_API_KEY}&symbols={from_currency},{to_currency}"

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        from_currency_rate = data['rates'][from_currency]
        to_currency_rate = data['rates'][to_currency]

        # convert to_currency into 1 from_currency_rate
        to_currency_rate_one  = to_currency_rate / from_currency_rate
        to_currency_rate = amount * to_currency_rate_one

        print("Converted Currency Amount: ", round(to_currency_rate,2))

except Exception as e:
    print("Error: ",e)

