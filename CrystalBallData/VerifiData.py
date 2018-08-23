import csv
import sys
import collections

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

userData = collections.OrderedDict()

f = open('verifi-1.0.csv', 'r', encoding="utf8")
file = csv.reader(f)
data = list(file) #Stores csv file info into a list called 'data'



timeStartedOnPanel = data[0][1] #To be used in loop below when setting tuples as keys for dictionaries
########################## First loop to add users to dictionary and make dictionaries of actions in panels user used ##############################################
for x in range(0,len(data)):
    userName = data[x][0].lower()
    currentPanel = data[x][2]
    if(x-1 >= 0):
        prevPanel = data[x-1][2]
        prevUserName = data[x-1][0].lower()
    else:
        prevPanel = None
        prevUserName = None
    if(x+1 < len(data)):
        nextPanel = data[x+1][2]    #Makes sure the next index is NOT out of range
        timeStartedOnNextPanel = data[x + 1][1]     #Makes sure the next start time for a panel is NOT out of range
        nextUserName = data[x+1][0].lower()   #Makes sure index for the next username is NOT out of range
    else:
        nextPanel = None
        timeStartedOnNextPanel = None
        nextUserName = None
    #if(data[x][5] == '#REF!' or data[x][5] == ''):      #Makes sure that the time spent on action is existent for the row
    #    currentTimeSpent = 0
    #else:
    #    currentTimeSpent = data[x][5]


    if(not userName in userData): #If a user is not in the dictionary, he/she is added with an empty list in which to fill their actions
        userData[userName] = collections.OrderedDict() #The first panel that the user is on is added to their list of panels
        if(nextPanel == None and (currentPanel != prevPanel or userName != prevUserName)): #If on the last item of the CSV file
            userData[userName][(currentPanel, timeStartedOnPanel)] = []  # Adds tuple of current panel and time spent on it as key to user's dictionary
            timeStartedOnPanel = timeStartedOnNextPanel  # Updates time for new panel; NEEDED for unique tuples
        elif(currentPanel != nextPanel or userName != nextUserName):  #If last action on current panel
            #totalTimeOnPanel += int(currentTimeSpent)   #Increases time spent on specific panel
            userData[userName][(currentPanel, timeStartedOnPanel)] = []   #Adds tuple of current panel and time spent on it as key to user's dictionary
            timeStartedOnPanel = timeStartedOnNextPanel   #Updates time for new panel; NEEDED for unique tuples
            #totalTimeOnPanel = 0    #Resets time spent on panel for the next panel
        else:
            timeStartedOnPanel = timeStartedOnPanel
            #totalTimeOnPanel += int(currentTimeSpent)   #Increases time spent on panel
    else: #The user IS in the dictionary
        if(nextPanel == None and (currentPanel != prevPanel or userName != prevUserName)):
            userData[userName][(currentPanel, timeStartedOnPanel)] = []  # Adds tuple of current panel and time spent on it as key to user's dictionary
            timeStartedOnPanel = timeStartedOnNextPanel  # Updates time for new panel; NEEDED for unique tuples
        elif(currentPanel != nextPanel or userName != nextUserName):
            #totalTimeOnPanel += int(currentTimeSpent)
            userData[userName][(currentPanel, timeStartedOnPanel)] = []
            timeStartedOnPanel = timeStartedOnNextPanel
            #totalTimeOnPanel = 0
        else:
            timeStartedOnPanel = timeStartedOnPanel
            #totalTimeOnPanel += int(currentTimeSpent)
##################################################################################################################################################

########################## Second loop to add individual actions per user per panel ################################################################################
timeStartedOnPanel = data[0][1]
for x in range(0,len(data)):
    userName = data[x][0].lower()
    currentPanel = data[x][2]
    currentAction = data[x][3]
    currentActionDetails = data[x][4]
    if (x-1 >= 0):
        prevPanel = data[x-1][2]
        prevUserName = data[x-1][0].lower()
    else:
        prevPanel = None
        prevUserName = None
    if(x+1 < len(data)):
        nextPanel = data[x+1][2]        #Makes sure index for the next panel is NOT out of range
        timeStartedOnNextPanel = data[x+1][1]     #Makes sure index for the next start time for a panel is NOT out of range
        nextUserName = data[x+1][0].lower()     #Makes sure index for the next username is NOT out of range
    else:
        nextPanel = None
        timeStartedOnNextPanel = None
        nextUserName = None
    if(data[x][9] == '#REF!' or data[x][9] == '' or data[x][9] == 'NA'):      #Makes sure that the time spent on action is existent for the row
        currentTimeSpent = 0
    else:
        currentTimeSpent = float(data[x][9])
        currentTimeSpent *= 1000 #Converts to milliseconds

    #Appending data on individual actions to the corresponding users and panels
    if(nextPanel == None and (currentPanel != prevPanel or userName != prevUserName)):            #If on final panel in CSV
        if (currentTimeSpent <= 100):
            userData[userName][(currentPanel, timeStartedOnPanel)].append(["Nonsignificant & Others", currentAction, currentActionDetails, currentTimeSpent])
        elif (currentTimeSpent > 100 and currentTimeSpent <= 1000):
            userData[userName][(currentPanel, timeStartedOnPanel)].append(["Deliberate Action", currentAction, currentActionDetails, currentTimeSpent])
        elif (currentTimeSpent > 1000 and currentTimeSpent <= 10000):
            userData[userName][(currentPanel, timeStartedOnPanel)].append(["Cognitive Operation", currentAction, currentActionDetails, currentTimeSpent])
        elif (currentTimeSpent > 10000):
            userData[userName][(currentPanel, timeStartedOnPanel)].append(["Unit Task", currentAction, currentActionDetails, currentTimeSpent])
    if(currentPanel != nextPanel or userName != nextUserName):       #If the next panel is different from the current one OR the next user is different from the current one
        if(currentTimeSpent <= 100):
            userData[userName][(currentPanel,timeStartedOnPanel)].append(["Nonsignificant & Others", currentAction, currentActionDetails, currentTimeSpent])
        elif(currentTimeSpent > 100 and currentTimeSpent <= 1000):
            userData[userName][(currentPanel,timeStartedOnPanel)].append(["Deliberate Action", currentAction, currentActionDetails, currentTimeSpent])
        elif(currentTimeSpent > 1000 and currentTimeSpent <= 10000):
            userData[userName][(currentPanel,timeStartedOnPanel)].append(["Cognitive Operation", currentAction, currentActionDetails, currentTimeSpent])
        elif(currentTimeSpent > 10000):
            userData[userName][(currentPanel,timeStartedOnPanel)].append(["Unit Task", currentAction, currentActionDetails, currentTimeSpent])
        timeStartedOnPanel = timeStartedOnNextPanel     #Update time for next panel
    else:
        if (currentTimeSpent <= 100):
            userData[userName][(currentPanel, timeStartedOnPanel)].append(["Nonsignificant & Others", currentAction, currentActionDetails, currentTimeSpent])
        elif (currentTimeSpent > 100 and currentTimeSpent <= 1000):
            userData[userName][(currentPanel, timeStartedOnPanel)].append(["Deliberate Action", currentAction, currentActionDetails, currentTimeSpent])
        elif (currentTimeSpent > 1000 and currentTimeSpent <= 10000):
            userData[userName][(currentPanel, timeStartedOnPanel)].append(["Cognitive Operation", currentAction, currentActionDetails, currentTimeSpent])
        elif (currentTimeSpent > 10000):
            userData[userName][(currentPanel, timeStartedOnPanel)].append(["Unit Task", currentAction, currentActionDetails, currentTimeSpent])


f.close() ########End of reading csv file#######################################################################################################################

#print(userData["C1"])



totalSequence = [] #Holds sequences of actions per user

for key, value in userData.items(): #First level is the usernames
    currentUser = key
    innerUserData = value
    currentUserSequence = []

    for key2, value2 in innerUserData.items():  # Second level is the panels on which the users were
        currentPanel = key2[0]  # Holds string of current panel
        arrayOfSignificances = [x[0] for x in value2]  # Holds array of significances of actions
        arrayOfActions = [x[1] for x in value2]  # Holds array of actions
        tempSequenceOfActionsString = ""  # Will hold the sequence of actions for the specific panel

        for i in range(0, len(arrayOfSignificances)):  # Builds string of numbers that correspond to actions' significance AND action (Nonsignificant -> n, Deliberate -> d, Cognitive and Unit Tasks -> c)
            if(currentPanel == "form"):
                tempSequenceOfActionsString += "F"
            else:
                tempSequenceOfActionsString += "V"
            if (arrayOfSignificances[i] == 'Nonsignificant & Others'):  # (ex: "n0d1c2" -> [nonsignificant click -> deliberate navigate -> cognitive hover])
                if (arrayOfActions[i] == 'choice_button click' or arrayOfActions[i] == 'marker click' or arrayOfActions[i] == 'cluster click' or arrayOfActions[i] == 'geoSearchButton click' or arrayOfActions[i] == 'submit' or arrayOfActions[i] == 'acc_id click' or arrayOfActions[i] == 'click' or arrayOfActions[i] == 'loadMore click' or arrayOfActions[i] == 'emotion_header clickSort' or arrayOfActions[i] == 'resetButton click' or arrayOfActions[i] == 'search-account click' or arrayOfActions[i] == 'search-keyword click'):
                    tempSequenceOfActionsString += "n0"
                elif (arrayOfActions[i] == 'zoom' or arrayOfActions[i] == 'move' or arrayOfActions[i] == 'enter view' or arrayOfActions[i] == 'leave view' or arrayOfActions[i] == 'LanguageFeaturesFake enter' or arrayOfActions[i] == 'LanguageFeaturesFake leave' or arrayOfActions[i] == 'LanguageFeaturesReal enter' or arrayOfActions[i] == 'LanguageFeaturesReal leave' ):
                    tempSequenceOfActionsString += "n1"
                elif (arrayOfActions[i] == 'languageFeature hover' or arrayOfActions[i] == 'hover' or arrayOfActions[i] == 'sparkline hover'):
                    tempSequenceOfActionsString += "n2"
                elif (arrayOfActions[i] == 'scrollUp' or arrayOfActions[i] == 'scrollDown'):
                    tempSequenceOfActionsString += "n3"
            elif (arrayOfSignificances[i] == 'Deliberate Action'):  # (ex: "n0d1c2" -> [nonsignificant click -> deliberate navigate -> cognitive hover])
                if (arrayOfActions[i] == 'choice_button click' or arrayOfActions[i] == 'marker click' or arrayOfActions[i] == 'cluster click' or arrayOfActions[i] == 'geoSearchButton click' or arrayOfActions[i] == 'submit' or arrayOfActions[i] == 'acc_id click' or arrayOfActions[i] == 'click' or arrayOfActions[i] == 'loadMore click' or arrayOfActions[i] == 'emotion_header clickSort' or arrayOfActions[i] == 'resetButton click' or arrayOfActions[i] == 'search-account click' or arrayOfActions[i] == 'search-keyword click'):
                    tempSequenceOfActionsString += "d0"
                elif (arrayOfActions[i] == 'zoom' or arrayOfActions[i] == 'move' or arrayOfActions[i] == 'enter view' or arrayOfActions[i] == 'leave view' or arrayOfActions[i] == 'LanguageFeaturesFake enter' or arrayOfActions[i] == 'LanguageFeaturesFake leave' or arrayOfActions[i] == 'LanguageFeaturesReal enter' or arrayOfActions[i] == 'LanguageFeaturesReal leave'):
                    tempSequenceOfActionsString += "d1"
                elif (arrayOfActions[i] == 'languageFeature hover' or arrayOfActions[i] == 'hover' or arrayOfActions[i] == 'sparkline hover'):
                    tempSequenceOfActionsString += "d2"
                elif (arrayOfActions[i] == 'scrollUp' or arrayOfActions[i] == 'scrollDown'):
                    tempSequenceOfActionsString += "d3"
            elif(arrayOfSignificances[i] == 'Cognitive Operation' or arrayOfSignificances[i] == 'Unit Task'):
                if (arrayOfActions[i] == 'choice_button click' or arrayOfActions[i] == 'marker click' or arrayOfActions[i] == 'cluster click' or arrayOfActions[i] == 'geoSearchButton click' or arrayOfActions[i] == 'submit' or arrayOfActions[i] == 'acc_id click' or arrayOfActions[i] == 'click' or arrayOfActions[i] == 'loadMore click' or arrayOfActions[i] == 'emotion_header clickSort' or arrayOfActions[i] == 'resetButton click' or arrayOfActions[i] == 'search-account click' or arrayOfActions[i] == 'search-keyword click'):
                    tempSequenceOfActionsString += "c0"
                elif (arrayOfActions[i] == 'zoom' or arrayOfActions[i] == 'move' or arrayOfActions[i] == 'enter view' or arrayOfActions[i] == 'leave view' or arrayOfActions[i] == 'LanguageFeaturesFake enter' or arrayOfActions[i] == 'LanguageFeaturesFake leave' or arrayOfActions[i] == 'LanguageFeaturesReal enter' or arrayOfActions[i] == 'LanguageFeaturesReal leave' ):
                    tempSequenceOfActionsString += "c1"
                elif (arrayOfActions[i] == 'languageFeature hover' or arrayOfActions[i] == 'hover' or arrayOfActions[i] == 'sparkline hover'):
                    tempSequenceOfActionsString += "c2"
                elif (arrayOfActions[i] == 'scrollUp' or arrayOfActions[i] == 'scrollDown'):
                    tempSequenceOfActionsString += "c3"

        currentUserSequence.append(tempSequenceOfActionsString)

    totalSequence.append(currentUserSequence)


totalSequencesCombined = [] #Holds combined total sequence of each of the 81 users
for i in range(len(totalSequence)):
    tempTotalSequence = "" #Will hold the ENTIRE sequence of actions of a user
    for j in range(len(totalSequence[i])):
        tempTotalSequence += totalSequence[i][j]
    totalSequencesCombined.append(tempTotalSequence)

#print(totalSequencesCombined[0])
#print(userData["C1"])

print(len(totalSequencesCombined[1]))
print(len(totalSequencesCombined[2])/3)
print(totalSequencesCombined[1])



######################################################   Shorthand section   ######################################################################################################
totalSequencesCombinedShorthand = [] #Same as totalSequencesCombined, but uses an integer shorthand for values like "n1"
for i in range(len(totalSequencesCombined)):
    tempTotalSequence = ""
    for j in range(0, len(totalSequencesCombined[i]), 3):
        #for k in range(0, len(totalSequencesCombined[i][j]), 2): #Goes through each significance + action pairing ("n1", "c3", "d2", etc.)
        isFormSubmit = totalSequencesCombined[i][j]#k]
        actionSignificancePair = totalSequencesCombined[i][j+1]+ totalSequencesCombined[i][j+2] #+ totalSequencesCombined[i][j][k+2]

        # if(isFormSubmit == "F"):
        #     tempTotalSequence += "12, " #Treats form submit as a separate action
        #     continue

        if (actionSignificancePair == "c0"):
            tempTotalSequence += "0, "
        elif (actionSignificancePair == "c1"):
            tempTotalSequence += "1, "
        elif (actionSignificancePair == "c2"):
            tempTotalSequence += "2, "
        elif (actionSignificancePair == "d0"):
            tempTotalSequence += "3, "
        elif (actionSignificancePair == "d1"):
            tempTotalSequence += "4, "
        elif (actionSignificancePair == "d2"):
            tempTotalSequence += "5, "
        elif (actionSignificancePair == "n0"):
            tempTotalSequence += "6, "
        elif (actionSignificancePair == "n1"):
            tempTotalSequence += "7, "
        elif (actionSignificancePair == "n2"):
            tempTotalSequence += "8, "
        elif (actionSignificancePair == "n3"):
            tempTotalSequence += "9, "
        # elif (actionSignificancePair == "c3"):
        #     tempTotalSequence += "10, "
        # elif (actionSignificancePair == "d3"):
        #     tempTotalSequence += "11, "

        # else:
        #     tempTotalSequence += "-, " #If the action + significance pair isn't one of the 10 observable states from our Hidden Markov Model
    totalSequencesCombinedShorthand.append(tempTotalSequence)

print(len(totalSequencesCombinedShorthand))

########################### Writes each users total sequence of actions + significance to text file using shorthand #############################
# with open('Verifi-1.0 (Without cogn or delib scroll; submit treated as click).txt', 'a') as textFile:
#    textFile.write('\n'.join(totalSequencesCombinedShorthand))
# textFile.close()
#################################################################################################################################################

