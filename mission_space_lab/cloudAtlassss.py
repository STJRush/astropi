#Cloud Atlas -- Daniel and Jordan
from logzero import logger, logfile
#from sense_hat import SenseHat
from ephem import readtle, degree
#from picamera import PiCamera
from datetime import datetime, timedelta
from time import sleep
#import random
from pathlib import Path
import csv

dir_path = Path(__file__).parent.resolve()

# Sets a name for our 'Cloud Atlas'
logfile(dir_path/"cloud-atlas.log")

# I am here!
name = "ISS (ZARYA)"

line1 = "1 25544U 98067A   21039.89161926 -.00000043  00000-0  73771-5 0  9995"

line2 = "2 25544  51.6440 257.2891 0002486 351.4127  16.5936 15.48938694268710"

iss = readtle(name, line1, line2)

# Mum, get the camera 
photocapture= PiCamera()
photocapture.resolution = (1296, 972)

def filecreate(space_scrolls):
    """Create a new datasheet for the details,  and add the first part, the header row"""
    with open(space_scrolls, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time")
        writer.writerow(header)

def add_csv_data(space_scrolls, data):
    """Add a row of data to the data_file CSV"""
    with open(space_scrolls, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
        
def get_latlon():
    """Return our location, through Latiude-Longitude format, in Degrees"""
    iss.compute() # Get the lat/long values from ephem
    return (iss.sublat / degree, iss.sublong / degree)

def convert(angle):
    """
    Converts an angle. with complex telemtry data and mathematics! 
    """
    degrees, minutes, seconds = (float(field) for field in str(angle).split(":"))
    exif_angle = f'{abs(degrees):.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return degrees < 0, exif_angle

def capture(camera, image):
    """Use our camera to snap a picture of the Earth, with our location included"""
    iss.compute() # Get the lat/long values from ephem

    # convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(iss.sublat)
    west, exif_longitude = convert(iss.sublong)

    # set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # capture the image
    camera.capture(image)


# initialise the CSV file
space_scrolls = dir_path/"data.csv"
filecreate(space_scrolls)
# initialise the photo counter
photo_counter = 1
# record the start and current time
start_time = datetime.now()
now_time = datetime.now()
# run a loop for (almost) three hours
while (now_time < start_time + timedelta(minutes=178)):
    try:
        # get latitude and longitude
        latitude, longitude = get_latlon()
        # Save the data to the file
        data = (
            datetime.now(),
            photo_counter,
            latitude,
            longitude
        )
        add_csv_data(space_scrolls, data)
        # capture image
        our_pic = f"{dir_path}/photo_{photo_counter:03d}.jpg"
        capture(photocapture, our_pic)
        logger.info(f"iteration {photo_counter}")
        photo_counter += 1
        sleep(30)
        # update the current time, right now!!
        now_time = datetime.now()
    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__, e))
