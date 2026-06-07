import datetime
import os
from dotenv import load_dotenv
import anthropic
from flask import Flask, render_template, request
from supabase import create_client
import json as json_lib

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app = Flask(__name__)


@app.route("/")
def index():
    result = supabase.table("tickets").select("id", count="exact").execute()
    ticket_count = result.count
    return render_template("index.html", ticket_count=ticket_count)


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        thinking = True
        while thinking:
            ticket = request.form["ticket"]
            if ticket == "":
                return render_template(
                    "index.html", result="Please enter a support ticket to analyze."
                )
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system="""You are a support ticket analyzer. Analyze the ticket and respond with ONLY a valid JSON object, nothing else. No markdown, no extra text.
                        {
                            "issue_type": "Permission|Expense Report|Accounting|Interface|Other",
                            "urgency": "Low|Medium|High",
                            "suggested_action": "what to check or do first",
                            "draft_reply": "a helpful human response to send back"
                        }

                        IMPORTANT:
                        - issue_type and urgency must always be in English
                        - suggested_action and draft_reply must be in the SAME LANGUAGE as the ticket
                        - Never promise specific timelines
                        - draft_reply must sound human, no markdown, no bold, no symbols
                        - If issue is unclear, ask for more details in draft_reply
                        - Return ONLY the JSON object, no code blocks, no backticks
                        """,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze this support ticket - Ticket: {ticket}""",
                    }
                ],
            )
            response = message.content[0].text
            clean_response = response.strip()
            if "```" in clean_response:
                clean_response = clean_response.split("```")[1]
                clean_response = clean_response.replace("json", "", 1).strip()

            try:
                data = json_lib.loads(clean_response.strip())
                issue_type = data["issue_type"]
                urgency = data["urgency"]
                final_answer = f"Issue Type: {data['issue_type'].strip()}<br>Urgency: {data['urgency'].strip()}<br>Suggested Action: {data['suggested_action'].strip()}<br><br>Draft Reply:<br>{data['draft_reply'].strip()}"

            except:
                issue_type = "Other"
                urgency = "Medium"
                final_answer = response
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
                    "final_answer": final_answer,
                    "issue_type": issue_type,
                    "urgency": urgency,
                    "status": "resolved",
                    "timestamp": datetime.datetime.now().isoformat(),
                }
            ).execute()
            count_result = (
                supabase.table("tickets").select("id", count="exact").execute()
            )
            ticket_count = count_result.count
            return render_template(
                "index.html", result=final_answer, ticket_count=ticket_count
            )

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
        return f"An error occurred on analyze route: {str(e)}"


@app.route("/history")
def history():
    try:
        result = (
            supabase.table("tickets")
            .select("*")
            .order("ticket_number", desc=True)
            .execute()
        )
        tickets = result.data
        return render_template("history.html", tickets=tickets)
    except Exception as e:
        return f"An error occurred on history route: {str(e)}"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
