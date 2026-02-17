import asyncio
import sqlite3
import datetime
import time
from bleak import BleakScanner

TARGET_NAME = "CMF by Nothing Phone 1" 
REQUIRED_TIME = 10
MIN_SIGNAL = -90

def setup_database():
    conn = sqlite3.connect('class_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  time_in TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

def save_attendance(name):
    conn = sqlite3.connect('class_data.db')
    c = conn.cursor()

    c.execute("SELECT * FROM attendance WHERE name=?", (name,))
    if c.fetchone():
        print(f"   [DB] {name} is already marked.")
    else:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        c.execute("INSERT INTO attendance (name, time_in, status) VALUES (?, ?, ?)",
                  (name, now, "PRESENT"))
        conn.commit()
        print(f"\n [SUCCESS] Saved {name} to Database at {now}!\n")
    conn.close()

async def main():
    setup_database()
    timers = {}
    print(f"Scanning for Name: '{TARGET_NAME}'")

    while True:
        devices_dict = await BleakScanner.discover(return_adv=True, timeout=2.0)
        present_now = []
        for address, (device, adv_data) in devices_dict.items():
            d_name = device.name or ""
            l_name = adv_data.local_name or ""
            if TARGET_NAME in d_name or TARGET_NAME in l_name:

                if adv_data.rssi > MIN_SIGNAL:
                    present_now.append(TARGET_NAME)
                    print(f" >> Found '{TARGET_NAME}' at {address} (RSSI: {adv_data.rssi})")

        now = time.time()

        for student in present_now:
            if student not in timers:
                timers[student] = now
                print(f"timer: ")
            else:
                duration = int(now - timers[student])
                print(f"{student} present for {duration}s / {REQUIRED_TIME}s")

                if duration >= REQUIRED_TIME:
                    save_attendance(student)
                    timers.pop(student) 

        for student in list(timers.keys()):
            if student not in present_now:
                print(f"{student} signal lost. Timer reset.")
                del timers[student]

        await asyncio.sleep(0.5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping...")
