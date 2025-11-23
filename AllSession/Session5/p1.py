import re
text= "hello. English or Spanish?"
pattern = re.escape('.')
matches = re.findall(pattern,text)
print(matches)