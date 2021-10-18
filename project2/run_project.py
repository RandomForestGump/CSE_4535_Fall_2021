'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from tqdm import tqdm
import pdb
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
from linkedlist import Node
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def get_highest_tf_idf(self, cur1, cur2):

        if cur1.tf_idf >= cur2.tf_idf:
            return cur1, cur1.tf
        else:
            return cur2, cur2.tf

    def _merge_skip(self, l1, l2):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""

        cur1 = l1.start_node
        cur2 = l2.start_node

        compares = 0
        res = LinkedList()
        res.length = 0
        while cur1 and cur2:

            if cur1.value == cur2.value:
                compares += 1
                a, b = self.get_highest_tf_idf(cur1, cur2)
                res.insert_at_end(a.value, b, a.tf_idf)
                cur1 = cur1.next
                cur2 = cur2.next

            elif cur1.value < cur2.value:
                compares+= 1

                if cur1.skip_pointer and cur1.skip_pointer.value <= cur2.value:
                    compares+=1
                    while cur1.skip_pointer and cur1.skip_pointer.value <= cur2.value:
                        cur1 = cur1.skip_pointer
                else:
                    cur1 = cur1.next

            elif cur1.value > cur2.value:
                compares+=1
                if cur2.skip_pointer and cur2.skip_pointer.value <= cur1.value:
                    compares+=1
                    while cur2.skip_pointer and cur2.skip_pointer.value <= cur1.value:
                        cur2 = cur2.skip_pointer
                else:
                    cur2 = cur2.next

        return res, compares

    def _merge(self, l1, l2):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""

        cur1 = l1.start_node
        cur2 = l2.start_node
        compares = 0
        res = LinkedList()

        while cur1 and cur2:
            if cur1.value == cur2.value:
                compares += 1
                a, b = self.get_highest_tf_idf(cur1, cur2)
                res.insert_at_end(a.value, b, a.tf_idf)
                cur1 = cur1.next
                cur2 = cur2.next
            elif cur1.value > cur2.value:
                compares += 1
                cur2 = cur2.next
            else:
                compares += 1
                cur1 = cur1.next
        return res, compares

    def sort_terms_in_order(self, query_terms):
        d = {}
        for term in query_terms:
            d[term] = self.indexer.inverted_index[term].length
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        return list(d.keys())

    def sort_tf_idf(self, ll):

        cur = ll.start_node
        var = {}
        while cur:
            var[cur.value] = cur.tf_idf
            cur = cur.next
        var = {k: v for k, v in sorted(var.items(), reverse = True,key=lambda item: item[1])}
        #var = {k: v for k, v in sorted(var.items(),key=lambda item: item[1])}
        return list(var.keys())

    def _daat_and(self, query_terms, sort = False):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""

        query_terms = self.sort_terms_in_order(query_terms)
        comparisons = 0
        res = self.indexer.inverted_index[query_terms[0]]

        for i in range(1, len(query_terms)):
            res, compares = self._merge(res, self.indexer.inverted_index[query_terms[i]])
            comparisons += compares
        if not sort:
            return res.traverse_list(), comparisons
        else:
            sorted_res = self.sort_tf_idf(res)
            return sorted_res, comparisons


    def _daat_and_skip(self, query_terms, sort = False):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""

        query_terms = self.sort_terms_in_order(query_terms)
        res = self.indexer.inverted_index[query_terms[0]]
        comparisons = 0

        for i in range(1, len(query_terms)):
            res, compares = self._merge_skip(res, self.indexer.inverted_index[query_terms[i]])

            res.add_skip_connections()
            comparisons += compares

        if not sort:
            return res.traverse_list(), comparisons
        else:
            sorted_res = self.sort_tf_idf(res)
            return sorted_res, comparisons

        return res, comparisons


    def _get_postings(self, terms, skip = False):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        dic = {}
        for term_ in terms:
            dic[term_] = self.indexer.inverted_index[term_]

        return {'postingsList': dic}



    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        total_docs = 0
        with open(corpus, 'r') as fp:
            for line in tqdm(fp.readlines()):
                total_docs+=1
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)

        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf(total_docs)
    
    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""

            input_term_arr = []  # Tokenized query. To be implemented.
            tokenized_document = self.preprocessor.tokenizer(query)
            input_term_arr = input_term_arr + tokenized_document
            input_term_arr = list(set(input_term_arr))

            for term in input_term_arr:
                postings, skip_postings = self.indexer.inverted_index[term], self.indexer.inverted_index[term]

                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""

                output_dict['postingsList'][term] = postings.traverse_list()
                output_dict['postingsListSkip'][term] = skip_postings.traverse_skips()


            and_op_no_skip, and_comparisons_no_skip = self._daat_and(input_term_arr)
            and_op_skip, and_comparisons_skip = self._daat_and_skip(input_term_arr)
            and_op_no_skip_sorted, and_comparisons_no_skip_sorted = self._daat_and(input_term_arr, sort = True)
            and_op_skip_sorted, and_comparisons_skip_sorted = self._daat_and_skip(input_term_arr, sort = True)
            
   """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)
            
            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip
            # print(output_dict)

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted
        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")

    # corpus = '/Users/rajatjain/Desktop/repos/CSE_4535_Fall_2021/project2/data/input_corpus.txt'
    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)
    # query = ['the novel coronavirus', 'from an epidemic to a pandemic','is hydroxychloroquine effective?']
    # out = runner.run_queries(query)

    # port = 9001
    port = 8983
    app.run(host="0.0.0.0", port=port)
