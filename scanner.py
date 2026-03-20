import asyncio
import sqlite3
import datetime
import time
from bleak import BleakScanner

TARGET_NAMES = [
    "CMF by Nothing Phone 1",
    "POCO X6 Pro 5G",
    "Device 3",
    "Device 4",
    "Device 5"
]

REQUIRED_TIME = 30     
GRACE_PERIOD = 15     
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
        print(f"[DB] {name} already marked.")
    else:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        c.execute("INSERT INTO attendance (name, time_in, status) VALUES (?, ?, ?)",
                  (name, now, "PRESENT"))
        conn.commit()
        print(f"\n[SUCCESS] Saved {name} at {now}\n")

    conn.close()

async def main():
    setup_database()

    timers = {}       
    last_seen = {}   

    print(f"Scanning for: {TARGET_NAMES}")

    while True:
        devices_dict = await BleakScanner.discover(return_adv=True, timeout=2.0)
        present_now = []

        for address, (device, adv_data) in devices_dict.items():
            d_name = device.name or ""
            l_name = adv_data.local_name or ""

            for target in TARGET_NAMES:
                if target in d_name or target in l_name:
                    if adv_data.rssi > MIN_SIGNAL:
                        present_now.append(target)
                        last_seen[target] = time.time()
                        print(f">> Found '{target}' (RSSI: {adv_data.rssi})")

        now = time.time()

        for student in TARGET_NAMES:

            if student in present_now:
                if student not in timers:
                    timers[student] = now
                    print(f"{student} timer started")
                else:
                    duration = int(now - timers[student])
                    print(f"{student} present {duration}s / {REQUIRED_TIME}s")

                    if duration >= REQUIRED_TIME:
                        save_attendance(student)
                        timers.pop(student, None)
                        last_seen.pop(student, None)

            else:
                if student in timers:
                    last_time = last_seen.get(student, 0)
                    gap = now - last_time

                    if gap <= GRACE_PERIOD:
                        print(f"{student} temporarily lost ({int(gap)}s), within grace...")
                    else:
                        print(f"{student} lost > {GRACE_PERIOD}s → RESET")
                        timers.pop(student, None)
                        last_seen.pop(student, None)

        await asyncio.sleep(0.5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping...")
