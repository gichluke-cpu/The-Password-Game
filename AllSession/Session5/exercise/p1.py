import re
text = "I have 5 cats, 7 dogs and 9 humans"
numbers = re.findall(r'\d+', text)
print(numbers)