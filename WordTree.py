class WTNode:
    def __init__(self,d,l,m,r):
        self.data = d
        self.left = l
        self.right = r
        self.next = m
        self.mult = 0
          
    # prints the node and all its children in a string
    def __str__(self):  
        st = "("+str(self.data)+", "+str(self.mult)+") -> ["
        if self.left != None:
            st += str(self.left)
        else:
            st += "None"
        if self.next != None:
            st += ", "+str(self.next)
        else:
            st += ", None"
        if self.right != None:
            st += ", "+str(self.right)
        else:
            st += ", None"
        return st + "]"
    
class WordTree:
    def __init__(self):
        self.root = None
        self.size = 0
        
    def __str__(self):
        return str(self.root)

    def add(self,st):
        if st == "":
            return None
        if self.root == None:
            self.root = WTNode(st[0],None,None,None)
        ptr = self.root
        for i in range(len(st)):
            d = st[i]
            while True:
                if d == ptr.data:
                    break
                elif d < ptr.data:
                    if ptr.left == None:
                        ptr.left = WTNode(d,None,None,None)
                    ptr = ptr.left
                else:
                    if ptr.right == None:
                        ptr.right = WTNode(d,None,None,None)
                    ptr = ptr.right
            if i < len(st)-1 and ptr.next == None:
                ptr.next = WTNode(st[i+1],None,None,None)
            if i < len(st)-1:
                ptr = ptr.next
        ptr.mult += 1
        self.size += 1    
        
    # returns the number of times that string st is stored in the tree
    def count(self, st):
        return self._search(self.root, st)
    
    def _search(self, ptr, st):
        if ptr and len(st)>0:
            if ptr.data == st[0]:
                if len(st)!=1 and ptr.next:
                    return self._search(ptr.next, st[1:])
            elif ptr.data < st[0] and ptr.right:
                return self._search(ptr.right, st[:])
            elif ptr.data > st[0] and ptr.left:
                return self._search(ptr.left, st[:])
        if ptr.data == st[-1] and ptr.mult > 0:
            return ptr.mult
        return 0
    
  # returns the lexicographically smallest string in the tree
    # if the tree is empty, return None
    def min(self):
        if self.root:
            ptr=self.root
            st=ptr.data
            while ptr:
                if (ptr.mult>0 and
                    not ptr.left):
                    break
                if ptr.left:
                    ptr=ptr.left
                    st=st[:-1]+ptr.data
                elif ptr.next:
                    ptr=ptr.next
                    st+=ptr.data
            return st
        return None 
    
    # returns the lexicographically largest string in the tree
    # if the tree is empty, return None
    def max(self):
        if self.root:
            ptr=self.root
            st=ptr.data
            while ptr:
                if (ptr.mult>0 and 
                    not ptr.right and
                    not ptr.next):
                    break
                if ptr.right:
                    ptr=ptr.right
                    st=st[:-1]+ptr.data
                elif ptr.next:
                    ptr=ptr.next
                    st+=ptr.data
            return st
        return None
    
    # removes one occurrence of string st from the tree and returns None
    # if st does not occur in the tree then it returns without changing the tree
    # it updates the size of the tree accordingly
    def remove(self,st):
        if self.root and st:
            nodes = self.root_to_leaf_path_of(st)
            i=len(nodes)-1
            # start with a reference to the end-node and its parent
            ptr = nodes[i]; pptr = nodes[i-1]
            try:
                # remove end-node and fix tree (if need be)
                self._remove_node(ptr,pptr) 
                # check if tree structure was preserved
                # if so, backtrack towards the root node
                # and remove every subsequent leaf node
                while i >= 3 and not ptr.next and ptr.mult == 0:
                    ptr = nodes[i-2]; pptr = nodes[i-3]
                    # remove every update tree structure
                    self._remove_node(ptr, pptr)
                    i-=1
                # check if tree is empty
                if self.size==0:
                    self.root = None
            except Exception as E:
                pass                        
    
    # Removes a given node from the tree.
    # Raises an exception if there aren't any structural fixes or node removals left
    def _remove_node(self, ptr, pptr):
        if ptr.mult>0:
            ptr.mult-=1
            self.size-=1
            if ptr.mult>0 or ptr.next:
                raise Exception("Done.")
        if not ptr.left and not ptr.right:
            self._update_node(ptr, pptr, None)
        elif not ptr.left:
            self._update_node(ptr, pptr, ptr.right)
        elif not ptr.right:
            self._update_node(ptr, pptr, ptr.left)
        else:
            pmin = ptr.right
            ppmin = ptr
            if not pmin.left:
                ptr.data = pmin.data
                ptr.mult = pmin.mult
                ptr.right = pmin.right
                if ptr.mult>0:
                    raise Exception("Done.")
                return 
            while pmin.left:
                ppmin = pmin
                pmin = pmin.left
            ptr.data = pmin.data
            ptr.mult = pmin.mult
            ppmin.left = pmin.right    
            if ptr.mult>0:
                raise Exception("Done.")
    
    # Updates child of parent node
    def _update_node(self, ptr, pptr, node):
        if not ptr.left:
            ptr = node
            pptr.next = ptr
        else:
            ptr = node
            pptr.next = node
    

    # Returns an array containing the nodes, whose root-to-leaf
    # path corresponds to that of st   
    def root_to_leaf_path_of(self, st):
        if self.root and st:
            ptr=self.root
            i=0
            arr = [ptr]
            # each time we visit a node,regardless of there
            # being a character match, we append it to the
            # base array. in a way similar to count, we advance
            # one position in the string only when the node we're
            # at matches the single-letter prefix
            while i<len(st)-1:
                char = st[i]
                if ptr.data == char and ptr.next:
                    ptr=ptr.next
                    i+=1                    
                elif ptr.data > char and ptr.left:
                    ptr=ptr.left
                elif ptr.data < char and ptr.right:
                    ptr=ptr.right
                arr += [ptr]
            if ptr.data < st[i] and ptr.right:
                arr+=[ptr.right]
            elif ptr.data > st[i] and ptr.left:
                arr+=[ptr.left]
            return arr
        return []
    
    def __str__(self):
        return str(self.root)
    