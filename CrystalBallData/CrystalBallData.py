import csv
import sys
import collections

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

userData = collections.OrderedDict()

f = open('crystalball_userlog_final.csv', 'r')
file = csv.reader(f)
data = list(file) #Stores csv file info into a list called 'data'

#totalTimeOnPanel = 0 #To be used in loop below when setting tuples as keys for dictionaries of each user's actions in panels they used

timeStartedOnPanel = data[0][1] #To be used in loop below when setting tuples as keys for dictionaries
########################## First loop to add users to dictionary and make dictionaries of actions in panels user used ##############################################
for x in range(0,len(data)):
    userName = data[x][0]
    currentPanel = data[x][2]
    if(x-1 >= 0):
        prevPanel = data[x-1][2]
        prevUserName = data[x-1][0]
    else:
        prevPanel = None
        prevUserName = None
    if(x+1 < len(data)):
        nextPanel = data[x+1][2]    #Makes sure the next index is NOT out of range
        timeStartedOnNextPanel = data[x + 1][1]     #Makes sure the next start time for a panel is NOT out of range
        nextUserName = data[x+1][0]   #Makes sure index for the next username is NOT out of range
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
####################################################################################################################################################################
########################## Second loop to add individual actions per user per panel ################################################################################
timeStartedOnPanel = data[0][1]
for x in range(0,len(data)):
    userName = data[x][0]
    currentPanel = data[x][2]
    currentAction = data[x][3]
    currentActionDetails = data[x][4]
    if (x-1 >= 0):
        prevPanel = data[x-1][2]
        prevUserName = data[x-1][0]
    else:
        prevPanel = None
        prevUserName = None
    if(x+1 < len(data)):
        nextPanel = data[x+1][2]        #Makes sure index for the next panel is NOT out of range
        timeStartedOnNextPanel = data[x+1][1]     #Makes sure index for the next start time for a panel is NOT out of range
        nextUserName = data[x+1][0]     #Makes sure index for the next username is NOT out of range
    else:
        nextPanel = None
        timeStartedOnNextPanel = None
        nextUserName = None
    if(data[x][5] == '#REF!' or data[x][5] == ''):      #Makes sure that the time spent on action is existent for the row
        currentTimeSpent = 0
    else:
        currentTimeSpent = int(data[x][5])

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


################################################################################################################################################################
################################ CODE FOR SEQUENCE OF ACTIONS BELOW ############################################################################################
userBeingExamined = "hg-1"
#print(userData[userBeingExamined])

graph = plt.subplot(111)
currentIndexOnSequenceOfPanels = 0 #Will use this index when determining which group to add individual bars to for graph
for key, value in userData[userBeingExamined].items():
    arrayOfActions = value
    for i in range(0, len(arrayOfActions)):
        currentIndexOnSequenceOfPanels += 1

        currentPanel = key[0]
        currentActionSignificance = value[i][0]
        currentAction = value[i][1]
        currentTimeSpentOnAction_y = value[i][3]
        bar_Label = "Action: " + currentAction + "  " + "Significance: " + currentActionSignificance

        if(currentPanel == 'map'):
            graph.bar(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, width = 1, color = 'green', align = 'center') #Green bar for the map panel
            graph.text(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, bar_Label, rotation = 'vertical', fontsize = 6)
        elif(currentPanel == 'menu'):
            graph.bar(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, width = 1, color = 'blue', align = 'center')  #Blue bar for the menu panel
            graph.text(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, bar_Label, rotation = 'vertical', fontsize = 6)
        elif(currentPanel == 'menu date picker'):
            graph.bar(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, width = 1, color = 'red', align = 'center')  #Red bar for the menu date picker panel
            graph.text(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, bar_Label, rotation = 'vertical', fontsize = 6)
        elif(currentPanel == 'word cloud'):
            graph.bar(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, width = 1, color = 'yellow', align = 'center')  #Yellow bar for the word cloud panel
            graph.text(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, bar_Label, rotation = 'vertical', fontsize = 6)
        elif(currentPanel == 'calendar'):
            graph.bar(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, width = 1, color = 'orange', align = 'center')  #Orange bar for the calendar panel
            graph.text(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, bar_Label, rotation = 'vertical', fontsize = 6)
        elif(currentPanel == 'social network'):
            graph.bar(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, width = 1, color = 'pink', align = 'center')  #Pink bar for the social network panel
            graph.text(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, bar_Label, rotation = 'vertical', fontsize = 6)
        elif(currentPanel == 'crystalball'):
            graph.bar(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, width = 1, color = 'teal', align = 'center')  #Teal bar for the crystalball panel
            graph.text(currentIndexOnSequenceOfPanels, currentTimeSpentOnAction_y, bar_Label, rotation = 'vertical', fontsize = 6)
#plt.show()
################################ CODE FOR SEQUENCE OF ACTIONS ABOVE ############################################################################################
################################################################################################################################################################


################################################################################################################################################################
################################ CODE FOR LEAST COMMON SEQUENCE PER PANEL BELOW ################################################################################
mapSequence = []
menuSequence = []
menuDatePickerSequence = []
wordCloudSequence = []
calendarSequence = []
socialNetworkSequence = []
crystalBallSequence = []
tweetSequence = []
for key, value in userData.items(): #First level is the usernames
    innerUserData = value
    for key2, value2 in innerUserData.items():  #Second level is the panels on which the users were
        currentPanel = key2[0]                  #Holds string of current panel
        arrayOfActions = [x[1] for x in value2] #Holds array of actions
        tempSequenceOfActionsString = ""        #Will hold the sequence of actions for the specific panel
        for i in range(0,len(arrayOfActions)):  #Builds string of numbers that correspond to actions (click -> 0, navigate -> 1, hover -> 2, scroll -> 3, login -> 4)
            if(arrayOfActions[i] == 'click'):   #(ex: "0133" -> [click -> navigate -> scroll -> scroll])
                tempSequenceOfActionsString += "0"
            elif(arrayOfActions[i] == 'navigate'):
                tempSequenceOfActionsString += "1"
            elif(arrayOfActions[i] == 'hover'):
                tempSequenceOfActionsString += "2"
            elif (arrayOfActions[i] == 'scroll'):
                tempSequenceOfActionsString += "3"
            elif (arrayOfActions[i] == 'login'):
                tempSequenceOfActionsString += "4"

        if(currentPanel == 'map'):                          #Appends string of sequence of actions to corresponding panel's array (each string represents
            mapSequence.append(tempSequenceOfActionsString) #a sequence of actions during a SINGLE INSTANCE on a panel)
        elif(currentPanel == 'menu'):
            menuSequence.append(tempSequenceOfActionsString)
        elif (currentPanel == 'menu date picker'):
            menuDatePickerSequence.append(tempSequenceOfActionsString)
        elif (currentPanel == 'word cloud'):
            wordCloudSequence.append(tempSequenceOfActionsString)
        elif(currentPanel == 'calendar'):
            calendarSequence.append(tempSequenceOfActionsString)
        elif (currentPanel == 'social network'):
            socialNetworkSequence.append(tempSequenceOfActionsString)
        elif(currentPanel == 'crystalball'):
            crystalBallSequence.append(tempSequenceOfActionsString)
        elif(currentPanel == 'tweet'):
            tweetSequence.append(tempSequenceOfActionsString)
#print(menuSequence)
################################ CODE FOR LEAST COMMON SEQUENCE PER PANEL ABOVE ################################################################################
################################################################################################################################################################

################################################################################################################################################################
################################ CODE FOR SIGNIFICANCE OF ACTIONS SEQUENCES PER PANEL PER USER BELOW ###########################################################
significanceSequences = {
    "map": {},
    "menu": {},
    "menu date picker": {},
    "word cloud": {},
    "calendar": {},
    "social network": {},
    "crystalball": {},
    "tweet": {}
}
###### Extracting significance of each action per panel per user
for key, value in userData.items(): #First level is the usernames
    currentUser = key
    innerUserData = value
    for key2, value2 in innerUserData.items():  #Second level is the panels on which the users were
        currentPanel = key2[0]  # Holds string of current panel
        arrayOfActions = [x[0] for x in value2]  # Holds array of significances of actions
        tempSequenceOfActionsString = ""  # Will hold the sequence of actions for the specific panel

        for i in range(0, len(arrayOfActions)):  # Builds string of numbers that correspond to actions' significance (Nonsignificant -> n, Deliberate -> d, Cognitive and Unit Tasks -> c)
            if (arrayOfActions[i] == 'Nonsignificant & Others'):  # (ex: "ndc" -> [click -> navigate -> scroll -> scroll])
                tempSequenceOfActionsString += "n"
            elif(arrayOfActions[i] == 'Deliberate Action'):
                tempSequenceOfActionsString += "d"
            elif(arrayOfActions[i] == 'Cognitive Operation' or arrayOfActions[i] == 'Unit Task'):
                tempSequenceOfActionsString += "c"

        if(currentUser in significanceSequences[currentPanel]): #Appends sequence to list that user already has if they are in the current panel's dictionary
            significanceSequences[currentPanel][currentUser].append(tempSequenceOfActionsString)
        else:   #Adds new user to dictionary of panel
            significanceSequences[currentPanel][currentUser] = [tempSequenceOfActionsString]

totalNonsignOperations = 0
totalDelibOperations = 0
totalCognitiveOperations = 0

for key, value in significanceSequences.items():
    innerPanelData = value
    for key2, value2 in innerPanelData.items():
        currentUser = key2
        arrayOfActions = value2  # Holds array of significances of actions
        for i in range(0,len(arrayOfActions)):
            for j in range(1,len(arrayOfActions[i])):
                if(arrayOfActions[i][j] == 'n'):
                    totalNonsignOperations += 1
                elif(arrayOfActions[i][j] == 'd'):
                    totalDelibOperations += 1
                elif(arrayOfActions[i][j] == 'c'):
                    totalCognitiveOperations += 1

#print(significanceSequences)
################################ CODE FOR SIGNIFICANCE OF ACTIONS SEQUENCES PER PANEL PER USER ABOVE ###########################################################
################################################################################################################################################################


################################################################################################################################################################
################################ CODE FOR MICROSOFT EXCEL CHARTS BELOW #########################################################################################
#################################Dictionary for the probabilities of each combination of action and significance################################################
ActionsAndSignificance = {      #Dictionary for the probabilities of each combination of action and significance
    ("Nonsignificant & Others", "click"): 0,
    ("Nonsignificant & Others", "navigate"): 0,
    ("Nonsignificant & Others", "hover"): 0,
    ("Nonsignificant & Others", "login"): 0,
    ("Nonsignificant & Others", "scroll"): 0,
    ("Deliberate Action", "click"): 0,
    ("Deliberate Action", "navigate"): 0,
    ("Deliberate Action", "hover"): 0,
    ("Deliberate Action", "login"): 0,
    ("Deliberate Action", "scroll"): 0,
    ("Cognitive Operation", "click"): 0,
    ("Cognitive Operation", "navigate"): 0,
    ("Cognitive Operation", "hover"): 0,
    ("Cognitive Operation", "login"): 0,
    ("Cognitive Operation", "scroll"): 0,
    ("Unit Task", "click"): 0,
    ("Unit Task", "navigate"): 0,
    ("Unit Task", "hover"): 0,
    ("Unit Task", "login"): 0,
    ("Unit Task", "scroll"): 0
}

for key, value in userData.items(): #First level is the usernames
    innerUserData = value
    for key2, value2 in innerUserData.items():  #Second level is the panels on which the users were
        arrayOfActions = value2
        for i in range(0, len(arrayOfActions)): #Third level is the individual actions along with their significances on these panels
            currentInnerActionSignificance = arrayOfActions[i][0]
            currentInnerAction = arrayOfActions[i][1]
            ActionsAndSignificance[(currentInnerActionSignificance, currentInnerAction)] += 1
#print(ActionsAndSignificance)




significances_AND_Actions_Sequences = [] # Holds NEW sequences of actions AND significances together ["n0n1n4d0d2d3c2n0"]
mapSequence = []
menuSequence = []
menuDatePickerSequence = []
wordCloudSequence = []
calendarSequence = []
socialNetworkSequence = []
crystalBallSequence = []
tweetSequence = []

totalSequence = [] #Holds sequences of actions per user

for key, value in userData.items(): #First level is the usernames
    currentUser = key
    innerUserData = value
    currentUserSequence = []
    for key2, value2 in innerUserData.items():  #Second level is the panels on which the users were
        currentPanel = key2[0]  # Holds string of current panel
        arrayOfSignificances = [x[0] for x in value2]  # Holds array of significances of actions
        arrayOfActions = [x[1] for x in value2] # Holds array of actions
        tempSequenceOfActionsString = ""  # Will hold the sequence of actions for the specific panel

        for i in range(0, len(arrayOfSignificances)):  # Builds string of numbers that correspond to actions' significance AND action (Nonsignificant -> n, Deliberate -> d, Cognitive and Unit Tasks -> c)
            if(currentPanel == 'calendar'):
                if (arrayOfSignificances[i] == 'Nonsignificant & Others'):  # (ex: "n0d1c2" -> [nonsignificant click -> deliberate navigate -> cognitive hover])
                    if(arrayOfActions[i] == 'click'):
                        tempSequenceOfActionsString += "Cn0"
                    elif(arrayOfActions[i] == 'navigate'):
                        tempSequenceOfActionsString += "Cn1"
                    elif (arrayOfActions[i] == 'hover'):
                        tempSequenceOfActionsString += "Cn2"
                    elif (arrayOfActions[i] == 'scroll'):
                        tempSequenceOfActionsString += "Cn3"
                    elif (arrayOfActions[i] == 'login'):
                        tempSequenceOfActionsString += "Cn4"
                elif(arrayOfSignificances[i] == 'Deliberate Action'):
                    if (arrayOfActions[i] == 'click'):
                        tempSequenceOfActionsString += "Cd0"
                    elif (arrayOfActions[i] == 'navigate'):
                        tempSequenceOfActionsString += "Cd1"
                    elif (arrayOfActions[i] == 'hover'):
                        tempSequenceOfActionsString += "Cd2"
                    elif (arrayOfActions[i] == 'scroll'):
                        tempSequenceOfActionsString += "Cd3"
                    elif (arrayOfActions[i] == 'login'):
                        tempSequenceOfActionsString += "Cd4"
                elif(arrayOfSignificances[i] == 'Cognitive Operation' or arrayOfSignificances[i] == 'Unit Task'):
                    if (arrayOfActions[i] == 'click'):
                        tempSequenceOfActionsString += "Cc0"
                    elif (arrayOfActions[i] == 'navigate'):
                        tempSequenceOfActionsString += "Cc1"
                    elif (arrayOfActions[i] == 'hover'):
                        tempSequenceOfActionsString += "Cc2"
                    elif (arrayOfActions[i] == 'scroll'):
                        tempSequenceOfActionsString += "Cc3"
                    elif (arrayOfActions[i] == 'login'):
                        tempSequenceOfActionsString += "Cc4"
            elif(currentPanel == 'map'):
                if (arrayOfSignificances[i] == 'Nonsignificant & Others'):  # (ex: "n0d1c2" -> [nonsignificant click -> deliberate navigate -> cognitive hover])
                    if(arrayOfActions[i] == 'click'):
                        tempSequenceOfActionsString += "Mn0"
                    elif(arrayOfActions[i] == 'navigate'):
                        tempSequenceOfActionsString += "Mn1"
                    elif (arrayOfActions[i] == 'hover'):
                        tempSequenceOfActionsString += "Mn2"
                    elif (arrayOfActions[i] == 'scroll'):
                        tempSequenceOfActionsString += "Mn3"
                    elif (arrayOfActions[i] == 'login'):
                        tempSequenceOfActionsString += "Mn4"
                elif(arrayOfSignificances[i] == 'Deliberate Action'):
                    if (arrayOfActions[i] == 'click'):
                        tempSequenceOfActionsString += "Md0"
                    elif (arrayOfActions[i] == 'navigate'):
                        tempSequenceOfActionsString += "Md1"
                    elif (arrayOfActions[i] == 'hover'):
                        tempSequenceOfActionsString += "Md2"
                    elif (arrayOfActions[i] == 'scroll'):
                        tempSequenceOfActionsString += "Md3"
                    elif (arrayOfActions[i] == 'login'):
                        tempSequenceOfActionsString += "Md4"
                elif(arrayOfSignificances[i] == 'Cognitive Operation' or arrayOfSignificances[i] == 'Unit Task'):
                    if (arrayOfActions[i] == 'click'):
                        tempSequenceOfActionsString += "Mc0"
                    elif (arrayOfActions[i] == 'navigate'):
                        tempSequenceOfActionsString += "Mc1"
                    elif (arrayOfActions[i] == 'hover'):
                        tempSequenceOfActionsString += "Mc2"
                    elif (arrayOfActions[i] == 'scroll'):
                        tempSequenceOfActionsString += "Mc3"
                    elif (arrayOfActions[i] == 'login'):
                        tempSequenceOfActionsString += "Mc4"
            elif (currentPanel == 'word cloud' or currentPanel == 'social network'):
                if (arrayOfSignificances[i] == 'Nonsignificant & Others'):  # (ex: "n0d1c2" -> [nonsignificant click -> deliberate navigate -> cognitive hover])
                    if (arrayOfActions[i] == 'click'):
                        tempSequenceOfActionsString += "Nn0"
                    elif (arrayOfActions[i] == 'navigate'):
                        tempSequenceOfActionsString += "Nn1"
                    elif (arrayOfActions[i] == 'hover'):
                        tempSequenceOfActionsString += "Nn2"
                    elif (arrayOfActions[i] == 'scroll'):
                        tempSequenceOfActionsString += "Nn3"
                    elif (arrayOfActions[i] == 'login'):
                        tempSequenceOfActionsString += "Nn4"
                elif (arrayOfSignificances[i] == 'Deliberate Action'):
                    if (arrayOfActions[i] == 'click'):
                        tempSequenceOfActionsString += "Nd0"
                    elif (arrayOfActions[i] == 'navigate'):
                        tempSequenceOfActionsString += "Nd1"
                    elif (arrayOfActions[i] == 'hover'):
                        tempSequenceOfActionsString += "Nd2"
                    elif (arrayOfActions[i] == 'scroll'):
                        tempSequenceOfActionsString += "Nd3"
                    elif (arrayOfActions[i] == 'login'):
                        tempSequenceOfActionsString += "Nd4"
                elif (arrayOfSignificances[i] == 'Cognitive Operation' or arrayOfSignificances[i] == 'Unit Task'):
                    if (arrayOfActions[i] == 'click'):
                        tempSequenceOfActionsString += "Nc0"
                    elif (arrayOfActions[i] == 'navigate'):
                        tempSequenceOfActionsString += "Nc1"
                    elif (arrayOfActions[i] == 'hover'):
                        tempSequenceOfActionsString += "Nc2"
                    elif (arrayOfActions[i] == 'scroll'):
                        tempSequenceOfActionsString += "Nc3"
                    elif (arrayOfActions[i] == 'login'):
                        tempSequenceOfActionsString += "Nc4"


        currentUserSequence.append(tempSequenceOfActionsString)

        if (currentPanel == 'map'):  # Appends string of sequence of actions to corresponding panel's array (each string represents
            mapSequence.append(tempSequenceOfActionsString)  # a sequence of actions during a SINGLE INSTANCE on a panel)
        elif (currentPanel == 'menu'):
            menuSequence.append(tempSequenceOfActionsString)
        elif (currentPanel == 'menu date picker'):
            menuDatePickerSequence.append(tempSequenceOfActionsString)
        elif (currentPanel == 'word cloud'):
            wordCloudSequence.append(tempSequenceOfActionsString)
        elif (currentPanel == 'calendar'):
            calendarSequence.append(tempSequenceOfActionsString)
        elif (currentPanel == 'social network'):
            socialNetworkSequence.append(tempSequenceOfActionsString)
        elif (currentPanel == 'crystalball'):
            crystalBallSequence.append(tempSequenceOfActionsString)
        elif (currentPanel == 'tweet'):
            tweetSequence.append(tempSequenceOfActionsString)
        significances_AND_Actions_Sequences.append(tempSequenceOfActionsString)

    totalSequence.append(currentUserSequence)


totalSequencesCombined = [] #Holds combined total sequence of each of the 81 users
for i in range(len(totalSequence)):
    tempTotalSequence = "" #Will hold the ENTIRE sequence of actions of a user
    for j in range(len(totalSequence[i])):
        tempTotalSequence += totalSequence[i][j]
    totalSequencesCombined.append(tempTotalSequence)

#print(totalSequencesCombined)

countsDictionary = {
    'Cn0': 0,
'Cn1': 0,
'Cn2': 0,
'Cn3': 0,
'Cn4': 0,
    'Cd0': 0,
'Cd1': 0,
'Cd2': 0,
'Cd3': 0,
'Cd4': 0,
    'Cc0': 0,
'Cc1': 0,
'Cc2': 0,
'Cc3': 0,
'Cc4': 0,
    'Mn0': 0,
'Mn1': 0,
'Mn2': 0,
'Mn3': 0,
'Mn4': 0,
    'Md0': 0,
'Md1': 0,
'Md2': 0,
'Md3': 0,
'Md4': 0,
    'Mc0': 0,
'Mc1': 0,
'Mc2': 0,
'Mc3': 0,
'Mc4': 0,
    'Nn0': 0,
'Nn1': 0,
'Nn2': 0,
'Nn3': 0,
'Nn4': 0,
    'Nd0': 0,
'Nd1': 0,
'Nd2': 0,
'Nd3': 0,
'Nd4': 0,
    'Nc0': 0,
'Nc1': 0,
'Nc2': 0,
'Nc3': 0,
'Nc4': 0
}

for i in range(len(totalSequence)):
    tempTotalSequence = ""
    for j in range(len(totalSequence[i])):
        for k in range(0, len(totalSequence[i][j]), 3): #Goes through each significance + action pairing ("n1", "c3", "d2", etc.)
            actionSignificancePair = totalSequence[i][j][k] + totalSequence[i][j][k+1] + totalSequence[i][j][k+2]
            countsDictionary[actionSignificancePair] += 1

print(countsDictionary)



totalSequencesCombinedShorthand = [] #Same as totalSequencesCombined, but uses an integer shorthand for values like "n1"
for i in range(len(totalSequence)):
    tempTotalSequence = ""
    for j in range(len(totalSequence[i])):
        for k in range(0, len(totalSequence[i][j]), 3): #Goes through each significance + action pairing ("n1", "c3", "d2", etc.)
            actionSignificancePair = totalSequence[i][j][k] + totalSequence[i][j][k+1] + totalSequence[i][j][k+2]
            if(actionSignificancePair == "Cc0"):
                tempTotalSequence += " 00,"
            elif(actionSignificancePair == "Cc2"):
                tempTotalSequence += " 01,"
            elif (actionSignificancePair == "Cd0"):
                tempTotalSequence += " 02,"
            elif (actionSignificancePair == "Cd2"):
                tempTotalSequence += " 03,"
            elif (actionSignificancePair == "Cn2"):
                tempTotalSequence += " 04,"
            elif (actionSignificancePair == "Cn3"):
                tempTotalSequence += " 05,"
            elif (actionSignificancePair == "Mc0"):
                tempTotalSequence += " 06,"
            elif (actionSignificancePair == "Mc1"):
                tempTotalSequence += " 07,"
            elif (actionSignificancePair == "Md0"):
                tempTotalSequence += " 08,"
            elif (actionSignificancePair == "Md1"):
                tempTotalSequence += " 09,"
            elif (actionSignificancePair == "Mn1"):
                tempTotalSequence += " 10,"
            elif (actionSignificancePair == "Nc0"):
                tempTotalSequence += " 11,"
            elif (actionSignificancePair == "Nc1"):
                tempTotalSequence += " 12,"
            elif (actionSignificancePair == "Nc2"):
                tempTotalSequence += " 13,"
            elif (actionSignificancePair == "Nd0"):
                tempTotalSequence += " 14,"
            elif (actionSignificancePair == "Nd1"):
                tempTotalSequence += " 15,"
            elif (actionSignificancePair == "Nd2"):
                tempTotalSequence += " 16,"
            elif (actionSignificancePair == "Nn1"):
                tempTotalSequence += " 17,"
            elif (actionSignificancePair == "Nn2"):
                tempTotalSequence += " 18,"
    totalSequencesCombinedShorthand.append(tempTotalSequence)

print(totalSequencesCombinedShorthand)


########################### Writes each users total sequence of actions + significance to text file using shorthand #############################
# with open('hmmArrayTraining3.txt', 'a') as textFile:
#    textFile.write('\n'.join(totalSequencesCombinedShorthand))
# textFile.close()
#################################################################################################################################################


# probabilityDictionary = {
#     ('n4','c0'): 0,
#     ('n4','c1'): 0,
#     ('n4','c2'): 0,
#     ('n4','c3'): 0,
#     ('n4','c4'): 0,
#     ('n4','d0'): 0,
#     ('n4','d1'): 0,
#     ('n4','d2'): 0,
#     ('n4','d3'): 0,
#     ('n4','d4'): 0,
#     ('n4','n0'): 0,
#     ('n4','n1'): 0,
#     ('n4','n2'): 0,
#     ('n4','n3'): 0,
#     ('n4','n4'): 0,
#     ('n4','END'): 0
# }
#
# for i in range(len(significances_AND_Actions_Sequences)):
#     for j in range(0, len(significances_AND_Actions_Sequences[i]), 2):
#         key = significances_AND_Actions_Sequences[i][j] + significances_AND_Actions_Sequences[i][j+1]
#         try:
#             key2 = significances_AND_Actions_Sequences[i][j+2] + significances_AND_Actions_Sequences[i][j+3] #The element following key
#         except IndexError:
#             key2 = 'END'
#         if(key == 'n4'):
#             probabilityDictionary[(key,key2)] += 1
# #print(probabilityDictionary)

################################ CODE FOR MICROSOFT EXCEL CHARTS ABOVE #########################################################################################

################################ CODE FOR ACTION + PANEL COMBINATION PER USER BELOW##################################################################################
ActionsAndPanels = {      #Dictionary for the count of each combination of action and panel
    ("word cloud", "click"): 0,
    ("word cloud", "navigate"): 0,
    ("word cloud", "hover"): 0,
    ("word cloud", "login"): 0,
    ("word cloud", "scroll"): 0,
    ("calendar", "click"): 0,
    ("calendar", "navigate"): 0,
    ("calendar", "hover"): 0,
    ("calendar", "login"): 0,
    ("calendar", "scroll"): 0,
    ("social network", "click"): 0,
    ("social network", "navigate"): 0,
    ("social network", "hover"): 0,
    ("social network", "login"): 0,
    ("social network", "scroll"): 0,
    ("map", "click"): 0,
    ("map", "navigate"): 0,
    ("map", "hover"): 0,
    ("map", "login"): 0,
    ("map", "scroll"): 0,
    ("menu", "click"): 0,
    ("menu", "navigate"): 0,
    ("menu", "hover"): 0,
    ("menu", "login"): 0,
    ("menu", "scroll"): 0,
    ("menu date picker", "click"): 0,
    ("menu date picker", "navigate"): 0,
    ("menu date picker", "hover"): 0,
    ("menu date picker", "login"): 0,
    ("menu date picker", "scroll"): 0,
    ("crystalball", "click"): 0,
    ("crystalball", "navigate"): 0,
    ("crystalball", "hover"): 0,
    ("crystalball", "login"): 0,
    ("crystalball", "scroll"): 0,
    ("tweet", "click"): 0,
    ("tweet", "navigate"): 0,
    ("tweet", "hover"): 0,
    ("tweet", "login"): 0,
    ("tweet", "scroll"): 0
}

currentUser = 'lt-9'
for key, value in userData[currentUser].items():
    arrayOfActions = value
    for i in range(0, len(arrayOfActions)):
        currentPanel = key[0]
        currentAction = value[i][1]

        ActionsAndPanels[(currentPanel, currentAction)] += 1

ActionsAndPanelsCounts = [currentUser]
for key, value in ActionsAndPanels.items():
    ActionsAndPanelsCounts.append(value)

print(ActionsAndPanels)
print(ActionsAndPanelsCounts)


#import csv

#with open('test.csv', 'a') as myfile:
#    wr = csv.writer(myfile)
#    wr.writerow(ActionsAndPanelsCounts)

#myfile.close()

################################ CODE FOR ACTION + PANEL COMBINATION PER USER ABOVE##################################################################################