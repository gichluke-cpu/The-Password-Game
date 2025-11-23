import zipfile
archive_name = 'C:\WebScrapingLibrary_NeoM2\folder_example'
file_to_extract = 'C:\WebScrapingLibrary_NeoM2\folder_example\video.mp4'
with zipfile.ZipFile(archive_name,'r') as zip_file:
    zip_file.extract(file_to_extract, path = 'C:\WebScrapingLibrary_NeoM2\Session9\homework\one_file')
print('extracted files!')