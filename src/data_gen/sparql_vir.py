import urllib
from urllib.parse import urlencode
import json
import os
from src.utils import config
import logging

lubm_data_named_graph = 'http://swat.cse.lehigh.edu/onto/univ-bench/data'
lubm_prefix = 'http://swat.cse.lehigh.edu/onto/univ-bench.owl'
query_base_url = 'http://localhost:8890/sparql/'

def issue_queries(query, query_name, dataset_prefix,
                  out_format = 'application/sparql-results+json', result_x_list=True):
    file_name = os.path.join(config.answers_save_dir, dataset_prefix+'_'+query_name+'.txt')
    if os.path.exists(file_name):
        logging.error('file %s exists, not running this query ...', file_name)
    params = {
        'default-graph': lubm_data_named_graph,
        'query': query,
        'save':'display',
        'format':out_format,
    }
    querybd = urlencode(params).encode('utf-8')
    req = urllib.request.Request(query_base_url)
    with urllib.request.urlopen(req,data=querybd) as f:
        resp = f.read()
        if result_x_list:
            resp = resp.decode('utf-8')
            resp = json.loads(resp)
            bindings = resp['results']['bindings']
            xs = [x['x']['value'] for x in bindings]
            resp = xs
    with open(file_name, 'w') as f:
        json.dump(resp, f)
    return resp



def lubm_sample_query_for_virtuoso(id):
    ids = [1, 3, 5, 6, 10, 11, 13, 14]
    if id not in ids:
        raise ValueError("query not supported: " + id)
    begin = [
        "DEFINE input:inference 'lubm:schema'",
        'PREFIX ub:<' + lubm_prefix + '#>',
        'select distinct ?x where {',
    ]
    end = [
        '}'
    ]
    Q1 = [
        '?x rdf:type ub:GraduateStudent . ',
        '?x ub:takesCourse <http://www.Department0.University0.edu/GraduateCourse0>'
    ]
    Q3 = [
        '?x rdf:type ub:Publication . ',
        '?x ub:publicationAuthor <http://www.Department0.University0.edu/AssistantProfessor0>'
    ]
    Q5 = [
        '?x rdf:type ub:Person .',
        '?x ub:memberOf <http://www.Department0.University0.edu>'
    ]
    Q6 = [
        '?x rdf:type ub:Student'
    ]
    Q10 = [
        '?x rdf:type ub:Student .',
        '?x ub:takesCourse <http://www.Department0.University0.edu/GraduateCourse0>'
    ]
    Q11 = [
        '?x rdf:type ub:ResearchGroup .',
        '?x ub:subOrganizationOf <http://www.University0.edu>'
    ]
    Q13 = [
        '?x rdf:type ub:Person .',
        '?x ub:degreeFrom <http://www.University0.edu> '
    ]
    Q14 = [
        '?x rdf:type ub:UndergraduateStudent'
    ]
    queries = dict()
    for i in ids:
        k = 'Q'+str(i)
        queries[k] = locals()[k]
    queryname = 'Q'+str(id)
    q = queries[queryname]
    query = ' '.join(begin+q+end)
    return queryname, query
