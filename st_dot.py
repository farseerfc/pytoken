from st import ST
    
def draw_node(node,tree,gen):
    tree_id = tree.tree_id
    string = tree.string
    leaf_str = ",shape=box" if node.is_leaf() else ""
    leaf_str+= ",style=filled" if node.gen == gen else ""
    print("\t\tt%dn%d [label=\"%r\"%s];"% \
            (tree_id,node.node_id,node,leaf_str))
    if len(node.children)>0:
        print("\t\t{ rank=same; %s}"%" ".join("t%dn%d"%(
            tree_id,x.dst.node_id) for x in node.get_children()))
    for edge in node.get_children():
        draw_node(edge.dst,tree,gen);
        if edge.end >= ST.INFINITY:
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
                (tree_id,node.node_id,tree_id, \
                edge.dst.node_id,edge_str))
        
    if node.suffix_link != None:
        print("\t\tt%dn%d -> t%dn%d [style=dotted,weight=0];"% \
            (tree_id,node.node_id,tree_id,node.suffix_link.node_id))

def draw_tree(tree):
    tree.tree_id = ST.alloc_treeid()
    print("\tsubgraph clusterST%d{\n"%(tree.tree_id))
    draw_node(tree.root,tree,tree.root.gen)
    print("\tcolor=blue")
    print("\t}")


def draw_step(string):
    st = ST("")
    for i in range(0,len(string)):
        st.append(string[i])
        draw_tree(st)

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
    import sys
    string = escape(sys.stdin.read())
    st = ST(string)
    result = []

    print("digraph ST{\n")
    draw_tree(st)
    #draw_step(string)
    print("}")

