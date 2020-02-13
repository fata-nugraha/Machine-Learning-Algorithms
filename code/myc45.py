from collections import Counter
from myid3 import *

import numpy as np

class myC45(myID3):

    def __init__(self, examples, target_attribute, attributes):
        self.contDictionary = {}
        # Handle missing values first
        correctExamples = self.handleMissingValues(examples)

        continuous_attributes = []
        # Classify continuous and discrete values
        for attribute in attributes:
            if (correctExamples[attribute].dtype == np.float64 or correctExamples[attribute].dtype == np.int64):
                continuous_attributes.append(attribute)
        
        self.getThreshold(self, correctExamples, target_attribute, continuous_attributes)


    def getThreshold(self, examples, target_attribute, continuous_attributes):
        for attribute in continuous_attributes:
            tresholdArr = []
            sortedExamples = examples.sort_values(by=attribute)
            
            # Get first value of target_attributes
            target_value = sortedExamples[target_attributes][0]

            for index in range (0, len(sortedExamples[target_value])):
                if (sortedExamples[target_value][0] != target_value):
                    tresholdArr.append(index)
                    
            tresholdArr.append(len(sortedExamples[target_value]) - 1)
                

    def gainRatio(self, examples, target_attribute, attribute, classEntropy):
        gain = self.getInformationGain(examples, target_attribute, returnAttr, classEntropy)
        splitInformation = self.getSplitInformation(examples, target_attribute, attribute)
        return gain/splitInformation

    def getSplitInformation(self, examples, target_attribute, attribute):
        classFreqRatios = examples[attribute].value_counts(normalize=True)
        splitInformation = 0
        for index in range (0, len(classFreqRatios)):
            value = classFreqRatios.keys()[index]
            splitInformation -= classFreqRatios[value] * self.getAttributeEntropy(examples, target_attribute, attribute, value)
        return splitInformation
    
    def handleMissingValues(hollowArray):
        # counter = Counter(hollowArray)
        # maxval = 0
        # maxkey = None
        # for key in counter:
        #     if (counter[key] > maxval):
        #         maxval = counter[key]
        #         maxkey = key
        # for i in range(0, len(hollowArray)):
        #     if hollowArray[i] == None:
        #         hollowArray[i] = maxkey
        # print(hollowArray)



    #splitAttributes for continuous variables
    # idea:
    ## 1. For all attributes:
    ## 2. sort the data according to the column.
    ## 3. Then try all possible adjacent pairs. 
    ## 4. Choose the attribute that yields maximum gain
    def splitAttributes(self, examples, target_attribute, attributes):
        splitted = []
        maxEnt = -1*float("inf")
        bestAttribute = -1
        #For all attributes, keeping its index
        for indexOfAttribute in range(0, len(attributes)):
            #Sort data according to the column
            sortedExamples = examples.sort_values(attributes[indexOfAttribute],inplace=True)
            #For all the example
            for j in range(0, len(sortedExamples) - 1):
                #Try all possible adjacent pairs, choose the attribute that yields maximum gain
                if sortedExamples.values[j][indexOfAttribute] != sortedExamples.values[j+1][indexOfAttribute]:
                    threshold = sortedExamples.values[j][indexOfAttribute] + sortedExamples.values[j+1][indexOfAttribute]/2
                    less = []
                    greater = []
                    for j in range(0, len(sortedExamples)):
                        if(sortedExamples.values[j][indexOfAttribute] > threshold):
                            greater.append(sortedExamples.values[j][indexOfAttribute])
                        else:
                            less.append(sortedExamples.values[j][indexOfAttribute])
                        # Get information gain with examples before splitting: current examples and subsets=[less,greater]
                        e = self.getInformationGain(examples=[less,greater], target_attribute=target_attribute, attribute=attributes[indexOfAttribute],  classEntropy=self.getEntropy(examples,target_attribute))
                        if e >= maxEnt:
                            splitted = [less, greater]
                            maxEnt = e
                            bestAttribute = attributes[indexOfAttribute]
                            bestThreshold = threshold
        #return chosen best attribute, threshold of best attribute and splitted examples
        return(bestAttribute, bestThreshold, splitted)

    def postPruning(overfitDecisionTree):
        rule = traverse_tree(overfitDecisionTree.root)

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


myC45.missingValues([1, 2, 3, None, 5, 6, 8, None, 6, 6, 6])