import re
from collections import Counter


# Define the service to analyze #
MATCH = r'http'

# Generate the regex pattern
REG_RSTR = r'(.)' + MATCH + r'\n'

print("Matching service: "+ MATCH + " ...\n")

# Preparing files
f = open('nmap_output.txt','r')                     # 'raw' nmap outputs

g = open('matched_ports.txt', 'w+')                 # A striped down version of the outputs
                                                    # containing only the port numbers of each
                                                    # entry

h = open('port_scan_priority.txt','w+')             # Generated list describing the scan priority


g.write('Ports matched for service: '+ MATCH + '\n')

# Initialize the port list
port_list = []

for line in f:
    matchObj = re.search( REG_RSTR, line, re.M|re.I)
    if (matchObj and not(matchObj.group(1))=='-' ):
        #print(line)
        # Grab the port number: ddddd, dddd, ddd, dd or d
        matchObj2 = re.search( r'\d\d\d\d\d|\d\d\d\d|\d\d\d|\d\d|\d', line, re.M|re.I )  
        g.write(matchObj2.group())
        g.write('\n')
        port_list.append(matchObj2.group())

f.close()
g.close()

# Analyze the result
cnt_dict = Counter(port_list)
for cnt_key in cnt_dict.keys():
    print(str(cnt_dict[cnt_key])+" out of "+str(len(port_list))+" entries uses port#: "+str(cnt_key))
    # first port listed has the highest scan priority, etc.
    h.write(str(cnt_key)+"\n")

h.close()









