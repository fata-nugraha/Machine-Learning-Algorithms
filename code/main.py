# examples are training examples
# target_attribute is the attribute whose value is to be predicted by the tree
# attributes is a list of other attributes that may be tested by the learned decision tree

import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

from tree_module import *
from myID3 import *
import math

pd.options.mode.chained_assignment = None
# df = pd.read_csv('../datasets/iris.csv', sep=',')
# attributes = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
# target = 'species'
# -------------------------------------------------------------
df = pd.read_csv('../datasets/play_tennis.csv')
df = df.drop('day', axis=1)
attributes = ["outlook", "temp", "humidity", "wind"]
target = 'play'
x = df.drop(target,axis=1)
y = df[target]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
train = x_train
train[target] = y_train
test = x_test
test[target] = y_test




# df = pd.read_csv('../datasets/play_tennis.csv')
# df = pd.read_csv('../datasets/iris.csv', sep=',')

# df = df.drop('day', axis=1)

# attributes = ["outlook", "temp", "humidity", "wind"]
# target = 'play'




# attributes = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
# target = 'species'
id3 = myID3(train, target, attributes)
tree = id3.tree_
tree.export_tree()
rules = tree.getRules()
testcopy = test
testcopy = testcopy.reset_index(drop=True)
for r in range(len(rules)):
	accuracy = 0
	checker = 0
	for i in range(len(testcopy)):
		check = True
		for attribute in attributes:
			try:
				check = testcopy.iloc[i][attribute] == rules[r][attribute] and check
			except Exception as e:
				pass
		if (check):
			output = not (testcopy.iloc[i][target] != rules[r]['class'])
			checker +=1
		if (output):
			accuracy += 1
	rules[r]['accuracy'] = accuracy/checker
sorted(rules, key = lambda i: i['accuracy'], reverse = True)
for rule in rules:
	print(rule)


