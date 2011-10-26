#!/usr/bin/python2
FCLOG=False

def log(string):
    if FCLOG:
        import sys
        print >>sys.stderr, string

class Node(object):
    RANKING = True

    def __init__(self,node_id,gen,suffix_link=None):
        self.children={}
        self.node_id=node_id
        self.gen=gen
        self.suffix_link=suffix_link

    def is_leaf(self): # root is not leaf and has no suffix_link
        return self.suffix_link == None and self.node_id != 0 

    def __repr__(self):
        return unicode(self.node_id)+u":"+unicode(self.gen)
    def get_children(self):
        child_list=[self[key] for key in self]
        child_list.sort(key=lambda x:x.dst.rank())
        return child_list

    def rank(self):
        result=self.node_id
        if Node.RANKING:
            for key in self:
                result = min(result,self[key].dst.rank())
        return result

    def __getitem__(self,key):
        return self.children[key]

    def __setitem__(self,key,value):
        self.children[key]=value

    def __contains__(self,item):
        return item in self.children

    def __iter__(self):
        return self.children.__iter__()

    # recursion version, use iteration version in ST.common
    def common(self,parent_len=0,edge_len=0):
        begin_set = set()
        for char in self.children:
            edge = self.children[char]
            len_edge = parent_len + len(edge)
            begin_set.add(edge.begin-parent_len)
            for x in edge.dst.common(len_edge,len(edge)):
                yield x
        yield parent_len,begin_set


class Edge(object):
    def __init__(self,begin,end,src,dst):
        self.begin=begin
        self.end=end
        self.src=src
        self.dst=dst


    def __len__(self):
        return self.end - self.begin + 1

    def split(self,suffix,suffix_tree,gen):
        log(u"edge %r,suffix %r"%(self,suffix))
        new_node=Node(suffix_tree.alloc_node(),gen)
        new_edge=Edge(self.begin+len(suffix), \
                self.end,new_node,self.dst )
        suffix_tree.insert_edge(new_edge)
        self.end = self.begin + len(suffix) -1
        self.dst=new_node
        self.gen=gen
        return new_node

class Suffix(object):
    def __init__(self,src,begin,end):
        self.src=src
        self.begin=begin
        self.end=end

    def __len__(self):
        return self.end-self.begin + 1

    def is_explicit(self):
        return self.begin > self.end

    def is_implicit(self):
        return not self.is_explicit()

    def canonize(self,suffix_tree):
        while True:
            if self.is_explicit(): return
            edge=self.src[suffix_tree.string[self.begin]]
            if len(edge) > len(self): return
            self.begin += len(edge)
            self.src = edge.dst

    def __repr__(self):
        return u"%d,%d" % (self.begin,self.end)

class ST(object):
    INFINITY=1 << 30

    NR_TREE=0 

    @classmethod
    def alloc_treeid(ST):
        ST.NR_TREE +=1
        return ST.NR_TREE

    def __init__(self,string,alphabet=None):
        self.string=string
        if alphabet == None:
            alphabet = set(string)
        self.alphabet=alphabet
        self.root=Node(0,0)
        self.nr_node=1 # root is counted
        self.tree_id=ST.alloc_treeid()
        self.active = Suffix(self.root,0,-1)
        for current in xrange(0,len(self.string)):
            # self.add(self.root,current)
            self.add(current)

    def append(self,string):
        old_len = len(self.string)
        self.string += string
        self.alphabet = self.alphabet.union(string)
        for current in xrange(old_len,len(self.string)):
            self.add(current)

    def add(self,current):
        last_parent=None
        last_char=self.string[current]
        active=self.active
        while True:
            parent = active.src
            if active.is_explicit():
                if last_char in active.src:
                    # already in tree
                    break
            else:
                edge=active.src[self.string[active.begin]]
                if self.string[edge.begin+len(active)]==last_char:
                    break
                parent=edge.split(active,self,current)
            # new leaf
            new_node = Node(self.alloc_node(),current)
            new_edge = Edge(current, ST.INFINITY,parent,new_node) 
            self.insert_edge(new_edge)
            # insert suffix link
            if last_parent!=None and last_parent!=self.root:
                last_parent.suffix_link = parent
            last_parent = parent
            if active.src == self.root:
                active.begin +=1
            else:
                active.src=active.src.suffix_link
            active.canonize(self)
        if last_parent!=None and last_parent!=self.root:
            last_parent.suffix_link = parent
        active.end+=1
        active.canonize(self)
        self.root.gen=current

    def insert_edge(self,edge):
        edge.src[self.string[edge.begin]]=edge

    def alloc_node(self):
        self.nr_node+=1
        return self.nr_node-1

    def lrs(self): #longest repeated substring
        self.root.lrs()

    def __len__(self):
        return len(self.string)

