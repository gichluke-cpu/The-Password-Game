import zipfile
archive_name = 'compressed1_file.zip'
file_to_extract = 'file1.txt'
with zipfile.ZipFile(archive_name,'r') as zip_file:
    zip_file.extract(file_to_extract, path = 'C:\WebScrapingLibrary_NeoM2\Session9\extracted_files')
print('extracted files!')