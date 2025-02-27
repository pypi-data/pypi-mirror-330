'''
yadloader is yet another downloader for those poor souls who have to use
Yandex.Disk shared folders to receive big data.

Details: https://pypi.org/project/yadloader
Git repo: https://codeberg.org/screwery/yadloader
'''

__version__ = 'v0.1.0'
__repository__ = 'https://codeberg.org/screwery/yadloader'
__bugtracker__ = 'https://codeberg.org/screwery/yadloader/issues'

import argparse #
import json
import logging
import os
import requests #
import sys
import time
import tqdm #

LIMIT = 100
TIMEOUT = 10
WAIT = 5
MAXTRIES = 3
METHODS = ['metadata', 'download']
CHUNKSIZE = 1024

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

def armored_request(link):
	logging.info(f'GET Request: {link}')
	tries = 0
	while True:
		try:
			response = requests.get(link, timeout=TIMEOUT)
			break
		except Exception as err:
			tries += 1
			logging.warning(f'Request error [try {tries}]: {err}')
			if (tries == MAXTRIES):
				logging.error(f'Cannot perform request. Exit.')
				exit(1)
		time.sleep(WAIT)
	try:
		data = response.json()
	except requests.exceptions.JSONDecodeError:
		logging.error(f'Invalid JSON response')
		exit(1)
	if 'error' in data:
		logging.error(f'{data["error"]}: {data["description"]} ({data["message"]})')
		exit(1)
	return data

def armored_download(name, link, path, total):
	tries = 0
	while True:
		try:
			stream = requests.get(link, stream=True, timeout=TIMEOUT)
			break
		except Exception as err:
			tries += 1
			logging.warning(f'Request error [try {tries}]: {err}')
			if (tries == MAXTRIES):
				logging.error(f'Cannot perform request. Exit.')
				exit(1)
		time.sleep(WAIT)
	stream.raise_for_status()
	output = open(path, 'wb')
	for chunk in tqdm.tqdm(
			stream.iter_content(chunk_size=CHUNKSIZE),
			total=int(total / CHUNKSIZE),
			desc=name,
			unit='kb'
			):
		output.write(chunk)

def render_arguments(arguments):
	key_value = list()
	for key, value in arguments.items():
		key_value.append(f'{key}={value}')
	return '&'.join(key_value)

def get_tree(link, path='/'):
	files = list()
	offset = 0
	while True:
		arguments = {
			'path': path,
			'limit': str(LIMIT),
			'offset': str(offset),
			'public_key': link
			}
		rendered_args = render_arguments(arguments)
		data = armored_request(
			f'https://cloud-api.yandex.net/v1/disk/public/resources?{rendered_args}'
			)
		if (not data['_embedded']['items']):
			break
		for item in data['_embedded']['items']:
			if item['type'] == 'file':
				files.append(item)
			elif item['type'] == 'dir':
				files.extend(get_tree(link, item['path']))
		offset += LIMIT
		time.sleep(WAIT)
	return files

def download_tree(meta_json, root_directory):
	with open(meta_json, 'rt') as meta:
		metadata = json.load(meta)
	try:
		os.mkdir(root_directory)
	except FileExistsError:
		logging.error(f'Output dir already exists!')
		exit(1)
	real_root = os.path.realpath(root_directory)
	for item in metadata:
		real_path = os.path.join(real_root, item['path'][1:])
		os.makedirs(os.path.dirname(real_path), exist_ok = True)
		armored_download(item['name'], item['file'], real_path, item['size'])


def create_parser():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=f'yadloader {__version__}: Yet another downloader for those poor souls who have to use Yandex.Disk shared folders to receive big data',
		epilog=f'Bugtracker: {__bugtracker__}'
		)

	parser.add_argument('-v', '--version', action='version', version=__version__)
	subparsers = parser.add_subparsers(title='Commands', dest='command')

	metadata_parser = subparsers.add_parser('metadata', help=f'Get shared folder tree metadata')
	metadata_parser.add_argument('-l', '--link', required=True, type=str, help=f'Ya.Disk shared folder link (https://disk.yandex.ru/d/XXXXXXXXXXXXXX)')
	metadata_parser.add_argument('-o', '--output', required=True, type=str, help=f'Metadata JSON file')
	metadata_parser.add_argument('-s', '--subdir', default='/', type=str, help=f'Shared folder subdirectory, prepended with /')

	download_parser = subparsers.add_parser('download', help=f'Download shared files listed in metadata JSON file')
	download_parser.add_argument('-m', '--meta', required=True, type=str, help=f'Metadata JSON file')
	download_parser.add_argument('-d', '--dir', required=True, type=str, help=f'Local root directory')
	return parser

def main():
	parser = create_parser()
	namespace = parser.parse_args(sys.argv[1:])
	if namespace.command == 'metadata':
		files = get_tree(namespace.link, namespace.subdir)
		with open(namespace.output, 'wt') as output:
			json.dump(files, output, ensure_ascii=False, indent='\t')
	elif namespace.command == 'download':
		download_tree(namespace.meta, namespace.dir)
	else:
		parser.print_help()

if __name__ == '__main__':
	main()
