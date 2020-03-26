import time
import random
from lib.BarberShop import BarberShop
from lib.People import Customer

def main():
    with open("./logs/CustomerInfo.txt", "w") as f:
        f.write("Customers Info\n")
    with open("./logs/BarberInfo.txt", "w") as f:
        f.write("Barber Info\n") 
    print("Barber shop opened at: ", time.ctime())
    shop = BarberShop()
    shop.open()
    for i in range(1, 51):
        time.sleep(random.randint(0, 3))
        customer = Customer(i)
        shop.newCustomer(customer)
        customer.timeEntered = time.ctime()
        print("Customer {} has entered the shop at: {}".format(i, customer.timeEntered))
    shop.close()

if __name__ == '__main__':
    main()