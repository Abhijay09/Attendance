import asyncio
from bleak import BleakScanner

async def main():
    print("Scanning for devices")
    devices_dict = await BleakScanner.discover(return_adv=True, timeout=5.0)
    devices_list = []

    for address, (device, adv_data) in devices_dict.items():
        rssi = adv_data.rssi
        name = device.name or "Unknown"

        if rssi > -100:
            devices_list.append((rssi, name, address))

    devices_list.sort(key=lambda x: x[0])

    for rssi, name, address in devices_list:
        print(f"Name:    {name}")
        print(f"Address: {address}")
        print(f"RSSI:    {rssi}")

if __name__ == "__main__":
    asyncio.run(main())
