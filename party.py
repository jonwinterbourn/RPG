class Party:
    """ A class representing a RPG party """

    def __init__(self, name, maxSize):
        self.name = name
        self.maxSize = maxSize
        self.characters = []

    def displayParty(self):
        return "Name : ", self.name,  ", maxSize: ", self.maxSize

    def dispayPartyMembers(self):
        charStr = ""
        for char in self.characters:
            charStr = charStr, ", ", char.name
        return(charStr.rstrip())

    def dispayAvailablePartyMembersWithNumbers(self):
        charStr = ""
        for index,char in enumerate(self.characters):
            if char.fatigue == 0:
                charNumber = convertIndextoCount(index)
                charStr = charStr + "  " + str(charNumber) +"." + char.name
        return(charStr.strip())

    def getCharAvailableIndices(self):
        availableIndices = []
        for index,char in enumerate(self.characters):
            if char.fatigue == 0:
                availableIndices.append(index)
        return(availableIndices)

    
    def addCharacter(self, character):
        self.characters.append(character)
        #return "character added with key ", key

    def killCharacter(self,character):
        self.characters.pop(character)
        
def convertIndextoCount(i):
    return i + 1

def counttoIndex(i):
    return i - 1
