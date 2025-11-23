import zipfile
archive_name = 'compressed1_file.zip'

with zipfile.ZipFile(archive_name,'r') as zip_file:
    zip_file.extractall( path = 'C:\WebScrapingLibrary_NeoM2\Session9\extracted_files')
print('extracted all files!')