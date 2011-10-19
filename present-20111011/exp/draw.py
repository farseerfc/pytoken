#!/usr/bin/python2
import sys,popen2

for i in range(1,63):
    command = "time cat " +"workqueue.txt "*i + "|python ../../st.py >/dev/zero"
    cout,cin,cerr=popen2.popen3(command)
    real = cerr.read().split("\n")[1]
    time=real.split("\t")[1].strip()
    second=time.split("m")[1].split("s")[0]
    print("%d\t%d\t%s"%(i,i*15993,second))
