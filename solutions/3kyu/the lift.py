'''Synopsis
A multi-floor building has a Lift in it.

People are queued on different floors waiting for the Lift.

Some people want to go up. Some people want to go down.

The floor they want to go to is represented by a number (i.e. when they enter the Lift this is the button they will press)

BEFORE (people waiting in queues)               AFTER (people at their destinations)
                   +--+                                          +--+ 
  /----------------|  |----------------\        /----------------|  |----------------\
10|                |  | 1,4,3,2        |      10|             10 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 9|                |  | 1,10,2         |       9|                |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 8|                |  |                |       8|                |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 7|                |  | 3,6,4,5,6      |       7|                |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 6|                |  |                |       6|          6,6,6 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 5|                |  |                |       5|            5,5 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 4|                |  | 0,0,0          |       4|          4,4,4 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 3|                |  |                |       3|            3,3 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 2|                |  | 4              |       2|          2,2,2 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 1|                |  | 6,5,2          |       1|            1,1 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 G|                |  |                |       G|          0,0,0 |  |                |
  |====================================|        |====================================|
Rules
Lift Rules
The Lift only goes up or down!
Each floor has both UP and DOWN Lift-call buttons (except top and ground floors which have only DOWN and UP respectively)
The Lift never changes direction until there are no more people wanting to get on/off in the direction it is already travelling
When empty the Lift tries to be smart. For example,
If it was going up then it may continue up to collect the highest floor person wanting to go down
If it was going down then it may continue down to collect the lowest floor person wanting to go up
The Lift has a maximum capacity of people
When called, the Lift will stop at a floor even if it is full, although unless somebody gets off nobody else can get on!
If the lift is empty, and no people are waiting, then it will return to the ground floor
People Rules
People are in "queues" that represent their order of arrival to wait for the Lift
All people can press the UP/DOWN Lift-call buttons
Only people going the same direction as the Lift may enter it
Entry is according to the "queue" order, but those unable to enter do not block those behind them that can
If a person is unable to enter a full Lift, they will press the UP/DOWN Lift-call button again after it has departed without them
Kata Task
Get all the people to the floors they want to go to while obeying the Lift rules and the People rules
Return a list of all floors that the Lift stopped at (in the order visited!)
NOTE: The Lift always starts on the ground floor (and people waiting on the ground floor may enter immediately)

I/O
Input
queues a list of queues of people for all floors of the building.
The height of the building varies
0 = the ground floor
Not all floors have queues
Queue index [0] is the "head" of the queue
Numbers indicate which floor the person wants go to
capacity maximum number of people allowed in the lift
Parameter validation - All input parameters can be assumed OK. No need to check for things like:

People wanting to go to floors that do not exist
People wanting to take the Lift to the floor they are already on
Buildings with < 2 floors
Basements
Output
A list of all floors that the Lift stopped at (in the order visited!)
Example
Refer to the example test cases.

Language Notes
Python : The object will be initialized for you in the tests
'''

UP = 1
DOWN = -1

class Dinglemouse(object):
    """ The Lift solver class """

    def __init__(self, queues, capacity):
        self.queues = tuples_to_list(queues)
        self.top_floor = len(self.queues) - 1
        self.ground_floor = 0
        self.capacity = capacity
        self.passengers = []
        self.stops = []
        self.floor = 0
        self.direction = UP
        self.lift_floor = None

    def theLift(self):
        """ main function """
        while not self.floor_queues_empty() or not self.lift_is_empty():
            if self.stop_lift():
                self.passengers_leaving()
                self.passengers_entering()
            if self.floor == self.top_floor:
                self.direction = DOWN
            if self.floor == self.ground_floor:
                self.direction = UP
            if self.floor == 0 and not self.stops:
                self.stops.append(0)
            self.floor += self.direction
        if self.stops[-1:] != [0]:
            self.stops.append(0)
        return self.stops

    def floor_queues_empty(self):
        """ check if floor queues are empty """
        return is_list_empty(self.queues)

    def lift_is_empty(self):
        """ check if lift is empty """
        return False if self.passengers else True

    def stop_lift(self):
        """ check whether the lift needs to stop """
        ret = False
        to_enter = [p for p in self.queues[self.floor] if self.passenger_to_enter(p)]
        if self.floor in self.passengers or to_enter:
            ret = True
            if self.floor != self.lift_floor:
                self.stops.append(self.floor)
                self.lift_floor = self.floor
        return ret

    def passengers_leaving(self):
        """ passengers leaving the lift """
        remain = [p for p in self.passengers if p != self.floor]
        if len(remain) != len(self.passengers):
            self.passengers = remain

    def passengers_entering(self):
        """ passengers enter the lift """
        passengers = self.queues[self.floor][:]
        for passenger in passengers:
            if len(self.passengers) < self.capacity and \
               self.passenger_to_enter(passenger):
                self.passengers.append(passenger)
                self.queues[self.floor].pop(self.queues[self.floor].index(passenger))

    def passenger_to_enter(self, p):
        """ check if a passenger will enter the lift """
        return (self.direction == UP and p > self.floor) or \
               (self.direction == DOWN and p < self.floor) or \
               self.floor == self.top_floor or \
               self.floor == self.ground_floor

def tuples_to_list(i):
    """ transform nested tuples to nested lists """
    if isinstance(i, (tuple, list)):
        l = [list(e) if isinstance(e, tuple) else e for e in i]
    else:
        return i
    for i, e in enumerate(l):
        l[i] = tuples_to_list(e)
    return l

def is_list_empty(in_list):
    """ check if all elements of a nested list are empty """
    if isinstance(in_list, list):
        return all(map(is_list_empty, in_list))
    return False

if __name__ == "__main__":
    q = ((), (0,), (), (), (2,), (3,), ())
    lift = Dinglemouse(q, 5)
    lift_stops = lift.theLift()
    print(lift_stops)