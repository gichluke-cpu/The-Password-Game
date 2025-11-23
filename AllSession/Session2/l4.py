import re
with open('Session2/text.txt.txt', 'r', encoding = 'utf-8') as file:
    doc = file.read()
thaythe = re.sub(r"An","Huy", doc)

with open('Session2/text2.txt', 'w', encoding = 'utf-8') as file:
    ghi = file.write(thaythe)

print('replacement completed!')