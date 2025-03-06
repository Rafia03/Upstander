from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import re
from anthropic import Anthropic
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Configure Claude API
load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Load UAP data
uap_data = pd.read_csv("uap_locations.csv")

# Context for the AI about the Upstander Program
SYSTEM_CONTEXT = """You are an AI assistant for the Canadian Museum for Human Rights' Upstander Program. 
The program aims to inspire individuals, particularly youth, to recognize injustices, identify their strengths, and take action.
You should help users understand:
1. Stories of upstanders 
2. How to recognize injustices and identify personal strengths
3. Ways to take action against human rights violations
4. Location-specific information in the museum using UAP (Universal Access Points)

Respond in a helpful, educational, and engaging manner, focusing on empowering users to become upstanders."""

def get_uap_info(uap_number):
    info = uap_data[uap_data['UAP Number'] == uap_number]
    if not info.empty:
        return info.to_dict('records')[0]
    return None

def get_ai_response(user_input):
    try:
        print("Attempting to call Claude API...")  # Debug log
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=300,
            messages=[
                {"role": "user", "content": user_input}
            ],
            system=SYSTEM_CONTEXT
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error with Claude API: {str(e)}")
        return "I apologize, but I'm having trouble generating a response right now. Please try again."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        print(f"User input: {user_input}")  # Debug: Print user input
        
        if not user_input:
            return jsonify({"response": "Please provide a message."})
        
        # Check if the user is asking about a UAP location
        if "UAP" in user_input.upper():
            print("UAP query detected")
            uap_number_match = re.search(r'\d+', user_input)
            if uap_number_match:
                uap_number = int(uap_number_match.group())
                uap_info = get_uap_info(uap_number)
                if uap_info:
                    response = f"UAP {uap_number} is located at {uap_info['Location']}."
                else:
                    response = f"Sorry, I couldn't find information for UAP {uap_number}. Available UAP numbers are: 102, 105-107, 201-205."
            else:
                response = "Please provide a valid UAP number. For example: 'Where is UAP 102?'"
        else:
            # Use AI for general responses
            response = get_ai_response(user_input)
        
        print(f"Bot response: {response}")  # Debug: Print bot response
        return jsonify({"response": response})
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"response": "An error occurred while processing your request. Please try again."})

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=0)