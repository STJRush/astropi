# Dr Space's Code

# DR Space is Dara, Ross, Scott & Karl

# Target: Photos of the ocean. (Not fussy about where)

# We are investigating ecological sea/coastal pollution/damage over time


from logzero import logger, logfile
from ephem import readtle, degree
from picamera import PiCamera
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path
import csv



print("           |       =-DRSPACE-=         ")
print("         \ _ /                         ")
print("       -= (_) =-                          ")
print("         /   \         _\/_             ")
print("           |           //o\  _\/_         ")
print("    _____ _ __ __ ____ _ | __/o\\ _       ")
print("  =-=-_-__=_-= _=_=-=_,-'|    -|-,_       ")
print("   =- _=-=- -_=-=_,-           |       ")
print("     =- =- -=.--                        ")
print("                                              ")

# says where to save stuff
dir_path = Path(__file__).parent.resolve()

# Captain's Log
logfile(dir_path / "drspace.log")

# Where is the ISS
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20316.41516162  .00001589  00000+0  36499-4 0  9995"
line2 = "2 25544  51.6454 339.9628 0001882  94.8340 265.2864 15.49409479254842"
station = readtle(name, line1, line2)


# Set up camera
phototaker = PiCamera()
#phototaker.resolution = (1296, 972)


# creates and adds things to CSV files

def newcsv(fileddata):
    """New CSV file"""
    with open(fileddata, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Temperature", "Humidity")
        writer.writerow(header)


def adddata(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)




def latitudeandlong():
    """Find the lat long"""
    station.compute()  # Get the lat/long values from ephem
    return (station.sublat / degree, station.sublong / degree)


def angleconversion(angle):
    """
converts angles so we can use EXIF
    """
    degrees, minutes, seconds = (float(field)
                                 for field in str(angle).split(":"))
    exif_angle = f'{abs(degrees):.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return degrees < 0, exif_angle


def photo(camera, image):

    station.compute()  # start wtih the lat/long values

    # convert lat/longitude to EXIF
    south, exif_latitude = angleconversion(station.sublat)
    west, exif_longitude = angleconversion(station.sublong)

    # make some EXIF tags
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # capture the image
    camera.capture(image)


# get the start time
time_we_started = datetime.now()

# get the time now
time_right_now = datetime.now()

# initialise the CSV file
data_file = dir_path / "drSpaceData.csv"

# use a function to make the csv file
newcsv(data_file)

# start counting pictures
pictureNumber = 1

# run a loop for (almost) three hours
while (time_right_now < time_we_started + (timedelta(minutes=2))):
    try:

        # first get the position
        latitude, longitude = latitudeandlong()
        
        
        # Save that into the file with the date and photo number
        data = (datetime.now(), pictureNumber, latitude, longitude)
        
        # put that into the csv
        adddata(data_file, data)
        
        
        # capture image
        savedImage = f"{dir_path}/photo_{pictureNumber:03d}.jpg"
        
        # put this thorugh the photo function
        photo(phototaker, savedImage)
        
        # log any issues
        logger.info(f"iteration {pictureNumber} Looking good!")
        
        # count up the pics
        pictureNumber += 1
        
        
        sleep(4)
        
        
        # change the time to the current time
        time_right_now = datetime.now()
        
        
    except Exception as e:
        
        # log things if they go wrong here too
        logger.error('{}: {})'.format(e.__class__.__name__, e))
        
print("Done")

