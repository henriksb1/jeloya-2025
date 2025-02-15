import asyncio

import websockets


async def send_data(websocket):
    print("New connection:", websocket)
    while True:
        data = "Hello from Python!"
        await websocket.send(data)
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(send_data, "0.0.0.0", 8765):
        print("Serving")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
