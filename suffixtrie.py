class Node:
    def __init__(self,char):
        self.char=char
        self.children={}

    def add(self,char,last):
        found=False
        for key in self.children:
            self.children[key].add(char,last)
            if key==char:
                found=True
        if (not found) and (self.char==last or self.char=="^"):
            self.children[char]=Node(char)

    def draw(self,level=0):
        print("%s%s"%(" "*level,self.char))
        for key in self.children:
            self.children[key].draw(level+1)

class STrie:
    def __init__(self,string):
        self.root=Node("^")
        self.string=string+"$"
        last="^"
        for ch in self.string:
            self.root.add(ch,last)
            last=ch

    def draw(self):
        self.root.draw()

if __name__=="__main__":
    st=STrie("a")
    st.draw()
