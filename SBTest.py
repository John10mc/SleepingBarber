import threading
import queue
import time
import random

def main():
    print("Barber shop opened at: ", time.ctime())
    shop = BarberShop()
    shop.open()
    time.sleep(5)
    for i in range(40):
        shop.newCustomer(Customer(i))
        time.sleep(3)


class BarberShop():

    def __init__(self):
        self.barbers = []
        self.numberOfBarbers = 1
        self.capacity = 15
        self.waitingRoom = queue.Queue()
        self.availableBarbers = self.numberOfBarbers

    def startDay(self, e):
        barber = Barber(threading.current_thread(), e, self.waitingRoom)
        self.barbers.append(barber)
        barber.goToWork()

    def con(self):
        time.sleep(5)
        print(self.barbers[0])
        if not self.barbers[0].isAwake():
            self.barbers[0].wakeUp()

    def open(self):
        for i in range(self.numberOfBarbers):
            e = threading.Event()
            self.barbers.append(threading.Thread(target=self.startDay, args=(e,)).start())

    def newCustomer(self, customer):
        if self.availableBarbers > 0:
            for barber in self.barbers:
                if not barber.isAwake():
                    self.availableBarbers - 1
                    self.availableBarbers += barber.wakeUp(customer)
        elif len(self.waitingRoom) < self.capacity:
            self.waitingRoom.put(customer)
        else:
            print("customer leaves")

class Barber():

    def __init__(self, name, e, waitingRoom):
        self.name = name
        self.event = e
        self.waitingRoom = waitingRoom
        print("Barber {} started work at: {}".format(self.name, time.ctime()))

    def goToWork(self):
        while True:
            if self.waitingRoom.empty():
                self.sleep()
            else:
                self.cutHair(waitingRoom.get())

    def sleep(self):
        #print(self.name, "sleep")
        self.event.wait()

    def wakeUp(self, customer):
        print(self.name, "awake")
        self.event.set()
        return self.cutHair(customer)


    def isAwake(self):
        return self.event.is_set()

    def cutHair(self, customer):
        print("Barber {} has started cutting {}'s hair at: {}".format(self.name, customer.name, time.ctime()))
        self.awake = True
        time.sleep(random.randint(0, 10))
        return 1


class Customer():
    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    main()