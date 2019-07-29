import sys
from save_urls import return_urls
from handle_files import validate_zips,get_empty_folders,delete_folders,is_unziped,unzip_files_mdb
from pymongo import MongoClient,UpdateOne
import os
import re
import json

DOWNLOAD_FOLDER = './'
FILES_FOLDER = './files/'
KEY_TITLES = ['Censo Escolar']




def switch(option):

    # Save the urls from the web page of INEP
    if option == '--save_urls' or option == '-s_u':
        list_urls = return_urls(KEY_TITLES)
        json.dump(list_urls,open("./downloads_list.json","w"))
    # Generate a list to be used on aria2c to download files
    if option == '--gen_down_list' or option == '-gdl':
        print('generating download list')
        with open(DOWNLOAD_FOLDER+'downloads.txt','w') as file_hand:
            json_schema = json.load(open("./downloads_list.json"))
            for objc in json_schema:
                file_hand.write(objc['zip_url']+'\n')

    # Return zip files problematic the downloads files
    if option == '--validate_zips' or option == '-vz':

        folder_name = DOWNLOAD_FOLDER

        # Get and string of the zips that were wrongly downloaded
        error_zips = validate_zips(folder_name)
        error_zips = re.compile('|'.join(error_zips))

        # Get the zips that weren't downloaded
        not_downloaded = [tuple((mdb_dic['_id'],mdb_dic['zip_url'][::-1].split('/')[0][::-1])) for mdb_dic in list(coll.find({}, {'zip_url': 1}))]
        not_downloaded = [UpdateOne({'_id':tup_mdb[0]},{'$set':{'redownload': not os.path.isfile(folder_name+tup_mdb[1])}}) for tup_mdb in not_downloaded]

        coll.bulk_write(not_downloaded)
        coll.update_many({'zip_url':{'$regex':error_zips}},{'$set': {'redownload':True}})

    # Check if the folder has data, delete if not and update on mongodb
    if option == '--validate_folder' or option == '-vf':
        folder_name = FILES_FOLDER

        #  Delete Folders that are empty
        delete_folders(parent_folder=folder_name, folders_list=get_empty_folders(folder_name))

        # Getting the folders that should have data but haven't
        not_unzipped_list = filter(lambda mdb_dic: is_unziped(folder_name, mdb_dic['title'], mdb_dic['year']), coll.find({}, {'title':1, 'year':1}))
        not_unzipped_ids = map(lambda mdb_dict:mdb_dict['_id'], not_unzipped_list)

        coll.update_many({'_id': {'$in':list(not_unzipped_ids)}}, {'$set': {'reunzip':True}})

    # Unzip files that weren't unzipped
    if option == '--unzip':
        # Generate the unzip list as mongodb expects
        unzip_list = [dict(folder_name=FILES_FOLDER+mdb_dic['title']+'/'+mdb_dic['year'],
              filename=DOWNLOAD_FOLDER+ mdb_dic['zip_url'][::-1].split('/')[0][::-1])
             for mdb_dic in  coll.find({'reunzip':True,"redownload":False},{'_id':0,'title':1,'year':1,'zip_url':1})]
        unzip_files_mdb(unzip_list)


arguments = sys.argv
switch(option = arguments[1])
