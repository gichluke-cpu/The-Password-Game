import shutil
source_directory = 'C:\WebScrapingLibrary_NeoM2\Session9\homework\my_folder'
archive_name = 'my_project_backup'
shutil.make_archive(archive_name,'zip',source_directory)
print(f"Archive '{archive_name}.zip' created!")