<<<<<<< HEAD
# My AI Assistant 🤖

A Python-based AI assistant with conversation memory and real-time web search.

## 🚀 Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/kathirvel-ux43/gemini-chatbot-api
   cd gemini-chatbot-api
   ```

2.Install dependencies
```bash
pip install -r requirements.txt
```
3.Get API Keys
-Google Gemini: https://makersuite.google.com/app/apikey
-SerpAPI: https://serpapi.com/

4.Configure Environment
```bash
cp env.template .env
```
5.Run the Assistant
```bash
python geminiapi.py
```
###Security Note
Never commit your .env file or share API keys publicly!
### **`requirements.txt`:**
google-generativeai>=0.3.0
python-dotenv>=1.0.0
requests>=2.25.0


## 🛡️ What to Do If You Already Pushed Keys

**If you accidentally pushed keys to GitHub:**

1. **IMMEDIATELY delete the keys** from your provider dashboards
2. **Generate new keys** - invalidate the old ones
3. **Remove the commit from GitHub** (if public)
4. **Check your billing** for any unauthorized usage

## 🎯 Safe GitHub Push Commands

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

Project Structure
```
=======
# gemini-chatbot-api
AI chatbot with web search capabilities using SERP API and Google Gemini AI
>>>>>>> 7d3192a5d508079674b191b50de60c97396431bd
