
class Node:

    def __init__(self,node_id,leaf=False):
        self.children={}
        self.node_id=node_id
        self.leaf=leaf
        self.gen=-1

    def __repr__(self):
        return str(self.node_id)+":"+str(self.gen)
    
    def drawdot(self,tree_id,gen):
        leaf_str = ",shape=box" if self.leaf else ""
        leaf_str+= ",style=filled" if self.gen == gen else ""
        print("\t\tt%dn%d [label=\"%r\"%s];"% \
                (tree_id,self.node_id,self,leaf_str))
        for edge in self.get_children():
            edge.node.drawdot(tree_id,gen);
            print("\t\t\tt%dn%d -> t%dn%d [label=\"%r\"];"% \
                    (tree_id,self.node_id,tree_id, \
                        edge.node.node_id,edge))

    def get_children(self):
        child_list=[self.children[key] for key in self.children]
        child_list.sort(key=lambda x:x.node.rank())
        return child_list

    def rank(self):
        result=self.node_id
        for key in self.children:
            result = min(result,self.children[key].node.rank())
        return result



class Edge:
    def __init__(self,string,start,end,node):
        self.string=string
        self.start=start
        self.end=end
        self.node=node

    def __repr__(self):
        return self.string[self.start:self.end]

    def __len__(self):
        return self.end-self.start

class STnaive:
    NR_TREE=0 

    def __init__(self,string):
        self.string=string
        self.root=Node(0)
        self.nr_node=1 # root is counted
        self.construct()
        self.tree_id=STnaive.NR_TREE
        STnaive.NR_TREE+=1

    def alloc_node(self):
        self.nr_node+=1
        return self.nr_node-1

    def construct(self):
        for current in range(0,len(self.string)):
            self.add(self.root,current)

    def drawdot(self):
        print("\tsubgraph clusterST%d{\n"%(self.tree_id))
        self.root.drawdot(self.tree_id,self.root.gen)
        print("\tcolor=blue")
        print("\t}")

    def add(self,node,start):
        while True:
            node.gen=start
            char=self.string[start]
            if not (char in node.children):
                node.children[char]=Edge(self.string,start, \
                        len(self.string), Node(self.alloc_node(),True))
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
                inter_node=Node(self.alloc_node())
                inter_node.children[self.string[common_end]]=Edge( \
                        self.string,common_end,old_edge.end,old_node)
                old_edge.node=inter_node
                old_edge.end=common_end
                # add new node
                #self.add(inter_node,new_end)
            node=old_edge.node
            start=new_end

def draw(st):
    for i in range(0,len(st)):
        STnaive(st[:i+1]).drawdot()


if __name__=="__main__":
    print("digraph ST{\n")
    
    #for i in range(0,len("mississippi$")):
    #    STnaive("mississippi$"[:i+1]).drawdot()
    draw("mississippi$")
    draw("ababcab$")
    #STnaive("papua").drawdot()
    #STnaive("a").drawdot()
    #STnaive("ab").drawdot()
    #STnaive("aba").drawdot()
    #STnaive("abab").drawdot()
    #STnaive("ababcab").drawdot()
    #STnaive("ababcabc").drawdot()
    #STnaive("ababcabca").drawdot()
    print("}")
