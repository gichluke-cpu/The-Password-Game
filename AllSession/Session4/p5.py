import re
pattern = r'\bapple\b'
text = "I have an apple, but I want an orange."
replace = "banana"
result = re.sub(pattern,replace,text)
print(result)