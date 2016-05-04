#!/usr/bin/env python
# Version 2010-02-R1
# pykismetkml@gmail.com
# http://code.google.com/p/pykismetkml

# USAGE: pykismetkml.py -i inputfile.netxml [-g gpsfile.gpsxml] [-n alternatename] [-o outputfile.kml]
# HELP: pykismetkml.py -h

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import datetime, optparse, os, re, sys
import xml.dom.minidom
from xml.dom.minidom import Node
from xml.sax.saxutils import escape

class OptionParser (optparse.OptionParser):
    def check_required (self, opt, stop):
        option = self.get_option(opt)
        if getattr(self.values, option.dest) is None:
            if stop:
                return False
            else:
                self.error("%s option not supplied" % option)
        else:
            return True

parser = OptionParser()
parser.add_option("-i", "--input", dest="filename", help="Path to netxml input file.")
parser.add_option("-g", "--gps", dest="gpsfile", help="Path to gpsxml file. OPTIONAL.")
parser.add_option("-o", "--output", dest="outputfile", help="Path to desired output file. If this is not specified the outputfile name will be \
the same as the input filename. OPTIONAL. ")
parser.add_option("-n", "--name", dest="prettyname", help="Setting this will override the default name that appears in Google Earth. OPTIONAL.")
parser.add_option("-e", "--encryption", dest="enc_filters", help="Filter encryption. Comma seperated list, i.e \"WEP,WPA,None\" or \"WPA+PSK,WPA+AES\". OPTIONAL. ")

(options, args) = parser.parse_args()

parser.check_required("-i", False)
filename = options.filename

if parser.check_required("-o", True):
    outputfile = options.outputfile
else:
    outputfile = os.path.basename(filename)[:-7] + ".kml"

#finish optionparser
    
genwarpath = parser.check_required("-g", True)
prettifyname = parser.check_required("-n", True)
if prettifyname:
    prettyname = options.prettyname

filter_encryption = parser.check_required("-e", True);
if filter_encryption:
  enc_filters = options.enc_filters.split(",")

customicons = True
apcount = 0

def parse_date(date): #likely to fail if you have a custom set template in kismet.conf
    basename = os.path.basename(date)
    capturen = re.findall(r"[\d]{1,}[\.]", basename)
    clean = basename.replace(capturen[0], "")
    clean = re.sub(r"\D", "", clean)
    struct = datetime.datetime.strptime(clean, "%Y%m%d%H%M%S")
    prettydate = datetime.datetime.strftime(struct, "%A %d %b %Y %H:%M:%S")
    return prettydate

def ext_data(nodelist, tagname, index=0, branch=False):
    if branch:
        return nodelist.item(index).getElementsByTagName(tagname)
    else:
        try:
            return nodelist.item(index).getElementsByTagName(tagname).item(0).firstChild.data
        except AttributeError: #damn you cloaked networks!
            if tagname == "essid":
                return "?Cloaked Network?"
             
def gen_warpath():
    document = xml.dom.minidom.parse(options.gpsfile)
    points = document.getElementsByTagName("gps-point")
    partstr = """<Placemark>
                    <description>Warpath Route Taken</description>
                    <name>Route</name>
                    <visibility>1</visibility>
                    <open>0</open>
                    <Style>
                        <LineStyle>
                            <color>BB0000FF</color>
                            <width>4</width>
                        </LineStyle>
                    </Style>
                    <LineString>
                        <extrude>0</extrude>
                        <tessellate>1</tessellate>
                        <altitudeMode>clampedToGround</altitudeMode> 
                        <coordinates>"""
    index = 0
    prev = [0, 0]
    for each in points:
        lat = points.item(index).getAttribute("lat")
        lon = points.item(index).getAttribute("lon")

        if lat != prev[0] and lon != prev[1]: #discard readings that are identical.
            partstr += lon+","+lat+",0 "
            prev[0] = lat
            prev[1] = lon
        index += 1

    partstr += "</coordinates></LineString></Placemark>"
    return partstr
    
def write_file(string, file):
    f = open(file, 'wt')
    if prettifyname is False:
        prettyname = parse_date(filename)
    else:
        prettyname = options.prettyname
    f.write("""<?xml version='1.0' encoding='UTF-8'?>
            <kml xmlns='http://earth.google.com/kml/2.0'>
            <Folder><name>""" + prettyname + "</name>")
    if genwarpath:
        f.write(gen_warpath())
    f.write(string)
    f.write("</Folder></kml>")
    f.close()
    print("File write successful.")

def iconify(nodelist): #make this neater
    part, full = "<Style><Icon>", ""
    for each in nodelist:
        full += each.firstChild.data + " "
    if 'WPA' in full:
        part += "node_wpa.png"
    elif 'WEP' in full:
        part += "node_wep.png"
    else:
        part += "node_open.png"
    return part + "</Icon></Style>"


def parse(filename):
    index = 0
    global apcount,filter_encryption,enc_filters
    document = xml.dom.minidom.parse(filename)
    networks = document.getElementsByTagName("wireless-network")
    fullstr = ""
    for network in networks:
        if networks.item(index).getAttribute("type") == "infrastructure":
            #now uses peaks
            gpsinfo = ext_data(networks, "gps-info", index, True)
            plotlat = ext_data(gpsinfo, "peak-lat")
            plotlon = ext_data(gpsinfo, "peak-lon")

            if plotlat==None or plotlon==None:
                index += 1
                continue
            
            essid = escape(ext_data(networks, "essid", index))
            #thanks daikin, going to see if minidom can do a pretty version of this
            #possibly use .toxml('utf8') or dom.parseString(e.toxml())
            
            #first seen/last seen
            firstseen = networks.item(index).getAttribute("first-time")
            lastseen = networks.item(index).getAttribute("last-time")
            
            #get min/max signal
            signalinfo = ext_data(networks, "snr-info", index, True)
            maxsignal = ext_data(signalinfo, "max_signal_dbm")
            minsignal = ext_data(signalinfo, "min_signal_dbm")

            #packet data
            packet = ext_data(networks, "packets", index, True)
            packets = []
            tags = ["LLC", "data", "crypt", "total", "fragments", "retries"]
            for x in tags:
                packets.append(ext_data(packet, x, 1))
            
            #encryption(s)
            encryption = networks.item(index).getElementsByTagName("encryption")
            enc = ""
            for each in encryption:
                enc += each.firstChild.data + " "

            # do not generate AP with unwanted encryption
            #print("encryption: "+enc)
            if filter_encryption:
              #print("check on "+str(apcount));
              enc_continue = False
              for enc_filter in enc_filters:
                if enc_filter in enc:
                  enc_continue = True
                  #print("encryption: "+enc)
                  #print("continue generation");
                  break
              if not enc_continue:
                #print("continue loop")
                index += 1
                continue

            #set up icons
            icon = ""
            if customicons:
                icon = iconify(encryption)

            netdetails, tags = [], ["BSSID", "channel", "freqmhz", "manuf"]
            for x in tags:
                netdetails.append(ext_data(networks, x, index))
            cdata = """<![CDATA[
                       First-seen:%s<br>
                       Last-seen:%s<br><hr>
                       BSSID:%s<br>
                       Manufacturer:%s<br>
                       Channel:%s<br>
                       Frequency:%sMhz<br>
                       Encryption:%s<br>
                       Min-Signal:%s dBm<br>
                       Max-Signal:%s dBm<br><hr>
                       <b>GPS Coordinates</b><br>
                       Avg lat/lon: %s, %s<br>
                       <b>Captured Packets</b><br>
                       LLC:%s<br>
                       data:%s<br>
                       crypt:%s<br>
                       total:%s<br>
                       fragments:%s<br>
                       retries:%s<br>
                       ]]>""" % (firstseen, lastseen, \
                           netdetails[0], netdetails[3], netdetails[1], \
                           netdetails[2], enc, minsignal, maxsignal, \
                           plotlat, plotlon, packets[0], packets[1], \
                           packets[2], packets[3], packets[4], packets[5])
            
            fullstr += """<Folder>
                                <name>%s</name>
                            
                                    <LookAt>
                                        <longitude>%s</longitude>
                                        <latitude>%s</latitude>
                                        <range>100</range>
                                        <tilt>54</tilt>
                                        <heading>-35</heading>
                                    </LookAt>
                            
                            <description>%s</description>
                                <Placemark>
                                    <name>%s</name>
                                    <description>%s</description>
                                    <visibility>1</visibility>
                                    <open>0</open>
                                    
                                    <LookAt>
                                        <longitude>%s</longitude>
                                        <latitude>%s</latitude>
                                        <range>100</range>
                                        <tilt>54</tilt>
                                        <heading>-35</heading>
                                    </LookAt>
                                                       
                                    %s
                                    
                                    <Point>
                                        <altitudeMode>clampedToGround</altitudeMode>
                                        <extrude>0</extrude>
                                        <tessellate>0</tessellate>
                                        <coordinates>%s,%s,0</coordinates>
                                    </Point>
                                </Placemark>
                            </Folder>\n\n\n""" % (essid, plotlon, plotlat, \
                            cdata, essid, cdata, plotlon, plotlat, \
                            icon, plotlon, plotlat)

            #print("add one to apcount: "+str(apcount)); 
            # only if it is really added...
            apcount += 1
        index += 1
    write_file(fullstr, outputfile)
    

parsed = parse(filename)
print("Generated "+outputfile+" ("+str(apcount)+" AP's written)")


