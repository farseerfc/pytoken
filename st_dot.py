#!/usr/bin/python2
from st import ST
    
def draw_node(node,tree,gen):
    tree_id = tree.tree_id
    string = tree.string
    leaf_str = u",shape=box" if node.is_leaf() else u""
    leaf_str+= u",style=filled" if node.gen == gen else u""
    leaf_str+= u",color=red" if node == tree.active.src else u""
    print u"\t\tt%dn%d [label=\"%r\"%s];"% \
            (tree_id,node.node_id,node,leaf_str)
    if len(node.children)>0:
        print u"\t\t{ rank=same; %s}"%u" ".join(u"t%dn%d"%(
            tree_id,x.dst.node_id) for x in node.get_children())
    for edge in node.get_children():
        draw_node(edge.dst,tree,gen);
        if edge.end >= ST.INFINITY:
            edge_str = u"(%d,...)\\n" % (edge.begin) 
        else:
            edge_str = u"(%d,%d)\\n" % (edge.begin,edge.end+1)
        if edge.end - edge.begin <16:
            edge_str += unicode(string[edge.begin:edge.end+1])
        else:
            edge_str += unicode(string[edge.begin:edge.begin+8])
            edge_str += u"..."
            edge_str += unicode(string[edge.end-8:edge.end])
        print u"\t\tt%dn%d -> t%dn%d [label=\"%s\",weight=1];"% \
                (tree_id,node.node_id,tree_id, \
                edge.dst.node_id,edge_str)
        
    if node.suffix_link != None:
        print u"\t\tt%dn%d -> t%dn%d [style=dotted,weight=0];"% \
            (tree_id,node.node_id,tree_id,node.suffix_link.node_id)

def draw_tree(tree):
    tree.tree_id = ST.alloc_treeid()
    print u"\tsubgraph clusterST%d{\n"%(tree.tree_id)
    active=u"<font color=\"grey\">%s</font>%s"%( \
		    tree.string[:tree.active.begin],
		    tree.string[tree.active.begin:])
    print u"\tlabel=<%s>"%active
    draw_node(tree.root,tree,tree.root.gen)
    print u"\tcolor=blue;ratio=0.75"
    print u"\t}"


def draw_step(string):
    st = ST(u"")
    for i in xrange(0,len(string)):
        st.append(string[i])
        draw_tree(st)

escape_list ={
    u"\\":u"\\\\",
    u"\n":u"",
    u"\"":u"",
    u" ":u""
    }


def escape(string):
    for esc in escape_list:
        string = string.replace(esc,escape_list[esc])
    return string
    

if __name__==u"__main__":
    import sys
    string = escape(sys.stdin.read())
    st = ST(string)
    result = []

    print u"digraph ST{\n"
    #draw_tree(st)
    draw_step(string)
    print u"ratio=0.75\n}"

