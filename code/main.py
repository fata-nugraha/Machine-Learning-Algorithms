# examples are training examples
# target_attribute is the attribute whose value is to be predicted by the tree
# attributes is a list of other attributes that may be tested by the learned decision tree

import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

from tree_module import *
from myid3 import *
from myc45 import *
import math
import copy

pd.options.mode.chained_assignment = None
df = pd.read_csv('../datasets/iris.csv', sep=',')
attributes = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
target = 'species'
# df = df.drop(target,axis=1)
# -------------------------------------------------------------
# df = pd.read_csv('../datasets/play_tennis.csv')
# df = df.drop('day', axis=1)
# attributes = ["outlook", "temp", "humidity", "wind"]
# target = 'play'

#separate the trained data and the test data
# x = df.drop(target,axis=1)
# y = df[target]
# x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
# train = x_train
# train[target] = y_train
# test = x_test
# test[target] = y_test
# train = train.reset_index(drop=True)


# def accuracy(tree, test):
# 	rules = tree.getRules()
# 	testcopy = test.reset_index(drop=True)
# 	point = 0
# 	for r in range(len(rules)):
# 		for i in range(len(testcopy)):
# 			check = True
# 			output = False
# 			for attribute in attributes:
# 				try:
# 					check = testcopy.iloc[i][attribute] == rules[r][attribute] and check
# 				except Exception as e:
# 					pass
# 			if (check):
# 				output = testcopy.iloc[i][target] == rules[r]['class']
# 				point -=1
# 			if (output):
# 				point += 5
# 		# if (checker>0):
# 		# 	rules[r]['accuracy'] = accuracy/checker
# 		# else:
# 		# 	rules[r]['accuracy'] = 0.01
# 	# rules = sorted(rules, key = lambda i: i['accuracy'], reverse = True)
# 	# for rule in rules:
# 		# print(rule)
# 	return point

# def multiprune(tree, test):
# 	result = []
# 	copytree = None
# 	for i in range(len(tree.children)):
# 		copytree = copy.deepcopy(tree)
# 		if (copytree.children[i].isLeafsParent()):
# 			copytree.children[i].prune()
# 		if accuracy(copytree, test) > accuracy(tree, test):
# 			result.append(copy.deepcopy(copytree))
# 	return result

c45 = myC45(df, target, attributes)
# print("===========")
