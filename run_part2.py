

import os
import sys
sys.path.insert(0,os.getcwd() + '/part1')
sys.path.insert(0,os.getcwd() + '/part2')
sys.path.insert(0,os.getcwd() + '/part3')
sys.path.insert(0,os.getcwd() + '/shared/scripts')
import buildCFG
from ckyViterbi import CkyViterbi
if __name__ == "__main__":
    os.system("python ./shared/scripts/preprocess.py ./shared/data/train.trees > ./shared/data/train.trees.pre")
    os.system("python ./shared/scripts/unknown.py ./shared/data/train.trees.pre > ./part2/data/train.trees.pre.unk")
    t_file = open(os.getcwd() + '/shared/data/train.trees.pre.unk')
    dev_file = open(os.getcwd() + '/shared/data/dev.strings')
    train_lines = t_file.readlines()
    dev_lines = dev_file.readlines()

    print("------------------------------------- PART 1 ----------------------------------------")
    buildCFG.main(train_lines)
    print("")
    print("------------------------------------- PART 2 ----------------------------------------")

    cky_viterbi = CkyViterbi(train_lines,dev_lines)
    cky_viterbi.main()

    os.system("python ./shared/scripts/postprocess.py ./part2/output/dev.parses > ./part2/output/dev.parses.post")
    print("")
    os.system("python ./shared/scripts/evalb.py ./part2/output/dev.parses.post ./shared/data/dev.trees")


