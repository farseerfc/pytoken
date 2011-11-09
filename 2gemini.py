#!/usr/bin/python2

def process(line):
    files=line.split("\t")[2]

if __name__=="__main__":
    import sys
    for line in sys.stdin:
        print process(line)

