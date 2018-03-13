from owlready2 import *
import logging
from ..utils import config
import numpy as np
import json

file_protocol = 'file://'

def load_tbox(fp):
    fp = file_protocol+ fp
    onto = get_ontology(fp).load()
    #onto = ontospy.Ontospy(fp)
    logging.info("onto %s loaded", fp)
    cls = sorted(list(onto.classes()), key=lambda c:c.iri)
    roles = sorted(list(onto.object_properties()), key=lambda c:c.iri)
    dps = sorted(list(onto.data_properties()), key=lambda c:c.iri)
    logging.info("%s classes, %s props, %s data props ", len(cls), len(roles), len(dps))
    cls = dict((x, i) for i, x in enumerate(cls))
    roles = dict((x, i) for i,x in enumerate(roles))
    dps = dict((x, i) for i,x in enumerate(dps))
    tbox = {
        'classes':cls,
        'ops': roles,
        'dps' : dps
    }
    return tbox


def init_relation_matrix(tbox):
    mat_ra = np.zeros((len(tbox['ops']), len(tbox['classes'])))
    mat_da = np.zeros(len(tbox['dps']))
    mat_ca = np.zeros(len(tbox['classes']))
    return (mat_ra, mat_da, mat_ca)

#load all RDF files from the dir
def load_abox(dir, tbox):
    rdfs = []
    for f in os.listdir(dir):
        fp = dir + '/' +f
        if fp.endswith('rdf'):
            rdfs.append(fp)
    jo = None
    for f in rdfs:
        res = __load_data(f, tbox)
        if not jo:
            jo = res
        else:
            #jo = merge_matrices(jo, res)
            jo = {**jo, **res}
    logging.info("%s total inds", len(jo))
    return jo

###safe to just replace
def merge_matrices(jo1, jo2):
    joined = {**jo1}
    for k,v in jo2.items():
        if k in joined:
            vp = joined[k]
            assert np.array_equal(v['mat_ra'], vp['mat_ra'])
            assert np.array_equal(v['mat_da'], vp['mat_da'])
            assert np.array_equal(v['mat_ca'], vp['mat_ca'])
        joined[k] = v
    return joined




def __load_data(rdf_fp, tbox):
    rdf_fp = file_protocol + rdf_fp
    onto = get_ontology(rdf_fp)
    onto.load()
    inds = list(onto.individuals())
    ops = list(tbox['ops'].keys())
    dps = list(tbox['dps'].keys())
    cps = list(tbox['classes'].keys())
    cas = dict()
    ret_jo = dict()
    for ind in inds:
        mat_ra, mat_da, mat_ca = init_relation_matrix(tbox)
        props = ind.get_properties()
        for p in props:
            if p in ops:
                # RA
                pi = tbox['ops'][p]
                vals = p[ind]
                for val in vals:
                    val_iri = val.iri
                    if val_iri in cas:
                        cas_val = cas[val_iri]
                    else:
                        cas_val = val.is_a
                        cas[val_iri] = cas_val
                    for c in cas_val:
                        ci = tbox['classes'][c]
                        mat_ra[pi][ci] += 1.0
            elif p in dps:
                #data property assertions, for now, only count the number of values. Maybe need to consider actual values?
                pi = tbox['dps'][p]
                vals = p[ind]
                mat_da[pi] += len(vals)
        cs = ind.is_a
        for c in cs:
            ci = tbox['classes'][c]
            mat_ca[ci] = 1.0
        ret_jo[ind.iri] = {'mat_ra':mat_ra, 'mat_ca':mat_ca, 'mat_da':mat_da}
    logging.info("%s ind processed", len(inds))
    return ret_jo



def populate_matrix(tbox, abox):
    '''
    for each individual, we get the matrix by looking at all relations <ind,p,o> (maybe also <o, p, ind>?)
    all concept assertions <ind:C>
    '''
    return