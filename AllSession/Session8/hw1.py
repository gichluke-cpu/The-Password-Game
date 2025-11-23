
while True:
    a = float(input('Nhập số bị chia: '))
    b = float(input('nhập số chia: '))
    if b == 0:
        raise ZeroDivisionError('Không chia được cho 0!')
    print('a chia b là: ', a/b)
