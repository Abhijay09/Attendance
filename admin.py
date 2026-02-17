import sqlite3
import csv
import os
import time
import sys

# Configuration
DB_FILE = 'class_data.db'

def clear_screen():
    os.system('clear')

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Exception as e:
        print(f"[ERROR] Could not connect to database: {e}")
        return None

def view_live_feed():
    """Simulates a raw SQL view that refreshes automatically"""
    try:
        while True:
            clear_screen()
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attendance ORDER BY id DESC")
            rows = cursor.fetchall()
            conn.close()

            print("==========================================")
            print("   LIVE DATABASE FEED (CTRL+C to Stop)    ")
            print("==========================================")
            print(f"{'ID':<5} | {'STUDENT NAME':<20} | {'TIME IN':<10} | {'STATUS':<10}")
            print("-" * 56)
            
            if not rows:
                print("       (No records found yet)")
            
            for row in rows:
                # row[0]=id, row[1]=name, row[2]=time, row[3]=status
                print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<10} | {row[3]:<10}")
            
            print("-" * 56)
            print("\nScanning for updates...")
            time.sleep(2)
    except KeyboardInterrupt:
        return

def export_data():
    """Exports data to CSV to satisfy the teacher's requirement"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    conn.close()

    filename = "attendance_export.csv"
    
    print(f"\n[SYSTEM] Exporting {len(rows)} records...")
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write Header
        writer.writerow(['ID', 'Student Name', 'Time In', 'Status'])
        # Write Data
        writer.writerows(rows)
    
    print(f"[SUCCESS] Data saved to '{filename}'")
    print(f"[INFO] Location: {os.path.abspath(filename)}")
    input("\nPress Enter to return...")

def main_menu():
    while True:
        clear_screen()
        print("==========================================")
        print("      ATTENDANCE SYSTEM: BACKEND v1.0     ")
        print("==========================================")
        print("1. View Live Database (Monitor Mode)")
        print("2. DOWNLOAD ATTENDANCE (Export CSV)")
        print("3. Reset Database (Clear All)")
        print("4. Exit")
        print("==========================================")
        
        choice = input("Enter Command [1-4]: ")
        
        if choice == '1':
            view_live_feed()
        elif choice == '2':
            export_data()
        elif choice == '3':
            confirm = input("Are you sure? This deletes all data (y/n): ")
            if confirm.lower() == 'y':
                conn = get_db_connection()
                conn.execute("DELETE FROM attendance")
                conn.commit()
                conn.close()
                print("[SYSTEM] Database cleared.")
                time.sleep(1)
        elif choice == '4':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid command.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
