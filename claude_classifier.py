import json
import os
from dotenv import load_dotenv
import anthropic

# Loads environment variables from a .env file into the system's environment variables.
# This allows you to keep sensitive information, such as API keys, out of your code and easily manage them in a separate file.
load_dotenv()

# setting client var to interact with anthropic api using the API key stored in the .env file.
client = anthropic.Anthropic(api_key=os.getenv("claude_api_key"))

# This code reads a JSON file containing support tickets, selects the first ticket, and sends its issue description to the Claude API for classification into one of three categories: Technical Issue, Billing Issue, or General Inquiry.
# The response from the API is printed, which includes the category and a one-sentence reason for the classification.
with open("tickets/tickets.json", "r") as file:
    tickets = json.load(file)


# ticket = tickets[0]

for ticket in tickets:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Classify this support ticket into one of the categories: Technical Issue, Billing Issue, General Inquiry. \n\n Ticket:{ticket['issue']} \n\n Always respond in this exact format: Category - Reason. One line only..",
            }
        ],
    )
    print(f"{ticket['id']} - {ticket['customer']}: {message.content[0].text}")
    print("---")
