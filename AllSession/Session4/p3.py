import re
pattern = r'^Hello'
text = "Hello, World!"
match_obj = re.match(pattern,text)
if match_obj:
    print('Matched text: ', match_obj.group())
    print('Starting position: ', match_obj.start())
    print('End position: ', match_obj.end())
    print('Start and end: ', match_obj.span())
else:
    print('no match found')