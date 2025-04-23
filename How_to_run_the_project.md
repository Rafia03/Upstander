# How to Run the Project

## System Requirements
- Operating System: macOS (tested on macOS 24.3.0), Windows 10/11
- Python 3.8 or higher
- Web browser (Chrome recommended)

## Initial Setup

1. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd Upstander-main
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Required Packages**
   ```bash
   pip install flask flask-cors flask-session pandas requests python-dotenv google-generativeai
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the project root with the following content:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   FLASK_ENV=development
   FLASK_APP=app.py
   ```

   Note: You'll need to obtain a Gemini API key from https://makersuite.google.com/app/apikey

## Running the Application

1. **Start the Flask Server**
   ```bash
   cd Phase\ 3/developed_version
   flask run
   ```

2. **Access the Application**
   - Open your web browser
   - Navigate to `http://localhost:5002`

## Project Structure

```
Upstander-main/
├── Phase 1/              # Research and planning documentation
├── Phase 2/              # Initial development and prototyping
├── Phase 3/              # Refinement and feature expansion
│   └── developed_version/ # Current working version
│       ├── src/          # Source code
│       │   ├── app.py    # Flask backend
│       │   ├── index.html # Frontend interface
│       │   └── utils/    # Utility functions
│       └── requirements.txt
├── Phase 4/              # Testing and finalization
└── README.md             # Project overview
```

## Key Features

1. **AI-Driven Chatbot**
   - Uses Google's Gemini 2.0 Flash model
   - Provides personalized responses
   - Handles conversation flow through different stages

2. **Strength Assessment**
   - Interactive strength evaluation
   - Three core strengths: Courage, Empathy, Persistence
   - Visual feedback and progress tracking

3. **Upstander Stories**
   - Integration with historical figures
   - Personalized story matching
   - Educational content delivery

## Chatbot Design Principles

1. **Defined Persona**: Establishing a specific attitude and communication style for the chatbot.

2. **Operational Rules**: Implementing clear guidelines the chatbot must follow.

3. **Adaptive Prompting**: Using selective and multi-stage prompts, where the instructions given to the AI change based on the user's choices or the current stage of the conversation.

4. **Guided Interaction**: Providing users with options or suggestions to steer the conversation effectively.

5. **Hybrid Response Strategy**: Combining pre-defined (default) answers for guaranteed accuracy on specific topics with AI-generated responses to maintain a natural and appropriate conversational tone.

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 for Python code
   - Use meaningful variable and function names
   - Include comments for complex logic

2. **Adding New Features**
   - Create a new branch for feature development
   - Update documentation as needed
   - Test thoroughly before merging

3. **Testing**
   - Test the application in different browsers
   - Verify AI responses and conversation flow
   - Check mobile responsiveness

## Troubleshooting

1. **Common Issues**
   - If the server fails to start, ensure all dependencies are installed
   - Check that the Gemini API key is valid
   - Verify the virtual environment is activated

2. **Error Messages**
   - "Module not found": Run `pip install -r requirements.txt`
   - "Invalid API key": Update the `.env` file with a valid Gemini API key
   - "Port already in use": Use a different port with `flask run --port 5003`

## Maintenance

1. **Regular Updates**
   - Keep dependencies updated
   - Monitor Gemini API usage and limits
   - Backup important data

2. **Security**
   - Never commit API keys to version control
   - Keep the `.env` file in `.gitignore`
   - Regularly update security patches


