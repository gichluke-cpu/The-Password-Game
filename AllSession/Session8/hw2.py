lst = [10,20,30]

while True:
    try:
        a = int(input('Nhập vào số phần tử muốn xem: '))
        print(lst[a])
    except IndexError:
        print('Không có phần tử')
    except ValueError:
        print('bạn phải nhập số nguyên')