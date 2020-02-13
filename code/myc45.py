from collections import Counter
from myid3 import *

class myC45(myID3):

    def getThreshold(self, examples, target_attribute, continuous_attribute):
        pass

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
    def missingValues(df):
        for data in df:
            df[data] = df[data].fillna(df[data].mode()[0])
        return df
    
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
    def parseTreeFromNode(node):
        pass