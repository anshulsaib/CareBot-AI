import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"reply": "Error: No message received"}), 400

    # Use an instructive prompt format
    prompt = f"You are a helpful AI assistant. Answer concisely and clearly.\n\nUser: {user_input}\nAI:"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,  # Limit response length
            "temperature": 0.6,  # Control randomness
            "top_p": 0.9,
            "do_sample": True,
            "stop_sequences": ["User:"],  # Stop response at logical end
        }
    }
    
    response = requests.post(HUGGING_FACE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        chatbot_response = response.json()
        return jsonify({"reply": chatbot_response[0]["generated_text"].strip().replace(prompt, "").strip()})
    else:
        return jsonify({"reply": "Error contacting Hugging Face API"}), 500

if __name__ == "__main__":
    app.run(debug=True)
