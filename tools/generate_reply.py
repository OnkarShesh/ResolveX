import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("🚫 GROQ_API_KEY is missing from your .env file")

client = Groq(api_key=GROQ_API_KEY)

def generate_reply(name: str, text: str) -> str:
    prompt = f"""
You are a friendly and professional customer support agent.

Respond to the following issue with empathy, clear explanation, and helpful advice.

Include a greeting using the customer's first name and end the message with:
Best regards,
Customer Support Team

Customer Name: {name}

Issue:
\"\"\"{text}\"\"\"

Only return the final response message.
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # supported model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
            top_p=1
        )

        # ✅ Extract reply text
        reply_text = completion.choices[0].message.content.strip()
        print("📨 Generated Reply:", reply_text)
        return reply_text

    except Exception as e:
        print("⚠️ API call failed in generate_reply.py!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e}")
        return (
            f"Hello {name},\n\n"
            "We are currently unable to process your request. Please try again later.\n\n"
            "Best regards,\n"
            "Customer Support Team"
        )
