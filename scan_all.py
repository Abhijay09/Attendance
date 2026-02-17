import asyncio
from bleak import BleakScanner

async def main():
    print("Scanning for 5 seconds...")
    print("Look for the device with RSSI closest to 0 (e.g., -40 is stronger than -90)")
    
    # return_adv=True fixes the error by giving us the data packet separately
    devices_dict = await BleakScanner.discover(return_adv=True, timeout=5.0)
    
    for address, (device, adv_data) in devices_dict.items():
        rssi = adv_data.rssi
        name = device.name or "Unknown"
        
        # Only print devices with decent signal to reduce clutter
        if rssi > -80: 
            print(f"-----------------------------------")
            print(f"Name:    {name}")
            print(f"Address: {address}")  # <--- COPY THIS
            print(f"RSSI:    {rssi}")

if __name__ == "__main__":
    asyncio.run(main())
