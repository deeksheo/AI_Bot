import google.generativeai as genai
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from datetime import datetime
import requests
import re
import urllib.parse

api_key = "AIzaSyAWgr-yS0TDrLg0ugyPZMLjYYDG0B67FhI"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(prompt):
    try:
        if "date" in prompt.lower():
            return datetime.now().strftime("Today is %A, %d %B %Y.")
        if "weather" in prompt.lower():
            city = extract_city_from_prompt(prompt)
            if city:
                return get_weather(city)
            else:
                return "Please provide a city name to get the weather."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Oops! I'm experiencing a glitch. Error: {str(e)}"

def extract_city_from_prompt(prompt):
    pattern = r"weather in ([A-Za-z\s]+)"
    match = re.search(pattern, prompt, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def get_weather(city):
    api_key = "f729abaa1187108ea98ea4c46471962a"
    city_encoded = urllib.parse.quote(city)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={api_key}&units=metric"
    print(f"Request URL: {url}")  # Debugging line to check the request URL
    response = requests.get(url).json()

    # Debugging: Print the response for better clarity
    print(f"Response: {response}")

    if response.get("cod") != 200:
        error_message = response.get("message", "Unknown error.")
        return f"Could not fetch weather information for {city}. Error: {error_message}. Please check the city name or try again later."
    
    main = response["main"]
    weather = response["weather"][0]["description"]
    temp = main["temp"]
    return f"The weather in {city} is {weather} with a temperature of {temp}°C."

class ChatBotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("BOT ChatBot")
        self.setGeometry(100, 100, 600, 400)

        # Chat area (where messages appear)
        self.chat_area = QtWidgets.QTextBrowser(self)
        self.chat_area.setGeometry(10, 10, 580, 300)
        self.chat_area.setStyleSheet("""
            background: linear-gradient(135deg, #f9f9f9, #e1e1e1); 
            color: #444; 
            font-family: 'Roboto', sans-serif; 
            font-size: 14pt; 
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        """)

        # Input field for user message
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setGeometry(10, 320, 480, 40)
        self.input_field.setStyleSheet("""
            font-family: 'Roboto', sans-serif; 
            font-size: 14pt;
            padding: 10px;
            border-radius: 20px;
            background-color: #ffffff;
            color: #333;
            border: 2px solid #ddd;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        """)
        self.input_field.returnPressed.connect(self.send_message)

        # Send button
        self.send_button = QtWidgets.QPushButton("Send", self)
        self.send_button.setGeometry(500, 320, 90, 40)
        self.send_button.setStyleSheet("""
            background: linear-gradient(135deg, #6a82fb, #fc5c7d); 
            color: white; 
            font-family: 'Roboto', sans-serif; 
            font-size: 14pt;
            border: none; 
            border-radius: 25px;
            padding: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background 0.3s ease;
        """)
        self.send_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))  # Pointer on hover
        self.send_button.clicked.connect(self.send_message)

        # Hover effect for the send button
        self.send_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #6a82fb, #fc5c7d);
                color: white;
                font-family: 'Roboto', sans-serif;
                font-size: 14pt;
                border: none;
                border-radius: 25px;
                padding: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: background 0.3s ease;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #fc5c7d, #6a82fb);
            }
        """)

    def display_chat(self, message, color="white"):
        formatted_message = f'<span style="color:{color};">{message}</span>'
        self.chat_area.append(formatted_message)

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            self.display_chat("BOT: You didn't type anything! What's on your mind?", "red")
            return

        self.display_chat(f"You: {user_input}", "cyan")
        self.input_field.clear()

        self.display_chat("BOT is typing...", "green")
        QtCore.QTimer.singleShot(1000, lambda: self.get_bot_response(user_input))

    def get_bot_response(self, user_input):
        bot_response = generate_response(user_input)
        self.display_chat(f"BOT: {bot_response}", "lightgreen")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    chatbot = ChatBotApp()
    chatbot.show()
    sys.exit(app.exec_())

