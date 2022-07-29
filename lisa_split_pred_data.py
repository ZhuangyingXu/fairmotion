import os
import numpy as np

dir_path = "D:\\gitHub\\GT\\fairmotion\\data\\rawdata\\synthetic60FPS\\Synthetic_60FPS"
train_split = 0.7
valid_split = 0.2

Combined_train_list = []
Combined_valid_list = []
Combined_test_list = []
for dir in os.listdir(dir_path):
    temp_dir_path = os.path.join(dir_path, dir)
    path_list = []
    for item in os.listdir(temp_dir_path):
        if not item.endswith('.pkl'):
            continue
        if dir.__contains__('AMASS'):
            file_name = f"{dir[6:]}/{item}"
        else:
            file_name = f"{dir}/{item}"
        path_list.append(file_name)
        print(file_name)

    train_end_index = int(len(path_list) * train_split)
    valid_end_index = int(len(path_list) * (train_split + valid_split))
    Combined_train_list.append(path_list[:train_end_index])
    Combined_valid_list.append(path_list[train_end_index:valid_end_index])
    Combined_test_list.append(path_list[valid_end_index:])
    print(f"{dir} split completed")

text_list = ["training_fnames.txt", "validation_fnames.txt", "test_fnames.txt"]
contents = [Combined_train_list, Combined_valid_list, Combined_test_list]
for i in range(len(text_list)):
    text_file = text_list[i]
    content_list = contents[i]
    flat_list = [item for sublist in content_list for item in sublist]
    with open(text_file, 'w') as f:
        for line in flat_list:
            f.write(line)
            f.write('\n')
            
print(f"Data split completed")