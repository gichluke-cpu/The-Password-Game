import zipfile

zip_filename = 'file.zip'

with zipfile.ZipFile(zip_filename, 'r') as zf:
    list_of_files = zf.namelist()
    
    print(f"Danh sách các file trong '{zip_filename}':")
    
    for name in list_of_files:
        print(f"- {name}")