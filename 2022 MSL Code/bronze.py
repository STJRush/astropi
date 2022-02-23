from pathlib import Path
from logzero import logger, logfile
from sense_hat import SenseHat
from picamera import PiCamera
from orbit import ISS
from time import sleep
from datetime import datetime, timedelta
import csv

'''
__________                                     
\______   \_______  ____   ____ ________ ____  
 |    |  _/\_  __ \/  _ \ /    \\___   // __ \ 
 |    |   \ |  | \(  <_> )   |  \/    /\  ___/ 
 |______  / |__|   \____/|___|  /_____ \\___  >
        \/                    \/      \/    \/ 
Team Bronze
Classifying cloud types using ML using data obtained from snapping the earth for 3 hours.
Abigail Bosch & Stephen Flynn
St Josephs Rush, Dublin, Ireland, Planet Earth, Milky Way Galaxy
2022

Well here it is, we made it to orbit before Bezos! We have a few things we'd like to say but thanks to Danny Murray for setting this up, legend.

Abigails Message:
But, Moon, and Star,
Though you're very far-,
There is one - farther than you-,
She - is more than a firmament - from Me -
So I can never go!
- Emily Dickisnon

Stephens Message:
Well better put something nice on this yoke,
Bridie, Rose, thank you!
Stephen was here.


"I serisously can't beat that wth...Like I made a Jeff Bezos joke and you did a poem lmao" - Stephens message to Abigail after comparing our messages.

'''

def make_the_csv_file(data_stored_directory):
    """Create a new CSV file and add the header row"""
    with open(data_stored_directory, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Latitude", "Longitude", "Temperature", "Humidity")
        writer.writerow(header)

def plus_data_from_csv(data_stored_directory, data):
    """Add a row of data to the data_stored_directory CSV"""
    with open(data_stored_directory, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def calculate_angle(angle):
    """
    calculate_angle a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the calculate_angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def take_picture(camera, image):
    """Use `camera` to take_picture an `image` file with lat/long EXIF data."""
    location = ISS.coordinates()

    # calculate_angle the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = calculate_angle(location.latitude)
    west, exif_longitude = calculate_angle(location.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # take_picture the image
    camera.take_picture(image)


base_folder = Path(__file__).parent.resolve()

# Set a logfile name
logfile(base_folder/"events.log")

# Set up Sense Hat
sense = SenseHat()

# Set up camera
cam = PiCamera()
cam.resolution = (1296, 972)

# Initialise the CSV file
data_stored_directory = base_folder/"data.csv"
make_the_csv_file(data_stored_directory)

# Initialise the photo counter
counter = 1
# Record the start and current time
begin_experiment = datetime.now()
current_time = datetime.now()
# Run a loop for (almost) three hours
while (current_time < begin_experiment + timedelta(minutes=178)):
    try:
        humidity = round(sense.humidity, 4)
        temperature = round(sense.temperature, 4)
        # Get coordinates of location on Earth below the ISS
        location = ISS.coordinates()
        # Save the data to the file
        data = (
            counter,
            datetime.now(),
            location.latitude.degrees,
            location.longitude.degrees,
            temperature,
            humidity,
        )
        plus_data_from_csv(data_stored_directory, data)
        # take_picture image
        image_file = f"{base_folder}/photo_{counter:03d}.jpg"
        take_picture(cam, image_file)
        # Log event
        logger.info(f"iteration {counter}")
        counter += 1
        sleep(30)
        # Update the current time
        current_time = datetime.now()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}')
