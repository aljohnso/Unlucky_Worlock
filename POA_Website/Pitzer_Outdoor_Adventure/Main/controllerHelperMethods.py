#Think of a better name for this file
#This file contains helper methods for Main/controllers

def calculateProgress_participantRatio(masterInfo):
    if int(round(masterInfo.Participant_Cap)) == 0:
        return "100"
    participantRatio =str(round(100 * float(masterInfo.Participant_Num) / float(masterInfo.Participant_Cap)))
    if int(participantRatio) < 0:
        return "0"
    elif int(participantRatio) > 100:
        return "100"
    return participantRatio

def calculateProgress_carRatio(masterInfo):
    if int(round(masterInfo.Car_Cap)) == 0:
        return "100"
    carRatio = str(round(100 * float(masterInfo.Car_Num) / float(masterInfo.Car_Cap)))
    if int(carRatio) < 0:
        return "0"
    elif int(carRatio) > 100:
        return "100"
    return carRatio

