import os
import datetime


FILE_HOA_DON = "C:\WebScrapingLibrary_NeoM2\Session8\Kducbtbuoi8\hoadon.txt"
FILE_ERROR_LOG = "error_log.txt"

def ghi_log_loi(noi_dung_loi, so_dong):
    """
    Hàm ghi nội dung lỗi vào file error_log.txt.
    """
    thoi_gian = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chuoi_log = f"[{thoi_gian}] Dòng {so_dong}: {noi_dung_loi}\n"
    
    try:

        with open(FILE_ERROR_LOG, "a", encoding="utf-8") as file:
            file.write(chuoi_log)
    except IOError as e:
        print(f"Lỗi hệ thống: Không thể ghi vào file log '{FILE_ERROR_LOG}'. Chi tiết: {e}")

def kiem_tra_va_tao_file_hoa_don(ten_file):
    """
    Kiểm tra xem file hóa đơn có tồn tại không. 
    Nếu không, báo lỗi và tạo file với nội dung mẫu.
    """
    if not os.path.exists(ten_file):
        print(f"⚠️ CẢNH BÁO: File '{ten_file}' không tồn tại. Đang tạo file mẫu...")
        try:

            noi_dung_mau = (
                "Check:\n\n"
                "Product name, Quantity, Price\n"
                "Pen, 10, 2500\n"
                "Notebook, 5, 8000\n"
                "Book, 4, 15000\n" 
            )
            with open(ten_file, "w", encoding="utf-8") as file:
                file.write(noi_dung_mau)
            print(f"✅ Đã tạo file '{ten_file}' thành công với nội dung mẫu.")
            return False 
        except IOError as e:
            print(f"❌ LỖI: Không thể tạo file '{ten_file}'. Chi tiết: {e}")
            return False
    return True

def tinh_tong_tien_hoa_don():
    """
    Tính tổng tiền trong hóa đơn, xử lý và ghi lỗi vào file log.
    """

    if not kiem_tra_va_tao_file_hoa_don(FILE_HOA_DON):

        print("Vui lòng chỉnh sửa nội dung file mẫu và chạy lại chương trình.")
        return

    tong_tien = 0.0
    
    try:
        with open(FILE_HOA_DON, "r", encoding="utf-8") as file:

            lines = file.readlines()
            

            start_index = 0
            for i, line in enumerate(lines):
                if "Product name, Quantity, Price" in line.strip():
                    start_index = i + 1 
                    break
            
            so_dong_giao_dich = 0
            for i in range(start_index, len(lines)):
                line = lines[i].strip()
                so_dong_giao_dich += 1 
                
                if not line or line.startswith('#') or line.startswith('['):
                    continue  

                try:
                   
                    parts = line.split(',')
                    
                   
                    if len(parts) < 3:
                        raise IndexError("Thiếu cột dữ liệu (cần ít nhất 3 cột: Tên, Số lượng, Giá).")
                        
                    ten_san_pham = parts[0].strip()
                    so_luong_str = parts[1].strip()
                    gia_str = parts[2].strip()

                  
                    so_luong = float(so_luong_str)
                    gia = float(gia_str)

                    
                    thanh_tien = so_luong * gia
                    tong_tien += thanh_tien

                except ValueError as e:
 
                    ghi_log_loi(f"Lỗi kiểu dữ liệu (ValueError). Chi tiết: {e}. Dữ liệu dòng: '{line}'", so_dong_giao_dich)
                    continue 

                except IndexError as e:
   
                    ghi_log_loi(f"Lỗi cấu trúc dữ liệu (IndexError). Chi tiết: {e}. Dữ liệu dòng: '{line}'", so_dong_giao_dich)
                    continue 
                    
                except Exception as e:
                 
                    ghi_log_loi(f"Lỗi không xác định. Chi tiết: {e}. Dữ liệu dòng: '{line}'", so_dong_giao_dich)
                    continue 

    except FileNotFoundError:
     
        print(f"❌ LỖI KHÔNG THỂ XỬ LÝ: File '{FILE_HOA_DON}' không tìm thấy sau khi kiểm tra.")
        return

    except IOError as e:
        print(f"❌ LỖI: Lỗi khi đọc file '{FILE_HOA_DON}'. Chi tiết: {e}")
        return


    tong_tien_format = "{:,.0f}".format(tong_tien).replace(",", ".")
    print("\n--- KẾT QUẢ TÍNH TOÁN ---")
    print(f"TỔNG TIỀN HÓA ĐƠN (từ các dòng hợp lệ): **{tong_tien_format}**")
    print(f"Các dòng lỗi đã được ghi lại trong file '{FILE_ERROR_LOG}'")
    

if os.path.exists(FILE_ERROR_LOG):
    os.remove(FILE_ERROR_LOG)
    

tinh_tong_tien_hoa_don()