import zipfile
with zipfile.ZipFile('backup.zip','w',compression=zipfile.ZIP_STORED) as z:
    z.write('C:\WebScrapingLibrary_NeoM2\Session7\data1.txt')
    z.write('C:\WebScrapingLibrary_NeoM2\Session7\data2.txt')
print('Backup files made!')