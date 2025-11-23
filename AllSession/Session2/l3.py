import re

pattern = r'^(?:\d{4}-){3}\d{4}$|^\d{16}$|^(?:\d{4}\s){3}\d{4}$'




while True:
    password = input("Please type in Credit Card Number:")
    if re.match(pattern,password):
        print("Number is correct!")
        break
    print("Number is incorrect!")