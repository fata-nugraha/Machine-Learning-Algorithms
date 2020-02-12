# examples are training examples
# target_attribute is the attribute whose value is to be predicted by the tree
# attributes is a list of other attributes that may be tested by the learned decision tree

import pandas as pd
import numpy as np


from tree_module import *
from myID3 import *
import math



# df = pd.read_csv('../datasets/play_tennis.csv')
df = pd.read_csv('../datasets/iris.csv', sep=',')

# df = df.drop('day', axis=1)

# attributes = ["outlook", "temp", "humidity", "wind"]
# target = 'play'

attributes = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
target = 'species'
def sorter(stuff):
	return stuff[0]
newlist = list()
a = list()
b = list()
for data in df['sepal_length']:
	a.append(data)
for data in df['species']:
	b.append(data)
for i in range(len(a)):
	newlist.append((a[i], b[i]))
newlist.sort(key = sorter)
for data in newlist:
	print(data)
exit()
temp = newlist[0][1]
for i in range(len(newlist)):
	if newlist[i][1] != temp:
		print(newlist[i-1], newlist[i])
		temp = newlist[i][1]
exit()

id3 = myID3(df, target, attributes)
tree = id3.tree_
tree.export_tree()