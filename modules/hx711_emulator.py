#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
## An HX711 emulator to test code on other platform than the Raspberry Pi or if no load cell connected.

Author: Wilfried Grousson
Created Date: 2023/01/13
------------------------------------
MIT License

Copyright (c) 2023 WG

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import time
import random
import math
import threading

class HX711:
    def __init__(self,
                 dout_pin,
                 pd_sck_pin,
                 gain=128):

        self.PD_SCK = pd_sck_pin
        self.DOUT = dout_pin

        # Last time we've been read.
        self.lastReadTime = time.time()
        self.sampleRateHz = 80.0
        self.resetTimeStamp = time.time()
        self.sampleCount = 0
        self.simulateTare = True

        # Mutex for reading from the HX711, in case multiple threads in client
        # software try to access get values from the class at the same time.
        self.readLock = threading.Lock()
        
        self.GAIN = 0
        self.REFERENCE_UNIT = 1  # The value returned by the hx711 that corresponds to your reference unit AFTER dividing by the SCALE.
        
        self.OFFSET = 1
        self.lastVal = int(0)

        self.DEBUG_PRINTING = False
        
        self.byte_format = 'MSB'
        self.bit_format = 'MSB'

        self.set_gain(gain)




        # Think about whether this is necessary.
        time.sleep(1)

    def convertToTwosComplement24bit(self, inputValue):
       # HX711 has saturating logic.
       if inputValue >= 0x7fffff:
          return 0x7fffff

       # If it's a positive value, just return it, masked with our max value.
       if inputValue >= 0:
          return inputValue & 0x7fffff

       if inputValue < 0:
          # HX711 has saturating logic.
          if inputValue < -0x800000:
             inputValue = -0x800000

          diff = inputValue + 0x800000

          return 0x800000 + diff

        
    def convertFromTwosComplement24bit(self, inputValue):
        return -(inputValue & 0x800000) + (inputValue & 0x7fffff)

    
    def is_ready(self):
        # Calculate how long we should be waiting between samples, given the
        # sample rate.
        sampleDelaySeconds = 1.0 / self.sampleRateHz

        return time.time() >= self.lastReadTime + sampleDelaySeconds

    
    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        # Read out a set of raw bytes and throw it away.
        self.readRawBytes()

        
    def get_gain(self):
        if self.GAIN == 1:
            return 128
        if self.GAIN == 3:
            return 64
        if self.GAIN == 2:
            return 32

        # Shouldn't get here.
        return 0
        

    def readRawBytes(self):
        # Wait for and get the Read Lock, incase another thread is already
        # driving the virtual HX711 serial interface.
        self.readLock.acquire()

        # Wait until HX711 is ready for us to read a sample.
        while not self.is_ready():
           pass

        self.lastReadTime = time.time()

        # Generate a 24bit 2s complement sample for the virtual HX711.
        rawSample = self.convertToTwosComplement24bit(self.generateFakeSample())
        
        # Read three bytes of data from the HX711.
        firstByte  = (rawSample >> 16) & 0xFF
        secondByte = (rawSample >> 8)  & 0xFF
        thirdByte  = rawSample & 0xFF

        # Release the Read Lock, now that we've finished driving the virtual HX711
        # serial interface.
        self.readLock.release()           

        # Depending on how we're configured, return an orderd list of raw byte
        # values.
        if self.byte_format == 'LSB':
           return [thirdByte, secondByte, firstByte]
        else:
           return [firstByte, secondByte, thirdByte]


    def read_long(self):
        # Get a sample from the HX711 in the form of raw bytes.
        dataBytes = self.readRawBytes()


        if self.DEBUG_PRINTING:
            print(dataBytes,)
        
        # Join the raw bytes into a single 24bit 2s complement value.
        twosComplementValue = ((dataBytes[0] << 16) |
                               (dataBytes[1] << 8)  |
                               dataBytes[2])

        if self.DEBUG_PRINTING:
            print("Twos: 0x%06x" % twosComplementValue)
        
        # Convert from 24bit twos-complement to a signed value.
        signedIntValue = self.convertFromTwosComplement24bit(twosComplementValue)

        # Record the latest sample value we've read.
        self.lastVal = signedIntValue

        # Return the sample value we've read from the HX711.
        return int(signedIntValue)

    
    def get_raw_data_mean(self, times=3):
        # Make sure we've been asked to take a rational amount of samples.
        if times <= 0:
            print("HX711().get_raw_data_mean(): times must >= 1!!  Assuming value of 1.")
            times = 1

        # If we're only average across one value, just read it and return it.
        if times == 1:
            return self.read_long()

        # If we're averaging across a low amount of values, just take an
        # arithmetic mean.
        if times < 5:
            values = int(0)
            for i in range(times):
                values += self.read_long()

            return values / times

        # If we're taking a lot of samples, we'll collect them in a list, remove
        # the outliers, then take the mean of the remaining set.
        valueList = []

        for x in range(times):
            valueList += [self.read_long()]

        valueList.sort()

        # We'll be trimming 20% of outlier samples from top and bottom of collected set.
        trimAmount = int(len(valueList) * 0.2)

        # Trim the edge case values.
        valueList = valueList[trimAmount:-trimAmount]

        # Return the mean of remaining samples.
        return sum(valueList) / len(valueList)

    
    def get_data_mean(self, readings=30):
        return self.get_raw_data_mean(readings) - self.OFFSET

    
    def get_weight_mean(self, readings=30):
        value = self.get_data_mean(readings)
        value = value / (self.REFERENCE_UNIT * 100)
        return value

    
    def zero(self, readings=30):
        # If we aren't simulating Taring because it takes too long, just skip it.
        if not self.simulateTare:
            return False

        # Backup REFERENCE_UNIT value
        reference_unit = self.REFERENCE_UNIT
        self.set_scale_ratio(1)

        value = self.get_raw_data_mean(readings)

        if self.DEBUG_PRINTING:
            print("Tare value:", value)
        
        self.set_offset(value)

        # Restore the reference unit, now that we've got our offset.
        self.set_scale_ratio(reference_unit)
        # wait for the sensor to stabilize
        time.sleep(1)
        return False

    
    def set_reading_format(self, byte_format="LSB", bit_format="MSB"):

        if byte_format == "LSB":
            self.byte_format = byte_format
        elif byte_format == "MSB":
            self.byte_format = byte_format
        else:
            print("Unrecognised byte_format: \"%s\"" % byte_format)

        if bit_format == "LSB":
            self.bit_format = bit_format
        elif bit_format == "MSB":
            self.bit_format = bit_format
        else:
            print("Unrecognised bit_format: \"%s\"" % bit_format)

            

    def set_offset(self, offset):
        self.OFFSET = offset

        
    def get_offset(self):
        return self.OFFSET

    
    def set_scale_ratio(self, scale_ratio, channel='', gain_A=0):
        # Make sure we aren't asked to use an invalid reference unit.
        if scale_ratio == 0:
            print("HX711().set_reference_unit(): Can't use 0 as a reference unit!!")
            return

        self.REFERENCE_UNIT = scale_ratio


    def power_down(self):
        # Wait for and get the Read Lock, incase another thread is already
        # driving the HX711 serial interface.
        self.readLock.acquire()

        # Wait 100us for the virtual HX711 to power down.
        time.sleep(0.0001)

        # Release the Read Lock, now that we've finished driving the HX711
        # serial interface.
        self.readLock.release()           


    def power_up(self):
        # Wait for and get the Read Lock, incase another thread is already
        # driving the HX711 serial interface.
        self.readLock.acquire()

        # Wait 100 us for the virtual HX711 to power back up.
        time.sleep(0.0001)

        # Release the Read Lock, now that we've finished driving the HX711
        # serial interface.
        self.readLock.release()

        # HX711 will now be defaulted to Channel A with gain of 128.  If this
        # isn't what client software has requested from us, take a sample and
        # throw it away, so that next sample from the HX711 will be from the
        # correct channel/gain.
        if self.get_gain() != 128:
            self.readRawBytes()


    def reset(self):
        # self.power_down()
        # self.power_up()

        # Mark time when we were reset.  We'll use this for sample generation.
        self.resetTimeStamp = time.time()


    def generateFakeSample(self):
       sampleTimeStamp = time.time() - self.resetTimeStamp

       noiseScale = 1.0
       noiseValue = random.randrange(-(noiseScale * 1000),(noiseScale * 1000)) / 1000.0
       sample     = math.sin(math.radians(sampleTimeStamp * 20)) * 72.0

       self.sampleCount += 1

       if sample < 0.0:
          sample = -sample

       sample += noiseValue

       BIG_ERROR_SAMPLE_FREQUENCY = 142
       ###BIG_ERROR_SAMPLE_FREQUENCY = 15
       BIG_ERROR_SAMPLES = [0.0, 40.0, 70.0, 150.0, 280.0, 580.0]

       if random.randrange(0, BIG_ERROR_SAMPLE_FREQUENCY) == 0:
          sample = random.sample(BIG_ERROR_SAMPLES, 1)[0]
          print("Sample %d: Injecting %f as a random bad sample." % (self.sampleCount, sample))

       sample *= 1000

       sample *= self.REFERENCE_UNIT

       return int(sample)


# EOF - emulated_hx711.py
