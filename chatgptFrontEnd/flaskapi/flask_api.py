from dotenv import load_dotenv
import os
import openai
import chatgpt_ai.openai
from flask import Flask, request, jsonify
from chatgpt_ai.openai import chatgpt_response
from utils import get_embeddings, search_for_context, form_prompt, qdrant_client
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

CORS(app)

# Load environment variables from a .env file
load_dotenv()

# Set OpenAI API key from environment variables
api_key = chatgpt_ai.openai.api_key

@app.route('/process', methods=['POST'])
def process_message():
    #Get the incoming message from the POST request
    data = request.json  #Expecting a JSON body
    message_content = data.get('message')  #Extract the message from the JSON
    print(message_content)

    #Ensure the message content is provided
    if not message_content:
        print("No message content.")
        return jsonify({"message": "Error: No message content provided"}), 400

    user_message = message_content
    #Proceed only if a valid command was detected
    clean_question = user_message.strip()

    search_vector = get_embeddings(clean_question)
    try:
        contexts = search_for_context(qdrant_client(), "Fed_Speeches", search_vector)
    except Exception as e:
        print("Unable to get context.",e)
        return jsonify({"error": f"Qdrant connection failed: {e}"}), 500
    prompt = form_prompt(contexts, clean_question)

    client2 = chatgpt_ai.openai.client

    bot_response = chatgpt_response(prompt,client2)

    return jsonify({"message": bot_response})
