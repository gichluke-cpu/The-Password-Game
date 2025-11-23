import shutil
source_directory = 'C:\WebScrapingLibrary_NeoM2\Session9\homework\restored_project'
archive_name = 'my_project_backup.zip'
shutil.unpack_archive(archive_name,source_directory)
print(f"Archive '{archive_name}.zip' created!")