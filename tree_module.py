# https://stackoverflow.com/questions/2358045/how-can-i-implement-a-tree-in-python with some modifications
class Tree:
    def __init__(self, data, children=None, branchNames=None):
        self.data =data
        self.children = []
        self.branchNames = []

        if children is not None:
            for child in children:
                self.add_child(child)
        
        if branchNames is not None:
            for name in branchNames:
                self.add_name(name)

    def add_child(self, node):
        # assert isinstance(node, Tree)
        self.children.append(node)
    
    def add_name(self, name):
        self.branchNames.append(name)