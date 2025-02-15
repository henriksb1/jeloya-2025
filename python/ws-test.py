import asyncio
import websockets

async def send_data(websocket):
    while True:
        data = "Hello from Python!"
        await websocket.send(data)
        await asyncio.sleep(1)

async def main():
    async with websockets.serve(send_data, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())