import re
pattern = r'\s'
text = "this is a sample sentence with spaces."
replacement='-'
result = re.sub(pattern,replacement,text,count=2)
print(result)