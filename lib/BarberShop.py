import queue
import time
import threading
from lib.People import Barber

class BarberShop():

    def __init__(self):
        self.names = ["Bob", "Billy", "Carl", "Ben", "Bernie"]
        self.barbers = []
        self.numberOfBarbers = 5
        self.isOpen = True
        self.capacity = 15
        self.waitingRoom = queue.Queue()
        self.availableBarbers = self.numberOfBarbers
        self.writeLock = threading.Lock()
        self.accessLock = threading.Lock()

    def startDay(self):
        barber = Barber(threading.current_thread().getName())
        self.barbers.append(barber)

        while self.isOpen:
            if self.waitingRoom.empty():
                barber.sleep()
            else:
                self.availableBarbers -= 1
                customer = self.waitingRoom.get()
                if self.accessLock.locked():
                    self.accessLock.release()
                barber.cutHair(customer)
                threading.Thread(target=self.customerInfo, args=(customer,)).start()
                self.availableBarbers += 1

        self.writeLock.acquire()
        with open("./logs/BarberInfo.txt", "a") as f:
            f.write(str(barber) + "\n\n")
        self.writeLock.release()

    def open(self):
        for i in range(self.numberOfBarbers):
            threading.Thread(target=self.startDay, name=self.names[i]).start()

    def close(self):
        while self.waitingRoom.qsize() > 0:
            pass
        self.isOpen = False
        for barber in self.barbers:
            if not barber.isAwake():
                barber.wakeUp()
        print("Barber shop is closing at: {}".format(time.ctime()))

    def newCustomer(self, customer):
        if self.waitingRoom.qsize() == 0 and self.availableBarbers > 0:
            for barber in self.barbers:
                if not barber.isAwake():
                    self.waitingRoom.put(customer)
                    self.accessLock.acquire()
                    barber.wakeUp(customer)
                    break
        elif self.waitingRoom.qsize() < self.capacity:
            customer.timeEnteredWaitingRoom = time.ctime()
            print("Customer {} waits in the waiting room at: {}".format(customer.name, customer.timeEnteredWaitingRoom))
            self.waitingRoom.put(customer)
        else:
            customer.timeLeft = time.ctime()
            print("Customer {} leaving at: {}".format(customer.name, customer.timeLeft))
            threading.Thread(target=self.customerInfo, args=(customer,)).start()

    def customerInfo(self, customer):
        self.writeLock.acquire()
        with open("./logs/CustomerInfo.txt", "a") as f:
            f.write(str(customer))
        self.writeLock.release()