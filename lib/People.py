import random
import time
import threading

class Customer():

    def __init__(self, name):
        self.name = name
        self.haircutTime = random.randint(1, 12)
        self.hadHaircut = False
        self.barber = ""
        self.haircutStart = ""
        self.haircutEnd = ""
        self.timeEntered = ""
        self.timeEnteredWaitingRoom = ""
        self.timeLeft = ""

    def __str__(self):
        if self.hadHaircut:
            out = ("Name: " + str(self.name) + "\n" + "Time entered the barber shop at: " +
            self.timeEntered + "\n" + "Time Entered waiting room: " + self.timeEnteredWaitingRoom +
            "\n" + "Barber: " + self.barber + "\n" + "Haircut started at: " + self.haircutStart +
            "\n" + "Haircut finished getting cut at: " + self.haircutEnd + "\n"
             + "Haircut time: " + str(self.haircutTime) + "\n\n")
        else:
            out = ("Name: " + str(self.name) + "\n" + "Time entered the barber shop at: " +
            self.timeEntered + "\n" + "Time left: " + self.timeLeft + "\n\n")
        return out


class Barber():

    def __init__(self, name):
        self.name = name
        self.event = threading.Event()
        self.activity = "Barber {} started work at: {}\n".format(self.name, time.ctime())
        print(self.activity.strip())

    def sleep(self):
        self.event.clear()
        sleepInfo = "Barber {} has gone to sleep at: {}".format(self.name, time.ctime())
        self.activity += sleepInfo + "\n"
        print(sleepInfo)
        self.event.wait()

    def wakeUp(self, customer=None):
        if customer is not None:
            wakeInfo = "Barber {} has been woke up by {} at {}".format(self.name, customer.name, time.ctime())
            self.activity += wakeInfo + "\n"
            print(wakeInfo)
            self.event.set()
        else:
            wakeInfo = "Barber {} has woken up for the end of the day at {}".format(self.name, time.ctime())
            self.activity += wakeInfo
            print()
            self.event.set()

    def isAwake(self):
        return self.event.is_set()

    def cutHair(self, customer):
        customer.barber = self.name
        customer.hadHaircut = True
        customer.haircutStart = time.ctime()

        haircutStartInfo = "Barber {} has started cutting {}'s hair at: {}".format(self.name, customer.name, customer.haircutStart)
        self.activity += haircutStartInfo + "\n"
        print(haircutStartInfo)

        time.sleep(customer.haircutTime)
        customer.haircutEnd = time.ctime()

        haircutEndInfo = "Barber {} has finished cutting {}'s hair at: {}".format(self.name, customer.name, customer.haircutEnd)
        self.activity += haircutEndInfo + "\n"
        print(haircutEndInfo)

    def __str__(self):
        return self.activity