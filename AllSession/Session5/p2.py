import re
text = 'Hello\nWorld'
pattern = "Hello.World"
match = re.search(pattern,text,re.S)
if match:
    print('Matched!: ', match.group()) 
else:
    print('P not found')