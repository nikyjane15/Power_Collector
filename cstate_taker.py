from datetime import datetime
import json
import threading
import time
import os
import re
from model import State, Time, CPU_Time

import configuration

hostname = configuration.hostname
counters_time = CPU_Time(timestamp=datetime.now(), block=[])
counter_usage = CPU_Time(timestamp=datetime.now(), block=[])
count = 0
time_state = {}
usage_state = {}

f = "/sys/devices/system/cpu"
p = re.compile(r'\d+')
dir_temp = sorted([element for element in os.listdir(f) if re.match('cpu\d+', element)])
dir_cpu = sorted(dir_temp, key=lambda s: int(re.search(r'\d+', s).group()))
now = datetime.now()
for element in dir_cpu:
    f1 = f + "/" + element + "/cpuidle"
    cpu_time = Time(cpu=element, state=[])
    cpu_usage = Time(cpu=element, state=[])
    a = sorted(os.listdir(f1))

    for state in a:
        f2_time = f1 + "/" + state + "/time"
        f2_usage = f1 + "/" + state + "/usage"

        with open(f2_time, "r") as file:
            temp = file.readlines()
            cpu_time.state.append(State(state=state, value=temp[0]))
        with open(f2_usage, "r") as file:
            temp = file.readlines()
            cpu_usage.state.append(State(state=state, value=temp[0]))

    counters_time.block.append(cpu_time)
    counter_usage.block.append(cpu_usage)


reu = counters_time.json()

print("done")