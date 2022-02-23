
# we are looking out for any sort of rivers, lakes, or any body of water doesnt matter how big or small it is.

# we go by the name of the BTRfanclub (short for Big Time Rush Fan Club)
# we got Eoghan Brennan as Kendall Schmidt, Amy Roche as Logan Henderson, Lucas Price as James Maslow, Rory McBride as Carlos PenaVega and Dominic kelly as the assistant manager. 
# big thanks to our manager Danny Murray who helped us with this.
#    ____ _______ _____     __                   _       _     
#   |  _ \__   __|  __ \   / _|                 | |     | |    
#   | |_) | | |  | |__) | | |_ __ _ _ __     ___| |_   _| |__  
#   |  _ <  | |  |  _  /  |  _/ _` | '_ \   / __| | | | | '_ \ 
#   | |_) | | |  | | \ \  | || (_| | | | | | (__| | |_| | |_) |
#   |____/  |_|  |_|  \_\ |_| \__,_|_| |_|  \___|_|\__,_|_.__/ 


# if you havent noticed we are big fans of the band Big Time Rush i suggest some of their songs.



from pathlib import Path
from logzero import logger, logfile
from sense_hat import SenseHat
from picamera import PiCamera
from orbit import ISS
from time import sleep
from datetime import datetime, timedelta
import csv
"""our programe is going to take """
def make_big_csv(info_file):
    """make a spread sheet for the data in the future"""
    with open(info_file, 'w') as f:
        writer = csv.writer(f)
        header = ("number_count", "Date/time", "Latitude", "Longitude", "Temperature", "Humidity")
        writer.writerow(header)

def data_goes_into_csv(info_file, data):
    """insert the data into the info_file CSV"""
    with open(info_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def convert(angle):
    """convert the angle"""
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def capture(camera, image):
    """Use `camera` to capture with lat/long EXIF data."""
    location = ISS.coordinates()

    south, exif_latitude = convert(location.latitude)
    west, exif_longitude = convert(location.longitude)
    
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

   
    camera.capture(image)
   

base_folder = Path(__file__).parent.resolve()


logfile(base_folder/"events.diary")


sense = SenseHat()


cam = PiCamera()
cam.resolution = (1296, 972)


info_file = base_folder/"data.csv"
make_big_csv(info_file)


number_count = 1

start_time = datetime.now()
now_time = datetime.now()

while (now_time < start_time + timedelta(minutes=178)):
    try:
        humidity = round(sense.humidity, 4)
        temperature = round(sense.temperature, 4)
        
        location = ISS.coordinates()
        
        data = (
            number_count,
            datetime.now(),
            location.latitude.degrees,
            location.longitude.degrees,
            temperature,
            humidity,
        )
        data_goes_into_csv(info_file, data)
       
        image_file = f"{base_folder}/photo_{number_count:03d}.jpg"
        capture(cam, image_file)
      
        logger.info(f"iteration {number_count}")
        number_count += 1
        sleep(60)
        
        now_time = datetime.now()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}')
        
# thanks for listening to our story of love and joy to our favorite band Big Time Rush

# Our messages to our parents cause who has the chance to have a message to someone from space.

# Eoghan's message to his family, space is cool you should come up here some time the view is nice.

# Lucas's message to his family, here your name might be in space, thank you for raising me, much appreciated.

# Amy's message,
#Hello! Thanks for everything. This message is in space now, which is quite cool. :)

# Rory's message:
#Thank you for bringing me into this life. This message is now up in Space which is extremely cool. Thank you again for everything.
    

