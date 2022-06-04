from sys import argv
import os

def get_all_files(dir_, ext):
    all_files = []
    all_files_ext = []
    for root, _, files in os.walk(dir_, topdown=True):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file_path)[1][1:]
            if ext == file_ext:
                all_files_ext.append(file_path)
            all_files.append(file_path)
    files = all_files if len(ext) == 0 else all_files_ext
    return files

def get_same_size_files(files):
    same_size_files = {}
    for file in files:
        file_size = os.path.getsize(file)
        if file_size not in same_size_files:
            same_size_files[file_size] = [file]
        else:
            same_size_files[file_size].append(file)
    return same_size_files

def sort_files(files, option):
    option = True if option == "1" else False
    return {key: files[key] for key in sorted(files.keys(), reverse=option)}

def get_sorting_order_from_user():
    print("\nSize sorting options:\n1. Descending\n2. Ascending\n")
    while True:
        option = input("Enter a sorting option:\n> ")
        if option not in ("1", "2"):
            print("\nWrong option\n")
        else:
            break
    return option

def print_files(files_dict):
    for size,files in files_dict.items():
        print(f"\n{size} bytes")
        for file in files:
            print(file)

if __name__ == "__main__":
    if len(argv) != 2:
        print("Directory is not specified")
        exit()
    dir_ = argv[1]
    file_format = input("\nEbter file format:\n>")
    sorting_option = get_sorting_order_from_user()
    all_files = get_all_files(dir_, file_format)
    same_size_files = sort_files(get_same_size_files(all_files), sorting_option)
    print_files(same_size_files)
