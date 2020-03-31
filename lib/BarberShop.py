import queue
import time
import threading
from lib.People import Barber

class BarberShop():

    def __init__(self, numberOfBarbers, waitingRoomCapacity, silent):
        self.names = ["Bob", "Billy", "Carl", "Ben", "Bernie", "John", "Peter", "Odin", "Zuse", "Tom"]
        self.barbers = []
        self.numberOfBarbers = numberOfBarbers
        self.isOpen = True
        self.capacity = waitingRoomCapacity
        self.waitingRoom = queue.Queue()
        # semaphore to indicate how many threads(Barbers) are avaiable
        self.availableBarbers = self.numberOfBarbers
        # lock used to allow only one thread to write to a file at one time
        self.writeLock = threading.Lock()
        # lock used to allow only one thread to access shared variables at one time
        self.accessLock = threading.Lock()
        self.silent = silent

    # for every thread created associate a Barber object with it to control the thread
    # the thread will continue to work while the Barber shop is open
    def startDay(self):
        barber = Barber(threading.current_thread().getName(), self.silent)
        self.barbers.append(barber)

        while self.isOpen:
            if self.waitingRoom.empty():
                barber.sleep()
            else:
                # after serving a customer and waiting room not empty
                # get the next customer and cut their hair
                self.availableBarbers -= 1
                customer = self.waitingRoom.get()
                if self.accessLock.locked():
                    self.accessLock.release()
                barber.cutHair(customer)
                # create a thread to write to a file while the barber continues to work
                # write a record of the customers events
                threading.Thread(target=self.customerInfo, args=(customer,)).start()
                self.availableBarbers += 1

        # write a record of the barbers events to a file
        self.writeLock.acquire()
        with open("./logs/BarberInfo.txt", "a") as f:
            f.write(str(barber) + "\n\n")
        self.writeLock.release()

    # create a thread for the amount number of barbers input
    # set them to work on the startDay method
    def open(self):
        # 10 barber names are given. Will resort to numbers if more than that is asked
        for i in range(self.numberOfBarbers):
            if i < len(self.names):
                name = self.names[i]
            else:
                name = "Barber " + str(i + 1)
            threading.Thread(target=self.startDay, name=name).start()

    # when every customer has entered the Barber shop close it
    def close(self):
        #wait until no more customers are in the waiting room 
        while self.waitingRoom.qsize() > 0:
            pass
        self.isOpen = False
        # if any barber thread is asleep then wake them up so they can terminate
        for barber in self.barbers:
            if not barber.isAwake():
                barber.wakeUp()
        if self.silent: print("Barber shop is closing at: {}".format(time.ctime()))

    # for every customer object created they are entered into the barber shop using NewCustomer method
    def newCustomer(self, customer):
        # if no other customer in the waiting room and a barber is available wake a barber
        # to cut the customers hair
        if self.waitingRoom.qsize() == 0 and self.availableBarbers > 0:
            # loop through each barber and find one that is not busy
            # a barber will be asleep based on the condition above
            for barber in self.barbers:
                if not barber.isAwake():
                    self.waitingRoom.put(customer)
                    # lock the asleep barber thread so that another barber cant service this customer
                    # while the barber wakes up
                    self.accessLock.acquire()
                    barber.wakeUp(customer)
                    break
        # if all barbers are busy and waiting room is not full customer enters the waiting room
        elif self.waitingRoom.qsize() < self.capacity:
            # note what time the customer enters the waiting room
            customer.timeEnteredWaitingRoom = time.ctime()
            if self.silent: print("Customer {} waits in the waiting room at: {}".format(customer.name, customer.timeEnteredWaitingRoom))
            self.waitingRoom.put(customer)
        # if all barbers are busy and waiting room is full the customer leaves
        else:
            customer.timeLeft = time.ctime()
            if self.silent: print("Customer {} leaving at: {}".format(customer.name, customer.timeLeft))
            # this customer has no more events so write its record to a file
            threading.Thread(target=self.customerInfo, args=(customer,)).start()

    # function to write customer events to a file
    def customerInfo(self, customer):
        self.writeLock.acquire()
        with open("./logs/CustomerInfo.txt", "a") as f:
            f.write(str(customer))
        self.writeLock.release()