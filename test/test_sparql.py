from src.data_gen import sparql_vir
import logging
import unittest
from src.owlio import process_axioms
from src.modelling import gen_input
import os
from src.utils import config
import time

class MyTestCase(unittest.TestCase):

    def test_queries(self):
        for i in [1, 3, 5, 6, 10, 11, 13, 14]:
            qid, q = sparql_vir.lubm_sample_query_for_virtuoso(i)
            logging.info("query to issue: %s", q)
            resp = sparql_vir.issue_queries(q, query_name=qid, dataset_prefix='u1')
            #logging.info(resp)
            time.sleep(2)


if __name__ == '__main__':
    unittest.main()