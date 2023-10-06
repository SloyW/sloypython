from geopy.distance import geodesic
import math
#Set-ExecutionPolicy Unrestricted -Scope Process
coordinates = [(50.946152, 6.948278),
(50.946488, 6.948642),
(50.946592, 6.947893),
(50.946748, 6.947805),
(50.946690, 6.948164),
(50.946944, 6.948863),
(50.946350, 6.949104),
(50.946370, 6.950279),
(50.946564, 6.950753),
(50.946363, 6.951435),
(50.945419, 6.950364),
(50.945461, 6.949825),
(50.945887, 6.949482),
(50.946019, 6.949198),
(50.946349, 6.949102),
(50.946369, 6.948764)]

def fileEntry(coordinate, time):
    routeFile.write('\n')
    waypointString = '<wpt lat="'+str(coordinate[0])+str('" lon="')+str(coordinate[1])+str('">\n')
    routeFile.write(waypointString)
    seconds = str(int(time % 60))
    minutes = str(int((time-float(seconds))/60))
    if float(seconds) < 10:
        seconds = '0'+seconds
    if float(minutes) < 10:
        minutes = '0'+minutes
    timeString = '<time>2023-01-01T00:'+minutes+':'+seconds+'Z</time>\n'
    routeFile.write(timeString)
    routeFile.write('</wpt>\n')

routeFile = open("route.gpx", "w")

## fileheader
routeFile.write('<?xml version="1.0"?>\n')
routeFile.write('<gpx version="1.1" creator="gpxgenerator.com">\n')
##
totalDistance = 0.0
totalTime = 0.0
## first coord pls setup time
fileEntry(coordinates[0],0)
fileEntry(coordinates[0],60)
totalTime += 60
##

for index in range(1, len(coordinates)):
    fromCoord = coordinates[index-1]
    toCoord = coordinates[index]

    distance = geodesic(fromCoord,toCoord).km
    totalDistance += distance
    time =  math.ceil(distance*1000/1.25)
    totalTime += time
    fileEntry(coordinates[index], totalTime)
## last coord cooldown
totalTime += 60
fileEntry(coordinates[len(coordinates)-1],totalTime)
##

## loop
loopDistance = geodesic(coordinates[len(coordinates)-1],coordinates[0]).km
loopTime = math.ceil(loopDistance*1000/1.25)
fileEntry(coordinates[0], loopTime + totalTime)
##

# file close
routeFile.write('\n')
routeFile.write('</gpx>\n')
routeFile.close

print('TOTAL DISTANCE ', (totalDistance*1000), 'm TOTAL TIME ', totalTime , 's')