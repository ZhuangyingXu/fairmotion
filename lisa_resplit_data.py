import os
import numpy as np

dir_path = "D:\\gitHub\\GT\\fairmotion\\fairmotion\\tasks\\motion_prediction\\data"
train_split = 0.7
valid_split = 0.2

text_list = ["original_training_fnames.txt", "original_validation_fnames.txt", "original_test_fnames.txt"]
combined_list = []
for text_fname in text_list:
    text_file_path = os.path.join(dir_path, text_fname)
    with open(text_file_path) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        combined_list.append(lines)

flat_combined_list = [item for sublist in combined_list for item in sublist]
flat_combined_list.sort()

Combined_train_list = []
Combined_valid_list = []
Combined_test_list = []
temp_folder_prefix = ""
temp_category_files = []
for file in flat_combined_list:
    file_prefix = file.split('/')[0]
    if temp_folder_prefix != file_prefix:
        if len(temp_category_files) > 0:
            train_end_index = int(len(temp_category_files) * train_split)
            valid_end_index = int(len(temp_category_files) * (train_split + valid_split))
            Combined_train_list.append(temp_category_files[:train_end_index])
            Combined_valid_list.append(temp_category_files[train_end_index:valid_end_index])
            Combined_test_list.append(temp_category_files[valid_end_index:])
        temp_category_files = []
        temp_folder_prefix = file_prefix
    temp_category_files.append(file)

train_end_index = int(len(temp_category_files) * train_split)
valid_end_index = int(len(temp_category_files) * (train_split + valid_split))
Combined_train_list.append(temp_category_files[:train_end_index])
Combined_valid_list.append(temp_category_files[train_end_index:valid_end_index])
Combined_test_list.append(temp_category_files[valid_end_index:])

text_list = ["training_fnames.txt", "validation_fnames.txt", "test_fnames.txt"]
contents = [Combined_train_list, Combined_valid_list, Combined_test_list]
for i in range(len(text_list)):
    text_file = text_list[i]
    text_file_path = os.path.join(dir_path, text_file)
    content_list = contents[i]
    flat_list = [item for sublist in content_list for item in sublist]
    with open(text_file_path, 'w') as f:
        for line in flat_list:
            f.write(line)
            f.write('\n')
            
print(f"Data split completed")





