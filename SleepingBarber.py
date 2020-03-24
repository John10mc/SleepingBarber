import threading
import queue
import time
import random

def main():
    print("Barber shop opened at: ", time.ctime())
    shop = BarberShop()
    shop.open()
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

    def startDay(self, i):
        barber = Barber(i, self.waitingRoom)
        self.barbers.append(barber)
        barber.goToWork()

    def open(self):
        for i in range(self.numberOfBarbers):
            barbers.append(threading.Thread(target=self.startDay).start())

    def newCustomer(self, customer):
        if self.availableBarbers > 0:
            for barber in self.barbers:
                if barber.is_set():
                    self.availableBarbers - 1
                    self.availableBarbers += barber.wakeUp(customer)
        elif len(self.waitingRoom) < self.capacity:
            self.waitingRoom.put(customer)
        else:
            print("customer leaves")


class Barber():

    def __init__(self, name, waitingRoom):
        self.name = name
        self.waitingRoom = waitingRoom
        print("Barber {} started work at: {}".format(self.name, time.ctime()))

    def goToWork(self):
        while True:
            #mutex.acquire()

            if self.waitingRoom.qsize() > 0:
                self.barber.cutHair(waitingRoom.get())
                mutex.release()
            else:
                #mutex.release()
                print(self.state.current_thread())
                self.sleep()
                print("Barber {} woke up at: {}".format(self.name, time.ctime()))

    def checkWaitingRoom(self, barber):
        if self.waitingRoom.empty():
            barber.sleep()
        else:
            self.numberOfBarbers - 1
            availableBarbers += barber.cutHair(self.waitingRoom.get())

    def sleep(self):
        self.state.wait()
        print("Barber {} has gone to sleep at: {}".format(self.name, time.ctime()))

    def wakeUp(self, customer):
        state.set()
        return self.cutHair(customer)

    def cutHair(self, customer):
        print("Barber {} has started cutting {}'s hair at: {}".format(self.name, customer.name, time.ctime()))
        self.awake = True
        time.sleep(random.ranint(0, 10))
        return 1


class Customer():
    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    main()