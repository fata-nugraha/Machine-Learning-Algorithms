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
    
    def missingValues(hollowArray):
        counter = Counter(hollowArray)
        maxval = 0
        maxkey = None
        for key in counter:
            if (counter[key] > maxval):
                maxval = counter[key]
                maxkey = key
        for i in range(0, len(hollowArray)):
            if hollowArray[i] == None:
                hollowArray[i] = maxkey
        print(hollowArray)

    #splitAttributes for continuous variables
    def splitAttributes(self, examples, attributes):
        splitted = []
        maxEnt = -1*float("inf")
        bestAttribute = -1
        #sort the data according to the column.Then try all 
		#possible adjacent pairs. Choose the one that 
		#yields maximum gain
        #examples is dataframe, examples.loc[0] is attribute+value, examples.loc[0][0] is value of 1st attribute
        for indexOfAttribute in range(0, len(attributes)):
            # indexOfAttribute = examples.attribute.index(attribute)
            # examples.sort_values([attribute],inplace=True) 
            sortedExamples = examples.sort_values(attributes[indexOfAttribute],inplace=True)
            for j in range(0, len(sortedExamples) - 1):
                #if value of example[attribute][n] != value of example[attribute][n+1]
                if sortedExamples.values[j][indexOfAttribute] != sortedExamples.values[j+1][indexOfAttribute]:
                    threshold = sortedExamples.values[j][indexOfAttribute] + sortedExamples.values[j+1][indexOfAttribute]/2
                    less = []
                    greater = []
                    for j in range(0, len(sortedExamples)):
                        if(sortedExamples.values[j][indexOfAttribute] > threshold):
                            greater.append(sortedExamples.values[j][indexOfAttribute])
                        else:
                            less.append(sortedExamples.values[j][indexOfAttribute])
                        # Find the entropy of examples
                        e = getInformationGain(examples.values.tolist, [less, greater])
                        if e >= maxEnt:
                            splitted = [less, greater]
                            maxEnt = e
                            bestAttribute = attributes[index]
                            bestThreshold = threshold
        return(bestAttribute, bestThreshold, splitted)

    def getInformationGain(unionSet, subsets):
        S = len(unionSet)
        #calculate impurity before split
		impurityBeforeSplit = self.entropy(unionSet)
		#calculate impurity after split
		weights = [len(subset)/S for subset in subsets]
		impurityAfterSplit = 0
		for i in range(len(subsets)):
			impurityAfterSplit += weights[i]*self.entropy(subsets[i])
		#calculate total gain
		totalGain = impurityBeforeSplit - impurityAfterSplit
		return totalGain

myC45.missingValues([1, 2, 3, None, 5, 6, 8, 6, 6, 6, 6])