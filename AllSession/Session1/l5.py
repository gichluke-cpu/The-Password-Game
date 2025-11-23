import logging

def tinh_trung_binh(danh_sach):
    logging.debug("Bắt đầu tính trung bình")

    logging.debug("Danh sách đầu vào: %s", danh_sach)

    tong = sum(danh_sach)

    trung_binh =tong/len (danh_sach)

    logging.info ("Đã tính xong trung bình: %.2f", trung_binh)

#Thêm điều kiện lỗi để minh họa

    if trung_binh > 100:

        logging.error("Giá trị trung bình quá cao bất thường: %.2f", trung_binh)

    elif trung_binh < 0:

        logging.warning("Giá trị trung bình ăn: %.2f", trung_binh)

        return trung_binh



def main():

# Cấu hình logging: mức độ DE BUG và định dạng

    logging.basicConfig(filename = 'app.log',  encoding='uft-8'

        level=logging.DEBUG,
        format='%(asctine)s - %(levelname)s - %(message)s'
    )
    danh_sach = [5, 10, 15, 20, -99]
    logging.debug("Bắt đầu chương trình")
    ket_qua = tinh_trung_binh(danh_sach)
    logging.info("Kết quả trung bình: %.2f", ket_qua)



if __name__ == "__main__":
    main()