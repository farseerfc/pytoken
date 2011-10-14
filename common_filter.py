from st import ST

if __name__ == "__main__":
    import sys
    string = sys.stdin.read()
    st = ST(string)
    result = []

    for length , start_set in st.root.common():
        if len(start_set)==0:continue
        #if length < 2 : continue
        start = list(start_set)[0]
        print("%s\t%d:%s"%(string[start:start+length],length,start_set))


