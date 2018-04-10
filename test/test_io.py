import unittest
from src.owlio import process_axioms
from src.modelling import gen_input
import os
from src.utils import config


class MyTestCase(unittest.TestCase):
    def notest_tbox(self):
        dir = '/projects/PycharmProjects/query-answering/src/files/lubm'
        fp = dir + '/univ-bench.rdf'
        tb = process_axioms.load_tbox(fp)
        inds = process_axioms.load_abox(dir + '/data', tb)
        k = inds.keys()
        k = list(k)
        # print(type(inds[k[1]]), k)

    def test_model(self):
        dir = '/projects/PycharmProjects/query-answering/src/files/lubm'
        fp = dir + '/univ-bench.rdf'
        tb = process_axioms.load_tbox(fp)
        inds = process_axioms.load_abox(dir + '/data', tb)
        ins, outs = gen_input.get_inout(inds)
        m = gen_input.base_model()
        gen_input.train_model(m, ins, outs)

    def notest_pred(self):
        fp = os.path.join(config.model_save_dir, '03_10_19_029_ACC_0.951.hdf5')
        dir = '/projects/PycharmProjects/query-answering/src/files/lubm'
        owlfp = dir + '/univ-bench.rdf'
        tb = process_axioms.load_tbox(owlfp)
        gen_input.test_model(fp, tb)


if __name__ == '__main__':
    unittest.main()
