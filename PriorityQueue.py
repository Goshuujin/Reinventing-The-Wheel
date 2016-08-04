# Min Priority Queue
# Author: David Allen
#
# Uses MinPairingHeap to implement the
# major chunk of the data structure

import MinPairingHeap

class PriorityQueue:
    def __init__(self):
        self.queue = MinPairingHeap.MinPairingHeap()

    def push(self, value):
        self.queue = self.queue.insert(value)

    def pop(self):
        val = self.peek()
        self.queue = self.queue.del_min()
        return val

    def peek(self):
        return self.queue.find_min()

    def is_empty(self):
        return self.queue.is_empty()

class MaxPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()

    def push(self, value):
        self.queue = self.queue.insert(-value)

    def pop(self):
        return super().pop()

    def peek(self):
        return -super().peek()

# q = PriorityQueue()
# q = MaxPriorityQueue()
# q.push(1)
# q.push(10)
# q.push(-5)
# q.push(3)

# print(q.peek())
# while not q.is_empty():
#     print(str(q.pop()))
