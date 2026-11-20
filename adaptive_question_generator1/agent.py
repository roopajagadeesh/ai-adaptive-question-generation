from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Groq(
    api_key=os.getenv("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")
)

MODEL = "openai/gpt-oss-20b"

def generate_questions(subject, topic, difficulty, number):

    prompt = f"""
Generate exactly {number} multiple choice questions.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

Return ONLY JSON.

Example:

[
  {{
    "question":"What is Python?",
    "options":["Language","Animal","Car","Game"],
    "answer":"Language",
    "explanation":"Python is a programming language."
  }}
]

Rules:
- 4 options
- Correct answer must match one option
- No markdown
- No extra text
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"user","content":prompt}
        ],
        temperature=0.3
    )

    text = response.choices[0].message.content.strip()

    text = re.sub(r"```json|```", "", text).strip()

    return json.loads(text)