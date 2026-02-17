import asyncio
from bleak import BleakScanner

async def main():
    print("--- SCANNING FOR 'STUDENT_ONE' (5 Seconds) ---")
    
    # scan for 5 seconds
    devices = await BleakScanner.discover(timeout=5.0)
    
    found = False
    for d in devices:
        # Check if the name matches (case sensitive usually)
        name = d.name or "Unknown"
        
        if name == "STUDENT_ONE":
            print(f"\n✅ FOUND IT!")
            print(f"   Name: {name}")
            print(f"   Address: {d.address}")
            print(f"   Signal (RSSI): {d.rssi}")
            found = True
            break # Stop looking, we found it
        else:
            # Uncomment this line if you want to see OTHER devices while debugging
            # print(f"Ignored: {name} ({d.address})")
            pass

    if not found:
        print("\n❌ NOT FOUND.")
        print("Tip: Toggle Bluetooth OFF/ON on your Laptop.")
        print("Tip: Toggle the Switch OFF/ON in the nRF Connect App.")

if __name__ == "__main__":
    asyncio.run(main())
