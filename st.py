INFINITY=1 << 20

def log(string):
    if False:
        import sys
        print(string,file=sys.stderr)

class Node:
    def __init__(self,node_id,suffix_link=None):
        self.children={}
        self.node_id=node_id
        self.suffix_link=suffix_link
        self.gen=-1

    def is_leaf(self):
        return self.suffix_link == None and self.node_id != 0 

    def __repr__(self):
        return str(self.node_id)+":"+str(self.gen)
    
    def drawdot(self,tree_id,gen):
        leaf_str = ",shape=box" if self.is_leaf() else ""
        leaf_str+= ",style=filled" if self.gen == gen else ""
        print("\t\tt%dn%d [label=\"%r\"%s];"% \
                (tree_id,self.node_id,self,leaf_str))
        for edge in self.get_children():
            edge.dst_node.drawdot(tree_id,gen);
            print("\t\t\tt%dn%d -> t%dn%d [label=\"%r\"];"% \
                    (tree_id,self.node_id,tree_id, \
                        edge.dst_node.node_id,edge))
        if self.suffix_link != None:
            print("\t\tt%dn%d -> t%dn%d [style=dotted];"% \
                (tree_id,self.node_id,tree_id,self.suffix_link.node_id))

    def get_children(self):
        child_list=[self.children[key] for key in self.children]
        child_list.sort(key=lambda x:x.dst_node.rank())
        return child_list

    def rank(self):
        result=self.node_id
        for key in self.children:
            result = min(result,self.children[key].dst_node.rank())
        return result


class Edge:
    def __init__(self,string,begin,end,src_node,dst_node):
        self.string=string
        self.begin=begin
        self.end=end
        self.src_node=src_node
        self.dst_node=dst_node

    def __repr__(self):
        return self.string[self.begin:self.end+1]

    def __len__(self):
        return self.end - self.begin + 1

    def split(self,suffix,suffix_tree,gen):
        log("edge %r,suffix %r"%(self,suffix))
        new_node=Node(suffix_tree.alloc_node())
        new_node.gen=gen
        new_edge=Edge(self.string, self.begin+len(suffix), 
                self.end,new_node,self.dst_node )
        suffix_tree.insert_edge(new_edge)
        self.end = self.begin + len(suffix) -1
        self.dst_node=new_node
        self.gen=gen
        return new_node

class Suffix:
    def __init__(self,src_node,begin,end):
        self.src_node=src_node
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
            edge=self.src_node.children[suffix_tree.string[self.begin]]
            if len(edge) > len(self): return
            self.begin += len(edge)
            self.src_node = edge.dst_node

    def __repr__(self):
        return "%d,%d" % (self.begin,self.end)

class ST:
    NR_TREE=0 

    def __init__(self,string,alphabet=None):
        self.string=string
        if alphabet == None:
            alphabet = set(string)
        self.alphabet=alphabet
        self.root=Node(0)
        self.nr_node=1 # root is counted
        self.tree_id=ST.NR_TREE
        ST.NR_TREE+=1
        self.active_point = Suffix(self.root,0,-1)
        for current in range(0,len(self.string)):
            # self.add(self.root,current)
            self.add_prefix(current)
            self.root.gen=current

    def add_prefix(self,last_char_idx):
        last_parent_node=None
        last_char=self.string[last_char_idx]
        active_point=self.active_point
        while True:
            # print("here!110")
            parent_node = active_point.src_node
            if active_point.is_explicit():
                if last_char in active_point.src_node.children:
                    # already in tree
                    break
            else:
                edge =  active_point.src_node.children[self.string \
                        [active_point.begin]]
                if self.string[edge.begin+len(active_point)]== \
                        last_char:
                    break
                else:
                    parent_node=edge.split(active_point,self,last_char_idx)
            new_node = Node(self.alloc_node())
            new_edge = Edge(self.string,last_char_idx, INFINITY, \
                    parent_node,new_node) 
            self.insert_edge(new_edge)
            # insert suffix link
            if last_parent_node!=None and last_parent_node!=self.root:
                last_parent_node.suffix_link = parent_node
            last_parent_node = parent_node
            if active_point.src_node == self.root:
                active_point.begin +=1
            else:
                active_point.src_node=active_point.src_node.suffix_link
            active_point.canonize(self)
        if last_parent_node!=None and last_parent_node!=self.root:
            last_parent_node.suffix_link = parent_node
        active_point.end+=1
        active_point.canonize(self)

    def insert_edge(self,edge):
        edge.src_node.children[self.string[edge.begin]]=edge

    def alloc_node(self):
        self.nr_node+=1
        return self.nr_node-1


    def drawdot(self):
        print("\tsubgraph clusterST%d{\n"%(self.tree_id))
        self.root.drawdot(self.tree_id,self.root.gen)
        print("\tcolor=blue")
        print("\t}")


def draw(st):
    for i in range(0,len(st)):
        ST(st[:i+1]).drawdot()


if __name__=="__main__":
    INFINITY = 100
    print("digraph ST{\n")
    draw("mississippi$")
    draw("papua$")
    print("}")
