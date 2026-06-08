import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

ticket_text = input("Paste your ticket and press Enter \n")
print("\nAnalyzing...\n")

# Send ticket to Claude with structured prompt asking for analysis
try:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system="""You are a helpful support assistant that analyzes support tickets and provides structured information,
            1. Issue Type : (What type of issue is this? Examples: Permission / Expense report / Accounting/ Interface / Other)
            2. Urgency: (How urgent is this issue? Low / Medium / High)
            3. Suggested Action: (What should I check or do first to resolve this issue?)
            4. Draft Reply: (Write a helpful response to send back to the customer, be empathetic and polite, with human-like conversational tone, no AI-sounding text. Do not use markdown formatting, bold, or special symbols in the draft reply.)
            IMPORTANT:
            - Always ask for more details if the issue is not clear.
            - Respond in the SAME LANGUAGE as the ticket (Hebrew tickets get Hebrew responses)
            - Never promise specific timelines, use "as soon as possible"
            """,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze this support ticket - Ticket: {ticket_text}""",
            }
        ],
    )
    print(message.content[0].text)
except Exception as e:
    print("Error communicating with Claude API: ", e)


#### Day 8 Explaining the system ###
""" In our message = client.messages.create(...
There can be multiple roles in the messages array - the most common are "system" and "user".
Role: system - sets the rules and instructions for the AI, this is where you can define the behavior and constraints of the model.

EXAMPLE SYSTEM PROMPT:

"role": "system",
"content": "You are a helpful assistant that classifies support tickets into categories.
            Always respond with only the category name: Technical Issue, Billing Issue, or General Inquiry.
            Do not provide any explanations or additional text."

Without system prompt the model is generic, with it model follows the rules

Role: user - this is the input from the user, in our case the ticket issue description.
This is where you provide the specific content that you want the model to analyze or respond to.

Max_tokens - controls how long the model's response can be -
More tokens = Longer reponse , costs more
Fewer tokens = Shorter response, costs less.

Temperature -controls creativity vs consistency of the model's responses, ranges from 0.0 to 2.0
Lower temperature (e.g., 0.2) = More focused and deterministic responses, good for tasks that require accuracy and consistency.
Higher temperature (e.g., 0.8) = More creative and varied responses, good for brainstorming or creative writing.
 """
