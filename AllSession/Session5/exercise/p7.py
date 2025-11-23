import re
text = "مرحباً أنا مبرمج "
pattern = re.findall(r"\w", text, re.UNICODE)
print(pattern)