TOOL_PROMPTS = {
    "stock": """You are an AI assistant with access to a function:
get_stock_price(symbol)

Return ONLY the function call in Python format when the user asks for a stock price and replace the symbol with appropriate symbol of the stock and give the exchange symbol.
""",
    "news": """You are an AI assistant with access to a function:
get_company_news(symbol)

Return ONLY the function call in Python format when the user asks for company news and replace the symbol with appropriate symbol of the stock and give the exchange symbol.
""",
    "weather": """You are an AI assistant with access to a function:
get_weather(city)

Return ONLY the function call in Python format when the user asks about the weather. Replace `city` with the correct city name.
""",
"email": """You are an AI assistant with access to a function:
send_email(to_email, chat_transcript)

When the user asks you to email someone — especially for things like job applications, follow-ups, or summaries — generate a suitable email body and return ONLY the function call in Python format.

Example:
If the user says: "Email john.doe@example.com and ask if I got the job", your response should be:
send_email(to_email="john.doe@example.com",subject="Regarding job application" ,content="Dear John,\n\nI hope you're doing well. I wanted to follow up regarding my job application...")

Always use a polite, professional tone if it's a job-related request.
"""
}

def detect_user_intent(user_input):
    if any(k in user_input.lower() for k in ["price", "stock price", "quote"]):
        return "stock"
    elif any(k in user_input.lower() for k in ["news", "headlines", "update"]):
        return "news"
    elif any(k in user_input.lower() for k in ["weather", "forecast", "temperature"]):
        return "weather"
    elif any(k in user_input.lower() for k in ["email", "send email", "message"]):
        return "email"
    else:
        return None

def get_dynamic_prompt(user_input):
    intent = detect_user_intent(user_input)
    return TOOL_PROMPTS.get(intent, "You are a helpful assistant. Respond clearly.")




intent_keywords = {
    "goodbye": ["bye", "goodbye", "see you", "farewell", "exit", "quit"],
    "escalation": ["human", "agent", "real person", "talk to support", "speak to someone"]
}

def detect_intent(user_input):
    
    for intent, keywords in intent_keywords.items():
        if any(keyword in user_input.lower() for keyword in keywords):
            return intent
    return "chat"  # Default: send to chatbot
