# https://stackoverflow.com/questions/2358045/how-can-i-implement-a-tree-in-python with some modifications
class Tree:
    def __init__(self, data, names=None, children=None):
        self.data = data
        self.children = [] #array of tree
        self.names = [] #array of tree

        if children:
            for child in children:
                self.add_child(child)
        if names:
            for name in names:
                self.add_name(name)
        
    def add_child(self, tree):
        self.children.append(tree)

    def add_name(self, name):
        self.names.append(name)

    def export_tree(self, paramSpace=0):
        if (self.data):
            if (len(self.children) > 0):
                print(paramSpace * ' ' + self.data)
            else:
                print(paramSpace * ' ' + 'class: ' + self.data)
        
        space = paramSpace + 1

        for index in range(0, len(self.children)):
            print(space * ' ' + '---' + str(self.names[index]))
            self.children[index].export_tree(space + 2)

    def getRules(self):
        if (len(self.children)<=0):
            rule = dict()
            rule['class'] = self.data
            return [rule]
        count = 0
        rules = []
        for index in range(len(self.children)):
            temp = self.children[index].getRules()
            for i in range(len(temp)):
                rules.append(temp[i])
                rules[count][self.data] = self.names[index]
                count+=1
        return rules