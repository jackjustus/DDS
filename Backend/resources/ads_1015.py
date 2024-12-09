# ADS 1015 class for Terrier Motorsport's DDS
    # Code by Jackson Justus (jackjust@bu.edu)
from interface import I2CDevice, InterfaceProtocol, Interface
from .data_logger import File
import smbus2
from typing import List
import time
from ads1015 import ADS1015 # This is a helper package. This class cusomizes it functionality.
from analog_in import Analog_In


class ADS_1015(I2CDevice):
    """
    Adafruit Analog -> Digital Converter on an I2C interface with caching functionality.
    """

    # This list represensts the four channels that correspond to the four on the physical ADC pins
    inputs : List[Analog_In]

    # ===== CONSTANTS FOR DATA DECODING =====

    CHANNELS = ["in0/ref", "in1/ref", "in2/ref", "in3/ref"]

    # ===== METHODS =====

    def __init__(self, name: str, logFile: File, i2c_bus: smbus2.SMBus, inputs : List[Analog_In]):

        # Initialize super class (I2CDevice)
        super().__init__(name, logFile=logFile, i2c_address=0x00)   # i2c address isn't used, so I put 0

        # Init I2C bus
        self.bus = i2c_bus
        self.last_retrieval_time = time.time()  # Time of the last successful data retrieval

        # Init ADC Device
        self._init_ads()
        
        # Init virtual analog inputs
        self.inputs = inputs


    def update(self):
        """
        Retrieve data from the sensor, log it, and cache it.
        """

        # Fetch the sensor data
        voltages = self._fetch_sensor_data()

        # Store it in the virtual inputs
        for input, voltage in zip(self.inputs, voltages):
            input.voltage = voltage


        # Check to see if there is null data. If there is, it means that there are no messages to be recieved.
        # Thus, we can end the update poll early.
        if any(value is None for value in voltages):

            # If no new values are discovered, we check to see if the cache has expired.
            self._update_cache_timeout()
            return
        

        for input in self.inputs: 
            # Update cache with new data
            self.cached_values[input.name] = input.voltage

            # Log the data
            self.log_data(input.name, input.voltage)

        # Reset the timeout timer
        self.reset_last_retrival_timer() 
            

    def get_data(self, key: str):
        """
        Retrieve the most recent data associated with the key from the cache.
        To be called by some higher power, not by the class itself.
        """

        if key in self.cached_values:
            return self.cached_values[key]
        else:
            print(f"No cached data found for key: {key}")
            return None


    def close_connection(self):
        """
        Closing I2C connection if needed.
        """

        # Close the i2c connection.
        self.bus.close()


    def _fetch_sensor_data(self) -> List[float]:
        """
        Internal method to encapsulate sensor read logic
        """

        voltages = []

        # For every channel on the ADC...
        for channel, input in zip(self.CHANNELS, self.inputs):

            # Get the voltage input
            voltage = self.ads.get_compensated_voltage(
                channel=channel, reference_voltage=self.reference
            )

            # Set the voltage of the analog_in object
            input.voltage = voltage

            voltages.append(voltage)

            print("{}: {:6.3f}v".format(channel, voltage))
        
        return voltages
    

    def _init_ads(self):
        # Make ADS object
        self.ads = ADS1015()

        # Double check chip type (debug)
        self.chip_type = self.ads.detect_chip_type()
        print("Found: {}".format(self.chip_type))

        # Configure ADS
        self.ads.set_mode("single")
        self.ads.set_programmable_gain(2.048)
        self.ads.set_sample_rate(1600)

        # Get reference voltage
        self.reference = self.ads.get_reference_voltage()
        print(f"Reference: {self.reference}")
    

    # ===== Super Function Calls =====


    def _update_cache_timeout(self):
        return super()._update_cache_timeout()


    def log_data(self, param_name, value):
        return super().log_data(param_name, value)
    

    def reset_last_retrival_timer():
        return super().reset_last_retrival_timer()
    

# Example usage
DEBUG_ENABLED = False

if DEBUG_ENABLED:
    
    pass