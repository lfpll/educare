from queue import Queue
import threading
import os
import zipfile
from shutil import move
import shutil


# Return to see if the file was unziped on the folder pattern /title/year
def is_unziped(parent_folder,title,year):
	file_path = '{folder}{title}/{year}'.format(folder=parent_folder, title=title, year=year)
	return not os.path.isdir(file_path)


# Validate if the zips in the folder works
def validate_zips(folder_name='./downloads/'):
	files_list = [item.path for item in os.scandir(folder_name)]
	problem_files = list(filter(lambda item: not zipfile.is_zipfile(item),files_list))
	problem_files = [file.strip(folder_name) for file in problem_files]
	return problem_files


# Return the folders that are empty
def get_empty_folders(parent_folder='./files/'):
	list_empty_dirs = list()
	# Iterate over the directory tree and check if directory is empty.
	for (dir_path , dir_name, filenames) in os.walk(parent_folder):
		if len(dir_name) == 0 and len(filenames) == 0:
			list_empty_dirs.append(dir_path)
	return list_empty_dirs


# Delete a list of folders based on the patter parent_folder/title/year
def delete_folders(parent_folder,folders_list):
	# Treating to the right style
	empty_folders = [{'title': folder.split('/')[2], 'year': folder.split('/')[3]} for folder in folders_list]

	# Removing the empty folders
	[shutil.rmtree('%s%s/%s' % (parent_folder, file_dic['title'], file_dic['year'])) for file_dic in empty_folders]
	return empty_folders


def create_folder(folder_name):
	if not os.path.isdir(folder_name):
		os.makedirs(folder_name, exist_ok=True)


# Unzip files from mongodb dicst with {'title',
def unzip_files_mdb(list_files):
	q_zip = Queue()
	unzip_class = Unzip(q_zip=q_zip)
	[q_zip.put_nowait(file_dic) for file_dic in list_files]
	[unzip_class.start_thread() for _ in range(len(list_files))]


class Unzip:
	def __init__(self, q_zip):
		self.q_zip = q_zip

	# Receives a object with filename and files
	# Create a files if doens't exist and unzip file
	def unzip_file(self):
		file_path = self.q_zip.get()
		folder = file_path['folder_name']
		filename = file_path['filename']
		print('Unzipping {filename}...'.format(filename=filename))

		# Check if is a zip file
		if filename.endswith('.zip'):
			if not zipfile.is_zipfile(filename):
				raise ('%s not valid dowload' % filename)
			else:
				with zipfile.ZipFile(filename, 'r') as zip_file:
					create_folder(folder_name=folder)
					zip_file.extractall(path='%s' % folder)
					print('{} Extracted to {} !'.format(filename,folder))
		# if it's not just move the file
		else:
			create_folder(folder_name=folder)
			move(filename, folder)
			print('{} Moved to {} !'.format(filename, folder))

	def start_thread(self):
		print('thread started')
		threading.Thread(target=self.unzip_file).start()

