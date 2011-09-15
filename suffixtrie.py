class Node:
    def __init__(self,char):
        self.char=char

    def __str__(self):
        return self.char
    def __repr__(self):
        return "(%s)"%self.char

class SuffixTrie:
    def __init__(self,string,end_mark='$'):
        self.string=string
        self.end_mark=end_mark
        self.root=None
        self.construct()

    def construct():
        pass

    def drawTrie

if __name__=="__main__":
    st=SuffixTrie("a")
    st.drawTrie()
