import asyncio
import argparse
import sys
from bleak import BleakScanner
from datetime import datetime, timedelta

# Set the target device name
TARGET_DEVICE_NAME = ['Dangerous-Vehicle']
TARGET_SERVICE_UUID = "6362b48b-130c-4e9e-9e48-c068f959084b"

device_info = {}
scan_delay = 30
device_timeout_period = 3
program_timeout_period = 1 #TODO implement
scan_duration = 10
advertisement_scan_duration = 30

def detection_callback(device, advertisement_data):
    now = datetime.now()
    if device.name in TARGET_DEVICE_NAME:
        if device.address not in device_info:
            device_info[device.address] = {
                'device_name': device.name,
                'advertisement_count': 1,
                'first_heard': now,
                'last_heard': now
            }

        else:
            device_info[device.address]['last_heard'] = now
            device_info[device.address]['advertisement_count'] += 1


async def advertisment_scan():
    #TODO Update to initialize scanner with callback
    #scanner = BleakScanner(detection_callback())
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(advertisement_scan_duration)
    await scanner.stop()

async def log_bluetooth_broadcasts():
    device_has_been_seen = False
    device_registered = False

    start_time = datetime.now()
    print("******************************************************************")
    print("Program Start time: ", start_time)
    print("Program Timeout: ", program_timeout_period, " minutes (LOGIC NOT IMPLEMENTED)")
    print(f"Target Device Name: {TARGET_DEVICE_NAME}")
    print(f"Target Service UUID: {TARGET_SERVICE_UUID}")
    print(f"Scan Duration: {scan_duration} seconds")
    print(f"Scan Delay: {scan_delay} seconds")
    print(f"Device Timeout: {device_timeout_period} minutes")
    print(f"Advertisement Scan Duration: {advertisement_scan_duration} seconds")
    print("******************************************************************\n")

    print("Performing Initial scan to determine advertising interval...")
    await advertisment_scan()
    if len(device_info) == 0:
        print("No devices found during initial scan, not able to calculate advertisement interval!!!")

    for addr, info in list(device_info.items()):
        print(f"Advertisng Report for {addr}:")
        print(f"    Advertising count: {info['advertisement_count']} over {advertisement_scan_duration} seconds")
        print(f"    Avg Adv Interval: {advertisement_scan_duration/info['advertisement_count']} seconds")

    while True:
        devices = await BleakScanner.discover(timeout=scan_duration,
                                              discovery_data_filter={"uuids": [TARGET_SERVICE_UUID]})
        now = datetime.now()
        device_seen_this_scan = False
        for device in devices:
            if device.name in TARGET_DEVICE_NAME:
                device_has_been_seen = True
                device_seen_this_scan = True
                if device.address not in device_info:
                    device_info[device.address] = {
                        'device_name': device.name,
                        'first_heard': now,
                        'last_heard': now
                    }
                else:
                    device_info[device.address]['last_heard'] = now

        if (device_has_been_seen and not device_registered):
            print()
            print("Device registered: ", datetime.now())
            print(device_info)
            device_registered = True

        timeout = timedelta(minutes=device_timeout_period)
        for addr, info in list(device_info.items()):
            if now - info['last_heard'] >= timeout:
                first_heard = info['first_heard']
                last_heard = info['last_heard']
                active_time = last_heard - first_heard
                active_hours = active_time.total_seconds() / 3600

                print("\n")
                print(f"Device {addr} report:")
                print(f"  Device name: {info['device_name']}")
                print(f"  First heard: {first_heard}")
                print(f"  Last heard: {last_heard}")
                print(f"  Active time: {active_time} (approximately {active_hours:.2f} hours)")

                del device_info[addr]
                exit(0)

        #TODO add logic for program timeout?

        if (device_seen_this_scan):
            print(".", end="", flush=True)
        else:
            print("X", end="", flush=True)

        # Wait for a while before scanning again
        await asyncio.sleep(scan_delay)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Description of your program')
    
    parser.add_argument('-s','--scan_duration', help='Scan duration in seconds', required=False, default=10)
    parser.add_argument('-d','--scan_delay', help='Scan delay in seconds', required=False, default=30)
    parser.add_argument('-t','--device_timeout_period', help='Device timeout period in minutes', required=False, default=3)
    parser.add_argument('-a','--advertisement_scan_duration', help='Advertisement scan duration in seconds', required=False, default=30)
    parser.add_argument('-n','--target_device_name', help='Target device name', type=str, required=False, default='Dangerous-Vehicle')
    parser.add_argument('-u','--target_service_uuid', help='Target service UUID', type=str, required=False, default='6362b48b-130c-4e9e-9e48-c068f959084b')
    parser.add_argument('-p','--program_timeout_period', help='Program timeout period in minutes (Not Currenlty Implemented!!!)', required=False, default=1)

    args = vars(parser.parse_args())

    print("******************************************************************") 
    print("Starting program...")
    print("Press Ctrl+C to exit\n")
    print("******************************************************************")

    scan_duration = int(args['scan_duration'])
    scan_delay = int(args['scan_delay'])
    device_timeout_period = int(args['device_timeout_period'])
    advertisement_scan_duration = int(args['advertisement_scan_duration'])
    TARGET_DEVICE_NAME = str(args['target_device_name'])
    TARGET_SERVICE_UUID = str(args['target_service_uuid'])
    program_timeout_period = int(args['program_timeout_period'])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(log_filtered_bluetooth_broadcasts())