#!/usr/bin/python2

###########################################################
# Multithreading model
from threading import Thread
class CSThread(Thread):
    def __init__(self,stack,result):
        Thread.__init__(self)
        self.stack=stack
        self.result=result
        self.nr=0
    def run(self):
        stack=self.stack
        result=self.result
        while not stack.empty():
            self.nr+=1
            node,parent_len,edge_len=stack.get()
            begin_set = set()
            for char in node.children:
                edge = node.children[char]
                len_edge = parent_len + len(edge)
                begin_set.add(edge.begin-parent_len)
                stack.put((edge.dst,len_edge,len(edge)))
            #yield parent_len,begin_set
            result.put((parent_len,begin_set))
    

#########################################################
# original model

def clear_passed(node):
  stack=[]
  stack.append(node)

  while len(stack) >0:
    node = stack.pop()
    node.passed=False

    for char in node:
      edge = node[char]
      if edge.dst != None:
          stack.append(edge.dst)

def common_orig(st):
    stack=[]
    stack.append((st.root,0,0))
    result=[]

    if st.root.passed: clear_passed(st.root)

    while len(stack)>0:
        node,parent_len,edge_len=stack.pop()
        if st.is_leaf(node): continue
        end_set = set()
        for char in node:
            edge = node[char]
            len_edge = parent_len + len(edge)
            end_set.add(edge.begin)
            stack.append((edge.dst,len_edge,len(edge)))
        if node.passed: continue
        node.passed=True
        while node.suffix_link != None:
            node = node.suffix_link
            node.passed=True
        yield parent_len,end_set


#########################################################
# multiprocess model
def mp_proc(que,result,i):
    cnt=0
    while not que.empty():
        cnt+=1
        node,parent_len,edge_len=que.get()
        end_set = set()
        for char in node.children:
            edge = node.children[char]
            len_edge = parent_len + len(edge)
            end_set.put(edge.begin)
            que.add((edge.dst,len_edge,len(edge)))
        result.put(parent_len,end_set)
    import sys
    print >>sys.stderr,"Thread %d:%d"%(i,cnt)



def common_mp(st):
    from multiprocessing import Process,Queue
    stack=Queue()
    stack.put((st.root,0,0))
    result=Queue()
    
    procs=[]
    NR_PROC=2
    for i in xrange(0,NR_PROC):
        proc=Process(target=mp_proc,args=(stack,result,i+1))
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()

    mp_proc(stack,result,0)

    while not result.empty():
        yield result.get()

common=common_orig

