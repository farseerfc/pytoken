#!/usr/bin/python2

def ngram(tokenseq,time,n):
    result={}
    for i in xrange(0,len(tokenseq)-n+1):
        gram=tuple(tokenseq[i:i+n])
        if gram in result:
            result[gram]+=time
        else:
            result[gram]=time
    return result

def input(filename,n):
    result = {}
    for line in open(filename):
        pos, tokenseq_str = line.split("\t")
        length_str,start_set_str = pos.split(":")
        length = int(length_str)
        start_set=eval(start_set_str)
        tokenseq_str = tokenseq_str.strip()
        tokenseq = tokenseq_str.split(",")

        grams = ngram(tokenseq,len(start_set),n)
        for tupl in grams:
            if tupl in result:
                result[tupl] += grams[tupl]
            else:
                result[tupl]  = grams[tupl]
    return result

def filter_ngram(tokenseq,filename,n,gen):
    ngrams = input(filename,n)
    for length,start_set in gen:
        occur = 0.0
        for start in start_set:
            tokenlist =[x.type for x in tokenseq[start:start+length]]
            for i in xrange(0,len(tokenlist)-n+1):
                gram=tuple(tokenlist[i:i+n])
                if gram in ngrams:
                    occur+=ngrams[gram]
        occur = occur/(len(tokenlist)-n+1)/len(tokenlist)
        yield occur,length,start_set

def filter_sort_occur(gen):
    lst = [x for x in gen]
    lst.sort(key=lambda x:x[0])
    return lst

if __name__=="__main__":
    import sys
    for filename in sys.argv[1:]:
        result= input(filename,5)
        for gram in result:
            print "%d:%s"%(result[gram],gram)
        
