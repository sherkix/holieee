import threading
import time
from cache_manager import clear_cache

def routine():
    while True:
        clear_cache()
        time.sleep(604800)

t = threading.Thread(target=routine)
t.start()
