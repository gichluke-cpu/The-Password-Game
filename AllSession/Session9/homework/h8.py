import zipfile
import csv
from io import TextIOWrapper

with zipfile.ZipFile('Scratch.zip', 'r') as z:
    print("files.csv in zip: ")
    for f in z.namelist():
        if f.endswith('csv'):
            print('-',f)

'''zip_filename = 'file.zip'
csv_file_in_zip = 'data.csv'

with zipfile.ZipFile(zip_filename, 'r') as zf:
    if csv_file_in_zip in zf.namelist():
        with zf.open(csv_file_in_zip, 'r') as csv_stream:
            text_stream = TextIOWrapper(csv_stream, encoding='utf-8')
            csv_reader = csv.reader(text_stream)
            
            print(f"--- Dữ liệu trong {csv_file_in_zip} ---")
            
            for row_index, row in enumerate(csv_reader):
                if row_index < 10:
                    print(f"Hàng {row_index + 1}: {row}")
                elif row_index == 10:
                    print("... (và nhiều hàng khác) ...")
                    break
    else:
        print(f"Lỗi: Không tìm thấy file '{csv_file_in_zip}' trong '{zip_filename}'.")'''
