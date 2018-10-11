from redis import StrictRedis

from victims.settings import REDIS_DB, REDIS_URL


cache = StrictRedis.from_url(REDIS_URL, db=REDIS_DB)
total = len(cache.keys())
print(f"Flushing {total} key/value pair(s)")
cache.flushall()
print("Done :)")
