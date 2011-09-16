class Node:
    def __init__(self,char):
        self.children={}
        self.char=char

    def __str__(self):
        return self.char
    def __repr__(self):
        return "(%s)"%self.char

    def append(self,char,last):
       # found=False
       # for key in self.children:
       #     child=self.children[key]
       #     child.append(char,last)
       #     if key == char:
       #         found=True
       # if not found :
       #     self.children[char]=Node(char)
        found=False
        for key in self.children:
            child=self.children[key]
            child.append(char,last)
            if key==char:
                found=True
            if key==last:
                child
        if not found and self.char == last:
            self.children[char]=Node(char)

    def draw(self,level=0):
        print("%s%s"%(" "*level,self.char))
        children_sort=[c for c in self.children.keys()]
        children_sort.sort()
        for key in children_sort:
            child=self.children[key]
            child.draw(level+1)


class SuffixTrie:
    def __init__(self,string,end_mark='$'):
        self.string=string
        self.alphabet=list(set(self.string))
        self.alphabet.sort()
        self.end_mark=end_mark
        self.root=Node("^")
        self.construct()

    def construct(self):
        last='^'
        for char in self.string:
            self.append(char,last)
            last=char
        self.append(self.end_mark,last)

    def append(self,char,last):
        self.root.append(char,last)
        self.root.children[char]=Node(char)

    def draw(self):
        self.root.draw()

if __name__=="__main__":
    st=SuffixTrie("aa")
    st.draw()
