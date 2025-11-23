import re
pattern = r'(\d{2})-(\d{2})-(\d{4})'
text = "today is 07-24-2023"
replacement = r'\2/\1/\3'
result = re.sub(pattern,replacement,text)
print(result)