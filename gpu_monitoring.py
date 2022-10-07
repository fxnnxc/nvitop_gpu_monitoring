import time
from nvitop import Device
import csv 
import os 
import csv
import argparse

# --------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--duration", type=int, default=60)
args = parser.parse_args()
DURATION = args.duration # seconds
fieldnames = ['date', 'time', 'username', 'pid', 'gpu_memory', 'gpu_memory_percent', 'device']
# --------------------------

# 1. make the save directory
base_dir = "gpu_monitoring"
if not os.path.exists(base_dir):
    os.mkdir(base_dir)

# 2. get devices 
devices = Device.all() 

# 3. running the snap-shot
save_date, _ = time.strftime('%Y-%m-%d_%H:%M:%S').split("_")
count = 0
while True:
    # 3. get the current time 
    current_date, current_time = time.strftime('%Y-%m-%d_%H:%M:%S').split("_")

    # change the date when it is over and make a new csv file
    if current_date != save_date or count == 0:
        save_date = current_date
        save_path = f"{base_dir}/{save_date}.csv"
        with open(save_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
    save_path = f"{base_dir}/{save_date}.csv"
    for processes in list(map(Device.processes, devices)):
        for p_id, proc in processes.items():
            dic = {}
            dic['date'] = current_date
            dic['time'] = current_time
            dic['username'] = proc.username()
            dic['pid'] = proc.pid
            dic['gpu_memory'] = proc.gpu_memory_human()
            dic['gpu_memory_percent'] = proc.gpu_memory_percent()
            dic['device'] = proc.device.index
            
            with open(save_path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(dic)
                print(f"[INFO] saved at {save_date} {current_time}")
            
    # save duration 
    time.sleep(DURATION)
    count += 1
    
