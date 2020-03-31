import sys
import time
import random
from lib.BarberShop import BarberShop
from lib.People import Customer

def main():
    noOfCustomers = 50
    minArrivalTime = 0
    maxArrivalTime = 3
    numberOfBarbers = 4
    haircutTime = 12
    waitingRoomCapacity = 15
    silent = True

    # optional switches used for the input of the program
    # switch used to set amount of customers 
    if "-c" in sys.argv:
        noOfCustomers = int(sys.argv[sys.argv.index("-c") + 1]) + 1
    # switch used to set the size of the waiting room
    if "-w" in sys.argv:
        waitingRoomCapacity = int(sys.argv[sys.argv.index("-w") + 1])
    # switch used for setting time between arrival of customers
    if "-a" in sys.argv:
        minArrivalTime = int(sys.argv[sys.argv.index("-a") + 1])
        maxArrivalTime = int(sys.argv[sys.argv.index("-a") + 2])
    # switch used to set amount of barbers
    if "-b" in sys.argv:
        numberOfBarbers = int(sys.argv[sys.argv.index("-b") + 1])
    # switch used to set max amount of time a haircut can take
    if "-h" in sys.argv:
        haircutTime = int(sys.argv[sys.argv.index("-h") + 1])
    if "-q" in sys.argv:
        silent = False

    # create a CustomerInfo.txt file to record each customers actions
    with open("./logs/CustomerInfo.txt", "w") as f:
        f.write("Customers Info\n")
    # create a BarbersInfo.txt file to record the barbers actions
    with open("./logs/BarberInfo.txt", "w") as f:
        f.write("Barber Info\n") 
    if silent: print("Barber shop opened at: ", time.ctime())

    shop = BarberShop(numberOfBarbers, waitingRoomCapacity, silent)
    shop.open()

    for i in range(1, noOfCustomers):
        time.sleep(random.randint(minArrivalTime, maxArrivalTime))
        customer = Customer(i, haircutTime, silent)
        # pass the customer object to the BarberShop.newCustomer method for the customer
        # to be processd by one of the barbers
        customer.timeEntered = time.ctime()
        if silent: print("Customer {} has entered the shop at: {}".format(i, customer.timeEntered))
        shop.newCustomer(customer)
    shop.close()

if __name__ == '__main__':
    main()