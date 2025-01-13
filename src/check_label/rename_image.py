import os
import json

def rename_images(folder_path, bookname):
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            # Extract the number from the filename
            number = filename.split('_')[1].split('.')[0]
            # Create the new filename with zero-padded number
            new_filename = f"{bookname}_page{int(number):03}.png"
            # Rename the file
            print(f"Renaming {filename} to {new_filename}")
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))



if __name__ == "__main__":
    input_folder = 'Sach-Nom-Cong-Giao-1995-049-cropped'
    folder_path = 'images_label'
    bookname = 'Prj_55g_Nam_APCS2_Sách Nôm công giáo 1995 - 049'
    mapping = {}
    mapping[bookname] = {
        "page_pairs": [
            (22, 591),
        ]
    }

    for i in range(23, 55):
        mapping[bookname]["page_pairs"].append((i, 591+22 - i))

    for i in range(55, 300):
        mapping[bookname]["page_pairs"].append((i, 55+556 - i))


    for i, j in mapping[bookname]["page_pairs"]: 
        file_name = f"page_{j}.png"
        new_file_name = f"{bookname}_page{j:03}.png"
        file_path = f"'{input_folder}/{file_name}'"
        new_file_path = f"'{folder_path}/{new_file_name}'"
        # Find the file_name in input_folder and copy it to images_label and rename it
        os.system(f"cp {file_path} {new_file_path}")
        print(f"Copying {file_path} to {new_file_path}")


    # rename_images(folder_path, bookname)