import re

def scam_detector(website):
    link_pattern = re.compile(r"(https?:\/\/\S+|www\.\S+|\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b)", re.I)
    return link_pattern.sub("***LINK BLOCKED!***",website)

def censorer():
    print("Hệ thống kiểm duyệt tin nhắn (Nhập 'thoat' để kết thúc)")
    while True:
        tin_nhan_input = input("Nhập tin nhắn: ")
        if tin_nhan_input.lower() == 'thoat':
            break

        censored = scam_detector(tin_nhan_input)

        if censored != tin_nhan_input:
            print(">>> CẢNH BÁO LỪA ĐẢO: " + censored)
        else:
            print(censored)

censorer()