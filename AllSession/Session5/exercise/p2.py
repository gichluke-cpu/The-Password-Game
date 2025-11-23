import re
text = "python is hard, but python is powerful"
pattern = re.sub(r"python", "Java",text)
print(pattern)
