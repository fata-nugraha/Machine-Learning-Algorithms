from collections import Counter
from myid3 import *

import numpy as np

class myC45(myID3):

    def thisIsHowToPrune():
        df = pd.read_csv('../datasets/play_tennis.csv')
        attributes = ["outlook", "temp", "humidity", "wind"]
        target = 'play'
        x = df.drop(target,axis=1)
        y = df[target]
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
        print(x_train, x_test, y_train, y_test)


    def __init__(self, examples, target_attribute, attributes):
        self.contDictionary = {}
        # Handle missing values first
        correctExamples = self.handleMissingValues(examples)

        continuous_attributes = []
        # Classify continuous and discrete values
        for attribute in attributes:
            if (correctExamples[attribute].dtype == np.float64 or correctExamples[attribute].dtype == np.int64):
                continuous_attributes.append(attribute)
        
        self.getThreshold(correctExamples, target_attribute, continuous_attributes)
                
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
    
    def handleMissingValues(self, df):
        for data in df:
            df[data] = df[data].fillna(df[data].mode()[0])
        return df

    def changeContinuousAttributeValues(self, examples, attribute, thresholdIndex):
        tempExamples = examples
        changedAttributes = []
        if thresholdIndex == len(examples[attribute])-1 :
            tempExamples[attribute][thresholdIndex] = " <= " + str(tempExamples[attribute][thresholdIndex]+0.5) 
            changedAttributes.append(" <= " + str(tempExamples[attribute][thresholdIndex]+0.5))
        else:
            for index in range(0, len(examples[attribute])):
                if (index <= thresholdIndex): 
                    tempExamples[attribute][index] = " <= " + str((tempExamples[attribute][thresholdIndex]+tempExamples[attribute][thresholdIndex+1])/2)
                    changedAttributes.append(" <= " + str((tempExamples[attribute][thresholdIndex]+tempExamples[attribute][thresholdIndex+1])/2))
                else:
                    tempExamples[attribute][index] = " > " + str((tempExamples[attribute][thresholdIndex]+tempExamples[attribute][thresholdIndex+1])/2)
                    changedAttributes.append(" > " + str((tempExamples[attribute][thresholdIndex]+tempExamples[attribute][thresholdIndex+1])/2))
        return tempExamples

    #splitAttributes for continuous variables
    # idea:
    ## 1. For all attributes:
    ## 2. sort the data according to the column.
    ## 3. Then try all possible adjacent pairs. 
    ## 4. Choose the threshold that yields maximum gain
    def splitAttributes(self, examples, target_attribute, attributes):
        maxGain = -1*float("inf")
        #For all attributes, keeping its index
        for attribute in attributes:
            #Sort data according to the column
            sortedExamples = df.sort_values(attribute)
            # print(sortedExamples)
            #For all the example
            for index in range(0, len(sortedExamples)-1):
                #Try all possible adindexacent pairs, choose the threshold that yields maximum gain
                if sortedExamples[attribute][index] != sortedExamples[attribute][index+1]:
                    tempExamples = self.changeContinuousAttributeValues(sortedExamples, attribute, index)
                    classEntropy = self.getEntropy(tempExamples, target)
                    gain = self.getInformationGain(tempExamples, target, attribute, classEntropy)
                    if gain >= maxGain:
                        maxGain = gain
                        bestTempExamples = tempExamples
            if self.areAllValuesSame(sortedExamples[target_attribute]):
                bestTempExamples = self.changeContinuousAttributeValues(sortedExamples, attribute, len(sortedExamples[attribute])-1)
        return bestTempExamples

    # def postPruning(overfitDecisionTree):
    #     pass

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

df = pd.read_csv('../datasets/iris.csv', sep=',')
attributes = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
target = 'species'

c45 = myC45(examples=df, target_attribute=target, attributes=attributes)
c45.splitAttributes(df, target, attributes) 
