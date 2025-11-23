import re
pattern = r"apple"
text = "I have an apple"
match = re.search(pattern, text)
if match:
    print("Pattern found!")
else:
    print("Pattern not found :(")