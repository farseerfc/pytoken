INFINITY=1 << 20
RANKING=True

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

    def is_leaf(self): # root is not leaf and has no suffix_link
        return self.suffix_link == None and self.node_id != 0 

    def __repr__(self):
        return str(self.node_id)+":"+str(self.gen)
    
    def drawdot(self,tree,gen):
        tree_id = tree.tree_id
        string = tree.string
        leaf_str = ",shape=box" if self.is_leaf() else ""
        leaf_str+= ",style=filled" if self.gen == gen else ""
        print("\t\tt%dn%d [label=\"%r\"%s];"% \
                (tree_id,self.node_id,self,leaf_str))
        for edge in self.get_children():
            edge.dst.drawdot(tree,gen);
            if edge.end >= INFINITY:
                edge_str = "(%d,∞)\\n" % (edge.begin) 
            else:
                edge_str = "(%d,%d)\\n" % (edge.begin,edge.end+1)
            if edge.end - edge.begin <16:
                edge_str += string[edge.begin:edge.end+1]
            else:
                edge_str += string[edge.begin:edge.begin+8]
                edge_str += "..."
                edge_str += string[edge.end-8:edge.end]
            print("\t\tt%dn%d -> t%dn%d [label=\"%s\",weight=1];"% \
                    (tree_id,self.node_id,tree_id, \
                    edge.dst.node_id,edge_str))
        if self.suffix_link != None:
            print("\t\tt%dn%d -> t%dn%d [style=dotted,weight=0];"% \
                (tree_id,self.node_id,tree_id,self.suffix_link.node_id))

    def get_children(self):
        child_list=[self[key] for key in self]
        child_list.sort(key=lambda x:x.dst.rank())
        return child_list

    def rank(self):
        result=self.node_id
        if RANKING:
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
    

class Edge:
    def __init__(self,begin,end,src,dst):
        self.begin=begin
        self.end=end
        self.src=src
        self.dst=dst


    def __len__(self):
        return self.end - self.begin + 1

    def split(self,suffix,suffix_tree,gen):
        log("edge %r,suffix %r"%(self,suffix))
        new_node=Node(suffix_tree.alloc_node())
        new_node.gen=gen
        new_edge=Edge(self.begin+len(suffix), \
                self.end,new_node,self.dst )
        suffix_tree.insert_edge(new_edge)
        self.end = self.begin + len(suffix) -1
        self.dst=new_node
        self.gen=gen
        return new_node

class Suffix:
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
        self.active = Suffix(self.root,0,-1)
        for current in range(0,len(self.string)):
            # self.add(self.root,current)
            self.add(current)
            self.root.gen=current

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
            new_node = Node(self.alloc_node())
            new_edge = Edge(current, INFINITY,parent,new_node) 
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

    def insert_edge(self,edge):
        edge.src[self.string[edge.begin]]=edge

    def alloc_node(self):
        self.nr_node+=1
        return self.nr_node-1


    def drawdot(self):
        print("\tsubgraph clusterST%d{\n"%(self.tree_id))
        self.root.drawdot(self,self.root.gen)
        print("\tcolor=blue")
        print("\t}")


def draw_step(st):
    for i in range(0,len(st)):
        ST(st[:i+1]).drawdot()

escape_list ={
    "\\":"\\\\",
    "\n":"",
    "\"":"",
    " ":""
    }


def escape(string):
    for esc in escape_list:
        string = string.replace(esc,escape_list[esc])
    return string
    

if __name__=="__main__":
    #INFINITY = 100
    import sys
    string = escape(sys.stdin.read())
    
    print("digraph ST{\n")
    #draw_step(string)
    ST(string).drawdot()
    #ST("mississipi").drawdot()
    print("}")
