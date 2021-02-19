class Party:
    """ A class representing a RPG party """

    def __init__(self, name, maxSize):
        self.name = name
        self.maxSize = maxSize
        self.characters = []

    def displayParty(self):
        return "Name : ", self.name,  ", maxSize: ", self.maxSize
    
    def addCharacter(self, character):
        self.characters.append(character)
        #return "character added with key ", key

    def killCharacter(self):
        return 0
        
