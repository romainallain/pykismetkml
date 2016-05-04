# Introduction #

Look for any errors you may be getting here for a possible solution.

# FAQ #

Q: How do I execute python scripts from the command line (Windows)?

A: http://www.voidspace.org.uk/python/articles/command_line.shtml#path

Q: The plot of my AP's is all over the place. Why?!?! Please help me!

A: Take a few deep breaths. pykismetkml plots any AP at the point of its maximum signal, that is the longitude and latitude of the strongest signal we recieve. Sometimes, if a network is quite far away we may recieve a weak signal and therefore the plot may be less accurate to as if we recieve a very strong signal.

Q: My warpath doesn't look particularly accurate it's all over the place.

A: pykismetkml draws your warpath based on your gpsd tracklog. If for some reason your GPS freezes up, loses satellites or for some other reason your warpath may not appear to be **exactly** the path you followed. If for example you lose one or more satellites your warpath may deviate along the side of a road.


# Errors #

## **Parse Error** ##
Cause: A small character bug in Kismet that doesn't close some xml tags properly. This can happen in <= RC2.
Solution: Build Kismet from the latest version in the SVN and this will fix the bug.

## **IOError File not Found** ##
Cause: The file wasn't able to be opened, this is due to the fact that your OS isn't able to open the file using the specified path.
Solution: Double check the filepath, if you are using Windows, you may need to escape backslashes in a file path using '\\' e.g. "C:\\Python30\\mykismetfile.netxml"

## **IOError Permission Denied** ##
Cause: File permissions prevent read access to netxml or gpsxml file OR pykismetkml is unable to create a new file to write to.
Solution: Double check permissions and chmod certain files if needed. If trying to write to /var/log/kismet this error may occur.