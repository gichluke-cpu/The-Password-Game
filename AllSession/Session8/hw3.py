while True:
    data = input('Nhập tên File: ')
    try:
        a = open(data, 'r')
        print(a.read())
        a.close()
    except FileNotFoundError:
        print('Không có file')
    except Exception as e:
        print('Lỗi')
    finally:
        a.close()