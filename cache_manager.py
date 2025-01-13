import pymysql
import os
import logger
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
	with connect() as conn:
		with conn.cursor() as cur:
			sql = 'SELECT CachedLinks FROM Links WHERE RequestedLinks = %s'
			cur.execute(sql, requested_link)
			output = cur.fetchall()
	if len(output) == 0:
		return None
	else:
		return output[0][0] + ' (Cached)'

def insert_links(requested_link, debrider_link):
	with connect() as conn:
		with conn.cursor() as cur:
			sql = 'INSERT INTO Links (RequestedLinks, CachedLinks) VALUES (%s, %s)'
			cur.execute(sql, (requested_link, debrider_link))
		conn.commit()
	return 