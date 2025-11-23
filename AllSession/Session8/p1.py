try:
    f = open('data.txt','r')
    print(f.read())
    f.close()
except FileNotFoundError:
    print('Cannot find file')
finally:
    print('End program')