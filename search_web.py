def search_web(self, query):
    """Search the web for current info with better weather handling"""
    if not self.serpapi_key:
        return "Web search not available (no SERPAPI_KEY)"
    
    try:
        # Enhanced query for weather searches
        enhanced_query = query
        
        # Improve weather-related searches
        if any(word in query.lower() for word in ['weather', 'rainfall', 'temperature', 'forecast']):
            # Add "today" and location context
            if 'delhi' in query.lower():
                enhanced_query = f"Delhi weather today current temperature rainfall {datetime.now().strftime('%Y-%m-%d')}"
            elif any(loc in query.lower() for loc in ['tamilnadu', 'chennai', 'mumbai', 'kolkata', 'bangalore']):
                enhanced_query = f"{query} today current {datetime.now().strftime('%Y-%m-%d')}"
            else:
                enhanced_query = f"{query} today {datetime.now().strftime('%Y-%m-%d')}"
        
        params = {
            'q': enhanced_query,
            'api_key': self.serpapi_key,
            'engine': 'google',
            'num': 5  # Get more results
        }
        
        print(f"🔍 Searching: {enhanced_query}")
        response = requests.get('https://serpapi.com/search', params=params)
        data = response.json()
        
        # Try to extract weather-specific data first
        weather_data = self.extract_weather_info(data, query)
        if weather_data:
            return weather_data
        
        # Fallback to general results
        result_text = ""
        
        # Get direct answer if available
        if 'answer_box' in data:
            answer_box = data['answer_box']
            if 'answer' in answer_box:
                result_text += f"🌤️ Direct Answer: {answer_box['answer']}\n\n"
            elif 'temperature' in answer_box:
                result_text += f"🌡️ Temperature: {answer_box['temperature']}\n\n"
            elif 'precipitation' in answer_box:
                result_text += f"🌧️ Precipitation: {answer_box['precipitation']}\n\n"
        
        # Get top results
        if 'organic_results' in data:
            result_text += "📰 Top Results:\n"
            for i, result in enumerate(data['organic_results'][:3], 1):
                title = result.get('title', 'No title')
                snippet = result.get('snippet', 'No description')
                link = result.get('link', '')
                
                # Highlight weather-related results
                if any(word in title.lower() + snippet.lower() for word in ['weather', 'temperature', 'rain', 'forecast']):
                    result_text += f"🌤️ {i}. {title}\n   {snippet}\n\n"
                else:
                    result_text += f"{i}. {title}\n   {snippet}\n\n"
        
        return result_text if result_text else "No relevant results found for this specific query"
        
    except Exception as e:
        return f"Search error: {str(e)}"

def extract_weather_info(self, data, original_query):
    """Extract weather-specific information from search results"""
    try:
        weather_info = ""
        
        # Check knowledge graph for weather data
        if 'knowledge_graph' in data:
            kg = data['knowledge_graph']
            if 'weather' in kg:
                weather_info += "🌤️ Weather Information:\n"
                if 'temperature' in kg['weather']:
                    weather_info += f"🌡️ Temperature: {kg['weather']['temperature']}\n"
                if 'precipitation' in kg['weather']:
                    weather_info += f"🌧️ Precipitation: {kg['weather']['precipitation']}\n"
                if 'humidity' in kg['weather']:
                    weather_info += f"💧 Humidity: {kg['weather']['humidity']}\n"
                if 'forecast' in kg['weather']:
                    weather_info += f"📊 Forecast: {kg['weather']['forecast']}\n"
                weather_info += "\n"
                return weather_info
        
        # Look for specific weather data in organic results
        if 'organic_results' in data:
            for result in data['organic_results']:
                title = result.get('title', '').lower()
                snippet = result.get('snippet', '').lower()
                
                # Look for weather mentions
                if any(word in title + snippet for word in ['weather', 'temperature', '°c', '°f', 'humidity', 'rain']):
                    if any(location in title + snippet for location in ['delhi', 'new delhi', 'india']):
                        weather_info += f"🌤️ Weather Update:\n"
                        weather_info += f"📰 {result.get('title', 'Title')}\n"
                        weather_info += f"   {result.get('snippet', 'Description')}\n\n"
                        return weather_info
        
        return None
        
    except Exception as e:
        return None