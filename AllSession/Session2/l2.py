import re

pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$'



while True:
    password = input("Please type in password:")
    if re.match(pattern,password):
        print("Password is correct!")
        break
    print("Password is incorrect!")