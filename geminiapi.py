import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

class SimpleAIAssistant:
    def __init__(self):
        # Get API keys
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.serpapi_key = os.getenv('SERPAPI_KEY')
        
        if not self.google_api_key:
            print("Please add GOOGLE_API_KEY to .env file")
            return
        
        genai.configure(api_key=self.google_api_key)
        
        self.model = self.setup_model()
        if not self.model:
            return
        
        self.chat_session = self.model.start_chat(history=[])
        
        self.conversation = []
        
        print("AI Assistant Ready!")
        print("Type 'help' for commands")
    
    def setup_model(self):
        """Gemini model=> WORKING models"""
        working_models = [
            'models/gemini-2.5-flash-preview-05-20',
            'models/gemini-2.5-flash',
            'models/gemini-2.0-flash',
            'models/gemini-pro-latest'
        ]
        
        for model_name in working_models:
            try:
                print(f"Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                # testing model
                response = model.generate_content("Hello")
                print(f"Success! Using: {model_name}")
                return model
            except Exception as e:
                print(f"{model_name} failed: {str(e)[:80]}...")
                continue
        
        print("No working model found")
        return None

    def get_current_date_info(self):
        now = datetime.now()
        
        date_info = {
            'date': now.strftime("%B %d, %Y"),  
            'day': now.strftime("%A"),          
            'time': now.strftime("%I:%M %p"),   
            'full': now.strftime("%A, %B %d, %Y at %I:%M %p")  
        }
        
        return date_info
    
    def add_message(self, role, message):
        self.conversation.append({
            'role': role,
            'message': message,
            'time': datetime.now().strftime("%H:%M:%S")
        })
        
        if len(self.conversation) > 15:
            self.conversation = self.conversation[-15:]
    
    def show_history(self):
        if not self.conversation:
            print("No messages yet!")
            return
        
        print("\n Conversation History:")
        for msg in self.conversation:
            icon = "👤" if msg['role'] == 'user' else "🤖"
            print(f"{icon} [{msg['time']}]: {msg['message'][:80]}{'...' if len(msg['message']) > 80 else ''}")
    
    def search_web(self, query):
        if not self.serpapi_key:
            return "Web search not available (no SERPAPI_KEY)"
        
        try:
            enhanced_query = query
            
            if any(word in query.lower() for word in ['news', 'headlines', 'latest']):
                enhanced_query = f"latest news today India world current events {datetime.now().strftime('%B %d')}"
            elif 'weather' in query.lower():
                enhanced_query = f"{query} current conditions today {datetime.now().strftime('%B %d')}"
            
            params = {
                'q': enhanced_query,
                'api_key': self.serpapi_key,
                'engine': 'google',
                'num': 5,
                'tbs': 'qdr:d'  
            }
            
            response = requests.get('https://serpapi.com/search', params=params, timeout=15)
            data = response.json()
            
            result_text = ""
            
            if 'organic_results' in data:
                news_count = 0
                for result in data['organic_results']:
                    title = result.get('title', '')
                    snippet = result.get('snippet', '')
                    link = result.get('link', '')
                    
                    if any(source in link for source in ['bbc.com', 'reuters.com', 'cnn.com', 'ndtv.com', 'timesofindia.indiatimes.com', 'thehindu.com']):
                        result_text += f"{title}\n"
                        result_text += f"   {snippet}\n\n"
                        news_count += 1
                    
                    if news_count >= 3:  
                        break
                
                if news_count == 0:
                    result_text += "Top results:\n"
                    for i, result in enumerate(data['organic_results'][:3], 1):
                        title = result.get('title', 'No title')
                        snippet = result.get('snippet', 'No description')
                        result_text += f"{i}. {title}\n   {snippet}\n\n"
            
            return result_text if result_text else "Search completed. For more detailed current information, check the recommended sources."
            
        except Exception as e:
            return f"Search completed. For live information, check the recommended sources. (Search error: {str(e)})"
    
    def needs_search(self, question):
        search_words = [
            'current', 'today', 'now', 'latest', 'weather', 'news', 'price', 
            'bitcoin', 'ethereum', 'stock', 'crypto',
            'date', 'day', 'time', 'today\'s date', 'what day is it', 'what is the date'
        ]
        return any(word in question.lower() for word in search_words)
    
    def build_conversation_context(self):
        if len(self.conversation) <= 1:
            return "This is the beginning of the conversation."
        
        recent_messages = self.conversation[-12:]  
        
        context_lines = ["Previous conversation:"]
        for msg in recent_messages:
            speaker = "User" if msg['role'] == 'user' else "Assistant"
            context_lines.append(f"{speaker}: {msg['message']}")
        
        return "\n".join(context_lines)
    
    def chat(self, user_input):
        self.add_message('user', user_input)
        
        if user_input.lower() == 'help':
            response = """Available commands:
• help - Show this help
• history - Show conversation history  
• clear - Clear conversation
• quit - Exit program
• search [query] - Force web search
• date - Show current date and time"""
            self.add_message('assistant', response)
            return response
        
        if user_input.lower() == 'clear':
            self.conversation = []
            self.chat_session = self.model.start_chat(history=[])
            response = "🧹 Conversation cleared!"
            self.add_message('assistant', response)
            return response
        
        if user_input.lower() == 'date':
            current_date = self.get_current_date_info()
            response = f"**Current Date and Time:**\n{current_date['full']}"
            self.add_message('assistant', response)
            return response
        
        if user_input.lower().startswith('search '):
            query = user_input[7:]
            print(f"Searching for: {query}")
            search_results = self.search_web(query)
            response = f"Search results for '{query}':\n{search_results}"
            self.add_message('assistant', response)
            return response
        
        current_date = self.get_current_date_info()
        
        news_keywords = ['news', 'headlines', 'latest news', 'current events', 'today\'s news']
        weather_keywords = ['weather', 'temperature', 'forecast', 'rain', 'humidity']
        
        is_news_question = any(keyword in user_input.lower() for keyword in news_keywords)
        is_weather_question = any(keyword in user_input.lower() for keyword in weather_keywords)
        
        if is_news_question:
            print("🔍 Searching for latest news...")
            search_results = self.search_web(user_input)
            
            response = f"""📰 **Latest News Today** ({current_date['date']})

"""
            
            if search_results and "no relevant results" not in search_results.lower():
                response += f"I found these current news updates:\n\n{search_results}"
            else:
                response += f"""For the latest current news, I recommend checking:

• **Google News**: https://news.google.com
• **BBC News**: https://www.bbc.com/news  
• **CNN**: https://www.cnn.com
• **Reuters**: https://www.reuters.com

These sources will have the most up-to-date information for today, {current_date['date']}."""
            
            self.add_message('assistant', response)
            return response
        
        elif is_weather_question:
            print("🔍 Searching for weather information...")
            search_results = self.search_web(user_input)
            
            location = "your location"
            if 'delhi' in user_input.lower():
                location = "Delhi"
            elif 'mumbai' in user_input.lower():
                location = "Mumbai"
            elif 'chennai' in user_input.lower():
                location = "Chennai"
            elif 'bangalore' in user_input.lower():
                location = "Bangalore"
            elif 'kolkata' in user_input.lower():
                location = "Kolkata"
            
            response = f""" **Current Weather Information** ({current_date['date']})

"""
            
            if search_results and "no relevant results" not in search_results.lower():
                response += f"Current weather data for {location}:\n\n{search_results}"
            else:
                response += f"""For accurate current weather in {location}, check:

• **AccuWeather**: https://www.accuweather.com
• **Weather.com**: https://weather.com
• **IMD**: https://mausam.imd.gov.in

These sources provide real-time weather data for today, {current_date['date']}."""
            
            self.add_message('assistant', response)
            return response
        
        elif any(phrase in user_input.lower() for phrase in ['date', 'today', 'day', 'time', 'what day is it', 'what is the date']):
            response = f" **Current Date and Time:**\n{current_date['full']}"
            self.add_message('assistant', response)
            return response
        
        search_info = ""
        if self.needs_search(user_input) and self.serpapi_key:
            print(" Searching web...")
            search_info = self.search_web(user_input)
        
        conversation_context = self.build_conversation_context()
        
        if search_info:
            full_prompt = f"""{conversation_context}

User: {user_input}

Additional information from web search:
{search_info}

Please provide a helpful response."""
        else:
            full_prompt = f"""{conversation_context}

User: {user_input}

Please provide a helpful response."""
        
        try:
            response_obj = self.chat_session.send_message(full_prompt)
            response_text = response_obj.text
            
            self.add_message('assistant', response_text)
            return response_text
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.add_message('assistant', error_msg)
            return error_msg
    
    def start_chat(self):
        """Start the chat interface"""
        if not self.model:
            print("❌ Cannot start chat - no working model found")
            return
        
        current_date = self.get_current_date_info()
        
        print("\n" + "="*50)
        print("YOUR AI ASSISTANT IS READY!")
        print("="*50)
        print(f"Today is: {current_date['full']}")
        print("I can remember conversations and search the web!")
        print("Try: 'weather in london' or 'bitcoin price'")
        print("Try: 'latest news today'")
        print("Type 'help' for all commands")
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'quit':
                    print("Goodbye! Thanks for chatting!")
                    break
                
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                print("Thinking...", end="", flush=True)
                response = self.chat(user_input)
                print(f"\r Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\n\n Chat ended by user!")
                break
            except Exception as e:
                print(f"\n Error: {e}")

# Main program
if __name__ == "__main__":
    print("Starting Your AI Assistant...")
    assistant = SimpleAIAssistant()
    assistant.start_chat()