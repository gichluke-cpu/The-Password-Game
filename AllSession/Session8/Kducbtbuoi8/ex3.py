import datetime
print('Chương trình chia')
def bug_recorder(bug):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"[{time}] {bug}\n"
    with open("error.log.txt", "a", encoding="utf-8") as file:
        file.write(log)
    print("-> Đã ghi lỗi vào file 'error_log.txt'")

while True:
    try:
        a = float(input('Mời nhập giá trị số bị chia: '))
        b = float(input('Mời nhập giá trị số chia: '))
        print('A chia B là: ', a/b)
    except ValueError:
        noi_dung_loi1 = f"Lỗi ValueError: Giá trị nhập vào không hợp lệ (Không phải là số)"
        print('Lỗi giá trị!')
        bug_recorder(noi_dung_loi1)

    except ZeroDivisionError:
        noi_dung_loi = f"Lỗi ZeroDivisionError: Không thể chia cho 0"
        print('Lỗi chia cho 0!')
        bug_recorder(noi_dung_loi)
    except Exception as e:
        noi_dung_loi2 =f"Đã xảy ra lỗi ngoài dự kiến"
        print('Lỗi!')
        bug_recorder(noi_dung_loi2)

