'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, next=None, tf = 0):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.skip_point = None
        self.tf = tf


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list.
                To be implemented."""
            cur = self.start_node
            while cur:
                traversal.append(cur.val)

            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            raise NotImplementedError
            return traversal

    def has(self, doc_id_):

        cur = self.start_node
        # print(cur)
        # print(cur.value)
        while cur:
            if cur.value == doc_id_:
                return True
            cur = cur.next
        return False


    def add_skip_connections(self):
        n_skips = math.floor(math.sqrt(self.length))
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1

        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented."""




        raise NotImplementedError

    def insert_at_end(self, value, tf):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """

        newNode = Node(value=value, next=None, tf = tf)
        n = self.start_node

        self.length+=1

        if self.start_node is None:
            self.start_node = newNode
            self.end_node = newNode
            return
        elif self.start_node.value >= value:
            self.start_node = newNode
            self.start_node.next = n
            return
        elif self.end_node.value <= value:
            self.end_node.next = newNode
            self.end_node = newNode
            return
        else:
            while n.value < value < self.end_node.value and n.next is not None:
                n = n.next

            m = self.start_node
            while m.next != n and m.next is not None:
                m = m.next
            m.next = newNode
            newNode.next = n
            return


