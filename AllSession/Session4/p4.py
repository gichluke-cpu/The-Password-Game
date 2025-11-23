import re

pattern = r'(\w+)@(\w+\.\w+)'# #Matches email addresses and captures the username and domain separately

text = "Contact us at info@example.com or support@Website.org" 
matches = re.findall (pattern, text, flags=re.IGNORECASE)

print("Email addresses found: ")

for match in matches:
    username, domain = match

    print (f"Username {username}. Domain: {domain}")