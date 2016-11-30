
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
    t_file = open(os.getcwd() + '/part3/data/train.trees.pre.imp')
    old_train = open(os.getcwd() + '/part3/data/train.trees.pre.unk')
    dev_file = open(os.getcwd() + '/shared/data/dev.strings')
    test_file = open(os.getcwd() + '/shared/data/test.strings')
    old_train_lines = old_train.readlines()
    train_lines = t_file.readlines()
    dev_lines = dev_file.readlines()
    test_lines = test_file.readlines()

    imp_cky = ImpCky(old_train_lines,train_lines,dev_lines,test_lines)

    imp_cky.main()
    # post process dev and test
    os.system("python ./part3/imp_postprocess.py ./part3/output/dev.parses.imp > ./part3/output/dev.parses.post.imp")
    os.system("python ./part3/imp_postprocess.py ./part3/output/test.parses.imp > ./part3/output/test.parses.post.imp")
    print("improved results:")
    os.system("python ./shared/scripts/evalb.py ./part3/output/dev.parses.post.imp ./shared/data/dev.trees")
    print("test results:")
    os.system("python ./shared/scripts/evalb.py ./part3/output/test.parses.post.imp ./shared/data/test.trees")
  





