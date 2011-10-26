#!/usr/bin/python2
from Queue import LifoQueue,Queue
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
    

def common(st):
    stack=[]
    stack.append((st.root,0,0))
    result=[]

    while len(stack)>0:
        node,parent_len,edge_len=stack.pop()
        begin_set = set()
        for char in node.children:
            edge = node.children[char]
            len_edge = parent_len + len(edge)
            begin_set.add(edge.begin-parent_len)
            stack.append((edge.dst,len_edge,len(edge)))
        #yield parent_len,begin_set
        result.append((parent_len,begin_set))
    return result


