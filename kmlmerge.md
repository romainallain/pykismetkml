# Introduction #

A basic overview of kmlmerge.

# Details #

KMLmerge is designed to merge two .kml files together. The script produces an output .kml file with unique BSSID's. If a BSSID is not unique, the AP with the strongest signal is selected and added to the output file. War paths are also merged.

Usage: kmlmerge.py Kismet-May-31-2009-1.kml Kismet-May-31-2009-2.kml output.kml
OR set filename, filename2, and output variables

# Note #

This script has not received extensive testing and may (but hopefully not) produce unexpected results.