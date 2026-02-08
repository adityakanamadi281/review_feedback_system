import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def call_ollama(prompt: str) -> str:
    """Call local Ollama LLM (llama3.2)"""
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 200
            }
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        print(f"Ollama error: {e}")
        return f"Error calling LLM: {str(e)}"

def generate_user_response(rating, review):
    """Generate personalized user response using llama3.2"""
    prompt = f"""Based on this Yelp review with {rating} stars, generate a brief, professional response that acknowledges the customer's feedback.

Review: {review}

Keep the response to 1-2 sentences, professional and empathetic."""
    
    return call_ollama(prompt)

def summarize_review(review):
    """Summarize the review using llama3.2"""
    prompt = f"""Summarize this customer review in 1-2 sentences:

Review: {review}

Summary:"""
    
    return call_ollama(prompt)

def recommend_action(rating):
    """Recommend business action based on rating using llama3.2"""
    prompt = f"""Based on a {rating}-star rating, recommend one specific action the business should take. Keep it brief (1 sentence max).

Action:"""
    
    return call_ollama(prompt)
