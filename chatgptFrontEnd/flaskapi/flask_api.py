from flask import Flask, request, jsonify
from claude_ai.claude import claude_answer
from chatgpt_ai.openai import chatgpt_evaluate
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

CORS(app)

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

    claude_response = claude_answer(clean_question)

    chatgpt_response = chatgpt_evaluate(clean_question, claude_response)

    return jsonify({"answer": claude_response,
        "evaluation": chatgpt_response})
