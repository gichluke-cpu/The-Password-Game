import pyzipper
import os
import zipfile


file_to_zip = 'file_can_bao_ve.txt'
try:
    with open(file_to_zip, 'w', encoding='utf-8') as f:
        f.write("Đây là nội dung cần được bảo mật.")
except IOError as e:
    print(f"Không thể tạo file mẫu: {e}")
    exit()


zip_filename = 'secure.zip'

password = b'MatKhauSieuManh123!' 

try:
   
    with pyzipper.AESZipFile(zip_filename, 
                           'w', 
                           compression=pyzipper.ZIP_DEFLATED) as z:
        
     
        z.setpassword(password)
        z.setencryption(pyzipper.WZ_AES, nbits=256)
       
        z.write(file_to_zip)

    print(f"Đã tạo thành công file '{zip_filename}' được bảo vệ bằng mật khẩu.")
    
    
    os.remove(file_to_zip)

except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")