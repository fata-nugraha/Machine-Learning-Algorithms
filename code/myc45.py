from collections import Counter
from myid3 import *
from sklearn.model_selection import train_test_split

import copy

import numpy as np
pd.options.mode.chained_assignment = None


class myC45(myID3):

    def __init__(self, examples, target_attribute, attributes):
        self.contDictionary = {}
        # Handle missing values first
        handledExamples = self.handleMissingValues(examples)

        continuous_attributes = []
        # Classify continuous and discrete values
        for attribute in attributes:
            if (handledExamples[attribute].dtype == np.float64 or handledExamples[attribute].dtype == np.int64):
                continuous_attributes.append(attribute)
        
        bestTempExamples = self.splitAttributes(handledExamples, target_attribute, continuous_attributes)

        x = bestTempExamples.drop(target_attribute,axis=1)
        y = bestTempExamples[target_attribute]
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
        train = x_train
        train[target_attribute] = y_train
        test = x_test
        test[target_attribute] = y_test
        train = train.reset_index(drop=True)

        self.id3 = myID3(train, target_attribute, continuous_attributes)
        
        #initialize tree
        tree = self.id3.tree_

        #prune tree
        result = self.multiprune(tree, test, target_attribute, continuous_attributes)
        if result != []:
            #print pruned tree
            result[0].export_tree()
        else:
            tree.export_tree()
            #print tree awal
            # print(self.accuracy(tree, test, target_attribute, continuous_attributes))

    ## pruning
    #separate the trained data and the test data
    def separateTrainedData(self, examples, target):
        x = examples.drop(target,axis=1)
        y = examples[target]
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
        train = x_train
        train[target] = y_train
        test = x_test
        test[target] = y_test
        train = train.reset_index(drop=True)
    
    # accuracy of data
    def accuracy(self, tree, test, target_attribute, attributes):
        rules = tree.getRules()
        testcopy = test.reset_index(drop=True)
        point = 0
        for r in range(len(rules)):
            for i in range(len(testcopy)):
                check = True
                output = False
                for attribute in attributes:
                    try:
                        check = testcopy.iloc[i][attribute] == rules[r][attribute] and check
                    except Exception as e:
                        pass
                if (check):
                    output = testcopy.iloc[i][target_attribute] == rules[r]['class']
                    point -=1
                if (output):
                    point += 5
            # if (checker>0):
            # 	rules[r]['accuracy'] = accuracy/checker
            # else:
            # 	rules[r]['accuracy'] = 0.01
        # rules = sorted(rules, key = lambda i: i['accuracy'], reverse = True)
        # for rule in rules:
            # print(rule)
        return point
    
    def multiprune(self, tree, test, target_attribute, attributes):
        result = []
        copytree = None
        for i in range(len(tree.children)):
            copytree = copy.deepcopy(tree)
            if (copytree.children[i].isLeafsParent()):
                copytree.children[i].prune()
            if self.accuracy(copytree, test, target_attribute, attributes) > self.accuracy(tree, test, target_attribute, attributes):
                result.append(copy.deepcopy(copytree))
        return result

    ##
                
    # def gainRatio(self, examples, target_attribute, attribute, classEntropy):
    #     gain = self.getInformationGain(examples, target_attribute, returnAttr, classEntropy)
    #     splitInformation = self.getSplitInformation(examples, target_attribute, attribute)
    #     return gain/splitInformation

    # def getSplitInformation(self, examples, target_attribute, attribute):
    #     classFreqRatios = examples[attribute].value_counts(normalize=True)
    #     splitInformation = 0
    #     for index in range (0, len(classFreqRatios)):
    #         value = classFreqRatios.keys()[index]
    #         splitInformation -= classFreqRatios[value] * self.getAttributeEntropy(examples, target_attribute, attribute, value)
    #     return splitInformation
    
    def handleMissingValues(self, df):
        for data in df:
            df[data] = df[data].fillna(df[data].mode()[0])
        return df

    def changeContinuousAttributeValues(self, examples, attribute, threshold):
        tempExamples = copy.copy(examples)
        for index in range(len(examples[attribute])):
            tempExamples[attribute][index] = ' <= ' + str(threshold) if tempExamples[attribute][index] <= threshold else ' > ' + str(threshold)
        return tempExamples

    #splitAttributes for continuous variables
    # idea:
    ## 1. For all attributes:
    ## 2. sort the data according to the column.
    ## 3. Then try all possible adjacent pairs. 
    ## 4. Choose the threshold that yields maximum gain
    def splitAttributes(self, examples, target_attribute, attributes):
        bestTempExamples = examples
        #For all attributes, keeping its index
        for attribute in attributes:
            maxGain = -1*float("inf")
            #Sort data according to the column
            # print(attribute)
            sortedExamples = bestTempExamples.sort_values(attribute)
            #For all the example
            for index in range(0, len(sortedExamples)-1):
                #Try all possible adjacent pairs, choose the threshold that yields maximum gain
                if sortedExamples[attribute][index] != sortedExamples[attribute][index+1]:
                    tempExamples = self.changeContinuousAttributeValues(sortedExamples, attribute, sortedExamples[attribute][index])
                    classEntropy = self.getEntropy(tempExamples, target_attribute)
                    gain = self.getInformationGain(tempExamples, target_attribute, attribute, classEntropy)
                    if gain >= maxGain:
                        maxGain = gain
                        bestTempExamples = copy.copy(tempExamples)
        return bestTempExamples

    # 1. Infer the decision tree from the training set, growing the tree until the training 
    #    data is fit as well as possible and allowing overfitting to occur. 
    # 2. Convert the learned tree into an equivalent set of rules by creating one rule
    #    for each path from the root node to a leaf node. 
    # 3. Prune (generalize) each rule by removing any preconditions that result in
    #    improving its estimated accuracy
    # 4. Sort the pruned rules by their estimated accuracy, and consider them in this
    #    sequence when classifying subsequent instances. 

    #Preorder Traversal, getting rule each time it reaches a leaf
    # def parseTreeFromNode(node):