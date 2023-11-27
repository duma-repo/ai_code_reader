import os


def get_all_files_in_folder(folder_path):
    file_list = []
    anon_dirs = []
    for root, dirs, files in os.walk(folder_path):
        if root in anon_dirs:
            anon_dirs.extend([os.path.join(root, dir) for dir in dirs])
        else:
            anon_dirs.extend([os.path.join(root, dir) for dir in dirs if dir.startswith('.')])

        if root in anon_dirs:
            continue
        for file in files:
            if not file.startswith('.'):
                file_list.append(os.path.join(root, file))
    return file_list
