import zipfile


zip_filename = 'file.zip'
is_found = False

try:

    file_to_check = input("Nhập tên file bạn muốn kiểm tra trong file.zip: ")
    

    with zipfile.ZipFile(zip_filename, 'r') as zf:
        

        list_of_files = zf.namelist()
        

        if file_to_check in list_of_files:
            is_found = True

except FileNotFoundError:
    print(f"\nLỗi: Không tìm thấy file nén '{zip_filename}' trong thư mục hiện tại.")
except zipfile.BadZipFile:
    print(f"\nLỗi: File '{zip_filename}' không phải là file ZIP hợp lệ.")
except Exception as e:
    print(f"\nĐã xảy ra lỗi không xác định: {e}")



if is_found:
    print(f"\n✅ File '{file_to_check}' TỒN TẠI trong '{zip_filename}'.")
elif not is_found and 'Lỗi' not in locals(): 
    print(f"\n❌ File '{file_to_check}' KHÔNG TỒN TẠI trong '{zip_filename}'.")