import sys
from save_urls import return_urls
from download import async_dowload
from handle_files import validate_zips,validate_folders
from pymongo import MongoClient,UpdateOne
from os import path
import shutil
import re

KEY_TITLES = ['Censo Escolar', 'Encceja', 'Prova Brasil', 'ANA', 'Enem', 'Enem por Escola']

client = MongoClient()
coll = client['educare']['download']


def switch(option):
	if option == '--save_urls' or option == '-s_u':
		list_urls = return_urls(KEY_TITLES)
		coll.insert_many(list_urls)

	if option == '--download':
		zip_files = list(coll.find({'redownload':True},{'_id':0,'zip_url':1,'title':1,'year':1}))
		async_dowload(zip_files)

	if option == '--validate_zips' or option == '-vz':
		# Return zip files problematic the downloads files
		folder_name = './downloads/'

		# Get and string of the zips that were wrongly downloaded
		error_zips = validate_zips(folder_name)
		error_zips = re.compile('|'.join(error_zips))

		# Get the zips that weren't downloaded
		not_dowloaded = [tuple((mdb_dic['_id'],mdb_dic['zip_url'][::-1].split('/')[0][::-1])) for mdb_dic in list(coll.find({}, {'zip_url': 1}))]
		not_dowloaded = [UpdateOne({'_id':tup_mdb[0]},{'$set':{'redownload': not path.isfile(folder_name+tup_mdb[1])}}) for tup_mdb in not_dowloaded]

		coll.bulk_write(not_dowloaded)
		coll.update_many({'zip_url':{'$regex':error_zips}},{'$set':{'redownload':True}})


	if option == '--validate_folder' or option == '-vf':
		folder_name = './files/'
		empty_folders = validate_folders(folder_name)
		empty_folders = [{'title':folder.split('/')[2],'year':folder.split('/')[3]} for folder in empty_folders]
		[shutil.rmtree('%s%s/%s' % (folder_name,file_dic['title'],file_dic['year'])) for file_dic in empty_folders]
		query_mongodb = [UpdateOne(query_mdb,{'$set':{'reunzip':True}}) for query_mdb in empty_folders]
		coll.bulk_write(query_mongodb)
#



arguments = sys.argv

switch(option = arguments[1])