import csv
import datetime
import mindwave
import time

fs = 100
T = 1 / fs

print('Hi, give me name of the recording session, for example persons name. Timestamp will be added automatically.')
session_name = input('Session name: ')

ts = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H-%M-%S')
filename = f'recordings/{session_name}_{ts}.dat'

print(f'Writing to {filename}')

print('Connecting to Mindwave...')
headset = mindwave.Headset('/dev/rfcomm0')

print('Connected, waiting 10 seconds for data to start streaming')
# time.sleep(10)

print('Starting to record, automatically recording 10 minute slice so keep on working...')
f = open(filename, 'w')
now = time.time()
future = now + 60 * 10
with f:
    writer = csv.writer(f)
    writer.writerow(
        ['Timestamp', 'Poor-signal', 'Raw', 'Attention', 'Meditation', 'delta', 'theta', 'low-alpha', 'high-alpha',
         'low-beta', 'high-beta', 'low-gamma', 'mid-gamma'])
    while time.time() < future:
        ts = datetime.datetime.now(datetime.UTC).isoformat()
        if headset.poor_signal > 200:
            print("Poor signal, adjust headset", headset.poor_signal)
            time.sleep(1)
        print("Raw value: %s, Attention: %s, Meditation: %s" % (headset.raw_value, headset.attention, headset.meditation))
        print("Waves: {}".format(headset.waves))
        values = list(headset.waves.values())
        values = [ts, headset.poor_signal, headset.raw_value, headset.attention, headset.meditation] + values
        writer.writerow(values)
        time.sleep(T)
