import re

pattern = r'\b[A-ZÀ-Ỹ][a-zà-ỹ]*\b'
text = r"Hôm nay trời Đẹp. Tôi sẽ Đi học Python ở Aptech."

matches = re.findall(pattern, text) 
if matches:
    print('capital words are: ', matches)