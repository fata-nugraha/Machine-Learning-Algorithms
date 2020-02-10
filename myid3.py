# examples are training examples
# target_attribute is the attribute whose value is to be predicted by the tree
# attributes is a list of other attributes that may be tested by the learned decision tree

import pandas as pd
import numpy as np

from tree_module import *
import math

def myid3(examples, target_attribute, attributes):
    # If all examples are in one class:
    if (areAllValuesSame(examples[target_attribute])):
        return Tree(examples[target_attribute][0], None, None)

    if (len(attributes) == 0):
        # Check for most values
        data = examples[target_attribute].value_counts().idxmax()
        return Tree(data, None, None)
        
    # Use information gain to get best attr:
    chosenAttribute = getBestAttribute(examples, target_attribute, attributes)

    # Get unique values in the attribute
    uniqueValues = examples[chosenAttribute].unique()

    # Assign new attributes
    filteredAttributes = attributes
    filteredAttributes.remove(chosenAttribute)

    # Children of the tree
    nodes = []
    branchNames = []
    
    for value in uniqueValues:
        # Filter the example
        filterParam = examples[chosenAttribute] == value
        filteredExamples = examples[filterParam].reset_index()

        # If examples empty
        if (filteredExamples.empty):
            # Assign with most common value...
            data = examples[target_attribute].value_counts().idxmax()
            return Tree(data, None, None)
        else:
            # Recursion
            node = myid3(filteredExamples, target_attribute, filteredAttributes)

            nodes.append(node)
            branchNames.append(value)

    # Create tree
    return Tree(chosenAttribute, nodes, branchNames)

def getBestAttribute(examples, target_attribute, attributes):
    # Find the entropy of examples
    classEntropy = getEntropy(examples, target_attribute)

    # Assign initial value
    returnAttr = attributes[0]
    maxInformationGain = getInformationGain(examples, target_attribute, returnAttr, classEntropy)

    # For each attributes, check the information gain and find the maximum.
    for index in range(1, len(attributes)):
        informationGain = getInformationGain(examples, target_attribute, attributes[index], classEntropy)
        if (informationGain > maxInformationGain):
            maxInformationGain = informationGain
            returnAttr = attributes[index]

    # Return the best attribute
    return returnAttr

def getInformationGain(examples, target_attribute, attribute, classEntropy):
    classFreqRatio = examples[attribute].value_counts(normalize=True)
    # For each frequency of the class, find the gain:
    gain = 0
    for index in range (0, len(classFreqRatio)):
        value = classFreqRatio.keys()[index]
        gain += classFreqRatio[value] * getAttributeEntropy(examples, target_attribute, attribute, value)
    
    gain = classEntropy - gain
    return gain

def getAttributeEntropy(examples, target_attribute, attribute, value):
    # Filter examples that only has the value of the attribute
    filterParam = examples[attribute] == value
    filteredExamples = examples[filterParam].reset_index()

    return getEntropy(filteredExamples, target_attribute)

def getEntropy(examples, target_attribute):
    # Find class frequency
    classFreqRatio = examples[target_attribute].value_counts(normalize=True)

    entropy = 0
    for freqRatio in classFreqRatio:
        entropy += -1 * freqRatio * math.log2(freqRatio)

    return entropy

def areAllValuesSame (list):
    return all(elem == list[0] for elem in list)

# Read play-tennis dataset
# df = pd.read_csv('datasets/play_tennis.csv')

# # Then drop df['day']
# df = df.drop('day', axis=1)

# # Attributes for tree generation purposes
# attributes = ["outlook", "temp", "humidity", "wind"]

# tree = myid3(df, 'play', attributes)
# tree.export_tree(0)

df = pd.read_csv('datasets/iris.csv', sep=',')
print(df.head())

attributes = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
target = 'species'

tree = myid3(df, target, attributes)
tree.export_tree(0)
