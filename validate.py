import os


def validate_zips(folder):

def validate_folder(folder):
	for dirpath, dirnames, files in os.walk(folder):
		if not files:
			print("It is empty !")
			empty = True
		break;