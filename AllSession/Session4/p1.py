import re
pattern = r'^Hello'
text = "Hello, World!"
match_obj = re.match(pattern,text)
if match_obj:
    print('Match found: ', match_obj.group())
else:
    print('No match found..')