import subprocess as sp
import shodan as sd


API_KEY = "WAGzXnBd36NURypcfYnsn4LHb4xh8qSR"
SEARCH_STR = "HTTP" # can be checked from the results
api = sd.Shodan(API_KEY)

ip_list = []
p = []


results = api.search(SEARCH_STR)

for result in results['matches']:
    ip_list.append(result['ip_str'])

print((ip_list))

# Generate the list of IP to test our scan priority
test = open('test_ip.txt','w+')
for ip in ip_list:
    test.write(str(ip)+'\n')
test.close()

p = [None] * len(ip_list)  # for each ip, instantiate a nmap subprocess


i = 0
for ip in ip_list:

    # Currently only doing -F, which gives faster speed
    p[i] = sp.run(["nmap","-F", ip], capture_output=True) 
    i = i + 1
    
# problem: using fast scan mode '-F' gives faster speed
# but it does not always detects a service that is running
# on a alternative port. eg. There was a instance where
# a camera was running http on port 9000 but with '-F',
# nmap failed to detect such service.

# Order: fetch_and_scan -> parse_port_list -> test_scan

# fetch_and_scan: Generate test_ip.txt, Generate nmap_output.txt
# parse_port_list: Generate the priority file port_scan_priority.txt

# To, in a certain degree, solve this problem
# parse_port_list.py was created to generate
# a list that describe the scan priority of the ports
# if a certain service. The priorty is derived by determining
# the prevalence of each port number of a certain service, with
# the port scan result from the "unoptimized" nmap scan
# in this script.

# Once the priority is obtained, our next round of nmap scan of
# a certain service can be sped up by targeting at the port of
# high priority.

# The problem for now is that I cannot get enough IP addresses.
# Shodan API, without a account upgrade, only provide one single
# page of result of 100 entries. So right now, I am only able to
# apply the prioritized port scan to those IP from whom the script
# got its knowledge of the priority. So the test scan is really
# not a valid test.


# possible improvement: run subprocesses in parallel
# to increase speed

rets = [None] * len(ip_list)

f = open('nmap_output.txt','w+')
f.write('#\n')

i = 0
for process in p:
    rets[i] = str(process.stdout, "utf-8", "ignore")
    print(rets[i])
    f.write(str(rets[i]))
    f.write('\n\n')
    i = i + 1
f.close()

















