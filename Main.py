import csv
import re
import sys
import subprocess

f = open("TestUser.csv", "rt")
reader = csv.reader(f)

recordingID = str()
recordingName = str()
keepRecording = str()
rownum = 0

#def module phpDownloader():
#    subprocess.call(*popenargs, **kwargs)
#    subprocess.call(["php", "/Download.php"]);

for row in reader:
    if rownum == 0:
        header = row
        rownum += 1
    else:
        recordingID = row[0]
        recordingName = row[1]
        keepRecording = row[5]
        if keepRecording == 'true':
            print recordingID
            print recordingName
            print keepRecording

            PHP =
            #call Webex Download module

            rownum += 1
        else:
            rownum += 1



