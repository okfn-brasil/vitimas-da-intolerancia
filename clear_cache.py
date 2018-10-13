import asyncio

from aiocache import caches

from victims.settings import CACHE


loop = asyncio.get_event_loop()
caches.set_config(CACHE)
loop.run_until_complete(caches.get("default").clear())
print("Done :)")
