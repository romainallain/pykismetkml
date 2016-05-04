# Introduction #

pykismetkml is a python script designed to export .gps and .xml files (in < Kismet RC1) to .kml files and .netxml files to .kml files in => Kismet RC2. The oldest script is based largely on pykismetearth, while the most recent revision to work with the newest version of Kismet has been coded from scratch. As of writing the most recent stable of Kismet is Kismet-2010-01-[R1](https://code.google.com/p/pykismetkml/source/detail?r=1).

# Versions #

**2010-02-[R1](https://code.google.com/p/pykismetkml/source/detail?r=1)** - Thanks to daikin for pointing out the many bugs in the previous release. This release aims to squash those bugs, not limited to escaping essids, plotting by peakval as opposed to maxval and the introduction of a new filenaming system. The new filenaming system in the interests of readability will follow YYYY-MM-Rn where n is the revision number. As usual if you note any bugs submit an issue and I shall endeavour to get it fixed.

**0.42** - Was fail.

**0.41** - Newest version. Minor bugfix version (failed when trying to fetch essid of cloaked network). Outputfile parameter is also now optional, if no outputfile is specified pykismetkml will take the base name of the .netxml and use this.

e.g if -i Kismet-20090606-18-18-18-1.netxml
then output file would be Kismet-20090606-18-18-18-1.kml

**0.4** - Adds optionparser support as well as the additional feature of mapping a warpath and name date parsing.

**0.31-0.33** - Bugfix versions to deal with ^M characters and invalid option parsing (thanks Don)

**0.31b** - Beta designed to work with the latest version of Kismet. **NOTE:** The latest version of Kismet (RC2 as of writing) has a small bug that causes XML parse errors within .netxml log files. To use pykismetkml please build from the latest version of Kismet from the SVN. This addresses the parsing issue and allows pykismetkml to work with the log data.

**0.2** - Based on pykismetearth and will work only with versions of Kismet prior to RC1. It's highly suggested you update Kismet and use 0.3b instead.


# Details #

The functionality of pykismetkml is documented in "Features".

# Bugs? #

Feel free to submit an issue.