
class Node:
    NR_NODE=0

    def __init__(self,leaf=False):
        self.children={}
        self.node_id=Node.NR_NODE
        Node.NR_NODE+=1
        self.leaf=leaf

    def add(self,string,start):
        #if start >= len(string): return
        char=string[start]
        if(char in self.children):
            old_edge=self.children[char]
            # first find common
            common_end=old_edge.start
            new_end=start
            while common_end < len(string) and \
                    new_end < len(string) and \
                    string[common_end]==string[new_end] :
                common_end+=1
                new_end+=1

            if new_end>=len(string): return # this is already done
            if common_end>=old_edge.end:
                old_edge.node.add(string,new_end)
            else:
                # we need to split a edge
                old_node=old_edge.node
                inter_node=Node()
                inter_node.children[string[common_end]]=Edge( \
                    string,common_end,old_edge.end,old_node)
                old_edge.node=inter_node
                old_edge.end=common_end
                # add new node
                inter_node.add(string,new_end)
        else: # We append a new leaf here
            self.children[char]=Edge(string,start, len(string), Node(True))

    def __repr__(self):
        return str(self.node_id)
    
    def drawdot(self):
        leaf_str = ",shape=box" if self.leaf else ""
        print("\tn%d [label=\"%r\"%s];"%(self.node_id,self,leaf_str))
        for edge in self.get_children():
            edge.node.drawdot();
            print("\tn%d -> n%d [label=\"%r\"];"% \
                    (self.node_id,edge.node.node_id,edge))

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

class STnaive:
    def __init__(self,string):
        self.string=string
        self.root=Node()
        self.construct()

    def construct(self):
        for current in range(0,len(self.string)):
            self.root.add(self.string,current)

    def drawdot(self):
        #print("digraph ST%d{"%(self.root.node_id))
        self.root.drawdot()
        #print("}")

if __name__=="__main__":
    print("digraph ST{")
    STnaive("m").drawdot()
    STnaive("mi").drawdot()
    STnaive("mis").drawdot()
    STnaive("miss").drawdot()
    STnaive("missi").drawdot()
    STnaive("missis").drawdot()
    STnaive("mississ").drawdot()
    STnaive("mississi").drawdot()
    STnaive("mississip").drawdot()
    STnaive("mississipp").drawdot()
    STnaive("mississippi$").drawdot()
    #STnaive("papua").drawdot()
    #STnaive("a").drawdot()
    #STnaive("ab").drawdot()
    #STnaive("aba").drawdot()
    #STnaive("abab").drawdot()
    #STnaive("ababcab").drawdot()
    #STnaive("ababcabc").drawdot()
    #STnaive("ababcabca").drawdot()
    print("}")
