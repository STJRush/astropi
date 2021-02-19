# EpicSpaceCoders are Jessica, Liam, Morgan and Luke
# We're looking at deforistation over time

from logzero import logger, logfile
from ephem import readtle, degree
from picamera import PiCamera
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path
import csv


print("E P I C  S P A C E  C O D E R S")
print("Missions started!")


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
#picturetaker.resolution = (1296, 972)

def csvmaker(fileofdata):
    """make the new csv"""
    with open(fileofdata, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Lat", "Long", "PhotoNumber")
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

def takeapic(picturetaker, image):
    """use the camera to take some pics"""
    adorablespacestation.compute() # Get the lat/long values from ephem
    # get an image
    picturetaker.capture(image)


# begin the CSV file
data_file = dir_path/"data.csv"
csvmaker(data_file)
# begin the photo counter
photoAndDataCounter = 1
# record both the start plus the current time
start_time = datetime.now()
now_time = datetime.now()
# do a loop for so many (3) hours



while (now_time < start_time + timedelta(minutes=1)):
    try:
               
        
        # Report on % completeness
        
        
        # from testing this out on flight OS
        # Don't worry, the program will still end after 3 hours, even if it doesn't get to 100% on the progress indicator
        expected_Iteraions = 30 

        
        percent_complete = round((photoAndDataCounter/expected_Iteraions)*100,1) # calculates current completion % 
        
        
        #only report on progress every 5th data point to reduce text 
        if photoAndDataCounter % 5 == 0:
        
        
            print("We've got", percent_complete,"% of what we were hoping for ") # prints it over the last line

            if percent_complete > 100:
                print("Everything now is a bonus")
            elif percent_complete > 200:
                print("That's more than double what we need but hey... not complaining...")

        

        # acquire latitude and longitude
        latitude, longitude = latandlonggetter()
        
        # Save data on file
        data = (
            datetime.now(),
            latitude,
            longitude,
            photoAndDataCounter
        )
        
        # put things in csv file
        csvdataadder(data_file, data)
        
        # get an image
        image_file = f"{dir_path}/photo_{photoAndDataCounter:03d}.jpg"
        takeapic(picturetaker, image_file)
        
        #report on any problems
        logger.info(f" Looking good! We're on iteration {photoAndDataCounter}")
        
        # count them photos
        photoAndDataCounter += 1
        
        sleep(2)
        
        # change the time to the current time
        now_time = datetime.now()
        

    except Exception as e: # in case we get hit by cosmic rays
        logger.error('{}: {})'.format(e.__class__.__name__, e))


print("Program complete")

#our message to space:
print("Cancel the leaving cert :) ")


