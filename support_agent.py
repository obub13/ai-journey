import os
import anthropic
from dotenv import load_dotenv

load_dotenv()


ticket = input("Please enter the customer's support ticket: ")

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
try:
    messages = [{"role": "user", "content": ticket}]
    thinking = True;
    while thinking:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="""You are a support agent. First decide if you have enough information to solve the ticket. If If not, respond with ONLY: NEED_INFO: [one specific question]. If you have enough info, respond with ONLY: RESOLVED: [your answer]""",
            messages=messages,
        )
        response = message.content[0].text

        if response.startswith("NEED_INFO:"):
            # extract the question and ask user for more info
            question = response.replace("NEED_INFO:", "").strip()
            followup = input(f"\nClaude needs more info: {question}\nYour answer: ")
            # add claude question to messages
            messages.append({"role":"assistant", "content": response})
            # add user answer to messages
            messages.append({"role":"user", "content": followup})
            
            # # then send again with full context
            # message = client.messages.create(
            #     model="claude-haiku-4-5-20251001",
            #     max_tokens=1024,
            #     system="""You are a support agent. First decide if you have enough information to solve the ticket. If If not, respond with ONLY: NEED_INFO: [one specific question]. If you have enough info, respond with ONLY: RESOLVED: [your answer]. Answer respectfully and professionally, with a human-like tone.""",
            #     messages=[
            #         {
            #             "role": "user",
            #             "content": f"{ticket}\nCustomer's answer to follow-up question: {followup}",
            #         }
            #     ],
            # )
            # print(message.content[0].text)
        elif response.startswith("RESOLVED:"):
            print(response.replace("RESOLVED:", "").strip())
            thinking = False


except Exception as e:
    print("Error communicating with Claude API: ", e)
