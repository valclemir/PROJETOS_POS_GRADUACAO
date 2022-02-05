import os 
import shutil 

path_base = "db_images/train"
path_target = os.path.dirname(os.path.abspath(__file__)) + "/images/train"
dir_base = os.listdir(path_base)

for dir in dir_base:
    print(dir)
    num_images = 0
    path_dir = os.path.join(path_base, dir)
    for images in os.listdir(path_dir):
        dir_abs_images = path_dir+"/"+images

        shutil.copy(dir_abs_images, path_target)

        
        num_images = num_images + 1

        if num_images == 1500:
            break 
        
        
