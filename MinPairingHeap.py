# Min Pairing Heap
# Author: David Allen
#
# Good for use as a Priority Queue
# The heap must be reassigned after every -
#   INSERT, DEL_MIN, and MERGE
# operation as these functions work best by
# returning new Heaps
# This has the unfortunate side effect of 
# creating garbage however

class MinPairingHeap:

    def __init__(self, min_val=None, subheap=[]):
        self.subheap = subheap
        self.min_val = min_val

    # Returns the minimum value in the heap
    def find_min(self):
        return self.min_val

    # Merges @heap with the current heap
    # This mehod is destructive for both heaps
    def merge(self, heap1, heap2):
        if heap1.is_empty():
            return heap2

        if heap2.is_empty():
            return heap1

        if heap1.min_val > heap2.min_val:
            return MinPairingHeap(heap2.min_val, heap2.subheap + [heap1])
            
        return MinPairingHeap(heap1.min_val, heap1.subheap + [heap2])


    # Deletes the min element from the heap
    # If the heap is empty it will simply return the empty heap
    def del_min(self):
        def helper(sub):
            if len(sub) <= 0:
                return MinPairingHeap()
            if len(sub) == 1:
                return sub[0]
            new_heap = self.merge(sub[0], sub[1])
            return self.merge(new_heap, helper(sub[2:]))

        if self.is_empty():
            return self

        return helper(self.subheap)

    def insert(self, value):
        if self.is_empty():
            self.min_val = value
            return self
        else:
            return self.merge(self, MinPairingHeap(value))

    def is_empty(self):
        return self.min_val == None


# h = MinPairingHeap(10)
# h = h.insert(5)
# h = h.insert(15)
# h = h.insert(1)
# h = h.insert(20)
# print(h.min_val, h.subheap)

# h = h.del_min()
# print(h.min_val, h.subheap)
