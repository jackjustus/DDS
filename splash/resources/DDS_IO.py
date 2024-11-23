# Signal Input/Output for Terrier Motorsport's DDS
    # Code by Jackson Justus (jackjust@bu.edu)

from input import Input, SensorProtocol

"""
The purpose of this class is to handle all the low level data that the DDS Needs
There is functions for the higher level systems to pull data from various sources.
EX. The UI calls functions from here which pulls data from sensor objects.
"""

class DDS_IO:

    

    def __init__(self):
        
        pass

    def define_sensors(self):

        accelerometer = Input(SensorProtocol.SPI)

        self.sensors.append()



