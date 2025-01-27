import requests
import os
import cache_manager 
from dotenv import load_dotenv

load_dotenv()

endpoint = 'https://debrid-link.com/api/v2'
debrid_api_token = os.getenv('DEBRID_TOKEN')
timeout = 20
l = []

headers = { 
	'Connection': 'keep-alive',
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Accept-Encoding': 'gzip, deflate',
	'User-Agent': 'holieeedsbot',
	'Authorization': 'Bearer ' + debrid_api_token
}

def server_check():
	response = requests.get('https://debrid-link.com', verify=True)
	if response.status_code == 200:
		return True
	else:
		return False

def add_link(requested_link):
	l.clear()
	requested_link = requested_link.strip()
	cached_link = cache_manager.get_cached_links(requested_link) # * Get cached links in the db
	if cached_link is not None:
		print(f'Requested url: {requested_link}')
		print('The request was cached')
		return cached_link # * The function returns if the link is found in the db
	payload = {'url': requested_link}
	print(f'Requested url: {payload["url"]}')
	try:
		response = requests.post(url=endpoint + '/downloader/add', headers=headers, json=payload, timeout=timeout, verify=True)
		response.raise_for_status()
		d = response.json()
	except requests.exceptions.Timeout:
		return 'Timeout'
	except requests.exceptions.HTTPError:
		return 'Host non valido'
	except requests.exceptions.SSLError:
		return 'Errore SSL'
	
	if d['success'] is True:
		if type(d['value']) is list:
			for value in d['value']:
				l.append(value['downloadUrl'])
			output = str(l)[1:-1].replace("'", "") # * Slice from first '[' to last ']' and then remove single quotes
			cache_manager.insert_links(requested_link, output)
			return output
		else:
			cache_manager.insert_links(requested_link, d['value']['downloadUrl'])
			return d['value']['downloadUrl']