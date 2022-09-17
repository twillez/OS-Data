import getpass
import ctypes
import psutil
import GPUtil
import platform
import os
from uuid import getnode as get_mac
import requests 
from datetime import datetime 
import subprocess
import wmi
import psutil
import json

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

try:
    battery = psutil.sensors_battery()
    percent = int(battery.percent)
except:
    pass

svmem = psutil.virtual_memory()

dt_now = datetime.now()

c = wmi.WMI()

user = getpass.getuser()

def SystemInfo():
#--------------------------------------------------------------#
    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
#--------------------------------------------------------------#

    timen = dt_now.strftime("[%d/%m/%y] [%H:%M:%S]") 
 
    palcki = "-------------------------------------------"

    mac = get_mac()

    hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

    DiskFree = psutil.disk_usage('C:').free/(1024*1024*1024)

    MamkaSNI = c.Win32_BaseBoard()[0].SerialNumber.strip()

    DiskTotal = psutil.disk_usage('C:').total/(1024*1024*1024)

    DiskUsed = psutil.disk_usage('C:').used/(1024*1024*1024)

    allram = get_size(svmem.total)

    CPU = platform.processor() 

    for physical_disk in c.Win32_DiskDrive():
        hwid2 = physical_disk.SerialNumber

    try:
        gpus = GPUtil.getGPUs()
        list_gpus = []
        for gpu in gpus:
            GPU = 'GPU: ' + gpu.name
    except:
        pass

    DiskFree1 = '%.2f'%DiskFree

    DiskTotal1 = '%.2f'%DiskTotal

    DiskUsed1 = '%.2f'%DiskUsed
#--------------------------------------------------------------#
    Antiviruses1 = {
    'C:\\Program Files\\Windows Defender': 'Windows Defender',
    'C:\\Program Files\\AVAST Software\\Avast': 'Avast',
    'C:\\Program Files\\AVG\\Antivirus': 'AVG',
    'C:\\Program Files (x86)\\Avira\\Launcher': 'Avira',
    'C:\\Program Files (x86)\\IObit\\Advanced SystemCare': 'Advanced SystemCare',
    'C:\\Program Files\\Bitdefender Antivirus Free': 'Bitdefender',
    'C:\\Program Files\\DrWeb': 'Dr.Web',
    'C:\\Program Files\\ESET\\ESET Security': 'ESET',
    'C:\\Program Files (x86)\\Kaspersky Lab': 'Kaspersky Lab',
    'C:\\Program Files (x86)\\360\\Total Security': '360 Total Security',
    'C:\\Program Files\\ESET\\ESET NOD32 Antivirus': 'ESET NOD32'
    }
    Antivirus = [Antiviruses1[d] for d in filter(os.path.exists, Antiviruses1)] 

    Antiviruses = json.dumps(Antivirus)

#--------------------------------------------------------------#
    HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
    }

    try:

        ip = requests.get('https://api.ipify.org').text

        linkip = 'http://ip-api.com/json/'+ip

        local = requests.get(linkip,headers=HEADERS).json()

        data = {
            'Country': local.get('country'),
            'City': local.get('city'),
            'Provide': local.get('isp')
        }
    except:
        pass
#--------------------------------------------------------------#

    print(f"{palcki}")
    print(f"- Time: {timen}")
    try:
        print(f"- IP: {ip}")
        for k,v in data.items():
            print(f'- {k}: {v}')
    except:
        pass
    print(f"{palcki}")
    print(f"- Mac-Adress: {mac}")
    print(f'- HWID: {hwid}')
    print(f'- HWID2: {hwid2}')
    print(f'- MamkaSNI: {MamkaSNI}')
    print(f"{palcki}")
    print(f"- {GPU}")
    print(f"- CPU: {CPU}")
    print(f"- RAM: {allram}")
    try:
        print(f'- Battery: {percent}%')
    except:
        print('- Battery: None\n')
    print('- Screen:', str(screensize))
    print(f"{palcki}")
    print(f"- DiskFree: {DiskFree1}")
    print(f"- DiskTotal: {DiskTotal1}")
    print(f"- DiskUsed: {DiskUsed1}")
    #print('- Антивирус:',end="")
    print("- Antivirus: " + str(Antiviruses))
    print(f"{palcki}")

    #os.system('pause')
SystemInfo()
