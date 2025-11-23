try:
    soluong = int(input('Mời nhập số lượng sản phẩm: '))
    gia = float(input('Mời nhập giá sản phẩm: '))
    if soluong <0 or gia < 0:
        raise Exception('Giá trị ko hợp lệ')
    print('Tổng tiền là: ', soluong*gia)
except ValueError:
    print('Lỗi cú pháp')