import shutil
try:
    source_directory = 'C:\WebScrapingLibrary_NeoM2\Session9\my_project_backup'
    archive_name = 'my_project'
    shutil.make_archive(archive_name, 'zip', source_directory)
    print(f"Archive '{archive_name}.zip' ")
except FileNotFoundError:
    print('Cannot find file!')