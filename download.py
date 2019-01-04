import asyncio
import aiohttp
import aiofiles
import queue
from time import sleep
from handle_files import Unzip

TIME = 2
error = open('log.txt', 'w')


# Download and write files into chunks assynchronosly using threads to unzip
async def download_big_file(session, q_url, q_zip):
	data_obj = await q_url.get()
	url = data_obj['zip_url']
	filename = url[::-1].split('/')[0][::-1]
	folder, path_file = r'./files/%s/%s/'%(data_obj['title'], data_obj['year']), r'./downloads/%s' % filename
	resume_header = {}

	async with aiofiles.open(path_file, 'wb') as f:
		try:
			# Get requests of the file
			async with session.get(url,timeout=None,headers=resume_header) as response:
				# Download into chunks
				async for data, ended in response.content.iter_chunks():
					if ended:
						# Using a queue to communicate to threads and unzip files
						while q_zip.full():
							sleep(TIME)
						q_zip.put_nowait({'folder_name': folder, 'filename': './downloads/%s' % filename})
						unzip_class.start_thread()
						break
					await f.write(data)
		except Exception as e:
			await f.close()
			print('%s %s' % (filename, str(e)))
			error.write('filename: %s | %s\n' % (filename, str(e)))


# Async get urls from list
async def get_urls(urls: list, loop, q_zip):

	# Initiate the urls queue
	q_url = asyncio.Queue()
	[q_url.put_nowait(value) for value in urls]

	conn = aiohttp.TCPConnector(limit=50)
	tasks = []
	async with aiohttp.ClientSession(loop=loop,connector=conn) as session:
		for i in range(len(urls)):
			task = asyncio.ensure_future(download_big_file(session, q_url, q_zip))
			tasks.append(task)
		await asyncio.gather(*tasks)


def async_dowload(zip_dicts):
	# Handling the zip files to the entire code
	zip_queue = queue.Queue(maxsize=10)
	global unzip_class
	unzip_class = Unzip(zip_queue)

	# Loop Related
	new_loop = asyncio.new_event_loop()
	asyncio.set_event_loop(new_loop)
	new_loop.run_until_complete(asyncio.ensure_future(get_urls(urls=zip_dicts,loop=new_loop,q_zip=zip_queue)))
