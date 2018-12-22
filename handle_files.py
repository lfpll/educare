import threading
import os
import zipfile
from shutil import move


def create_folder(folder_name):
	if not os.path.isdir(folder_name):
		os.makedirs(folder_name, exist_ok=True)


def validate_zips(folder_name='./dowloads/'):
	files_list = [item.path for item in os.scandir(folder_name)]
	problem_files = list(filter(lambda item: not zipfile.is_zipfile(item),files_list))
	problem_files = [file.strip(folder_name) for file in problem_files]
	return problem_files


def validate_folders(folder_name='./files/'):
	list_empty_dirs = list()
	# Iterate over the directory tree and check if directory is empty.
	for (dir_path , dir_name, filenames) in os.walk(folder_name):
		if len(dir_name) == 0 and len(filenames) == 0:
			list_empty_dirs.append(dir_path)
	return list_empty_dirs


class Unzip:
	def __init__(self, q_zip):
		self.q_zip = q_zip

	# Receives a object with filename and files
	# Create a files if doens't exist and unzip file


	def unzip_file(self):
		file_path = self.q_zip.get()
		folder = file_path['files']
		filename = file_path['filename']

		if filename.endswith('.zip'):
			if not zipfile.is_zipfile(filename):
				raise ('%s not valid dowload' % filename)
			else:
				with zipfile.ZipFile(filename, 'r') as zip_file:
					create_folder(folder_name=folder)
					zip_file.extractall(path='%s' % folder)
					print(filename + ' Extracted!')

		else:
			create_folder(folder_name=folder)
			move(filename, folder)
			print(filename + ' Moved')

	def start_thread(self):
		threading.Thread(target=self.unzip_file).start()
