import asyncio
import sqlite3
import datetime
import time
from bleak import BleakScanner

# --- CONFIGURATION ---
TARGET_ADDRESS = "6F:6D:E5:C9:71:25"  # <--- PASTE YOUR ADDRESS HERE
REQUIRED_TIME = 10   # Seconds (Keep short for demo)
MIN_SIGNAL = -90     # Signal strength cutoff

# --- DATABASE SETUP ---
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
    
    # Check if already present
    c.execute("SELECT * FROM attendance WHERE name=?", (name,))
    if c.fetchone():
        print(f"   [DB] {name} is already marked.")
    else:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        c.execute("INSERT INTO attendance (name, time_in, status) VALUES (?, ?, ?)",
                  (name, now, "PRESENT"))
        conn.commit()
        print(f"\n🎉 [SUCCESS] Saved {name} to Database at {now}!\n")
    conn.close()

# --- MAIN LOOP ---
async def main():
    setup_database()
    timers = {}
    
    print(f"--- ATTENDANCE SYSTEM ACTIVE ---")
    print(f"Targeting Address: {TARGET_ADDRESS}")
    print(f"Press Ctrl+C to stop.\n")

    while True:
        # Scan using the method that fixes your 'rssi' error
        devices_dict = await BleakScanner.discover(return_adv=True, timeout=2.0)
        
        present_now = []
        
        # Check if our target is in the results
        if TARGET_ADDRESS in devices_dict:
            device, adv_data = devices_dict[TARGET_ADDRESS]
            
            if adv_data.rssi > MIN_SIGNAL:
                # We found the phone!
                student_name = "STUDENT_ONE" # Hardcoded name for the prototype
                present_now.append(student_name)
                print(f" >> Signal detected! RSSI: {adv_data.rssi} dBm")

        # Timer Logic
        now = time.time()
        
        for student in present_now:
            if student not in timers:
                timers[student] = now
                print(f"   [TIMER START] Counting...")
            else:
                duration = int(now - timers[student])
                print(f"   [TRACKING] {duration}s / {REQUIRED_TIME}s")
                
                if duration >= REQUIRED_TIME:
                    save_attendance(student)
                    timers.pop(student) 

        # Reset if signal lost
        for student in list(timers.keys()):
            if student not in present_now:
                print(f"   [LOST] Signal lost. Timer reset.")
                del timers[student]

        await asyncio.sleep(0.5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping...")
