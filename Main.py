import csv
import re
import sys
import subprocess
import webexdl
import os
import glob

path = '/Users/briancorbet/PycharmProjects/WebExRecording'
extension = 'csv'
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format(extension))]
#print(result)


for file in result:
    basename = os.path.splitext(file)[0]
    print basename
    f = open(file, "rt")
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
            #print row
        else:
            recordingID = row[0]
            recordingName = row[1]
            keepRecording = row[5]
            if keepRecording == 'true' or keepRecording == 'TRUE' or keepRecording == 'yes' or keepRecording == 'Yes':
                print recordingID
                print recordingName
                print keepRecording

                webexdl.downloader(recordingID,recordingName,basename)

                rownum += 1
            else:
                rownum += 1



