import shutil
source_directory = 'C:\WebScrapingLibrary_NeoM2\Session9\extract_data'
archive_name = 'sample_dir_archive.zip'
shutil.unpack_archive(archive_name, source_directory)
print(f"Archive '{archive_name}.zip' extracted!")