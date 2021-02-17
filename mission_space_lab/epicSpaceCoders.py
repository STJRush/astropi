#EpicSpaceCoders Code 

from logzero import logger, logfile
from ephem import readtle, degree
from picamera import PiCamera
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path
import csv

dir_path = Path(__file__).parent.resolve()

# ??log 
logfile(dir_path/"EpicSpaceCoders.log")

# find the place
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   21039.89161926 -.00000043  00000-0  73771-5 0  9995 2 25544  51.6440 257.2891 0002486 351.4127  16.5936 15.48938694268710 "
line2 = "2 25544  51.6454 339.9628 0001882  94.8340 265.2864 15.49409479254842"
adorablespacestation = readtle(name, line1, line2)


# Enable camera
picturetaker = PiCamera()
cam.resolution = (1296, 972)

def csvmaker(fileofdata):
    """make the new csv"""
    with open(fileofdata, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Temperature", "Humidity")
        writer.writerow(header)

def csvdataadder(dataoffile, dataaaa):
    """add more data"""
    with open(dataoffile, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(dataaaa)

def latandlonggetter():
    """give the lat and long in degrees"""
    adorablespacestation.compute() # Get the lat/long values from ephem
    return (adorablespacestation.sublat / degree, adorablespacestation.sublong / degree)

def changeandconvert(angle):
    """
    convert angle.
    """
    degrees, minutes, seconds = (float(field) for field in str(angle).split(":"))
    exif_angle = f'{abs(degrees):.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return degrees < 0, exif_angle

def takeapic(camera, image):
    """use the camera to take some pics"""
    adorablespacestation.compute() # Get the lat/long values from ephem

    # change the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = changeandconvert(adorablespacestation.sublat)
    west, exif_longitude = changeandconvert(adorablespacestation.sublong)

    # make sure the EXIF tags specify the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # get an image
    camera.capture(image)


# begin the CSV file
data_file = dir_path/"data.csv"
csvmaker(data_file)
# begin the photo counter
photo_counter = 1
# record both the start plus the current time
start_time = datetime.now()
now_time = datetime.now()
# do a loop for so many (3) hours
while (now_time < start_time + timedelta(minutes=178)):
    try:
        humidity = round(sh.humidity, 4)
        temperature = round(sh.temperature, 4)
        # acquire latitude and longitude
        latitude, longitude = latandlonggetter()
        # Save data on file
        data = (
            datetime.now(),
            photo_counter,
            humidity,
            temperature,
            latitude,
            longitude
        )
        csvdataadder(data_file, data)
        # get an image
        image_file = f"{dir_path}/photo_{photo_counter:03d}.jpg"
        takeapic(cam, image_file)
        logger.info(f"iteration {photo_counter}")
        photo_counter += 1
        sleep(30)
        # change the time
        now_time = datetime.now()
    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__, e))

      #our message to space:
        print "cancel the leaving cert :)"
