import os
import time


interface = input("source interface :")
timeup = input("uptime(in secs):")
timedown =input("downtime(in secs):")
routes =int(input("Enter number of routes:"))
target,gateway = [],[]

for _ in range(routes):
    target.append(input("target/netmask:"))
    gateway.append(input("gateway: "))


count =0
while True :
    os.system("ifconfig "+interface+" up")
    #tc qdisc add dev eth1 root netem loss 1%
    time.sleep(5)
    for i in range(routes):
        os.system("ip route add "+target[i]+" via "+gateway[i])
    print("interface up")
    time.sleep(int(timeup))
    os.system("ifconfig "+interface+" down")
    print("interface down")
    count = count + 1
    print("Down count:",count)
    time.sleep(int(timedown))
