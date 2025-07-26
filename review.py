# Review and refactor the following five code snippets.
# Identify any issues, explain the problems, and provide corrected versions.
"""
# Review 1
def add_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list

# Issue:
# The expression [] used as a default value is only run once — when the function is defined.”
print(add_to_list(1)) # Output: [1]
print(add_to_list(2)) # Output: [1, 2] — not [2]
"""


def add_to_list(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list


"""
# Review 2
def format_greeting(name, age):
    return "Hello, my name is {name} and I am {age} years old."

# Issue:
"Hello, my name is {name} and I am {age} years old." is just a raw string. 
"""


def format_greeting(name, age):
    return f"Hello, my name is {name} and I am {age} years old."


"""
# Review 3
class Counter:
    count = 0
    def __init__(self):
        self.count += 1
    def get_count(self):
        return self.count

# Issue:
count = 0 is a class variable.
Inside __init__, self.count += 1 does not modify the class variable directly.
Python looks for an instance variable self.count. It doesn’t find one yet.
It reads the class variable Counter.count (value = 0). Then it creates a new instance variable self.count = 1.
So the class-level Counter.count remains unchanged.
"""


class Counter:
    count = 0

    def __init__(self):
        Counter.count += 1

    def get_count(self):
        return Counter.count


"""
# Review 4
import threading
class SafeCounter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1

def worker(counter):
    for _ in range(1000):
        counter.increment()

counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Issue:
It is race condition due to lack of thread safety in the SafeCounter.increment() method.
In a multithreaded context, multiple threads may read the same value before any of them write back the updated value, causing increments to be lost.
"""
import threading


class SafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1


def worker(counter):
    for _ in range(10000):
        counter.increment()


counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

"""
# Review 5
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts

# Issue:
If the input list contains unhashable types(like other lists or dicts), 
it will get a TypeError because such items can’t be used as dictionary keys.
"""

from collections import Counter


def count_occurrences(lst):
    return Counter(lst)
