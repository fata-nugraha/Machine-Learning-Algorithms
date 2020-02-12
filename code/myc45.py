from collections import Counter
from myID3 import *

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
        


myC45.missingValues([1, 2, 3, None, 5, 6, 8, 6, 6, 6, 6])