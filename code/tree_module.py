# https://stackoverflow.com/questions/2358045/how-can-i-implement-a-tree-in-python with some modifications
class Tree:
    def __init__(self, data, children=None, branchNames=None):
        self.data = data
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

    def export_tree(self, paramSpace=0):
        if (self.data):
            if (len(self.children) > 0):
                print(paramSpace * ' ' + self.data)
            else:
                print(paramSpace * ' ' + 'class: ' + self.data)
        
        space = paramSpace + 2

        for index in range(0, len(self.children)):
            print(space * ' ' + '---' + str(self.branchNames[index]))
            self.children[index].export_tree(space + 4)