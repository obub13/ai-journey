import datetime
import os
from dotenv import load_dotenv
import anthropic
from flask import Flask, render_template, request
from supabase import create_client

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        thinking = True
        while thinking:
            ticket = request.form["ticket"]
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system="""You are a helpful support assistant that analyzes support tickets and provides structured information, answer as a support agent would. no markdowns, no symbols, just plain text.
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
                        "content": f"""Analyze this support ticket - Ticket: {ticket}""",
                    }
                ],
            )
            response = message.content[0].text

            supabase_data = (
                supabase.table("tickets")
                .select("ticket_number")
                .order("ticket_number", desc=True)
                .limit(1)
                .execute()
            )
            print(supabase_data.data)
            if (
                supabase_data.data
                and supabase_data.data[0]["ticket_number"] is not None
            ):
                ticket_number = supabase_data.data[0]["ticket_number"] + 1
            else:
                ticket_number = 1
            # Save the ticket, response, and metadata to Supabase
            supabase.table("tickets").insert(
                {
                    "ticket_number": ticket_number,
                    "issue": ticket,
                    "final_answer": response,
                    "status": "resolved",
                    "timestamp": datetime.datetime.now().isoformat(),
                }
            ).execute()
            return render_template("index.html", result=response)

            ##Agent loop logic - if claude needs more info, ask user for more info and then send again with full context, if claude is resolved, return the answer
            # if response.startswith("NEED_INFO:"):
            #     # extract the question and ask user for more info
            #     question = response.replace("NEED_INFO:", "").strip()
            #     followup = input(f"\nClaude needs more info: {question}\nYour answer: ")
            #     # add claude question to messages
            #     messages.append({"role": "assistant", "content": response})
            #     # add user answer to messages
            #     messages.append({"role": "user", "content": followup})
            # elif response.startswith("RESOLVED:"):
            #     print(response.replace("RESOLVED:", "").strip())
            # return ticket  # just returning it for now to test
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
