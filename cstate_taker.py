import os
import re
import time
from collections import OrderedDict
import requests

import pandas as pd

from model import State, Time, CPU_Time
from model import Energy, List_Zones
from model import tstep, maxtime, case_0

save_path = "/home/ubuntu/Get_time_usage_irl/"


def energies_to_file():
    if not os.path.exists(save_path + "metrics"):
        os.mkdir(save_path + "metrics")

    for index, element in enumerate(raritan_energies):
        file_name = save_path + 'metrics' + str(timestamp_energy[index]) + '.metric'
        with open(file_name, 'w') as fp:
            fp.write(element)


def json_to_excel_energies(rapl_ener):
    timestamps = []
    zones = []
    values = []

    path = save_path + "results_rapl_energies/"
    if not os.path.exists(path):
        os.mkdir(save_path + "results_rapl_energies/")

    for i in range(len(rapl_ener)):
        timestamps.append(rapl_ener[i]["timestamp"])

    for i in range(len(rapl_ener[0]["powercap"])):
        zones.append(rapl_ener[0]["powercap"][i]["zone"])

    df = pd.DataFrame(columns=zones, index=timestamps)
    for i in range(len(timestamps)):
        for k in range(len(zones)):
            a = rapl_ener[i]["powercap"][k]["value"]
            df.at[timestamps[i], zones[k]] = a
        filename = path + "rapl_energies.csv"
    df.to_csv(filename, sep=";", index_label="timestamp")


def json_to_excel_states(type_var, counter_type):
    timestamps = []
    cpus = []
    states = []

    path = save_path + "results_state/"
    if not os.path.exists(path):
        os.mkdir(save_path + "results_state/")

    for i in range(len(rapl_energies)):
        timestamps.append(counter_type[i]["timestamp"])

    for i in range(len(counter_type[0]["block"])):
        cpus.append(counter_type[0]["block"][i]["cpu"])

    for i in range(len(counter_type[0]["block"][0]["state"])):
        states.append(counter_type[0]["block"][0]["state"][i]["state"])

    df = pd.DataFrame(columns=cpus, index=timestamps)
    for j in range(len(states)):
        for i in range(len(timestamps)):
            for k in range(len(cpus)):
                a = counter_type[i]["block"][k]["state"][j]["value"]
                df.at[timestamps[i], cpus[k]] = int(a.rstrip('\n'))
            filename = path + type_var + "_" + states[j] + ".csv"
        df.to_csv(filename, sep=";", index_label="timestamp")


def json_to_excel_cpus(type, counter_type):
    timestamps = []
    cpus = []
    states = []

    path = save_path + "results_cpus/"
    if not os.path.exists(path):
        os.mkdir(save_path + "results_cpus/")

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
                df.at[timestamps[i], states[k]] = int(a.rstrip('\n'))
            filename = path + type + "_" + cpus[j] + ".csv"
        df.to_csv(filename, sep=";", index_label="timestamp")


counters_time = []
counters_usage = []
rapl_energies = []
count = 0
raritan_energies = []
timestamp_energy = []
dir_temp = []
dir_cpu = []
f = "/sys/devices/system/cpu"
fe = "/sys/class/powercap"

while count < maxtime:
    if count == 0:
        p = re.compile(r'\d+')
        dir_temp = sorted([element for element in os.listdir(f) if re.match('cpu\d+', element)])
        dir_cpu = sorted(dir_temp, key=lambda s: int(re.search(r'\d+', s).group()))
        dir_energies = sorted([element for element in os.listdir(fe) if element.startswith('intel-rapl') and element.count(':') == 1])

    time.sleep(1.55)
    now_ns = time.time_ns()
    temp_energy = List_Zones(timestamp=now_ns, powercap=[])
    for element in dir_energies:
        f1 = fe + "/" + element + "/energy_uj.txt"

        with open(f1, "r") as file:
            temp = file.readlines()
            temp_energy.powercap.append(Energy(zone=element, value=temp[0]))

    rapl_energies.append(temp_energy.model_dump(mode='json', context=OrderedDict))

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

    counters_time.append(temp_time.model_dump(mode='json', context=OrderedDict))
    counters_usage.append(temp_usage.model_dump(mode='json', context=OrderedDict))
    if case_0:
        r = requests.get("http://192.168.17.28:9950/metrics", verify=False)
        raritan_energies.append(r.text)
        timestamp_energy.append(now_ns)

    count += 1

if case_0:
    energies_to_file()

json_to_excel_cpus("time", counters_time)
json_to_excel_cpus("usage", counters_usage)
json_to_excel_states("time", counters_time)
json_to_excel_states("usage", counters_usage)
json_to_excel_energies(rapl_energies)
print("dumps")
