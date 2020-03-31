import random
import time
import threading

class Customer():

    def __init__(self, name, haircutTime, silent):
        self.name = name
        self.haircutTime = random.randint(1, haircutTime)
        self.hadHaircut = False
        self.barber = ""
        self.haircutStart = ""
        self.haircutEnd = ""
        self.timeEntered = ""
        self.timeEnteredWaitingRoom = ""
        self.timeLeft = ""
        self.silent = silent

    def __str__(self):
        if self.hadHaircut:
            activity = ("Name: " + str(self.name) + "\n" + "Time entered the barber shop at: " +
            self.timeEntered + "\n" + "Time Entered waiting room: " + self.timeEnteredWaitingRoom +
            "\n" + "Barber: " + self.barber + "\n" + "Haircut started at: " + self.haircutStart +
            "\n" + "Haircut finished getting cut at: " + self.haircutEnd + "\n"
             + "Haircut time: " + str(self.haircutTime) + "\n\n")
        else:
            activity = ("Name: " + str(self.name) + "\n" + "Time entered the barber shop at: " +
            self.timeEntered + "\n" + "Time left: " + self.timeLeft + "\n\n")
        return activity


class Barber():

    def __init__(self, name, silent):
        self.name = name
        # create an event object for this thread so that other threads can communicate with it
        self.event = threading.Event()
        # string variable to record barber events
        self.activity = "Barber {} started work at: {}\n".format(self.name, time.ctime())
        self.silent = silent
        if self.silent: print(self.activity.strip())

    # method used to make a barber thread wait
    def sleep(self):
        # set the event flag to false
        self.event.clear()
        sleepInfo = "Barber {} has gone to sleep at: {}".format(self.name, time.ctime())
        self.activity += sleepInfo + "\n"
        if self.silent: print(sleepInfo)
        # pause the thread while the flag is false
        self.event.wait()

    # overloaded method to allow a barber to be woke by a customer or the barber shop closing
    def wakeUp(self, customer=None):
        if customer is not None:
            wakeInfo = "Barber {} has been woke up by {} at {}".format(self.name, customer.name, time.ctime())
            self.activity += wakeInfo + "\n"
            if self.silent: print(wakeInfo)
            # set the event flag to true so that the thread may resume activity
            self.event.set()
        else:
            wakeInfo = "Barber {} has woken up for the end of the day at {}".format(self.name, time.ctime())
            self.activity += wakeInfo
            if self.silent: print(wakeInfo)
            # set the event flag to true so that the thread may resume activity
            self.event.set()

    def isAwake(self):
        # check to see if the flag of this event is set to true or false
        return self.event.is_set()

    def cutHair(self, customer):
        # record what barber cut the customers hair
        customer.barber = self.name
        customer.hadHaircut = True
        # record while the customer started getting their hair cut
        customer.haircutStart = time.ctime()

        haircutStartInfo = "Barber {} has started cutting {}'s hair at: {}".format(self.name, customer.name, customer.haircutStart)
        self.activity += haircutStartInfo + "\n"
        if self.silent: print(haircutStartInfo)

        # wait while the barber cuts the customers hair
        time.sleep(customer.haircutTime)
        # record what time the barber finished cutting the customers hair
        customer.haircutEnd = time.ctime()

        haircutEndInfo = "Barber {} has finished cutting {}'s hair at: {}".format(self.name, customer.name, customer.haircutEnd)
        self.activity += haircutEndInfo + "\n"
        if self.silent: print(haircutEndInfo)

    def __str__(self):
        return self.activity