import zipfile
import zipfile

archive_name = 'compressed1_file.zip'

try: 
    with zipfile.ZipFile(archive_name, 'w') as zipf:
        # Add 'r' before each path string
        zipf.write('file1.txt')
        zipf.write('file2.txt')

        zipf.write('directory1')
        zipf.write('directory2')

    print('Archive created! with the name:', archive_name)
except FileNotFoundError as e:
    print('khong tim thấy file')

# '''archive_name = 'compressed1_file.zip'
# with zipfile.ZipFile(archive_name, 'w') as zipf:
#     zipf.write('C:\WebScrapingLibrary_NeoM2\Session9\sample_dir\file1.txt')
#     zipf.write('C:\WebScrapingLibrary_NeoM2\Session9\file2.txt')

#     zipf.write('C:\WebScrapingLibrary_NeoM2\Session9\directory1')
#     zipf.write('C:\WebScrapingLibrary_NeoM2\Session9\directory2')

# print('Archive created! with the name:', archive_name)'''