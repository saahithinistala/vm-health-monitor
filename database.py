from sqlite3 import connect
from metrics import metrics_dict
from datetime import datetime

def connect_database():
    try:
        connection = connect("vm_health.db")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu_used REAL,
                memory_used REAL,
                disk_used REAL,
                load_average REAL,
                uptime TEXT
            )
        """)
        connection.commit()
        print("Metrics table created successfully")
        connection.close()
    except Exception as error:
        print(f"Database connection failed: {error}")


def save_metrics():
    try:
        connection = connect("vm_health.db")
        cursor = connection.cursor()
        current_time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO metrics
            (timestamp, cpu_used, memory_used, disk_used, load_average, uptime)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            current_time_stamp,
            metrics_dict['cpu_used'],
            metrics_dict['memory_used'],
            metrics_dict['disk_used'],
            metrics_dict['load_average'],
            metrics_dict['uptime']
        ))

        connection.commit()
        connection.close()
    except Exception as error:
        print(f"Database operation failed: {error}")

def view_metrics():
    try:
        connection = connect("vm_health.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM metrics")
        rows = cursor.fetchall()
        print(f"{'ID':<4} {'Timestamp':<20} {'CPU':<8} {'Memory':<8} {'Disk':<8} {'Load Avg':<12} {'Uptime'}")
        for row in rows:
            print(f"{row[0]:<4} {row[1]:<20} {row[2]:<8} {row[3]:<8} {row[4]:<8} {row[5]:<12} {row[6]}")
        connection.close()
    except Exception as error:
        print(f"Database operation failed: {error}")





