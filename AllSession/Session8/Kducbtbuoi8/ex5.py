import math
print('Chương trình tính căn')
while True:
    a = float(input('Mời nhập giá trị: '))
    if a < 0:
        raise ValueError('giá trị ko thể bé hơn 0!')
    else:
        print('căn bậc 2 của giá trị đã nhập là: ', math.sqrt(a))