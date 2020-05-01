#%%
from os import listdir, rename, makedirs
from os.path import isfile, isdir, join, splitext
import re

#%%
root_dir = "/Volumes/waitphoto/lion.local/photo/RAW/scanned"
# rootDir = '.'
if (len(sys.argv)>1):
    rootDir = sys.argv[1]

file_list = [f for f in listdir(root_dir) if isfile(join(root_dir, f))]

for f in file_list:
    file_parts = re.split('_',f)
    if (len(file_parts)<2):
        continue

    print(file_parts[0])
    out_dir = join(root_dir,file_parts[0])
    
    if (not isdir(out_dir)):
        makedirs(out_dir)

    old_name = join(root_dir,f)
    new_name = join(out_dir,f)
    print("{} -> {}".format(old_name, new_name))
    rename(old_name, new_name)
