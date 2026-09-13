import os
import time

CSV_FILE = "dataset/customer_service.csv"

last_modified = 0

while True:

    current_modified = os.path.getmtime(CSV_FILE)

    if current_modified != last_modified:
        print("Knowledge Base Updated!")

        last_modified = current_modified

    time.sleep(10)