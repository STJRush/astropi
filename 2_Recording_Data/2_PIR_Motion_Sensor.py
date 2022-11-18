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

"""
    Raspberry Pi
    
    Wiring Diagram
   ____________________
   !      |____|    o+ !     + = 5V
   !      sd card   oo !     - = GND
   !                o- ! 
   !                4o !     4 = GPIO 4
   !                oo !     
   !____            oo !
   !HDMI            oo !
   !PORT            oo !
   !____            oo !
   !                oo !
   !                oo !
   !                oo !
   !_____  _____  _____!
   ! eth    usb    usb !
   !_____  _____  _____!
   
   
   

                         .___.              
                  +3V3---|O O|---+5V
          (SDA)  GPIO2---|O O|---+5V
         (SCL1)  GPIO3---|O O|---_
    (GPIO_GLCK)  GPIO4---|O O|------GPIO14 (TXD0)
                      _--|O.O|------GPIO15 (RXD0)
    (GPIO_GEN0) GPIO17---|O O|------GPIO18 (GPIO_GEN1)
    (GPIO_GEN2) GPIO27---|O O|---_
    (GPIO_GEN3) GPIO22---|O O|------GPIO23 (GPIO_GEN4)
                  +3V3---|O O|------GPIO24 (GPIO_GEN5)
     (SPI_MOSI) GPIO10---|O.O|---_
     (SPI_MISO) GPIO9 ---|O O|------GPIO25 (GPIO_GEN6)
     (SPI_SCLK) GPIO11---|O O|------GPIO8  (SPI_C0_N)
                      _--|O O|------GPIO7  (SPI_C1_N)
       (EEPROM) ID_SD----|O O|------ID_SC Reserved for ID EEPROM
                GPIO5----|O.O|---_
                GPIO6----|O O|------GPIO12
                GPIO13---|O O|---_
                GPIO19---|O O|------GPIO16
                GPIO26---|O O|------GPIO20
                      _--|O O|------GPIO21
                           '---'
                       40W 0.1" PIN HDR

   
   
   """
