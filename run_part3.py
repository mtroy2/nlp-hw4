
import os
import sys

sys.path.insert(0,os.getcwd() + '/part3')
sys.path.insert(0,os.getcwd() + '/shared/scripts')

from imp_cky import ImpCky
from old_cky import CkyViterbi

if __name__ == "__main__":


    os.system("python ./part3/vert_preprocess.py ./shared/data/train.trees > ./part3/data/train.trees.pre.vert")
    os.system("python ./part3/horiz_preprocess.py ./shared/data/train.trees > ./part3/data/train.trees.pre.horiz")
    os.system("python ./shared/scripts/preprocess.py ./shared/data/train.trees > ./part3/data/train.trees.pre")
    os.system("python ./shared/scripts/unknown.py ./part3/data/train.trees.pre > ./part3/data/train.trees.pre.unk")
    horiz_file = open(os.getcwd() + '/part3/data/train.trees.pre.horiz')
    vert_file = open(os.getcwd() + '/part3/data/train.trees.pre.vert')
    old_train = open(os.getcwd() + '/part3/data/train.trees.pre.unk')
    dev_file = open(os.getcwd() + '/shared/data/dev.strings')
    test_file = open(os.getcwd() + '/shared/data/test.strings')
    old_train_lines = old_train.readlines()
    vert_lines = vert_file.readlines()
    horiz_lines = horiz_file.readlines()
    dev_lines = dev_file.readlines()
    test_lines = test_file.readlines()
    vert_cky = ImpCky(vert_lines,dev_lines,test_lines)
    horiz_cky = ImpCky(horiz_lines,dev_lines,test_lines)
    old_cky = CkyViterbi(old_train_lines,dev_lines,test_lines)
    
    vert_cky.main()
    horiz_cky.main()
    old_cky.main()
    horiz_cky.parse_dev('./part3/output/dev.parses.horiz')
    horiz_cky.parse_test('./part3/output/test.parses.horiz')
    old_cky.parse_dev('./part3/output/dev.parses.old')
    old_cky.parse_test('./part3/output/test.parses.old')
    vert_cky.compose(horiz_cky, old_cky)

    vert_cky.sim_all_dev()
    vert_cky.sim_all_test()
    # post process dev and test
    os.system("python ./part3/imp_postprocess.py ./part3/output/dev.parses.vert > ./part3/output/dev.parses.post.vert")
    os.system("python ./part3/imp_postprocess.py ./part3/output/test.parses.vert > ./part3/output/test.parses.post.vert")
    print("improved results:")
    os.system("python ./shared/scripts/evalb.py ./part3/output/dev.parses.post.vert ./shared/data/dev.trees")
    print("test results:")
    os.system("python ./shared/scripts/evalb.py ./part3/output/test.parses.post.vert ./shared/data/test.trees")
  





