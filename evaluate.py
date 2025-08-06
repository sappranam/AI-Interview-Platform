import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use light-weight model to avoid quota issues
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Load transcript
with open("transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

# Extract Q&A pairs
qa_pairs = re.findall(r"Q(\d+): (.*?)\nA\1: (.*?)(?=\nQ\d+:|$)", transcript, re.DOTALL)

# Evaluate each answer
report_lines = []
for idx, (num, question, answer) in enumerate(qa_pairs, 1):
    print(f" Evaluating Q{idx}...")
    prompt = f"""
You are an AI interview evaluator.

Evaluate the candidate's answer to the following technical interview question. Score out of 10 and provide concise, constructive feedback.

Question: {question.strip()}
Answer: {answer.strip()}

Respond only in this format:

Score: <x>/10
Feedback: <detailed feedback>
"""
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
    except Exception as e:
        result = f"Score: 0/10\nFeedback: Evaluation failed due to error: {e}"

    report_lines.append(f"Q{idx} Evaluation:\n{result}\n")

# Save the report
with open("report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print("\n All answers evaluated. Report saved as 'report.txt'")
