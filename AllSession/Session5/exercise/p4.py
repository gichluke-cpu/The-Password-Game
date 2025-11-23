import re
text = "HELLO World"
pattern = "Hello world"
find = re.search(text,pattern, re.I)
if find:
    print('found! ', find.group())
else:
    print('Nothing!')

