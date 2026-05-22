import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

ticket_text = input("Paste your ticket and press Enter \n")
print("\nAnalyzing...\n")

# Send ticket to Claude with structured prompt asking for analysis
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": f"""Analyze this support ticket and prove:
            1. Issue Type: (Permission / Expense report / Accounting/ Interface / Other)
            2. Urgency: (Low / Medium / High)
            3. Suggested Action: (What should I check or do first)
            4. Draft Reply: (A helpful response to send back)
            
            Ticket: {ticket_text}
            
            IMPORTANT: 
            - Always ask for more details if the issue is not clear.
            - Respond in the SAME LANGUAGE as the ticket (Hebrew tickets get Hebrew responses)
            - Never promise specific timelines, use "as soon as possible"
            - In the draft reply: NO markdown formatting, NO bold (**), NO special symbols
            - Write naturally like a real support person, not AI-generated text, always be polite and empathetic in the response.
            - Keep draft reply conversational and human""",
        }
    ],
)

print(message.content[0].text)
