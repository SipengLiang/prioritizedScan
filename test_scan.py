import subprocess as sp
import time

ip_list = []

# Prepare IP list
f = open('test_ip.txt','r')
for line in f:
    ip_list.append(line.strip()) # get rid of '\n'



p = [None] * len(ip_list)  # for each ip, instantiate a nmap subprocess
i = 0

# Ready

# start 'normal' scan
start_time = time.time()

for ip in ip_list:
    p[i] = sp.run(["nmap","-p1-25555", ip], capture_output=True) 
    i = i + 1

time_of_run = time.time() - start_time

# report the run time
print("Normal scan took: %s seconds." %time_of_run)

# reset for another test scan
p = [None] * len(ip_list)

# Prepare Priority file
g = open('port_scan_priority.txt','r')
priority = []
for line in g:
    priority.append(line.strip())
g.close()


# start 'priority' scan
start_time = time.time()

for pr_port in priority:
    i = 0
    for ip in ip_list:
        p[i] = sp.run(["nmap","-p"+str(pr_port), ip], capture_output=True) 
        i = i + 1

time_of_run = time.time() - start_time

# report the run time
print("'Priority' scan took: %s seconds." %time_of_run)







