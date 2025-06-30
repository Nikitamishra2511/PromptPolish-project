from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Load the .env file where your OpenAI key is stored
load_dotenv()

app = Flask(__name__)

# Read OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    prompt_output = ""
    
    if request.method == "POST":
        user_input = request.form["prompt"]
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a prompt engineer assistant. Make this prompt clearer, more effective, and more structured."},
                    {"role": "user", "content": user_input}
                ]
            )
            prompt_output = response['choices'][0]['message']['content']
        
        except Exception as e:
            prompt_output = f"Error: {e}"

    return render_template("index.html", prompt_output=prompt_output)

if __name__ == "__main__":
    app.run(debug=True)
