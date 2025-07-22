import requests
import os
import yfinance as yf
from ollama import chat

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
    

response = chat(
    messages = [
        {
            "role": "user",
            "content": "What is the stock price of AAPL?"
            },
    ],
    model = "llama3.2:latest",
    tools = [get_stock_price],
)

print(response)

available_funcs = {
    "get_stock_price": get_stock_price,
}

for tool in response.message.tool_calls:
    function_to_call = available_funcs.get(tool.function.name)
    if function_to_call:
        function_output = function_to_call(**tool.function.arguments)
        print(f"Function output: {function_output}")
        