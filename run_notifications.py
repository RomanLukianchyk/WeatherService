import time
import os

while True:
    print("Running send_notifications...")
    os.system("python manage.py send_notifications")
    time.sleep(60)
