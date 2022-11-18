# Tutorial at https://projects.raspberrypi.org/en/projects/physical-computing/11

from gpiozero import MotionSensor

pir = MotionSensor(12) # OUT plugged into GPIO12
                       # GND plugged into ground
                       # VCC plugged into 5V

while True:
    print("Continue scanning for humans...")
    pir.wait_for_motion()
    
    print("Moving human detected! Destroy human!")
    pir.wait_for_no_motion()
    
    print("Human deactivated...")

