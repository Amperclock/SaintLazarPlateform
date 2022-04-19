import requests
from bs4 import BeautifulSoup
import json
import time
import csv
import shutil
import os
from datetime import datetime
from datetime import timedelta

# Setup constants
url = "https://www.transilien.com/api/nextDeparture/search"
body = {"arrival":"","departure":"Paris Saint-Lazare","pmr":"false","prm":"false","uicArrival":"","uicDeparture":"8738400"}
workdDir = os.getcwd() + "\\"
backupsDir = workdDir + "backups\\"
dataFile = "data.csv"

# Setup variables
results = {}
counter = 0

#Defining functions
def noEmptyStrings(lst):
    canary = True
    for i in lst:
        if i == '':
            canary = False
            break
    return canary

# Writing headers to CSV file
print("Creating csv file")
f = open(dataFile, 'w')
writer = csv.writer(f)
header = ['writen','trainNumber','destinationMission','departureDate','departureTime','platform']
writer.writerow(header)
f.close()

print("Starting the main loop")
while 1: # Main loop

    # Fetching fresh data
    print("Fetching data")
    r = requests.post(url,json=body) # POST to API
    response = json.loads(r.text)
    for i in response["nextTrainsList"]: # For each trains
        train = [False,i["trainNumber"],i["destinationMission"],i["departureDate"],i["departureTime"],i["platform"]]
        if noEmptyStrings(train) and train[1] not in results: # If the train contains all data
            results[i["trainNumber"]] = train # Add it to the results
    print("Loaded trains : ")
    print(results)
    
    # Purging logged departed trains
    print("Purging departed trains...")
    now = datetime.now()
    for i in results:
        if results[i][0]: # If data has been writen
            tmp = results[i][3] + "_" + results[i][4]
            trainDate = datetime.strptime(tmp,'%Y-%m-%d_%H:%M').datetime() # 2022-04-19T21:46 timedelta(minutes=1) # Add a minute just to be sure that the train departed and can be purged
            if now > trainDate : # If the train departed for at least 10 minutes
                print("removing", results[i])
                result.pop(results[i]) # Delete if from memory
    

    # Writing data
    print("Wrinting data")
    src = workdDir + dataFile
    dst = backupsDir +  "data" + str(counter) + ".csv"
    shutil.copy(src, dst) # Archiving previous data
    counter +=1

    f = open(dataFile, 'a')
    writer = csv.writer(f)
    for i in results: # Write each trains in the result
        print(results[i][0])
        if results[i][0] == False:
            results[i][0] = True
            print("Inserting",results[i])
            writer.writerow(results[i])
    f.close()


    time.sleep(20)

"""
results = {               0             1               2                   3           4               5
    ["trainNumber"]: ['written?','trainNumber','destinationMission','departureDate','departureTime','platform']
}

"""
