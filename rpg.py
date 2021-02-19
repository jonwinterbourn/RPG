import party
import character
import uuid


def init_rpg_game(gamesetup):

    # RPG Game for AGS 6th form application 
    # need to build in a quit

    if gamesetup == "new":
        party = new_party(4)
    elif gamesetup == "import":
        party = import_party()

    print("\nYou're ready to start the game.")
    print("Meet your party:")
    print("\nParty Name : ", party.name)
    for x in party.characters:
        print("\tCharacter 1: ", x.name)
        print("\t\tHit Points: ", x.hp)
        print("\t\tStrength: ", x.strength)
        print("\t\tAgility: ", x.agility)
        print("\t\tMagic: ", x.magic)
        print("\t\tLuck: ", x.luck)
        
    option = input("\nEnter any character, word or phrase to begin, else enter [quit] to leave programme: ")
    if option.lower()=="quit":
        raise SystemExit
    else:
        gamePlay()
        
def gamePlay():
    return 0
    
def new_party(party_size):
    i = 1
    party_name = input('Provide name of Party: ')
    #create Party
    newParty = party.Party(party_name,party_size)
    print(newParty.displayParty(),"\n")
    while i <= party_size:
        char_name = input('Provide name of Character {0}: '.format(i))
        char = character.Character(char_name, 2, 3, 3, 3, 3, 0)
        print(i, char.displayCharacter())
        #generate 4 attributes
        a = 1
        attributes = ["strength", "agility", "magic", "luck"]
        while a <= 4:
            print("\n Rolling for attribute ", a, "...")
            attributeScore = roll_for_Attributes(char)
            #function the following, so you can loop back if input error
            char = assignAttribute(a,char,attributeScore,attributes)
            a += 1
        newParty.addCharacter(char)
        i += 1
    # need to print out full party as an output
    print("Party set-up complete.")
    return newParty

def assignAttribute(a,char,attributeScore,attributes):
    attStr = " ".join(attributes)
    if a == 4:
        attribute = attributes[0]
    else:
        attribute = input("Which Attribute would you like to assign this score to? ( {0} )".format(attStr))
    if attribute in (attributes):
        #assign
        if attribute.lower() == "strength":
            #add attribute to character
            char.strength = attributeScore
            #remove from list
            attributes.remove("strength")
            print("\n")
            print(char.displayCharacter(),"\n")
        elif attribute.lower() == "agility":
            #add attribute to character
            char.agility = attributeScore
            #remove from list
            attributes.remove("agility")
            print("\n")
            print(char.displayCharacter(),"\n")
        elif attribute.lower() == "magic":
            #add attribute to character
            char.magic = attributeScore
            #remove from list
            attributes.remove("magic")
            print("\n")
            print(char.displayCharacter(),"\n")
        elif attribute.lower() == "luck":
            #add attribute to character
            char.luck = attributeScore
            #remove from list
            attributes.remove("luck")
            print("\n")
            print(char.displayCharacter(),"\n")                
    else:
        print("input not recognised - please try again...")
        assignAttribute(a,char,attributeScore,attributes)
    return (char)

def roll_for_Attributes(char):
    rolls = character.generateAptitudeScore()
    score = sum(rolls)
    lowest = rolls[2]
    print(rolls)
    print("You have rolled a score of ", score)
    print("Your lowest roll was a ", lowest, ".")
    roleagain = input("Would you like to roll that die again (yes/no) ?")
    if roleagain.lower() in ("yes", "y"):
        newRoll = character.rollD6()
        rolls[2] = newRoll
        score = sum(rolls)
        print("You have rolled a ", newRoll)
        print("Your new score is ", score)
    return score
    
def import_party():
    return "import"

        
print('Welcome to the RPG')
gamesetup = input('Do you want to import an existing party (IMPORT) or create a new party (NEW)? ')

if gamesetup.lower() == "new":
    init_rpg_game("new")
    
elif gamesetup.lower() == "import":
    init_rpg_game("import")
    
else:
    print('input not recognised')

