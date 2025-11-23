import pyzipper
import os

zip_filename = 'secure.zip'
password = b'MatKhauSieuManh123!' # Mật khẩu phải đúng và cũng là bytes
extract_folder = 'giai_nen_o_day'

# Tạo thư mục giải nén nếu chưa có
os.makedirs(extract_folder, exist_ok=True)

try:
    with pyzipper.ZipFile(zip_filename, 'r') as zf:
        
        zf.setpassword(password)
        
        
        zf.extractall(path=extract_folder)
        
    print(f"Đã giải nén thành công vào thư mục '{extract_folder}'.")

except pyzipper.BadZipFile:
    print("Lỗi: File zip bị hỏng hoặc không phải file zip.")
except RuntimeError as e:
    if 'Bad password' in str(e):
        print("Lỗi: Sai mật khẩu!")
    else:
        print(f"Lỗi: {e}")
except Exception as e:
    print(f"Đã xảy ra lỗi không xác định: {e}")