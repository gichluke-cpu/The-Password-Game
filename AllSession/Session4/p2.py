import re
pattern = r'^(\d{4})-\d{3}-\d{3}'
phone = "1234-123-111"
match_obj = re.match(pattern, phone)
if match_obj:
    area = match_obj.group(1)
    print('Area code: ', area)
else:
    print("INVALID NUMBER")