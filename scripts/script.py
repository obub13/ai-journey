import json
import requests
from dotenv import load_dotenv
import os

#   DAY 1 - SINGLE TICKET
#
# with open('data.json','r') as file:
#     ticket = json.load(file);

# #Using with keyword is important as its ensures that the file is properly closed after its suite finishes, even if an exception is raised on the way.
# print("Before:", ticket["status"])

# #Updating the status of the ticket
# ticket["status"] = "resolved"
# ticket["resolved_by"] = "Support Agent 1"

# print("After:", ticket["status"])
# with open("data.json", "w") as file:
#     json.dump(ticket, file, indent=4)

# #Warning - write mode ('w') will overwrite the entire file.
# #If you want to update only a specific part of the JSON, you need to read the existing data, modify it, and then write it back to the file.

# print("Ticket updated successfully.")
# print("Updated Ticket:", ticket)

# #Breaking on purpose
# # open("dat.json", "r")
# # print(ticket["statsus"])
# # with open("data.json","r") as file:
# #     json.dump(ticket, file, indent=4)
# # json.dump(ticket, file, indent=4)

#   DAY 2 - MULTIPLE TICKETS
#
# with open("tickets/tickets.json","r") as file:
#     tickets = json.load(file)

# for ticket in tickets:
#     print(ticket["id"], "-", ticket["customer"], "-", ticket["status"])


# open_tickets=0
# resolved_tickets=0

# for t in tickets:
#     if t["status"] == "open":
#         open_tickets += 1
#     elif t["status"] == "resolved":
#         resolved_tickets += 1

# with open("report.txt","w") as file:
#     file.write(f"Open: {open_tickets}\n")
#     file.write(f"Resolved: {resolved_tickets}\n")
# print("Report saved.")


#   DAY 3 - API CALLS
#
load_dotenv()
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
response = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q=Tel Aviv&appid={openweather_api_key}"
)
data = response.json()
print(data)
c_temp = data["main"]["temp"] - 273.15
print(f"Current temperature in Tel Aviv: {c_temp:.2f}°C")

with open("report.txt", "a") as file:
    file.write(f"Current temperature in Tel Aviv: {c_temp:.2f}°C\n")
