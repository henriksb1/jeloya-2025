import asyncio


async def bg_tsk(flag):
    await asyncio.sleep(3)
    flag.set()


async def waiter():
    flag = asyncio.Event()
    asyncio.create_task(bg_tsk(flag))
    await flag.wait()
    print("After waiting")


asyncio.run(waiter())
