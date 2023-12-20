import os

from config import black_file_pattern_list


def get_all_files_in_folder(folder_path):
    anon_dirs = []
    for root, dirs, files in os.walk(folder_path):
        if root in anon_dirs:
            anon_dirs.extend([os.path.join(root, dir) for dir in dirs])
        else:
            anon_dirs.extend([os.path.join(root, dir) for dir in dirs if dir.startswith('.')])

        if root in anon_dirs:
            continue
        for file in files:
            fp = os.path.join(root, file)
            if not any(pattern in fp for pattern in black_file_pattern_list):
                yield fp