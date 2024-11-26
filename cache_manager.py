import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def connect():
	conn = pymysql.connect(
		host=os.getenv('DB_HOST'),
		user=os.getenv('DB_USER'),
		password=os.getenv('DB_PW'),
		db=os.getenv('DB_NAME'),
	)
	return conn
	
def get_cached_links(requested_link):
	conn = connect()
	cur = conn.cursor()
	sql = 'SELECT CachedLinks FROM Links WHERE RequestedLinks = %s'
	cur.execute(sql, f'{requested_link}')
	output = cur.fetchall()
	conn.close()
	
	if len(output) == 0:
		return None
	else:
		return output[0][0] + ' (Cached)'

def insert_links(requested_link, debrider_link):
	conn = connect()
	cur = conn.cursor()
	sql = 'INSERT INTO Links (RequestedLinks, CachedLinks) VALUES (%s, %s)'
	cur.execute(sql, (f'{requested_link}', f'{debrider_link}'))
	conn.commit()
	conn.close()
	return 