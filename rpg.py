import party
import character
import uuid
import random
import json
import sys
import os

def init_rpg_game(gamesetup):

    # RPG Game for AGS 6th form application 
    # need to build in a quit

    if gamesetup == "new":
        party = new_party(4)
    elif gamesetup == "import":
        party = import_party(4)

    print("\nYou're ready to start the game.")
    print("Meet your party:")
    print("\nParty Name : ", party.name)
    for i, item in enumerate(party.characters, start=1):
        print("\tCharacter ", i, ": ", item.name)
        print("\t\tHit Points: ", item.hp)
        print("\t\tStrength: ", item.strength)
        print("\t\tAgility: ", item.agility)
        print("\t\tMagic: ", item.magic)
        print("\t\tLuck: ", item.luck)
        
    option = input("\nEnter any character, word or phrase to begin, else enter [quit] to leave programme: ")
    if option.lower()=="quit":
        raise SystemExit
    else:
        gamePlay(party)
        
def gamePlay(party):
    print("\nWelcome ", party.name, " to the game and your 5 challenges.")
    g = 1
    maxChallenges = 5
    score = [0, 0]
    while g <= maxChallenges:
        challengeProfile = setChallengeProfile()
        print ("Challenge ", g, " has a rating of ", challengeProfile[0], " (/15) and is a ", challengeProfile[1], " challenge.")
        #need to give options for party members and how many members there are in the party
        characterStr = party.dispayAvailablePartyMembersWithNumbers()
        charAvailableIndices = party.getCharAvailableIndices()
        #call function pickCharacter(characterStr,charAvailableIndices)
        playerIndex = pickCharacter(characterStr,charAvailableIndices)
        player = party.characters[playerIndex]
        print("You have chosen ", player.name, " to play this challenge.") 
        
        result = newChallenge(challengeProfile,party,player)
        if result == "success":
            score[0] += 1
        else:
            score[1] += 1
        g += 1
    print("Challenges complete. Your party were successful in ", score[0], " challlenges and unsuccessful in ", score[1], " challenges.")
    print("You have ", len(party.characters), "characters alive in your party.")
    export = input("Would you like to export the remaining members of your party? (yes / no)")
    if export.lower() in ("yes", "y"):
        #export
        print("Here we go")        
        chars ={}
        a = 1
        while a <= len(party.characters):
            char_index = "Character" + str(a)
            print(char_index)
            char = {
                "name": party.characters[a-1].name,
                "hp": party.characters[a-1].hp,
                "strength": party.characters[a-1].strength,
                "agility": party.characters[a-1].agility,
                "magic": party.characters[a-1].magic,
                "luck": party.characters[a-1].luck,
                "fatigue": 0
                }
            char_value = char
            print(char_value)
            chars[char_index] = char_value
            a += 1
        ps = {
            "name": party.name,
            "maxSize": party.maxSize,
            "characters": chars
            }

        print(json.dumps(ps, indent=4))
        with open('data.json', 'w') as outfile:
            json.dump(ps, outfile, indent=4)
        
    print("Thank you for playing the game - see you next time.")
        
    #return to start
    

def pickCharacter(characterStr,charAvailableIndices):
    print(charAvailableIndices)
    charAvailableNumbers = [x+1 for x in charAvailableIndices] 
    print(charAvailableNumbers)
    print("Which available character do you want to pick for this challenge? Please enter the digit corresponding to the name of the character: ", characterStr)
    player = int(input("Please enter the digit corresponding to the name of the character "))
    if player in charAvailableNumbers:
        playerIndex = party.counttoIndex(player)
    else:
        print("That input wasn't recognised, please try again...")
        pickCharacter(characterStr,charAvailableIndices)
    return playerIndex

def setChallengeProfile():
    #2 features; challenge rating and attribute
    attributes = ["strength", "agility", "magic", "luck"]
    challengeRating = generateChallengeRating()
    challengeAttribute = random.choice(attributes)
    challengeProfile = (challengeRating, challengeAttribute)
    return challengeProfile

def newChallenge(challengeProfile,party,partyCharacter):
    #result is success or failure
    challengeResult = ""
    #defatigue all players
    for x in party.characters:
        x.fatigue = 0
    
    #the challange
    challengeRoll = rollD20()
    challengeTotal = challengeRoll + challengeProfile[0]

    print("\nThe challenge score is ", challengeTotal)
    
    #the character
    characterAttributeScore = 0
    if challengeProfile[1] == "strength":
        characterAttributeScore = partyCharacter.strength
    elif challengeProfile[1] == "agility":
        characterAttributeScore = partyCharacter.agility
    elif challengeProfile[1] == "magic":
        characterAttributeScore = partyCharacter.magic
    elif challengeProfile[1] == "luck":
        characterAttributeScore = partyCharacter.luck
        
    characterRoll = rollD20()
    characterTotal = characterRoll + characterAttributeScore

    print("\nThe player's score is ", characterTotal)
    #fatigue the player
    partyCharacter.fatigueCharacter()
    
    if characterTotal >= challengeTotal:
        print("\nYou win!")
        #add HP, if not @4
        if partyCharacter.hp <4:
              partyCharacter.hp += 1
              print("Your player has gained a hit point.")
        challengeResult  = "success" 
    else:
        print("\nYou lose!")
        #remove hit point
        partyCharacter.hp -= 1
        print("Your player has lost a hit point.")
        if partyCharacter.hp == 0:
            print("Your player has no hit points and is dead. This character will be removed from your party")
            party.killCharacter(partyCharacter)
        challengeResult  = "failure"
    return challengeResult
    
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
            char = assignAttribute(a,char,attributeScore,attributes)
            a += 1
        newParty.addCharacter(char)
        i += 1
    # need to print out full party as an output
    print("Party set-up complete.")
    return newParty

def import_party(party_size):

    #set filename
    #uf = "party_examplea.json"
    #suf = "party_example.json"
    #uf = "data.json"
    uf = input("Enter the full path of your json file: ")
    assert os.path.exists(uf), "I did not find the file at, "+str(uf)
    #load file
    json_data=open(uf).read()
    json_obj = json.loads(json_data)
    #process file
    print("Importing characters...")
    importedParty = party.Party(str(json_obj['name']),json_obj['maxSize'])
    imported_party_size = len(json_obj['characters'])
    print(imported_party_size, " characters imported.")
    #If there are less than four characters in the file then new characters must be generated, using the same rules
    #as above, until the party contains four characters in total.
    rem = 4-imported_party_size
    print("Remainder", rem)

    for key, value in json_obj['characters'].items():
        char_name = value["name"] #item.get("name", None)
        char_hp = value["hp"]
        char_strength = value["strength"]
        char_agility = value["agility"]
        char_magic = value["magic"]
        char_luck = value["luck"]
        char_fatigue = value["fatigue"]
        char = character.Character(char_name, char_hp, char_strength, char_agility, char_magic, char_luck, char_fatigue)
        importedParty.addCharacter(char)
    
    if rem > 0:
        print("Generate new characters...")
        a = 1
        while a <= rem:
            char_name = input('Provide name of Replacement Character {0}: '.format(a))
            char = character.Character(char_name, 2, 3, 3, 3, 3, 0)
            print(a, char.displayCharacter())
            #generate 4 attributes
            b = 1
            attributes = ["strength", "agility", "magic", "luck"]
            while b <= 4:
                print("\n Rolling for attribute ", a, "...")
                attributeScore = roll_for_Attributes(char)
                #function the following, so you can loop back if input error
                char = assignAttribute(b,char,attributeScore,attributes)
                b += 1
            importedParty.addCharacter(char)
            a += 1
    return importedParty

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
    

def generateChallengeRating():
    rating = random.randint(5,15)
    return rating

def rollD4():
    roll = random.randint(1,4)
    return roll
    
def rollD20():
    roll = random.randint(1,20)
    return roll

        
print('Welcome to the RPG')
gamesetup = input('Do you want to import an existing party (IMPORT) or create a new party (NEW)? ')

if gamesetup.lower() == "new":
    init_rpg_game("new")
    
elif gamesetup.lower() == "import":
    init_rpg_game("import")
    
else:
    print('input not recognised')

