import sqlite3
import csv
import os
import time
import sys

DB_FILE = 'class_data.db'

def clear_screen():
    os.system('clear')

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Exception as e:
        print(f"Could not connect to database: {e}")
        return None

def view_live_feed():
    try:
        while True:
            clear_screen()
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attendance ORDER BY id DESC")
            rows = cursor.fetchall()
            conn.close()

            print("DATABASE FEED")
            print(f"{'ID':<5} | {'STUDENT NAME':<20} | {'TIME IN':<10} | {'STATUS':<10}")
            print("-" * 56)

            if not rows:
                print("No records found yet")

            for row in rows:
                print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<10} | {row[3]:<10}")

            print("-" * 56)
            print("\nScanning for updates...")
            time.sleep(2)
    except KeyboardInterrupt:
        return

def export_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    conn.close()
    os.makedirs("info", exist_ok=True) 

    filename = "info/attendance_export.csv"
    print(f"\n Exporting {len(rows)} records...")

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Student Name', 'Time In', 'Status'])
        writer.writerows(rows)

    print(f"Data saved to '{filename}'")
    print(f"Location: {os.path.abspath(filename)}")

def main_menu():
    while True:
        clear_screen()
        print("ATTENDANCE SYSTEM:")
        print("1. View Live Database")
        print("2. DOWNLOAD ATTENDANCE")
        print("3. Reset Database")
        print("4. Exit")

        choice = input("Enter Command [1-4]: ")

        if choice == '1':
            view_live_feed()
        elif choice == '2':
            export_data()
        elif choice == '3':
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
