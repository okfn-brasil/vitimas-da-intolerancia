import asyncio

from victims import clear_cache


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(clear_cache())
