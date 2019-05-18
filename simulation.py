import random
from itertools import dropwhile

class Queue:
    """
    Pure python Queue implementation, not thread safe and not performant
    don't use this for anything.
    """
    def __init__(self):
        self.q = []

    def enqueue(self, item):
        self.q.insert(0, item)  # O(n) performance

    def dequeue(self):
        return self.q.pop()

    def size(self):
        return len(self.q)

    def is_empty(self):
        return len(self.q) == 0


class Task:
    def __init__(self, time_started):
        self.time_started = time_started

    def calc_wait_time(self, current_time):
        """
        Total time spent waiting.  Used by the simulation to know how long the task
        Remained in the queue before being pulled.
        """
        return current_time - self.time_started


class ConsumerStillBusy(Exception):
    pass


class Consumer:
    def __init__(self, tasks_per_min):
        self.tasks_per_min = tasks_per_min  # number of tasks per min the consumer can consume
        self.current_task = None
        self.time_remaining_on_curr_task = 0

    def is_busy(self):
        return self.current_task != None

    def add_task(self, new_task):
        if self.is_busy():
            raise ConsumerStillBusy('cannot add task when consumer is still busy')
        self.current_task = new_task
        self.time_remaining_on_curr_task = 60 / self.tasks_per_min

    def tick(self):
        if self.current_task != None:
            self.time_remaining_on_curr_task -= 1
            if self.time_remaining_on_curr_task <= 0:
                self.current_task = None


class Simulation:
    """
    num_sec_sim is the total period in seconds for the simulation
    new_task_chance is the ratio of 1:x where x is the odds of the task being generated
    """
    def __init__(self, num_sec_sim: int, new_task_chance: int, consumer: Consumer):
        self.num_sec_sim = num_sec_sim
        self.new_task_chance = new_task_chance
        self.consumer = consumer
        self.q = Queue()

    def simulate(self):
        """
        returns a list of wait times to complete the subtasks
        as a result of doing the simulation.
        """
        wait_times = []
        for curr_sec in range(self.num_sec_sim):
            if self.should_gen_new_task():
                new_task = self.gen_new_task(time_started=curr_sec)
                self.q.enqueue(new_task)
            if (not self.consumer.is_busy()) and (not self.q.is_empty()):
                next_task = self.q.dequeue()
                self.consumer.add_task(next_task)
                wait_times.append(next_task.calc_wait_time(current_time=curr_sec))
            self.consumer.tick()
        return wait_times

    def should_gen_new_task(self):
        return random.randrange(1, self.new_task_chance + 1) == self.new_task_chance

    def gen_new_task(self, time_started):
        return Task(time_started)


class Calculator:
    def __init__(self, wait_times: list):
        self.wait_times = wait_times

    def max(self):
        return max(self.wait_times)
    
    def min(self):
        """
        First task enqueued is immediately pulled and possibly some subsequent tasks so I filter out zeros.
        """
        return next(dropwhile(lambda x: x < 1, sorted(self.wait_times)))

    def average(self):
        if self.wait_times != 0:
            return sum(self.wait_times) / len(self.wait_times)
        
        
if __name__ == '__main__':
    # simulate any producer/consumer you'd like, here I'll simulate a chocolate eater and a chocolate factory

    # our chocolate eater can eat 20 pieces of chocolate per minute
    chocolate_eater = Consumer(tasks_per_min=10)
    # our chocolate factory will simulate 1800 secs (30 min).  The factory isn't very good 
    # so it only has a 1:5 chance of creating a new chocolate candy. 
    choc_factory_sim = Simulation(num_sec_sim=1800, new_task_chance=5, consumer=chocolate_eater)
    wait_times = choc_factory_sim.simulate()

    calc = Calculator(wait_times)
    print(f'Average wait times: {calc.average():.1f}s')
    print(f'Max wait time: {calc.max()}s')
    print(f'Min wait time: {calc.min()}s')
    print(f'Unfinished tasks: {choc_factory_sim.q.size()}s')



        




