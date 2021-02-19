import uuid
import random

class Character:
    """ A class representing a RPG character """

    def __init__(self, name, hp, strength, agility, magic, luck, fatigue):
        self.name = name
        self.hp = hp
        self.id = uuid.uuid4()
        self.strength = strength
        self.agility = agility
        self.magic = magic
        self.luck = luck
        self.fatigue = fatigue

    def displayCharacter(self):
        return "Name : ", self.name,  ", ID: ", self.id, ", HP: ", self.hp, ", Strength: ", self.strength, ", Agility: ", self.agility, ", Magic: ", self.magic, ", Luck: ", self.luck

    def reduceHP(self, amount=1):
        self.hp -= 1

    def fatigueCharacter(self):
        self.fatigue = 1

def generateAptitudeScore():
    #roll 4 x d6 and remove lowest
    maxRolls = 4
    bestRolls = []
    i = 1
    while i <= maxRolls:
        roll = rollD6()
        bestRolls.append(roll)
        i += 1
    bestRolls.sort(reverse=True)
    #remove lowest value
    bestRolls.pop(3)
    return bestRolls

def rollD6():
    roll = random.randint(1,6)
    return roll
