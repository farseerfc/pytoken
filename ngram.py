#!/usr/bin/python2
from tokenply import token_type, type_token

def ngram(tokenseq,time,n):
    result={}
    for i in xrange(0,len(tokenseq)-n+1):
        gram=tuple(tokenseq[i:i+n])
        if gram in result:
            result[gram]+=time
        else:
            result[gram]=time
    return result

def merge_ngram(ngrams):
    result = {}
    for grams in ngrams:
        for tupl in grams:
            if tupl in result:
                result[tupl] += grams[tupl]
            else:
                result[tupl]  = grams[tupl]
    return result


def input(filename,n):
    result = []
    for line in open(filename):
        pos, tokenseq_str = line.split("\t")[:2]
        length_str,end_set_str = pos.split(":")
        length = int(length_str.split(",")[1])
        end_set=eval(end_set_str)
        tokenseq_str = tokenseq_str.strip()
        tokenseq = tokenseq_str.split(",")

        grams = ngram(tokenseq,len(end_set),n)
        result.append(grams)
    return merge_ngram(result)

def filter_ngram(tokenseq,filename,n,gen):
    ngrams = input(filename,n)
    for length,end_set in gen:
        occur = 0.0
        for end in end_set:
            tokenlist =[type_token(x.type) for x in tokenseq[end-length:end]]
            for i in xrange(0,len(tokenlist)-n+1):
                gram=tuple(tokenlist[i:i+n])
                if gram in ngrams:
                    occur+=ngrams[gram]
        occur = occur/(len(tokenlist)-n+1)/len(tokenlist)
        yield occur,length,end_set

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
        
