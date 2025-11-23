import re

pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

while True:
    email = input("Nhập email: ")
    if re.match(pattern, email):
        print("Email hợp lệ")
        break
    else:
        print("Email không hợp lệ, mời bạn nhập lại")