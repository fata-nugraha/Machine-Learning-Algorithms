# examples are training examples
# target_attribute is the attribute whose value is to be predicted by the tree
# attributes is a list of other attributes that may be tested by the learned decision tree

import pandas as pd
import numpy as np


from tree_module import *
from myid3 import *
import math



df = pd.read_csv('../datasets/play_tennis.csv')
# df = pd.read_csv('../datasets/iris.csv', sep=',')

df = df.drop('day', axis=1)

attributes = ["outlook", "temp", "humidity", "wind"]
target = 'play'

# attributes = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
# target = 'species'

id3 = myID3(df, target, attributes)
tree = id3.tree_
tree.export_tree()