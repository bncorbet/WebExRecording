# Author twilson217@gmail.com

from lxml import etree
import requests
import os

def downloader(recordID, recordingName,basename):
    wbxXMLsvc = 'https://cignavirtual.webex.com/WBXService/XMLService'
    vaNBRstor = 'https://nva1wss.webex.com/nbr/services/NBRStorageService'
    vaNBRsvc = 'https://nva1wss.webex.com/nbr/services/nbrXMLService'
    sjNBRstor = 'https://nsj1wss.webex.com/nbr/services/NBRStorageService'
    sjNBRsvc = 'https://nsj1wss.webex.com/nbr/services/nbrXMLService'

    #siteID = '164033'
    siteID = '325282'
    userID = 'recording'
    userPW = 'Fall2017'
    #recordID = '48432177'
    #recordingName = 'testrecording'

    output_path = "output" + '/' + basename

    etLstRecording = etree.parse('wbx.LstRecording.xml').getroot()
    #print etLstRecording
    etNBRRecordIdList = etree.parse('wbx.getNBRRecordIdList.xml').getroot()
    #print etNBRRecordIdList
    etStorageAccessTicket = etree.parse('wbx.getStorageAccessTicket.xml').getroot()
    #print etStorageAccessTicket
    etDlNbrStorageFile = etree.parse('wbx.downloadNBRStorageFile.xml').getroot()
    #print etDlNbrStorageFile

    stXMLheaders = {'Content-Type': 'text/xml'}
    stSOAPheaders = {'Content-Type': 'text/xml', 'SOAPAction': ""}

    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    #Get recording info and put into text files in directories
    #print etLstRecording[0][0][2].text
    etLstRecording[0][0][0].text = userID
    etLstRecording[0][0][1].text = userPW
    etLstRecording[0][0][2].text = siteID
    #print etLstRecording[0][0][2].text

    rLstRecording = requests.post(wbxXMLsvc, data=etree.tostring(etLstRecording), headers=stXMLheaders)
    #print "etLstRecording", etree.tostring(etLstRecording)
    #print rLstRecording # This will return the response
    docLstRecording = etree.fromstring(rLstRecording.text.encode('utf-8'), parser=parser)
    with open('output/LstRecording.xml', 'w+') as outLstRecording:
        outLstRecording.write(etree.tostring(docLstRecording, pretty_print=True))

    #Get complete RecordID list

    #Get Storage Access Ticket
    etStorageAccessTicket[1][0][0].text = siteID
    etStorageAccessTicket[1][0][1].text = userID
    etStorageAccessTicket[1][0][2].text = userPW
    rStorageAccessTicket = requests.post(vaNBRstor, data=etree.tostring(etStorageAccessTicket), headers=stSOAPheaders)
    print "Storage Access Ticket Response:", rStorageAccessTicket
    rSATxml = etree.fromstring(rStorageAccessTicket.text.encode('utf-8'), parser=parser)
    sessionSAT = rSATxml[0][0][0].text
    #print sessionSAT

    #Download NBR Storage File
    etDlNbrStorageFile[1][0][2].text = sessionSAT
    with open('output/'+ basename + '/' + 'DlNbrStorageFile.xml', 'w+') as outDlNbrStorageFile:
        outDlNbrStorageFile.write(etree.tostring(etDlNbrStorageFile, pretty_print=True))
    etDlNbrStorageFile[1][0][0].text = siteID
    etDlNbrStorageFile[1][0][1].text = recordID
    etDlNbrStorageFile[1][0][2].text = sessionSAT
    rDlNbrStorageFile = requests.post(vaNBRstor, data=etree.tostring(etDlNbrStorageFile), headers=stSOAPheaders, stream=True)
    dlFile = open('output/' + basename + '/' + recordingName + '.xml', 'wb')
    for chunk in rDlNbrStorageFile.iter_content(chunk_size=512):
        if chunk:
            dlFile.write(chunk)
    dlFile.close()
    etDownloadData = etree.parse('output/'+ basename + '/' +recordingName+'.xml').getroot()
    etDownloadResults = etDownloadData[0][0][1].text
    if etDownloadResults == 'The recording you are looking for does not exist or is no longer available.':
        print ("The requested recording, " + recordID + " no longer exists")
        os.remove('output/' + basename + '/' + recordingName + '.xml')
    else:
        f = open('output/' + basename + '/' + recordingName + '.xml', 'rb').read().split('\r\n\r\n')
        arf = open('output/' + basename + '/' + recordingName + '.arf', 'wb')
        arf.write(f[3])
        os.remove('output/' + basename + '/' + recordingName + '.xml')
