import pymysql
import os
import logger
from dotenv import load_dotenv

load_dotenv()

class CacherError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        logger.log_error('CacherError: ' + msg)
        
    def __str__(self):
        return self.msg
	

def connect():
	try:
		conn = pymysql.connect(
			host=os.getenv('DB_HOST'),
			user=os.getenv('DB_USER'),
			password=os.getenv('DB_PW'),
			db=os.getenv('DB_NAME'),
		)
	except pymysql.OperationalError as err:
		raise CacherError(f"Can't connect to the database: {err}") from err
	return conn

def create_links_table():
	with connect() as conn:
		with conn.cursor() as cur:
			sql = ('CREATE TABLE IF NOT EXISTS '
					'Links'
					'(LinkId int auto_increment,'
					'UserId bigint,'
					'RequestedLinks varchar(1000),'
					'CachedLinks varchar(1000),'
					'Timestamp timestamp default current_timestamp,' 
					'primary key(LinkId));'
                )
			try:
				cur.execute(sql)
			except pymysql.OperationalError as err:
				raise CacherError(f"Can't create table Links {err}") from err
		conn.commit()
	return

def get_cached_links(requested_link: str) -> str | None:
	with connect() as conn:
		with conn.cursor() as cur:
			sql = 'SELECT CachedLinks FROM Links WHERE RequestedLinks = %s'
			cur.execute(sql, requested_link)
			output = cur.fetchall()
	if len(output) == 0:
		return None
	else:
		return output[0][0] + ' (Cached)'

def insert_links(userid: int, requested_link: str, debrider_link: str):
	with connect() as conn:
		with conn.cursor() as cur:
			sql = 'INSERT INTO Links (UserId, RequestedLinks, CachedLinks) VALUES (%s, %s, %s)'
			cur.execute(sql, (userid, requested_link, debrider_link))
		conn.commit()
	return

def clear_cache():
	with connect() as conn:
		with conn.cursor() as cur:
			sql = 'DELETE FROM Links WHERE Timestamp < (NOW() - INTERVAL 7 DAY)'
			cur.execute(sql)
		conn.commit()
	return