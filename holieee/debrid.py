import requests
import os
import cache_manager 
from dotenv import load_dotenv

load_dotenv()

endpoint = 'https://debrid-link.com/api/v2'
debrid_api_token = os.getenv('DEBRID_TOKEN')
timeout = 20

headers = { 
	'Connection': 'keep-alive',
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Accept-Encoding': 'gzip, deflate',
	'User-Agent': 'holieeedsbot',
	'Authorization': 'Bearer ' + debrid_api_token
}

def server_check() -> bool:
	try:
		requests.get('https://debrid-link.com', timeout=timeout, verify=True).raise_for_status()
	except requests.exceptions.RequestException:
		return False
	return True

def add_link(requested_link: str) -> str:
	l = []
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
		if isinstance(d['value'], list):
			for value in d['value']:
				l.append(value['downloadUrl'])
			output = str(l)[1:-1].replace("'", "") # * Slice from first '[' to last ']' and then remove single quotes
			cache_manager.insert_links(requested_link, output)
			return output
		else:
			cache_manager.insert_links(requested_link, d['value']['downloadUrl'])
			return d['value']['downloadUrl']
