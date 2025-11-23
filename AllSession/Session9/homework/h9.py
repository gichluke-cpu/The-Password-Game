'''import zipfile
import os

zip_files_to_combine = ['zip1.zip', 'zip2.zip']
output_zip_file = 'combined.zip'

with zipfile.ZipFile(output_zip_file, 'w', zipfile.ZIP_DEFLATED) as combined_zip:
    for input_zip_name in zip_files_to_combine:
        if not os.path.exists(input_zip_name):
            print(f"Cảnh báo: Không tìm thấy file '{input_zip_name}'. Bỏ qua file này.")
            continue
            
        with zipfile.ZipFile(input_zip_name, 'r') as input_zip:
            file_list = input_zip.namelist()
            
            for file_in_zip in file_list:
                with input_zip.open(file_in_zip) as source, \
                     combined_zip.open(file_in_zip, 'w') as target:
                    
                    target.write(source.read())
                    
                print(f"  -> Đã thêm '{file_in_zip}' từ '{input_zip_name}'")

print(f"\n✅ Đã gộp thành công nội dung của {', '.join(zip_files_to_combine)} vào '{output_zip_file}'.") '''

import zipfile
import os
output = "combined.zip"
with zipfile.ZipFile(output,'w') as new_zip:
    for zip_name in['Scratch.zip','folder_example']:
        with zipfile.ZipFile(zip_name,'r') as old_zip:
            for file in old_zip.namelist():
        
                extracted_path = old_zip.extract()
                new_zip.write(extracted_path)
                #os.remove(extracted_path)