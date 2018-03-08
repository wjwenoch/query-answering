import unittest
from src.owlio import process_axioms
from src.modelling import gen_input
import os
from src.untils import config

class MyTestCase(unittest.TestCase):
    def notest_tbox(self):
        dir = 'D:/ontologies/lubm'
        fp =   dir + '/univ-bench.rdf'
        tb = process_axioms.load_tbox(fp)
        inds = process_axioms.load_abox(dir+'/data', tb)



    def test_model(self):
        dir = 'D:/ontologies/lubm'
        fp =   dir + '/univ-bench.rdf'
        tb = process_axioms.load_tbox(fp)
        inds = process_axioms.load_abox(dir+'/data', tb)
        ins, outs = gen_input.get_inout(inds)
        m = gen_input.base_model()
        gen_input.train_model(m, ins, outs)


    def notest_pred(self):
        fp = os.path.join(config.model_save_dir , '03_07_14_008_ACC_0.951.hdf5')
        dir = 'D:/ontologies/lubm'
        owlfp =   dir + '/univ-bench.rdf'
        tb = process_axioms.load_tbox(owlfp)
        gen_input.test_model(fp, tb)


if __name__ == '__main__':
    unittest.main()
