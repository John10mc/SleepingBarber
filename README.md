When the SleepingBarber.py program is run by default it outputs to standard output all the events that are happening at real time. Along with this it keeps a log of each barbers and customers activity in ./logs/BarbersInfo.txt and ./logs/CustomerInfo.txt files respectively.

The log files allow us to see how barbers change states from sleeping to awake to cutting hair and back to being asleep. This represents what the thread associated with the barber is doing at that given time.

The log files also allow us to see the time line of each customer from entering the barber shop and either waiting in the waiting room, waking a barber or leaving the barber shop due to the waiting room being full. The customer also records when they started getting their haircut and when they finished if they didn't leave.

Using standard output and the log files we can see that each customer is serviced by only one barber, that whichever barber the customer wakes up then that barber cuts their hair, that while the barber is asleep they sleep and do nothing until woke up.

The program can be run with the command "python3 SleepingBarber.py".
Six switches are available to change the behavior of the program.
"-c int" sets how many customers enter the barber shop where int is an integer of how many customers there are. If not set defaults to 50
"-w int" sets the size of the waiting room where int is an integer of the size of the waiting room. It not set it defaults to 15
"-a int1 int2" sets the min and max time of customers arriving to the barber shop. int1 is the minimum amount of time between customers arriving and int2 is the maximum amount of time between customers arriving. If not set then they default to 0 and 3 respectively.
"-b int" sets how many barbers are in the barber shop and service the customers. int is an integer used to specify how many. This defaults to 4 if not set. Names of up to 10 barbers have been provided and anymore with result in the barbers being named numbers.
"-h int" sets the range of how long a customers hair cut takes from 0 up to the integer provided. If not set it defaults to 12.
"-q" it used to silence the output of standard output. 

Some sample inputs:

python3 SleepingBarber.py -c 15 -w 15 -a 0 5 -b 4 -h 7
This tests the barbers going to sleep and being woke up by a customer and can be clearly seen in standard output and the log files.

python3 SleepingBarber.py -c 40 -w 15 -a 0 1 -b 4 -h 10
This tests the waiting room filling up and customers leaving and can be clearly see in standard output and the log files

Running the program without switches shows a balance of everything.

The program can take quite a while to run due to the sleep methods throughout the program. However, this is used to understand what is going on in the background. A possible solution to this is instead of using random.randint() i could use random.uniform() to generate floating point numbers. This would cause a problem with time.ctime() because it is only accurate to the second and the time between events would not be noticed if the inputs were small enough. It is possible to overcome this using the datetime libiary and datetime method. While this is a possible improvement monitoring standard out might not be possible.