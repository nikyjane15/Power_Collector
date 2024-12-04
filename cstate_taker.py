import time
import os
import re
from model import State, Time, CPU_Time, maxtime, tstep
import pandas as pd


def json_to_excel(type, counter_type):
    timestamps = []
    cpus = []
    states = []
    #
    # with open('results/time_counter.json', 'r') as f:
    #     json_file = json.load(f, object_pairs_hook=OrderedDict)

    for i in range(len(counter_type)):
        timestamps.append(counter_type[i]["timestamp"])

    for i in range(len(counter_type[0]["block"])):
        cpus.append(counter_type[0]["block"][i]["cpu"])

    for i in range(len(counter_type[0]["block"][0]["state"])):
        states.append(counter_type[0]["block"][0]["state"][i]["state"])

    df = pd.DataFrame(columns=states, index=timestamps)
    for j in range(len(cpus)):
        for i in range(len(timestamps)):
            for k in range(len(states)):
                a = counter_type[i]["block"][j]["state"][k]["value"]
                a.rstrip('\n')
                print(a)
                df.at[timestamps[i], states[k]] = int(a.rstrip('\n'))
            filename = "results/" + type + "_" + cpus[j] + ".csv"
        df.to_csv(filename)



counters_time = []
counters_usage = []
count = 0
dir_temp = []
dir_cpu = []
f = "/sys/devices/system/cpu"
for i in range(maxtime):
    if count == 0:
        p = re.compile(r'\d+')
        dir_temp = sorted([element for element in os.listdir(f) if re.match('cpu\d+', element)])
        dir_cpu = sorted(dir_temp, key=lambda s: int(re.search(r'\d+', s).group()))
        count += 1

    now_ns = time.time_ns()
    temp_usage = CPU_Time(timestamp=now_ns, block=[])
    temp_time = CPU_Time(timestamp=now_ns, block=[])
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

        temp_time.block.append(cpu_time)
        temp_usage.block.append(cpu_usage)

    counters_time.append(temp_time)
    counters_usage.append(temp_usage)
    i += tstep

json_to_excel("time",counters_time)
json_to_excel("usage",counters_usage)
print("dumps")

