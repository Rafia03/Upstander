from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import re
import random
import requests
from dotenv import load_dotenv

app = Flask(__name__, static_folder='static')
CORS(app)

# Load environment variables
load_dotenv()

# Load UAP data
uap_data = pd.read_csv("uap_locations.csv")

# Hugging Face API settings
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")  # Your Hugging Face API token

# For better results, let's use a more capable model
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# Define upstander stories and strengths
upstander_stories = {
    "courage": [
        {
            "name": "Viola Desmond",
            "story": "In 1946, Viola Desmond refused to leave a whites-only area of a Nova Scotia theater. Her act of courage challenged racial segregation in Canada and helped spark the civil rights movement there. Her image now appears on the Canadian $10 bill.",
            "impact": "Her courage to stand up against discrimination helped change segregation policies in Canada."
        },
        {
            "name": "Malala Yousafzai",
            "story": "Despite facing threats from the Taliban for advocating for girls' education in Pakistan, Malala continued to speak out. After surviving an assassination attempt, she became a global advocate for education rights.",
            "impact": "Her courage inspired worldwide attention to the importance of education for all children, especially girls."
        }
    ],
    "empathy": [
        {
            "name": "Oskar Schindler",
            "story": "During World War II, Oskar Schindler, a German industrialist, saved over 1,000 Jews by employing them in his factories. He spent his entire fortune to protect his workers from deportation to concentration camps.",
            "impact": "His empathy and compassion saved many lives during one of history's darkest periods."
        },
        {
            "name": "Craig Kielburger",
            "story": "At age 12, Craig was moved by the story of a child laborer who was murdered for speaking out. He founded Free The Children (now WE Charity) to fight child labor and promote education.",
            "impact": "His empathy for other children's suffering led to a global movement empowering youth to make positive social change."
        }
    ],
    "persistence": [
        {
            "name": "Nelson Mandela",
            "story": "Despite being imprisoned for 27 years for fighting against apartheid in South Africa, Nelson Mandela continued his advocacy for equality and reconciliation. After his release, he became South Africa's first Black president.",
            "impact": "His persistence in fighting for justice transformed South Africa and inspired people worldwide."
        },
        {
            "name": "Autumn Peltier",
            "story": "As a young Indigenous water activist from Wiikwemkoong First Nation, Autumn has persistently advocated for clean drinking water in First Nations communities since she was 8 years old.",
            "impact": "Her persistent advocacy has brought international attention to water issues affecting Indigenous communities in Canada."
        }
    ]
}

# Conversation flow
conversation_stages = {
    "intro": {
        "message": "Welcome to the Canadian Museum for Human Rights Upstander Program! I'm here to help you discover your inner upstander. Would you like to learn about becoming an upstander?",
        "options": ["Yes, I'd like to learn more", "What is an upstander?", "Tell me about the museum"]
    },
    "explain_upstander": {
        "message": "An upstander is someone who recognizes when something is wrong and acts to make it right. Unlike a bystander who watches without acting, upstanders use their strengths to help others and stand up against injustice.",
        "next": "assess_strengths_intro"
    },
    "museum_info": {
        "message": "The Canadian Museum for Human Rights (CMHR) is located in Winnipeg, Manitoba. It's the first museum solely dedicated to human rights awareness and education. The Upstander Program is designed to help visitors discover how they can make a positive difference.",
        "next": "assess_strengths_intro"
    },
    "assess_strengths_intro": {
        "message": "To help you discover your upstander potential, I'd like to learn about your strengths. Which of these do you identify with most strongly?",
        "options": ["Courage - I stand up for what's right", "Empathy - I understand others' feelings", "Persistence - I don't give up easily"]
    },
    "scenario_courage": {
        "message": "Imagine this scenario: You witness someone being bullied in a public place. Most people are ignoring it. How would you respond?",
        "options": ["Directly confront the bully", "Support the person being bullied", "Get help from authorities", "Document what's happening"]
    },
    "scenario_empathy": {
        "message": "Imagine this scenario: You notice a new student at school who seems lonely and is excluded from activities. How would you respond?",
        "options": ["Invite them to join your group", "Start a conversation with them", "Create an inclusive activity", "Check in with them regularly"]
    },
    "scenario_persistence": {
        "message": "Imagine this scenario: You've started a petition for an important cause, but it's not getting much attention. How would you continue?",
        "options": ["Try different approaches to reach people", "Research successful campaigns", "Partner with others", "Focus on small, achievable goals"]
    },
    "inspiration_response": {
        "message": {
            "courage": {
                "courage": "Standing up for what's right, even in the face of opposition, is at the core of being an upstander. Viola Desmond's courage created a ripple effect that helped change laws and attitudes in Canada.",
                "difference": "Viola Desmond's seemingly small act of refusing to move from her seat challenged an entire system of segregation. Her courage led to legal changes and greater awareness of racial discrimination in Canada. She's now honored on the $10 bill, educating new generations about standing up for equality.",
                "commitment": "Viola Desmond's unwavering commitment to justice, even when facing arrest and legal penalties, shows how principled resistance can catalyze social change. Her legacy continues to inspire Canadians today."
            },
            "empathy": {
                "courage": "Craig Kielburger's courage to take action at such a young age shows that you're never too young to make a difference when you truly care about others' suffering.",
                "difference": "Craig's empathy for child laborers grew into a global movement that has built schools, provided clean water, and created opportunities for countless children. By founding Free The Children (WE Charity) at age 12, he showed how empathy combined with action can transform lives around the world.",
                "commitment": "Craig's long-term commitment turned a moment of empathy into decades of systemic change. By staying dedicated to his cause, he's created lasting impact across generations."
            },
            "persistence": {
                "courage": "Nelson Mandela's courage during 27 years of imprisonment demonstrates extraordinary personal strength and conviction. His refusal to give up inspired a nation.",
                "difference": "Mandela's persistence led to the dismantling of apartheid and the creation of a new democratic South Africa. After decades of struggle and 27 years in prison, he emerged to lead his country through a peaceful transition to democracy, showing the world how persistence can overcome seemingly impossible obstacles.",
                "commitment": "Mandela's lifelong commitment to equality, even when it cost him his freedom, demonstrates the power of holding true to one's principles through the most difficult circumstances."
            }
        }
    }
}

def get_uap_info(uap_number):
    info = uap_data[uap_data['UAP Number'] == uap_number]
    if not info.empty:
        return info.to_dict('records')[0]
    return None

def generate_ai_response(prompt):
    """Generate a response using Hugging Face's API"""
    try:
        # If no API token is available, return a default response
        if not HF_API_TOKEN:
            print("Warning: No Hugging Face API token found. Using rule-based responses.")
            return None
            
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.95,
                "return_full_text": False
            }
        }
        
        print(f"Sending request to Hugging Face API for free-form question")
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            # Extract the generated text from the response
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
                print(f"AI generated response: {generated_text[:50]}...")  # Print first 50 chars for debugging
                return generated_text
            return result.get("generated_text", "")
        else:
            print(f"Error from Hugging Face API: {response.status_code} - {response.text}")
            # Return upstander-related default response if API fails
            return "I can provide information about various upstanders like Viola Desmond, Malala Yousafzai, and Nelson Mandela. Would you like to learn more about a specific upstander or continue with your journey?"
    except Exception as e:
        print(f"Exception when calling Hugging Face API: {str(e)}")
        return None

def get_response(user_input, session_data=None):
    if not session_data:
        session_data = {"stage": "intro", "strengths": [], "progress": 10}
    
    # FIRST - Check for direct questions about upstanders/human rights topics
    upstander_keywords = [
        "viola desmond", "malala", "nelson mandela", "mandela", "kielburger", 
        "human rights", "segregation", "discrimination", "apartheid", 
        "civil rights", "activism", "upstander history", "rights movement"
    ]
    
    # If user is directly asking about an upstander or human rights topic
    if any(keyword in user_input.lower() for keyword in upstander_keywords) and not user_input.startswith("Yes") and not user_input.startswith("How") and len(user_input) > 5:
        print(f"Detected upstander question: {user_input}")
        
        # Create a detailed prompt for AI response
        ai_prompt = f"""<s>[INST] You are an educational AI assistant for the Canadian Museum for Human Rights' Upstander Program.
        
        The program focuses on:
        - Recognizing injustice and discrimination
        - Identifying personal strengths to make a difference
        - Learning from historical and contemporary upstanders
        
        Key upstanders include:
        - Viola Desmond: Canadian civil rights activist who challenged racial segregation
        - Malala Yousafzai: Education activist who stood up to the Taliban
        - Nelson Mandela: Anti-apartheid activist who became South Africa's first Black president
        - Craig Kielburger: Founded Free The Children at age 12 to fight child labor
        
        Please provide a brief, informative response about: {user_input}
        
        Keep your answer to 2-3 sentences, focused on how this relates to being an upstander.
        [/INST]</s>
        """
        
        # Try to get AI response
        ai_response = generate_ai_response(ai_prompt)
        
        # If we got a valid AI response, use it and maintain the current conversation stage
        if ai_response and len(ai_response) > 20:  # Ensure it's substantial
            # Clean up the response
            ai_response = ai_response.replace("[/INST]", "").replace("<s>", "").replace("</s>", "").strip()
            
            # Don't change the session stage for these informational questions
            current_stage = session_data["stage"]  # Keep current stage
            current_progress = session_data.get("progress", 10)  # Keep current progress
            
            # Return response while preserving conversation state
            return {
                "response": ai_response,
                "session_data": session_data  # Maintain current session state
            }
    
    # Check if the user is asking about a UAP location
    if "UAP" in user_input.upper():
        uap_number_match = re.search(r'\d+', user_input)
        if uap_number_match:
            uap_number = int(uap_number_match.group())
            uap_info = get_uap_info(uap_number)
            if uap_info:
                return {"response": f"UAP {uap_number} is located at {uap_info['Location']}.", "session_data": session_data}
            else:
                return {"response": f"Sorry, I couldn't find information for UAP {uap_number}. Available UAP numbers are: 102, 105-107, 201-205.", "session_data": session_data}
    
    # NOW - Handle the guided conversation flow as before
    current_stage = session_data["stage"]
    
    # Intro stage
    if current_stage == "intro":
        if "yes" in user_input.lower() or "learn more" in user_input.lower():
            print("User wants to learn more - moving to strength assessment")
            session_data["stage"] = "assess_strengths_intro"
            return {
                "response": conversation_stages["assess_strengths_intro"]["message"],
                "options": conversation_stages["assess_strengths_intro"]["options"],
                "session_data": session_data
            }
        elif "what is" in user_input.lower() or "upstander" in user_input.lower():
            session_data["stage"] = "explain_upstander"
            return {
                "response": conversation_stages["explain_upstander"]["message"],
                "next_question": conversation_stages["assess_strengths_intro"]["message"],
                "options": conversation_stages["assess_strengths_intro"]["options"],
                "session_data": session_data
            }
        elif "museum" in user_input.lower() or "cmhr" in user_input.lower():
            session_data["stage"] = "museum_info"
            return {
                "response": conversation_stages["museum_info"]["message"],
                "next_question": conversation_stages["assess_strengths_intro"]["message"],
                "options": conversation_stages["assess_strengths_intro"]["options"],
                "session_data": session_data
            }
    
    # Strength assessment
    elif current_stage == "assess_strengths_intro":
        if "courage" in user_input.lower():
            session_data["strengths"].append("courage")
            session_data["stage"] = "scenario_courage"
            session_data["progress"] = 40
            return {"response": conversation_stages["scenario_courage"]["message"], 
                    "options": conversation_stages["scenario_courage"]["options"],
                    "session_data": session_data}
        elif "empathy" in user_input.lower():
            session_data["strengths"].append("empathy")
            session_data["stage"] = "scenario_empathy"
            session_data["progress"] = 40
            return {"response": conversation_stages["scenario_empathy"]["message"], 
                    "options": conversation_stages["scenario_empathy"]["options"],
                    "session_data": session_data}
        elif "persistence" in user_input.lower():
            session_data["strengths"].append("persistence")
            session_data["stage"] = "scenario_persistence"
            session_data["progress"] = 40
            return {"response": conversation_stages["scenario_persistence"]["message"], 
                    "options": conversation_stages["scenario_persistence"]["options"],
                    "session_data": session_data}
    
    # Handle scenario responses
    elif current_stage.startswith("scenario_"):
        strength = current_stage.split("_")[1]
        session_data["stage"] = "reflection"
        session_data["progress"] = 70
        
        # Create personalized responses based on scenario choice
        response_messages = {
            "courage": {
                "confront": "Directly confronting a bully shows exceptional courage. Remember to prioritize safety and consider getting help if the situation could be dangerous.",
                "support": "Supporting the person being bullied is a compassionate act of courage. Your presence can make a huge difference to someone facing harassment.",
                "help": "Seeking help from authorities is a smart and courageous approach. Sometimes professional intervention is the most effective solution.",
                "document": "Documenting what's happening is strategic and can provide valuable evidence. This type of careful observation can lead to meaningful action."
            },
            "empathy": {
                "invite": "Inviting someone to join your group shows great empathy. This simple act can make someone feel included and valued.",
                "conversation": "Starting a conversation demonstrates your ability to connect with others. This kind of personal outreach can transform someone's day.",
                "inclusive": "Creating inclusive activities shows thoughtful empathy. By designing experiences where everyone belongs, you create community.",
                "check": "Checking in regularly shows sustained empathy. Consistent support often makes the biggest difference in someone's life."
            },
            "persistence": {
                "approaches": "Trying different approaches shows adaptable persistence. Being flexible while staying committed is key to long-term success.",
                "research": "Researching successful campaigns demonstrates strategic persistence. Learning from others can help you overcome obstacles.",
                "partner": "Partnering with others shows collaborative persistence. Combined efforts often achieve what individuals cannot alone.",
                "small": "Focusing on small goals shows practical persistence. Breaking big challenges into manageable steps makes progress possible."
            }
        }
        
        # Match the response to the option they chose
        choice_type = ""
        if "confront" in user_input.lower() or "directly" in user_input.lower():
            choice_type = "confront"
        elif "support" in user_input.lower():
            choice_type = "support"
        elif "help" in user_input.lower() or "authorit" in user_input.lower():
            choice_type = "help"
        elif "document" in user_input.lower():
            choice_type = "document"
        elif "invite" in user_input.lower() or "join" in user_input.lower():
            choice_type = "invite"
        elif "conversation" in user_input.lower() or "talk" in user_input.lower():
            choice_type = "conversation"
        elif "inclusive" in user_input.lower() or "activit" in user_input.lower():
            choice_type = "inclusive"
        elif "check" in user_input.lower() or "regular" in user_input.lower():
            choice_type = "check"
        elif "approach" in user_input.lower() or "different" in user_input.lower():
            choice_type = "approaches"
        elif "research" in user_input.lower():
            choice_type = "research"
        elif "partner" in user_input.lower():
            choice_type = "partner"
        elif "small" in user_input.lower() or "achievable" in user_input.lower():
            choice_type = "small"
        
        # Get the matching response or use a default
        response_text = response_messages[strength].get(choice_type, "That's a thoughtful approach to the situation.")
        
        # Prepare the next step message
        next_step = "Based on your responses, I can see you have strong potential as an upstander. Would you like to learn about an upstander who demonstrated similar qualities to yours?"
        
        return {
            "response": f"{response_text} {next_step}",
            "options": ["Yes, tell me about them", "How can I apply these skills in my life?", "Are there resources to learn more?"],
            "session_data": session_data
        }
    
    # Handle the reflection stage
    elif current_stage == "reflection":
        last_strength = session_data["strengths"][-1] if session_data["strengths"] else "courage"
        
        if "yes" in user_input.lower() or "tell me" in user_input.lower():
            session_data["stage"] = "inspiration_question"
            session_data["progress"] = 85  # Update progress to 85%
            
            upstander_info = {
                "courage": "Viola Desmond demonstrated remarkable courage in 1946 when she refused to leave a whites-only area of a theater in Nova Scotia, challenging racial segregation in Canada. Despite being arrested and fined, her brave act became a catalyst for the civil rights movement in Canada. In 2018, she became the first Canadian woman to appear on a regular Canadian banknote.",
                "empathy": "Craig Kielburger showed tremendous empathy at just 12 years old when he learned about child labor practices. Moved by the story of a child laborer who was murdered for speaking out, Craig founded Free The Children (now WE Charity) to fight child labor and promote education globally. His empathy has inspired youth worldwide to make positive change.",
                "persistence": "Nelson Mandela exemplified persistence throughout his 27 years imprisoned for fighting against apartheid in South Africa. Despite this hardship, he maintained his commitment to equality and reconciliation. After his release, he became South Africa's first Black president and continued his work for justice and peace."
            }
            
            response = f"{upstander_info[last_strength]} What inspires you most about this story?"
            options = ["Their courage to stand up", "How they made a difference", "Their commitment to justice"]
            
            return {
                "response": response,
                "options": options,
                "session_data": session_data
            }
        
        elif "apply" in user_input.lower() or "skills" in user_input.lower():
            application_tips = {
                "courage": "You can apply courage in everyday life by speaking up when you witness injustice, even in small situations. Start with your immediate community - stand up for someone being treated unfairly at school or work, correct misinformation when you hear it, or support causes you believe in publicly.",
                "empathy": "Practice empathy daily by actively listening to others without judgment, asking questions to understand different perspectives, and considering how your actions affect those around you. Look for opportunities to include those who may feel marginalized in your community.",
                "persistence": "Apply persistence by identifying a cause you care about and committing to regular, sustained action. Start small, set achievable goals, track your progress, and don't get discouraged by setbacks. Remember that meaningful change takes time."
            }
            
            response = f"{application_tips[last_strength]} Would you like to set a personal upstander goal?"
            options = ["Yes, I'd like to set a goal", "Tell me about local opportunities", "I need time to think about it"]
            
        elif "resources" in user_input.lower() or "learn more" in user_input.lower():
            response = "The Canadian Museum for Human Rights offers various resources for aspiring upstanders. You can explore their website for educational materials, attend workshops and events, or visit the museum in person to learn from their exhibits. Would you like specific recommendations based on your interests?"
            options = ["Online learning resources", "Local events and workshops", "Books and media recommendations"]
        
        else:
            response = "As you continue your upstander journey, remember that small actions can create meaningful change. Your awareness and willingness to engage with these issues is the first step toward making a difference. What area of upstanding interests you most going forward?"
            options = ["Standing up against discrimination", "Supporting vulnerable communities", "Educational advocacy"]
        
        return {
            "response": response,
            "options": options,
            "session_data": session_data
        }
    
    # Add this new handling for the inspiration question responses
    elif current_stage == "inspiration_question":
        last_strength = session_data["strengths"][-1] if session_data["strengths"] else "courage"
        session_data["stage"] = "final"
        session_data["progress"] = 100  # UPDATE PROGRESS TO 100%
        
        # Determine which inspiration aspect they selected
        inspiration_type = ""
        if "courage" in user_input.lower() or "stand up" in user_input.lower():
            inspiration_type = "courage"
        elif "difference" in user_input.lower() or "made a" in user_input.lower():
            inspiration_type = "difference"
        elif "commitment" in user_input.lower() or "justice" in user_input.lower():
            inspiration_type = "commitment"
        else:
            inspiration_type = "difference"  # Default if no match
        
        # Get the detailed inspiration response
        inspiration_response = conversation_stages["inspiration_response"]["message"][last_strength][inspiration_type]
        
        # Add the transition to the final message
        final_transition = "\n\nYou too can make a difference in your community using your own strengths and values."
        
        response = inspiration_response + final_transition
        
        return {
            "response": response,
            "options": ["Thank you for teaching me", "How can I continue my upstander journey?", "Tell me about more upstanders"],
            "session_data": session_data
        }
    
    # Handle final stage
    elif current_stage == "final":
        # ALWAYS ensure progress is 100% for ANY response in final stage
        session_data["progress"] = 100
        
        # Check for specific questions about being an upstander
        if "how" in user_input.lower() and "upstander" in user_input.lower():
            response = """To be an upstander, you can:
1. Speak up when you witness injustice or discrimination
2. Support those who are being marginalized or bullied
3. Learn about human rights issues and educate others
4. Use your specific strengths (courage, empathy, or persistence) to take meaningful action in your community
5. Start small - even simple acts like correcting misinformation or checking in on someone who's excluded can make a difference"""
            
            return {
                "response": response,
                "options": ["How can I get involved locally?", "Tell me about more upstanders", "Are there resources for young upstanders?"],
                "session_data": session_data
            }
        
        # Check for questions about developing skills
        elif ("how" in user_input.lower() and "skill" in user_input.lower()) or ("develop" in user_input.lower()):
            response = """You can develop your upstander skills by:
1. Practicing active listening and empathy in daily interactions
2. Finding opportunities to advocate for others in your school or workplace
3. Joining community groups focused on social justice issues
4. Reading books and watching films about human rights activists
5. Attending workshops or trainings on conflict resolution, ally-ship, and advocacy
6. Reflecting on your actions and seeking feedback on how to improve"""
            
            return {
                "response": response,
                "options": ["Are there online courses?", "How can I practice these skills?", "What organizations can I join?"],
                "session_data": session_data
            }
        
        # Check for questions about getting involved locally
        elif "local" in user_input.lower() or "involved" in user_input.lower() or "community" in user_input.lower():
            response = """To get involved locally, you can:
1. Connect with community organizations working on human rights issues
2. Volunteer at shelters, food banks, or advocacy groups
3. Attend town halls or community meetings to advocate for inclusive policies
4. Start or join clubs at your school or workplace focused on social justice
5. Organize awareness events or fundraisers for causes you care about"""
            
            return {
                "response": response,
                "options": ["How else can I help?", "Tell me about more upstanders", "Restart my journey"],
                "session_data": session_data
            }
        
        # Default final response for any other input
    else:
            response = "Your Upstander journey doesn't end here. You can continue to develop your skills and make a difference in your community every day. The Canadian Museum for Human Rights offers workshops, events, and online resources to help you grow as an upstander. What specific aspect would you like to learn more about?"
            
            return {
                "response": response,
                "options": ["How to be an upstander at school", "Finding local opportunities", "Resources for upstanders"],
                "session_data": session_data
            }
    

    
    # Default response if all else fails
    return {"response": "I'm here to help with the Upstander Program. Ask me about upstanders, UAP locations, or how to identify your strengths.", "session_data": session_data}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        session_data = request.json.get('session_data', None)
        print(f"User input: {user_input}")
        print(f"Session data before: {session_data}")
        
        if not user_input:
            return jsonify({"response": "Please provide a message."})
        
        result = get_response(user_input, session_data)
        
        # CRITICAL: Make sure progress is explicitly set to 100% if we're in final stage
        if result.get('session_data', {}).get('stage') == 'final':
            result['session_data']['progress'] = 100
            print("ENFORCING 100% progress for final stage")
        
        print(f"Result after: {result}")
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"response": "An error occurred while processing your request. Please try again."})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    # Check if Hugging Face token is available
    if not HF_API_TOKEN:
        print("Warning: No Hugging Face API token set. Using rule-based responses only.")
        print("To use AI responses, create a .env file with HF_API_TOKEN=your_token")
    else:
        print("Hugging Face API token found. AI responses are enabled.")
    
    app.run(debug=True, port=5002) 
