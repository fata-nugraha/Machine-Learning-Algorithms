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
# df = pd.read_csv('../datasets/iris.csv', sep=',')
# attributes = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
# target = 'species'
# -------------------------------------------------------------
df = pd.read_csv('../datasets/play_tennis.csv')
df = df.drop('day', axis=1)
attributes = ["outlook", "temp", "humidity", "wind"]
target = 'play'

c45 = myC45(df, target, attributes)
c45.id3.tree_.export_tree()
if c45.prunedTree_ != []:
	print("-------------------------AFTER PRUNING--------------------------")
	c45.prunedTree_[0].export_tree()

# id3 = myID3(df, target, attributes)
# id3.tree_.export_tree()