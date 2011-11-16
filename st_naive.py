#!/usr/bin/python2
class Node(object):

    def __init__(self,node_id,gen,leaf=False):
        self.children={}
        self.node_id=node_id
        self.leaf=leaf
        self.gen=gen

    def __repr__(self):
        return unicode(self.node_id)+u":"+unicode(self.gen)
    
    def drawdot(self,tree_id,gen):
        leaf_str = u",shape=box" if self.leaf else u""
        leaf_str+= u",style=filled" if self.gen == gen else u""
        print u"\t\tt%dn%d [label=\"%r\"%s];"% \
                (tree_id,self.node_id,self,leaf_str)
        for edge in self.get_children():
            edge.node.drawdot(tree_id,gen);
            print u"\t\t\tt%dn%d -> t%dn%d [label=\"%r\"];"% \
                    (tree_id,self.node_id,tree_id, \
                        edge.node.node_id,edge)

    def get_children(self):
        child_list=[self.children[key] for key in self.children]
        child_list.sort(key=lambda x:x.node.rank())
        return child_list

    def rank(self):
        result=self.node_id
        for key in self.children:
            result = min(result,self.children[key].node.rank())
        return result



class Edge(object):
    def __init__(self,string,start,end,node):
        self.string=string
        self.start=start
        self.end=end
        self.node=node

    def __repr__(self):
        return self.string[self.start:self.end]

class STnaive(object):
    NR_TREE=0 

    def __init__(self,string):
        self.string=string
        self.root=Node(0,0)
        self.nr_node=1 # root is counted
        self.construct()
        self.tree_id=STnaive.NR_TREE
        STnaive.NR_TREE+=1

    def alloc_node(self):
        self.nr_node+=1
        return self.nr_node-1

    def construct(self):
        for current in xrange(0,len(self.string)):
            self.add(self.root,current)

    def drawdot(self):
        #print u"\tsubgraph clusterST%d{\n"%(self.tree_id)
        self.root.drawdot(self.tree_id,self.root.gen)
        #print u"\tcolor=blue"
        #print u"\t}"

    def add(self,node,start):
        while True:
            node.gen=start
            char=self.string[start]
            if not (char in node.children):
                node.children[char]=Edge(self.string,start, \
                        len(self.string), Node(self.alloc_node(),start,True))
                return

            old_edge=node.children[char]
            # first find common
            common_end=old_edge.start
            new_end=start
            while common_end < len(self.string) and \
                    new_end < len(self.string) and \
                    self.string[common_end]==self.string[new_end] :
                common_end+=1
                new_end+=1
            if new_end>=len(self.string): return 
            if common_end<old_edge.end:
                # we need to split a edge
                old_node=old_edge.node
                inter_node=Node(self.alloc_node(),start)
                inter_node.children[self.string[common_end]]=Edge( \
                        self.string,common_end,old_edge.end,old_node)
                old_edge.node=inter_node
                old_edge.end=common_end
                # add new node
                #self.add(inter_node,new_end)
            node=old_edge.node
            start=new_end

def draw(st):
    for i in xrange(0,len(st)):
        STnaive(st[:i+1]).drawdot()


if __name__==u"__main__":
    print u"digraph ST{\n"
    import sys
    STnaive(sys.stdin.read().strip()).drawdot()
    #for i in range(0,len("mississippi$")):
    #    STnaive("mississippi$"[:i+1]).drawdot()
    #draw(u"mississippi$")
    #draw(u"ababcab$")
    #STnaive("papua").drawdot()
    #STnaive("a").drawdot()
    #STnaive("ab").drawdot()
    #STnaive("aba").drawdot()
    #STnaive("abab").drawdot()
    #STnaive("ababcab").drawdot()
    #STnaive("ababcabc").drawdot()
    #STnaive("ababcabca").drawdot()
    print u"}"
