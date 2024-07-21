import requests
import asyncio
from functools import partial
import aiohttp
import ssl
import pprint


# def non_awaitable_method(iter, delay):
def non_awaitable_method(iter):
    """blocking_method io"""
    # print(f"this is from sync method io: {iter}")
    # # begin = time.perf_counter()
    # # time.sleep(delay)
    # # end = time.perf_counter()
    # print(f"sync method io: {iter} done in {end - begin}")
    print(iter)
    response = requests.get("https://django-backend-rhm3xnqngq-uc.a.run.app/user?id=19")
    print(response)


# for idx in range(100):
#     print(idx)
#     response = requests.get("https://django-backend-rhm3xnqngq-uc.a.run.app/user?id=19")
#     print(response)


async def test():
    # asyncio.gather can be used as well from within a running loop as it
    # doesn't create a new loop and schedules coroutines on the current loop,
    # this alleviates the need to create tasks manually
    coros = []
    for idx in range(1000):
        coro = asyncio.to_thread(partial(non_awaitable_method, idx))
        coros.append(coro)
    await asyncio.gather(*coros)


# asyncio.run(test())


urls = ["https://django-backend-rhm3xnqngq-uc.a.run.app/user?id=19"] * 1000


async def fetch(session, url, idx):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        print(idx)
        return await response.json()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        coros = []
        for idx, url in enumerate(urls):
            coros.append(fetch(session, url, idx))
        results = await asyncio.gather(*coros, return_exceptions=True)
        return results


loop = asyncio.get_event_loop()
results = loop.run_until_complete(fetch_all(urls, loop))
pprint.pp(results)
