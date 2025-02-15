import asyncio
import datetime
import json
import sys

import websockets

import mindwave

# Keep track of all connected websocket clients
clients = set()


async def register(websocket):
    print("Register", websocket)
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        print("Close", websocket)
        clients.remove(websocket)


async def broadcast(message):
    if clients:  # Only send if there are connected clients
        # Create tasks for each client to send the message
        await asyncio.gather(
            *[client.send(message) for client in clients],
            return_exceptions=True
        )


async def mindwave_reader():
    input("Open serial port, then press ENTER to start")
    print('Connecting to Mindwave...')
    headset = mindwave.Headset('/dev/rfcomm0')

    print('Connected, start data stream')

    while True:
        try:
            ts = datetime.datetime.now(datetime.UTC).isoformat()

            if headset.poor_signal > 200:
                print("Poor signal, adjust headset", headset.poor_signal)
                await asyncio.sleep(1)

            # Create data dictionary
            data = {
                'timestamp': ts,
                'poor_signal': headset.poor_signal,
                'raw_value': headset.raw_value,
                'attention': headset.attention,
                'meditation': headset.meditation,
                'blink': headset.blink,
                'waves': headset.waves,
            }

            # Convert to JSON string
            message = json.dumps(data)

            # Broadcast to all connected clients
            await broadcast(message)

            # Sleep for a short duration (50Hz rate)
            await asyncio.sleep(1 / 50)

        except Exception as e:
            print(f"Error reading mindwave data: {e}")
            await asyncio.sleep(1)


async def main():
    # Start websocket server
    async with websockets.serve(register, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")

        # Start mindwave reader task
        mindwave_task = asyncio.create_task(mindwave_reader())

        # Run forever
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            mindwave_task.cancel()
            try:
                await mindwave_task
            except asyncio.CancelledError as e:
                print(e, file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
