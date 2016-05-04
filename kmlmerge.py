#!/usr/bin/env python

# Version 0.1
# http://www.ausphreak.com
# kat @ www.ausphreak.com
# PM with bug issues, not yet extensively tested.

# Usage: kmlmerge.py Kismet-May-31-2009-1.kml Kismet-May-31-2009-2.kml output.kml
# OR set filename, filename2, and output variables


import sys
import re, datetime
import xml.dom.minidom

def macs_array(dat): #puts the mac addresses and signals in the respective dictionary
    index,x = 0, 0
    strengths = re.findall(strength, dat)
    result = re.findall(bssidre, dat)
    while x != len(result):
        result[x] = result[x][0] + ":" + result[x][1] + ":" + result[x][2] + ":" + result[x][3] + ":" +result[x][4] + ":" + result[x][5]
        x += 1

    for bssid in result:
        if first:
            macs[bssid] = int(strengths[index].strip("!")) #convert unicode to integer
        else:
            macs2[bssid] = int(strengths[index].strip("!"))
        index += 1

    for x in macs.keys():
        for y in macs2.keys():
            if x == y:
                if macs[x] > macs2[y]: similar["".join(x)] = macs[x]
                else: similar["".join(x)] = macs2[y]

def get_warpath(document):
    placemarks = document.getElementsByTagName("Placemark")
    warpath = placemarks.item(0)
    return warpath.toxml()
    
def extract_warpath():
    added, index = 0, 1
    a = str(len(re.findall(bssidre, data)))
    b = str(len(re.findall(bssidre, data2)))
    print(a + " BSSID's found in " + filename + " and " + b + " in " + filename2)
    print("Since there is " + str(len(similar)) + " collisions we expect " + str((int(a)+int(b))-len(similar)) + " BSSID's in the resulting file.")
    
    doc = xml.dom.minidom.parse(open(filename, 'r'))
    doc2 = xml.dom.minidom.parse(open(filename2, 'r'))

    date = datetime.datetime.now().strftime("%a %d-%m-%Y %I:%M")
    #at this point warpath is the first warpath, and the given name/dat
    start = "<?xml version='1.0' encoding='UTF-8'?><kml xmlns='http://earth.google.com/kml/2.0'><Folder><name>"+name+"</name><description>"+date+"</description><visibility>1</visibility><open>1</open>"

    totalstr = start + get_warpath(doc) + get_warpath(doc2) 

    #start getting individual ssid folders and attaching them
    folders = doc.getElementsByTagName("Folder")
    folders2 = doc2.getElementsByTagName("Folder") #folders in second file

    #loop through all folder elements in first file
    while index != len(folders):
        desc = folders.item(index).getElementsByTagName("description").item(0)
        unique = True
        for bssid in similar.keys():
            if bssid in desc.toxml(): #see other comment
                unique = False
                break
                
        if unique:
            totalstr += folders.item(index).toxml() + folders.item(index+1).toxml()       
        index += 2

    index = 1

    while index != len(folders2):
        desc = folders2.item(index).getElementsByTagName("description").item(0)
        unique = True
        for bssid in similar.keys():
            if bssid in desc.toxml(): #is it unique or not?
                unique = False
                break
          
        if unique:
            totalstr += folders2.item(index).toxml() + folders2.item(index+1).toxml()
            
        index += 2

    #all unique's have been added to totalstr, now let's do the duplicates
    #1. find the desc of each given ssid in similar{}
    #2. extract the signal and compare with the other signal in similar
    #3. add to totalstr whichever has the stronger signal

    for bssid in similar:
        index = 1
        while index != len(folders): 
            desc = folders.item(index).getElementsByTagName("description").item(0)
            
            if bssid in desc.toxml():
                #now let's extract the signal
                signal = int(re.findall(strength, desc.toxml())[0].strip("!"))
                if verbose:
                    print(bssid, "found on index", index, "comparing", signal, "with", similar[bssid])

                if signal == similar[bssid]:
                    totalstr += folders.item(index).toxml() + folders.item(index+1).toxml()
                    added += 1
                    break
                else:
                    #otherwise scan the other file
                    sindex = 1
                    while sindex != len(folders2):
                        desc2 = folders.item(index).getElementsByTagName("description").item(0)
                        if bssid in desc2.toxml():
                            totalstr += folders2.item(index).toxml() + folders2.item(index+1).toxml()
                            added += 1
                            break
                        sindex += 2
                    sindex = 1

            index += 2
        index = 1  

    print("Writing file...")
    f3 = open(outputfile, 'w')
    f3.write(totalstr)
    f3.close()



#OPTIONS (you must/should set these!)

try:
    filename = sys.argv[1]
    filename2 = sys.argv[2]
    outputfile = sys.argv[3]
except IndexError:
    filename = "G:\\Kismet-May-31-2009-1.kml"
    filename2 = "G:\\Kismet-May-31-2009-5.kml"
    outputfile = "output.kml"

verbose = False
name = "Merge of " + filename + " and " + filename2
strength = re.compile(r"![\d-]{2,3}") #global for space saving reasons.
bssidre = re.compile(r"([A-F0-9]{2}):([A-F0-9]{2}):([A-F0-9]{2}):([A-F0-9]{2}):([A-F0-9]{2}):([A-F0-9]{2})")
first = True
macs, macs2, similar = {}, {}, {}
f = open(filename, 'r')
f2 = open(filename2, 'r')
data = f.read()
data2 = f2.read()

macs_array(data)
first = False
macs_array(data2)
extract_warpath()


#lovely, lovely.
f = open(outputfile, 'r')
rbssid = re.findall(bssidre, f.read())
f.close()
print(len(rbssid), "SSID's in output file")
     
f.close()
f2.close()
