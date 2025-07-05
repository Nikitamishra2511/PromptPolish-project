from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Load the .env file where your OpenAI key is stored
load_dotenv()

app = Flask(__name__)

# Read OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Refined system prompt for robust prompt engineering
SYSTEM_PROMPT = (
    "You are an elite prompt engineer. "
    "When a user submits a prompt, always rewrite it for these outcomes:\n"
    "- Maximum clarity and specificity\n"
    "- Add missing context or background if needed, but only the minimum to make the prompt work (never assume or invent details)\n"
    "- Assign a role to the AI (e.g., 'You are a marketing expert') if appropriate\n"
    "- Use step-by-step instructions or numbered lists for complex asks\n"
    "- Explicitly request output format if useful (e.g., table, summary, code block)\n"
    "- Ask for chain-of-thought or show-your-work reasoning when relevant\n"
    "- Fix any ambiguity or vague wording, but flag it instead of inventing details\n"
    "\n"
    "Strict rules:\n"
    "- Do NOT change the intent, tone, or meaning of the original prompt\n"
    "- Do NOT optimize, marketize, summarize, embellish, or make the prompt sound more impressive or professional than the user's real ask\n"
    "- Preserve all factual, emotional, and stylistic nuance from the user's input\n"
    "- Retain any informality, casual style, or technical level\n"
    "- If you are unsure about any ambiguity, flag it, but do NOT infer or invent details\n"
    "\n"
    "Your job is to make the prompt clear, actionable, and well-structured—without making it 'better' or different from what the user truly wants."
)

@app.route("/", methods=["GET", "POST"])
def index():
    prompt_output = ""
    
    if request.method == "POST":
        user_input = request.form["prompt"]
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Polish this prompt for best results: {user_input}"}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            prompt_output = response['choices'][0]['message']['content'].strip()
        
        except Exception as e:
            prompt_output = f"Error: {e}"

    return render_template("index.html", prompt_output=prompt_output)
