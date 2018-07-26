import Adafruit_BBIO.GPIO as GPIO
from time import sleep

  #  Four Digit Numeric Display
class FDND(object):
    def __init__(self, segments_pins, digit_pins, delay=0.01):
        segments_n = 8
        if len(segments_pins) != segments_n:
            print("Wrong number of segment pins! "
                  "Must be {}, got {} instead!".format(segments_n, len(segments_pins)))
            exit(1)

        digit_n = 4
        if len(digit_pins) != digit_n:
            print("Wrong number of digit pins! "
                  "Must be {}, got {} instead!".format(digit_n, len(digit_pins)))
            exit(1)

        segments = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'point']
        self.segments_pins = {segments[i]: [segments_pins[i], False] for i in range(len(segments_pins))}
        for segment_pin in self.segments_pins:
            GPIO.setup(self.segments_pins[segment_pin][0], GPIO.OUT)
            GPIO.setup(self.segments_pins[segment_pin][0], GPIO.LOW)


        digit = [1, 2, 3, 4]
        self.digit_pins = {digit[i]: digit_pins[i] for i in range(len(digit_pins))}
        for digit_pin in self.digit_pins:
            GPIO.setup(self.digit_pins[digit_pin], GPIO.OUT)
            GPIO.output(self.digit_pins[digit_pin], GPIO.LOW)

        numbers = {'0': "abcdef",
                   '1': "bc",
                   '2': "abged",
                   '3': "abgcd",
                   '4': "fgbc",
                   '5': "afgcd",
                   '6': "afgcde",
                   '7': "abc",
                   '8': "abcdefg",
                   '9': "abcdfg"}

        self.numbers = {n: {"low": numbers[n], "high": [c for c in "abcdefg" if c not in numbers[n]]} for n in numbers}

        self.delay = delay  # delay before swapping to a next digit

    def __del__(self):
        GPIO.cleanup()

    def lightUp(self, digit, number):
        GPIO.output(self.digit_pins[digit], GPIO.HIGH)
        for segment in "abcdefg":
            if segment in self.numbers[number] and not self.segments_pins[segment][1]:  # if segment must be lighted and has low level
                GPIO.output(self.segments_pins[segment][0], GPIO.LOW)
                self.segments_pins[segment][1] = True
            elif segment not in self.numbers[number] and self.segments_pins[segment][1]:  # if segment mustn't be lighted and has high level
                GPIO.output(self.segments_pins[segment][0], GPIO.HIGH)
                self.segments_pins[segment][1] = False
        sleep(self.delay)
        GPIO.output(self.digit_pins[digit], GPIO.LOW)

    def setNumber(self, number):
        if type(number) is int:
            if len(str(int)) > 4:
                print("Cannot show more than 9999")
            elif number > 0:
                numbers = list(str(number))
                for i in range(len(numbers) - 1, - 1, -1):
                    self.lightUp(4 - i, numbers[i])
            else:
                print("x < 0, haven't finished this part of the code yet")


if __name__ == "__main__":
    segments_pins = ["P8_7", "P8_8", "P8_9", "P8_10", "P8_11", "P8_12", "P8_15", "P8_16"]
    digit_pins = ["P9_15", "P9_23", "P9_25", "P9_27"]
    display = FDND(segments_pins, digit_pins)

    x = 0

    while x < 9999:
        for i in range(100):
            display.setNumber(x)
        x += 1

    print("Finish!")

