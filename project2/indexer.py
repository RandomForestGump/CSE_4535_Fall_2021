'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from linkedlist import LinkedList
from collections import OrderedDict, Counter


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        # print('Generating Inverted Index for Doc ID: {}'.format(doc_id))
        # print(tokenized_document)
        C = Counter(tokenized_document)
        for t in tokenized_document:
            self.add_to_index(t, doc_id, C)

    def print_list(self, cur):
        x = []
        print(cur)
        while cur:
            x.append(cur.value)
            cur = cur.next
        print(x)

    def add_to_index(self, term_, doc_id_, C):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the postings list of the term.
            To be implemented."""
        tf = C[term_]
        # if term_ not in self.inverted_index:
        #     self.inverted_index[term_] = LinkedList()
        # self.inverted_index[term_] = self.inverted_index[term_].insert_at_end(doc_id_)
        # print(term_)
        # print(1)
        if term_ not in self.inverted_index:
            self.inverted_index[term_] = LinkedList()
            self.inverted_index[term_].insert_at_end(doc_id_, tf)
        # print(2)
        # self.print_list(self.inverted_index[term_].start_node)
        if not (self.inverted_index[term_].has(doc_id_)):
            self.inverted_index[term_].insert_at_end(doc_id_, tf)
        # print(3)


        # print(self.inverted_index.get('ventilated', 0))
        # if term_ not in self.inverted_index or not self.inverted_index[term_]:
        #     self.inverted_index[term_] = LinkedList(doc_id_)
        #     self.inverted_index[term_].length+=1
        #
        # else:
            #Modify list to add doc id in sorted place using linked list ops



    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        raise NotImplementedError

    def calculate_tf_idf(self):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        raise NotImplementedError
