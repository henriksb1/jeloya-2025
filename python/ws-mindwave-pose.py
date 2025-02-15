import asyncio
import datetime
import json
import multiprocessing
import sys

import cv2
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


multi_manager = multiprocessing.Manager()
direction_value = multi_manager.Value('direction', 0.5)


async def broadcast(message):
    if clients:  # Only send if there are connected clients
        # Create tasks for each client to send the message
        value = json.dumps(message)
        await asyncio.gather(
            *[client.send(value) for client in clients],
            return_exceptions=True
        )


async def mindwave_reader(direction_value: multiprocessing.Value):
    input("Open serial port, then press ENTER to start")
    print('Connecting to Mindwave...')
    headset = mindwave.Headset('/dev/rfcomm0')

    print('Connected, start data stream')

    while True:
        print(direction_value, direction_value.value)
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
                'direction': direction_value.value,
            }

            # Broadcast to all connected clients
            await broadcast(data)

            # Sleep for a short duration (50Hz rate)
            await asyncio.sleep(1 / 50)

        except Exception as e:
            print(f"Error reading mindwave data: {e}")
            await asyncio.sleep(1)


def pose_reader(direction_value: multiprocessing.Value):
    from python.pose import detect
    print("Starting camera...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    print("Go!")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame")
                break

            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = detect(frame)
            # print(results)
            try:
                best = max((result for result in results if result['label'] == 'person'),
                           key=lambda result: result['score'])
            except ValueError:
                print("======== You're outside the frame! Move back in! =========")
                continue  # Keep previous reading
            width = frame.shape[1]
            r = best['box'][2]
            l = best['box'][0]
            person_center_x = (r - l) / 2 + l
            direction = person_center_x / width
            print(direction)
            print(direction_value, direction_value.value)
            direction_value.value = direction

            # cv2.imshow('Webcam', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            # if cv2.waitKey(1) == ord('q'):
            #     break
    except Exception as e:
        cap.release()
        raise e
    finally:
        cap.release()


async def main():
    # Start websocket server
    async with websockets.serve(register, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")

        # Start mindwave reader task
        mindwave_task = asyncio.create_task(mindwave_reader(direction_value))
        p = multiprocessing.Process(target=pose_reader, args=(direction_value,))
        p.start()

        # Run forever
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            mindwave_task.cancel()
            try:
                await mindwave_task
            except asyncio.CancelledError as e:
                print(e, file=sys.stderr)
        p.terminate()


if __name__ == "__main__":
    asyncio.run(main())
