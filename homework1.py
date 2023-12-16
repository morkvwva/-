import os
import shutil
import argparse
from pathlib import Path
from random import randint, choice, choices
import numpy as np
from PIL import Image
import lorem
import magic

def normalize(text):
    translit = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh',
        'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'IE', 'Ж': 'ZH',
        'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS',
        'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ю': 'IU', 'Я': 'IA'
    }
    normalized_text = ''.join([translit.get(c, '_') if c.isalpha() else c for c in text])
    return normalized_text


def get_random_filename(length=8):
    random_chars = '()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz' \
                   '{}~абвгдеєжзиіїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    return ''.join(choices(random_chars, k=length))


# ГЕНЕРУВАННЯ
def generate_text_files(path):
    documents = ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx')
    filename = f"{get_random_filename()}.{choice(documents)}"
    
    random_text = lorem.text()

    with open(path / filename, "w", encoding='utf-8') as f:
        f.write(random_text)




# АРХІВИ
def generate_archive_files(path):
    archives = ('zip', 'tar.gz', 'tar')
    filename = f"{get_random_filename()}.{choice(archives)}"
    shutil.make_archive(path / filename.split('.')[0], choice(archives), path)
def extract_archive(archive_path, extract_to):
    archive_name = Path(archive_path).stem 
    try:
        shutil.unpack_archive(archive_path, extract_to)
    except Exception as e:
        print(f"Failed to extract {archive_name}: {e}")
        # Якщо розпакування не вдалося, видаляємо
        os.remove(archive_path)
        return
    # Переносимо 
    destination_folder = Path(extract_to) / 'archives' / archive_name
    if not destination_folder.exists():
        destination_folder.mkdir(parents=True)
    for item in os.listdir(extract_to):
        shutil.move(os.path.join(extract_to, item), str(destination_folder))






def generate_image(path):
    images = ('jpeg', 'png', 'jpg')
    filename = f"{get_random_filename()}.{choice(images)}"
    image_array = np.random.rand(100, 100, 3) * 255
    image = Image.fromarray(image_array.astype('uint8'))
    image.save(path / filename)



def generate_folders(path, num_folders):
    folder_names = ['temp', 'folder', 'dir', 'tmp', 'OMG', 'is_it_true', 'no_way', 'find_it']
    weights = [10, 10, 1, 1, 1, 1, 1, 1]
    
    for _ in range(num_folders):
        num_subfolders = randint(1, 3) 
        new_folder = path / Path(*choices(folder_names, weights=weights, k=randint(1, len(folder_names))))
        
        # Перевірка, чи не потрапляємо у папки, які потрібно ігнорувати
        if new_folder.name.lower() not in ['archives', 'video', 'audio', 'documents', 'images', 'others']:
            new_folder.mkdir(parents=True, exist_ok=True)
            generate_files(new_folder, randint(3, 5), num_subfolders)



# ТИП ФАЙЛУ ВИЗНАЧ
def get_file_extension(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type    



def get_extensions_in_folder(folder_path):
    extensions = set()
    for file_name in os.listdir(folder_path):
        _, extension = os.path.splitext(file_name)
        extensions.add(extension)
    return extensions
target_folder = 'шлях_до_цільової_папки'
all_extensions = get_extensions_in_folder(target_folder)
print(all_extensions)


# ГЕНЕРУВАННЯ І НОВА НАЗВА
def generate_files(path, num_files, num_folders):
    for _ in range(num_files):
        file_types = [generate_text_files, generate_archive_files, generate_image]
        chosen_file_type = choice(file_types)
        chosen_file_type(path)
        file_extension = get_file_extension(chosen_file_type)
    generate_folders(path, num_folders)
    rename_files(path)  #  перейменування файлів
    delete_empty_folders(path) #  видалення порожніх папок
    all_extensions = get_extensions_in_folder(path)
    print("Усі розширення у папці:", all_extensions)


def rename_files(directory):
    for path, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(path, file)
            # Отримання нового імені файлу через normalize
            new_filename = normalize(file)
            # Перейменування файлу
            os.rename(file_path, os.path.join(path, new_filename))

# ГЕНЕРУВАННЯ І ВИДАЛЕННЯ ПОРОЖНІХ ПАПОК
def file_generator(output_path, num_files, num_folders):
    output_path.mkdir(parents=True, exist_ok=True)
    generate_files(output_path, num_files, num_folders)
def delete_empty_folders(directory):
    for root, dirs, _ in os.walk(directory, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            try:
                os.rmdir(folder_path)
            except OSError:
                pass  # якщоо папка не порожня або видалення неможливе, пропускаємо



def main():
    parser = argparse.ArgumentParser(description='Generate random files and folders')
    parser.add_argument('output_folder', type=str, help='Output folder path')
    parser.add_argument('--num_files', type=int, default=5, help='Number of files to generate')
    parser.add_argument('--num_folders', type=int, default=3, help='Number of folders to generate')

    args = parser.parse_args()

    output_path = Path(args.output_folder)
    file_generator(output_path, args.num_files, args.num_folders)

if __name__ == '__main__':
    main()
