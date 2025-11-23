import shutil
source_directory = 'C:\WebScrapingLibrary_NeoM2\Session9\sample_dir'
archive_name = 'sample_dir_archive'
shutil.make_archive(archive_name,'zip',source_directory)
print(f"Archive '{archive_name}.zip' created!")