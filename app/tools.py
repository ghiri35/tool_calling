import yfinance as yf
import requests
import smtplib
from email.message import EmailMessage

def get_stock_price(symbol: str) -> str:
    """
    Fetches the current stock price for a given stock symbol using Yahoo Finance.

    Args:
        symbol (str): The stock symbol (e.g., 'AAPL', 'GOOGL').

    Returns:
        str: A message with the current stock price or an error message.
    """
    try:
        stock = yf.Ticker(symbol)
        price = stock.info.get("regularMarketPrice")
        currency = stock.info.get("currency", "USD")
        if price is not None:
            return f"The current stock price of {symbol.upper()} is {price:.2f} {currency}"
        else:
            return f"Couldn't fetch the stock price for {symbol.upper()}."
    except Exception as e:
        return f"An error occurred: {str(e)}"



def get_company_news(symbol: str, count: int = 3) -> list[str]:
    """
    Fetches recent news headlines for a given stock symbol using yfinance.

    Args:
        symbol (str): The stock symbol (e.g., 'AAPL').
        count (int): Number of news headlines to return.

    Returns:
        List of news headlines (strings).
    """
    try:
        stock = yf.Ticker(symbol)
        news_items = stock.news[:count]
        return [item['content']['title'] for item in news_items]
    except Exception as e:
        return [f"Could not fetch news for {symbol}. Error: {str(e)}"]

def get_weather(city: str) -> str:
    """
    Fetches current weather from wttr.in (no API key required).

    Args:
        city (str): The city name.

    Returns:
        str: Weather summary or error message.
    """
    url = f"https://wttr.in/{city}?format=3"  # Short format: City: Weather, Temp
    try:
        response = requests.get(url)
        response.raise_for_status()
        raw = response.text.strip()

        parts = raw.split(": ")
        if len(parts) == 2:
            city_name, weather_info = parts
            return f"Current weather in {city_name} is {weather_info}"
        else:
            return f"Could not parse weather data for '{city}'."
    except requests.RequestException:
        return f"Could not fetch weather for '{city}'."

def send_email(to_email: str, subject:str,content: str) -> str:
    """
    Simulates sending an email. In a real-world scenario, this would use an email service.

    Args:
        to_email (str): Recipient's email address.
        chat_transcript (str): The content of the email.

    Returns:
        str: Confirmation message.
    """
    EMAIL_SENDER = "21f3002571@ds.study.iitm.ac.in"
    EMAIL_PASSWORD = "maum pygk krgy bxxv"  
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email
    msg.set_content(content+"\n\nBest ,\nGanesh")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
    # Here you would integrate with an actual email service
    return f"Email sent to {to_email} with the following content: {content}"