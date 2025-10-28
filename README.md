# gemini-chatbot-api 

A powerful Python-based chatbot API powered by Google Gemini with conversation memory and real-time web search capabilities.


## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kathirvel-ux43/gemini-chatbot-api.git
   cd gemini-chatbot-api
   ```

2.Install dependencies
```bash
pip install -r requirements.txt
```
3.Configure API keys
```
*.Google Gemini: https://makersuite.google.com/app/apikey
*.SerpAPI: https://serpapi.com/
```

4.Configure Environment
```bash
# Copy the environment template
cp env.template .env

# Edit .env with your actual API keys
nano .env  # or use any text editor
```
5.Run the Assistant
```bash
python geminiapi.py
```

6.Configuration
Environment Variables
Create a .env file with:
```
-GOOGLE_API_KEY=your_google_gemini_api_key_here
-SERPAPI_KEY=your_serpapi_key_here  
```
###Security Note
Never commit your .env file or share API keys publicly!
### **`requirements.txt`:**
```
google-generativeai>=0.3.0
python-dotenv>=1.0.0
requests>=2.25.0
```

Project Structure
```
gemini-chatbot-api/
├── geminiapi.py          # Main chatbot class
├── search_web.py         # chatbot class
├── requirements.txt      # Python dependencies
├── env.template         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md           # This file

```
## What to Do If You Already Pushed Keys

**If you accidentally pushed keys to GitHub:**

1. **IMMEDIATELY delete the keys** from your provider dashboards
2. **Generate new keys** - invalidate the old ones
3. **Remove the commit from GitHub** (if public)
4. **Check your billing** for any unauthorized usage

##  Safe GitHub Push Commands

```bash
# First, check what will be pushed:
git status

# Only these files should show:
git add geminiapi.py README.md requirements.txt env.template .gitignore

# Verify .env is NOT tracked:
git check-ignore .env

# Then commit and push:
git commit -m "Add Geminiapi ai assistant project"
git push
```
Usage
Basic Commands
```
help     - Show all available commands
history  - View conversation history
clear    - Clear conversation memory
date     - Show current date and time
search   - Force web search for any query
quit     - Exit the application
```

API Usage
Basic Integration
```
from geminiapi import SimpleAIAssistant

# Initialize assistant
assistant = SimpleAIAssistant()

# Single message
response = assistant.chat("Hello, how are you?")
print(response)

# Conversation with memory
response1 = assistant.chat("My favorite color is blue")
response2 = assistant.chat("What's my favorite color?")  # Remembers!
```

```
Security Important Notes
Never commit your .env file with API keys
The chatbot may have usage limits based on your API quotas
Web search requires a valid SerpAPI key
Always check the accuracy of real-time data from primary sources

🤝 Contributing
We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.
-Fork the repository
-Create your feature branch (git checkout -b feature/AmazingFeature)
-Commit your changes (git commit -m 'Add some AmazingFeature')
-Push to the branch (git push origin feature/AmazingFeature)
-Open a Pull Request

Acknowledgments
Google Gemini AI for the powerful AI model
SerpAPI for real-time search capabilities
The Python community for excellent libraries

Enjoy your smart chatbot! 

For questions and support, please open an issue on GitHub.

## 🚀 **GitHub Push Commands:**

```bash
# Initialize git
git init

# Add safe files only
git add geminiapi.py README.md requirements.txt env.template .gitignore

# Commit with new name
git commit -m "feat: Initial commit - Gemini Chatbot API with memory and web search"

# Create repo on GitHub first, then:
git remote add origin https://github.com/kathirvel-ux43/gemini-chatbot-api.git
git branch -M main
git push -u origin main
```
License :
This project is licensed under the MIT License - see the LICENSE file for details.
