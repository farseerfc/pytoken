#!/usr/bin/python2
class Node(object):
    nr_node = 0
    def __init__(self,char,suffix_link=None):
        self.char=char
        self.children={}
        self.node_id=Node.nr_node
        self.suffix_link=suffix_link
        Node.nr_node+=1


    def add(self,char,last):
        found=False
        for key in self.children:
            self.children[key].add(char,last)
            if key==char:
                found=True
        if (not found) and (self.char==last or self.char==u"^"):
            self.children[char]=Node(char)

    def draw(self,level=0):
        print u"%s%s"%(u" "*level,self.char)
        for child in self.allChildren():
            child.draw(level+1)

    def drawDot(self):
        print u"\t n%d [label=\"%s\"];"%(self.node_id,self.char)
        for child in self.allChildren():
            print u"\tn%d -> n%d;"%(self.node_id,child.node_id)
            child.drawDot()

    def printSuffix(self,pre=u""):
        new_pre=pre+self.char
        if len(self.children)==0:  # leaf
            print new_pre
        else:
            for child in self.allChildren():
                child.printSuffix(new_pre)



    def allChildren(self):
        children=[ self.children[key] for key in self.children]
        children.sort(key=lambda a: a.node_id)
        return children


class STrie(object):
    def __init__(self,string):
        self.root=Node(u"^")
        self.string=string+u"$"
        last=u"^"
        for ch in self.string:
            self.root.add(ch,last)
            last=ch

    def draw(self):
        self.root.draw()

    def drawDot(self):
        print u"digraph STrie{"
        self.root.drawDot()
        print u"}"

    def printSuffix(self):
        self.root.printSuffix()

if __name__==u"__main__":
    st=STrie(u"BANANAS")
    st.printSuffix()
