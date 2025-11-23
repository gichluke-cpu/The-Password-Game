import re

def inspector_msg(tin_nhan):
    cheat_pattern = re.compile(r'\bCHEAT_[A-Za-z0-9]+\b', re.I)
    return cheat_pattern.sub("***CHEAT_BLOCKED***", tin_nhan)

def censorer():
    print("Hệ thống kiểm duyệt tin nhắn (Nhập 'thoat' để kết thúc)")
    while True:
        tin_nhan_input = input("Nhập tin nhắn: ")
        if tin_nhan_input.lower() == 'thoat':
            break

        censored = inspector_msg(tin_nhan_input)

        if censored != tin_nhan_input:
            print(">>> Tin nhắn đã bị chặn: " + censored)
        else:
            print(censored)

censorer()
