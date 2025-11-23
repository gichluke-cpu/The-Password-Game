import pdb

def divide(x,y):
    pdb.set_trace()
    result = x/y
    return result

x=10
y =2

try:
    print(divide(x,y))
except ZeroDivisionError as e:
    print(f"Error:{e}")