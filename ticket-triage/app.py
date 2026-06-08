import datetime
import os
from dotenv import load_dotenv
import anthropic
from flask import Flask, redirect, render_template, request
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
                        - When responding in Hebrew, identify the grammatical gender from the ticket in the first sentence and maintain it consistently throughout the entire response. Do not switch gender mid-response.
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
            final_answer = f"<br>Suggested Action: {data['suggested_action'].strip()}<br><br>Draft Reply:<br>{data['draft_reply'].strip()}"

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

        if supabase_data.data and supabase_data.data[0]["ticket_number"] is not None:
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
                "status": "new",
                "timestamp": datetime.datetime.now().isoformat(),
            }
        ).execute()
        count_result = supabase.table("tickets").select("id", count="exact").execute()
        ticket_count = count_result.count
        return render_template(
            "index.html", result=final_answer, ticket_count=ticket_count
        )
    except Exception as e:
        return render_template(
            "index.html", result=f"Something went wrong: {str(e)}", ticket_count=0
        )


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
        return render_template(
            "history.html", result=f"An error occurred on history route: {str(e)}"
        )


# Add a route to update the status of a ticket with a dropdown menu in the history page, options: new, in_progress, resolved, closed


@app.route("/update_status", methods=["POST"])
def update_status():
    ticket_id = request.form["ticket_id"]
    new_status = request.form["status"]
    result = (
        supabase.table("tickets")
        .update({"status": new_status})
        .eq("id", ticket_id)
        .execute()
    )
    return redirect("/history")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
