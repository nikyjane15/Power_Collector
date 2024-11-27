# caso 0 ->  Is when we have a test with nothing running on top of it.
#            I take the counters at the beginning and at the end of test
# case 1 ->  Is when we have a test with up and down scaling for multiple times.
#            I take counter before the test, when the test is running every 10 minutes, and at the end

case = 1
time_test = 60  #per test veloci metti 60
URL = "http://192.168.254.15:8001"
hostname = ["r2hpgen8-test.maas", "r1hpgen9-2.maas"]
ip_client = "192.168.17.28"
ip_server_k8 = "192.168.17.29"
counters_name = ["Cstates-Usage", "Cstates-Time"]
password = "pap3rin0"
energy_time_range = 5 #per test veloci metti 5