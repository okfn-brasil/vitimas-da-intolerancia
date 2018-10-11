import asyncio

from aioredis import create_redis

from victims.settings import REDIS_URL


async def main():
    redis = await create_redis(REDIS_URL)
    keys = len(await redis.keys("*"))
    print(f"Flushing {keys} key/value pair(s)")
    await redis.flushall()
    print("Done :)")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
