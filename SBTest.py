import threading
import queue
import time
import random

def main():
    print("Barber shop opened at: ", time.ctime())
    shop = BarberShop()
    shop.open()
    for i in range(1, 51):
        time.sleep(1)
        shop.newCustomer(Customer(i))
        print("Customer {} has entered the shop".format(i))
    shop.close()


class BarberShop():

    def __init__(self):
        self.names = ["Bob", "Billy", "Carl", "Ben"]
        self.barbers = []
        self.numberOfBarbers = 4
        self.isOpen = True
        self.capacity = 5
        self.waitingRoom = queue.Queue()
        self.availableBarbers = self.numberOfBarbers
        self.lock = threading.Lock()

    def startDay(self):
        barber = Barber(threading.current_thread().getName())
        self.barbers.append(barber)
        while self.isOpen:
            self.lock.acquire()
            if self.waitingRoom.empty():
                print("Barber {} has gone to sleep.".format(barber.name))
                self.lock.release()
                barber.sleep()
                print("Barber {} has woke up.".format(barber.name))
            else:
                self.availableBarbers -= 1
                self.lock.release()
                barber.cutHair(self.waitingRoom.get())
                self.availableBarbers += 1

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
                    barber.wakeUp()
                    break
        elif self.waitingRoom.qsize() < self.capacity:
            print("Customer {} waits in the waiting room at: {}".format(customer.name, time.ctime()))
            self.waitingRoom.put(customer)
        else:
            print("Customer {} leaving.".format(customer.name))

class Barber():

    def __init__(self, name):
        self.name = name
        self.event = threading.Event()
        print("Barber {} started work at: {}".format(self.name, time.ctime()))

    def sleep(self):
        self.event.clear()
        self.event.wait()

    def wakeUp(self):
        self.event.set()

    def isAwake(self):
        return self.event.is_set()

    def cutHair(self, customer):
        print("Barber {} has started cutting {}'s hair at: {}".format(self.name, customer.name, time.ctime()))
        time.sleep(random.randint(1, 7))
        print("Barber {} has finished cutting {}'s hair at: {}".format(self.name, customer.name, time.ctime()))


class Customer():
    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    main()