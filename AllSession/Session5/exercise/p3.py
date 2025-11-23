import re
text = "do you like C++ or C#?"
pattern=re.escape('+')
matches = re.findall(pattern,text)
pattern2 = re.escape('#')
match2 = re.findall(pattern2,text)
print(matches)
print(match2)