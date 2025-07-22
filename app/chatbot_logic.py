import re
from .intent import get_dynamic_prompt
from .tools import get_stock_price, get_company_news, get_weather, send_email
import requests
from rapidfuzz import process, fuzz
import ast

available_funcs = {
    "get_stock_price": get_stock_price,
    "get_company_news": get_company_news,
    "get_weather": get_weather,
    "send_email": send_email,
    # Add more here as needed
}

def resolve_function_name(func_name: str, threshold: int = 50):
    match, score, _ = process.extractOne(func_name, available_funcs.keys(), scorer=fuzz.token_sort_ratio)
    return available_funcs.get(match) if score >= threshold else None

class ChatBot:
    def __init__(self,user_input) :
        self.OLLAMA_API = "http://localhost:11434/api/generate"
        self.prompt = get_dynamic_prompt(user_input) + f"\nUser: {user_input}\nAI:"

    def call_llama3(self,prompt: str) -> str:
        response = requests.post(
            self.OLLAMA_API,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

    def extract_function_call(self,response):
        match = re.search(r'(\w+)\((.*?)\)', response)
        if not match:
            return None, None
        func_name = match.group(1)
        args = match.group(2)
        return func_name, args
        
    def get_response(self,user_input,retry_count=0,max_retries=2):

        prompt = get_dynamic_prompt(user_input) + f"\nUser: {user_input}\nAI:"
        response = self.call_llama3(prompt)
        print("🤖 Model Response:", response)

        if "send_email" in response:
            print("📧 Email detected in response")
            # Extract the email address and chat transcript
            try:
                to_email = (re.search(r'to_email\s*=\s*"([^"]+)"', response)).group(1)
                subject = (re.search(r'subject\s*=\s*"([^"]+)"', response)).group(1)
                content = re.search(r'content\s*=\s*"((?:.|\n)*?)(?:Best regards,)', response).group(1).strip()
                print(f"📧 Email: {to_email}")
                if not to_email:
                    return None

                send_email(to_email=to_email,subject=subject,content=content)

                return f"Email sent to {to_email}"

            except Exception as e:
                print(f"❌ Failed to parse email response: {e}")
                if retry_count < max_retries:
                    print(f"🔄 Retrying LLM email parse (attempt {retry_count + 1})...")
                    return self.get_response(user_input, retry_count + 1, max_retries)
                return "Failed to send email after retries."
            
        func_name, args_str = self.extract_function_call(response)
        print(args_str)
        if not func_name:
            if retry_count < max_retries:
                print("🔄 Retrying...")
                for key, func in available_funcs.items():
                    if key in response.lower():
                        return self.get_response(user_input, retry_count + 1, max_retries)
            else:
                return response
            


        resolved_func = resolve_function_name(func_name)


        if resolved_func:
            args = re.findall(r"'(.*?)'", args_str)
            print(args)
            result = resolved_func(args[0] if args else args_str[1:-1])
            print("📈 Tool Result:", result)
        else:
            return response

        print("📊 Tool Result:", result)
        return result




