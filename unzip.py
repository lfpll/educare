import threading
import os
import zipfile
from shutil import move


class Unzip:
	def __init__(self, q_zip):
		self.q_zip = q_zip

	# Receiveis a object with filename and folder
	# Create a folder if doens't exist and unzip file

	def unzip_file(self):
		file_path = self.q_zip.get()
		folder = file_path['folder']
		filename = file_path['filename']

		if not os.path.isdir(folder):
			os.makedirs(folder, exist_ok=True)

		if not zipfile.is_zipfile(filename):
			if filename.endswith('.zip'):
				raise('%s not valid dowload' % filename)
			move(filename,folder)
		else:
			with zipfile.ZipFile(filename, 'r') as zip_file:
				zip_file.extractall(path='%s' % folder)
				print(filename+' Extracted!')

	def start_thread(self):
		threading.Thread(target=self.unzip_file).start()

