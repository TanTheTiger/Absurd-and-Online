from flask import Flask, render_template, request, jsonify, redirect
import pyttsx3
import webbrowser
import random
import google.generativeai as genai
import threading

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyAaDAw7s8B9_llgrbMBL_B1vUroz6Lk76Y"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro")

def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
    thread = threading.Thread(target=run)
    thread.start()
    return text

def get_roast(user_input):
    try:
        if random.random() < 0.2:
            actions = [
                ("This might help! bozo", lambda: webbrowser.open("https://www.yountube.com/watch?v=xvFZjo5PgG0")),
                ("Dont you go to school?, give me your teachers number! ", lambda:None)
            ]
            action_text, action = random.choice(actions)
            if action:
                action()
            return action_text
        
        response = model.generate_content(f"Roast me hard on {user_input}")
        roast_text = response.text if response.text else "Lucky Sea Dog, You have been saved by my roasts!"
        return roast_text
    except Exception:
        return "Aw Shucks, something went wrong!"

@app.route("/")
def index():
    return redirect("/login")
    

@app.route("/roast", methods=["POST", "GET"])
def roast():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        roast_response = get_roast(user_input)
        speak(roast_response)
        return jsonify({"response": roast_response})
    
    return render_template("roast.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect("/roast")
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
