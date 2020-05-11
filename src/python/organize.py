# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ## Setup modules

import os
import sys
from datetime import datetime
# from location import get_closest_city
import re

# %%
import exifread

# %% [markdown]
# ## Get directories from the user

# %%
if len(sys.argv) < 3:
	sys.exit("Usage: organize.py source_path destination_path [reorg_path]")

input_dir = sys.argv[1]
output_dir = sys.argv[2]
if len(sys.argv) > 3:
	reorg_dir = sys.argv[3]
else:
	reorg_dir = None

# filename, file_extension = os.path.splitext(input_dir)
# now = datetime.now()
# log_file = os.path.join(filename,now.strftime('_%Y-%m-%d_%H-%M-%S') + '.log')
# print('stdout going to ' + log_file)
# sys.stdout = open(log_file,'w')

print('Moving files: ', input_dir, ' --> ', output_dir)

# %% [markdown]
# ## Define the image types

# %%
def is_image(argument):
	image_ext = {
		'.jpg': True,
		'.JPG': True,
		'.cr2': True,
		'.CR2': True,
		'.dng': True,
		'.DNG': True,
		'.png': True,
		'.PNG': True
	}
	return image_ext.get(argument,False)

# %% [markdown]
# ## Walk over all of the files and directories to find photos

# %%
for root, dirs, files in os.walk(input_dir):
	if not (re.search('@',root) is None):
		print('Found @ in ' + root)
		continue

	for f in files:
		if not (re.search('@',f) is None):
			print('Found @ in ' + f)
			continue

		filename, file_extension = os.path.splitext(f)
		cur_file = os.path.join(root,f)
		
		if not is_image(file_extension):
			if file_extension == '.log':
				print('Not touching log file')
				continue
			print('--Not reconized: ' + f)
			if not (reorg_dir is None):
				out_dir = os.path.join(reorg_dir,root[len(input_dir):len(root)])
				if not os.path.exists(out_dir):
					os.makedirs(out_dir)
				new_file = os.path.join(out_dir,f)
				print('\t Moving to: ' + new_file)
				os.rename(cur_file,new_file)
			continue

		file_handle = open(cur_file,'rb')
		
		tags = exifread.process_file(file_handle)
		dt = tags.get('EXIF DateTimeOriginal')

		if dt is None:
			print('--No EXIF DateTime: ' + cur_file)
			if not (reorg_dir is None):
				out_dir = os.path.join(reorg_dir,root[len(input_dir):len(root)])
				if not os.path.exists(out_dir):
					os.makedirs(out_dir)
				new_file = os.path.join(out_dir,f)
				print('\t   Moving to: ' + new_file)
				os.rename(cur_file,new_file)
			continue

		datetime_obj = datetime.strptime(str(dt), '%Y:%m:%d %H:%M:%S')
		new_file_name = datetime_obj.strftime('%Y-%m-%d_%H-%M-%S') + file_extension

		new_dir = os.path.join(output_dir,datetime_obj.strftime('%Y'),datetime_obj.strftime('%m'),datetime_obj.strftime('%d'))

		if not os.path.exists(new_dir):
			os.makedirs(new_dir)

		found_file = True
		inc = 0

		while(found_file):
			if os.path.exists(os.path.join(new_dir,new_file_name)):
				new_file_name = datetime_obj.strftime('%Y-%m-%d_%H-%M-%S')
				new_file_name += '_' + '{0:03d}'.format(inc) + file_extension
				inc += 1
			else:
				found_file = False

		new_file = os.path.join(new_dir,new_file_name)
		print('++' + cur_file + ' --> ' + new_file)
		os.rename(cur_file, new_file)

# %%
# ## Clean-up all embpty directories
for root, dirs, files in os.walk(input_dir, topdown=False):
	for name in dirs:
		try:
			if len(os.listdir( os.path.join(root, name) )) == 0: #check whether the directory is empty
				print("Deleting", os.path.join(root, name) )
				try:
					os.rmdir( os.path.join(root, name) )
				except:
					print( "FAILED :", os.path.join(root, name) )
					pass
		except:
			pass

# %%
print('Done')
