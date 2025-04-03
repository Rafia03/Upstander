# filepath: /upstander_project/upstander_project/src/utils/conversation_stages.py
from utils import upstander_stories

conversation_stages = {
    "basic_information": {
        "message": "Welcome to the Upstander Project! Let's start with some basic information.",
        "options": ["Start"]
    },
    "assess_strengths_intro": {
        "message": "Let's assess your strengths as an upstander. What qualities do you think you possess?",
        "options": ["Courage", "Empathy", "Persistence"]
    },
    "explain_upstander": {
        "message": "An upstander is someone who takes action to support others and stand up against injustice. Here are criteria of upstander:",
        "options": list(upstander_stories.upstander_stories.keys())  # Show upstander names as options
    },
    "identify_upstander": {
        "message": "Can you think of a person who you consider an upstander? Here are some examples:",
        "options": [story["name"] for category in upstander_stories.upstander_stories.values() for story in category] # Show upstander names as options
    },
    "uap_intro": {
        "message": "The Universal Accountability Principles (UAP) are guidelines that help us understand our responsibilities towards human rights.",
        "options": []
    },
    "final": {
        "message": "Your Upstander journey doesn't end here. You can continue to develop your skills and make a difference in your community every day.",
        "options": ["Continue Learning", "Finish"]
    }
}