from redis import StrictRedis

from victims.settings import REDIS_DB, REDIS_URL


StrictRedis.from_url(REDIS_URL, db=REDIS_DB).flushall()
