#!/usr/bin/python2

CC="cpp"

from subprocess import Popen,PIPE,CalledProcessError

def preprocess(filename):
    p = Popen(["gcc","-E",filename],stdout=PIPE,stderr=PIPE)
    out,err=p.communicate()
    exit_code = p.wait()
    if exit_code != 0:
        import sys
        print >>sys.stderr,"Gcc returned non-zero exit status\n" + err
        raise SystemError
    return out

if __name__=="__main__":
    import sys
    for arg in sys.argv[1:]:
        print preprocess(arg)
