def get_pesq(filename):
    pesq_file = open(filename,"r")
    lines = pesq_file.readlines()
    pesq_list=[]
    pesq_list.append(lines[-1].split()[3])
    pesq_list.append(str(float(lines[-1].split()[2])+0.1))
     
    print(pesq_list)
    return (pesq_list)

def get_one_way_delay(filename):
    one_way_delay_list=[]
    one_way_delay = open(filename,"r")
    lines = one_way_delay.readlines()
    a = lines[2:-1]
    firstline = a[0].split()[-1]
    lastline = a[-1].split()[-1]
    one_way_delay_list.append(firstline)
    one_way_delay_list.append(lastline)
    print(one_way_delay_list)
    return one_way_delay_list

#import subprocess
#import sys

#subprocess.run(['ls'], stderr=sys.stderr, stdout=sys.stdout)
#get_pesq("pesq_results.txt")
#get_one_way_delay("one_way_delay.txt")