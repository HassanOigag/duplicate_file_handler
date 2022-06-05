from sys import argv
import os
import hashlib

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
    all_files = {}
    for file in files:
        file_size = os.path.getsize(file)
        if file_size not in all_files:
            all_files[file_size] = [file]
        else:
            all_files[file_size].append(file)
    same_size_files = {key: value for key,value in all_files.items() if len(value) > 1}
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

def print_duplicate_files(duplicate_files):
    for size, hashes in duplicate_files.items():
        print(f"\n{size} bytes")
        for file_hash, files in hashes.items():
            print(f"Hash: {file_hash}")
            for file in files:
                print(f"{file[0]}. {file[1]}")


def get_duplicate_files(same_size_files):
    duplicate_files = {}
    for size, files in same_size_files.items():
        duplicate_files[size] = {}
        for file in files:
            with open(file, 'rb') as f:
                content = f.read()
                file_hash = hashlib.md5(content).hexdigest()
            if file_hash not in duplicate_files[size].keys():
                duplicate_files[size][file_hash] = [file]
            else:
                duplicate_files[size][file_hash].append(file)
    res = {}
    #selecting hashes that have more that one file
    for size, value in duplicate_files.items():
        res[size] = {}
        for file_hash, files in value.items():
            if len(files) > 1:
                res[size][file_hash] = files
    return res

def assign_file_ids_to_files(duplicate_files):
    dups = {}
    file_id = 1
    for size, hashes in duplicate_files.items():
        dups[size] = {}
        for hash_, files in hashes.items():
            dups[size][hash_] = []
            for file in files:
                dups[size][hash_].append((file_id, file))
                file_id += 1
    return dups

def get_files_to_delete(dups, file_ids):
    all_files = []
    for _, hashes in dups.items():
        for _, files in hashes.items():
            for file in files:
                if file[0] in file_ids:
                    all_files.append(file[1])
    return all_files

def delete_files(files):
    memory_freed = 0
    for file in files:
        memory_freed += os.path.getsize(file)
        os.remove(file)
    return memory_freed

def ask_question(question):
    while True:
        option = input(f"\n{question}\n> ")
        if option not in ("yes", "no"):
            print("\nWrong option")
        else:
            break
    return option 

if __name__ == "__main__":
    if len(argv) != 2:
        print("Directory is not specified")
        exit()
    dir_ = argv[1]
    file_format = input("\nEnter file format:\n>")
    sorting_option = get_sorting_order_from_user()
    all_files = get_all_files(dir_, file_format)
    same_size_files = sort_files(get_same_size_files(all_files), sorting_option)
    print_files(same_size_files)
    if ask_question("Check for duplicates?") == "yes":
        duplicate_files = get_duplicate_files(same_size_files)
        duplicate_files = assign_file_ids_to_files(duplicate_files)
        print_duplicate_files(duplicate_files)
    else:
        exit()
    
    if ask_question("Delete files?") == "yes":
        while True:
            file_ids = input("\nEnter file numbers to delete:\n> ").split()
            try:
                file_ids = [int(file_id) for file_id in file_ids]
            except ValueError:
                print("\nWrong format")
                continue
            files_to_delete = get_files_to_delete(duplicate_files, file_ids)
            if len(files_to_delete) != len(file_ids):
                print("\nWrong format")
            else:
                break
        print(f"\nTotal freed up space: {delete_files(files_to_delete)} bytes")
    else:
        exit()