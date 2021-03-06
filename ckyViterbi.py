from tree import *
import os
import numpy as np
import time
import matplotlib.pyplot as plt
grammar = {}
sorted_rules = []
non_terms= []
term_lookup = {}
back = []
vocabulary = []

def main():
    
    read_training()    
    unique_rules = convert_probs()
    prep_syms()
    parse_dev()
def prep_syms():
    global non_terms
    global term_lookup
    global vocabulary
    non_terms = set(non_terms)
    non_terms = sorted(non_terms)
    for i, term in enumerate(non_terms):
       term_lookup[term ] = i 
    vocabulary = set(vocabulary)
def parse_dev():
    sentence_lengths = []
    times = []
    global vocabulary
    dev_in = open(os.getcwd() + "/dev.strings")
    
    dev_lines = dev_in.readlines()
    dev_parse = open('dev.parses', 'w')
    print("Output for first 5 lines of dev file:")
    for i,line in enumerate(dev_lines):
        line = line.rstrip()
        line = line.split()
   
        for j,word in enumerate(line):
            if word not in vocabulary:
                line[j] = '<unk>' 
        start_time = time.time()
        parse,prob = cky_parse( line, dev_parse )
        tot_time = time.time() - start_time
        times.append(np.log(tot_time))
        sentence_lengths.append(np.log(len(line)))
        dev_parse.write(parse)
        dev_parse.write('\n')

        if i < 5:
            print("Line " + str(i) + '\n' + "parse: \n" + parse + "\nLog prob: " + str(prob))

    plot(sentence_lengths, times)

def plot(x,y):
    x = np.array(x)
    y = np.array(y)
    plt.scatter(x,y)
    plt.show()
    weights = np.polyfit(x,y,1)
    print("The best fit for this equation = " + str(round(weights[0],3)) + " log(x) - " +  str(round(weights[1],3))   )
def cky_parse(line, out_file):
    global non_terms
    global grammar
    global term_lookup
    # build matrix n by n by X
    best = []
    back = []

    sen_length = len(line)
    neg_inf = -1 * np.inf
    if len(line) == 0:
        return "",""
    # fill best and back matricies
    for i in range(0,sen_length):
        best.append([0]*(sen_length+1))  
        back.append([0] *( sen_length+1)) 
    for i in range(0,sen_length):
        for j in range(0,sen_length+1):
            best[i][j] = [neg_inf] * len(non_terms)
            back[i][j] = [0] * len(non_terms)

    # populate first diag
    # for each word in sentence
    for i in range(1, sen_length + 1):
        for gen_rule, child_rule_dict in grammar.items():
            # if word can be generated by this rule
            if line[i - 1] in child_rule_dict.keys():
                # prob of this rule
                
            
                if child_rule_dict[line[i-1]] > best[i-1][i][term_lookup[gen_rule]]:
          
                    best[i-1][i][term_lookup[gen_rule]] = child_rule_dict[line[i-1]]
                    back[i-1][i][term_lookup[gen_rule]] = [] 
                    back[i-1][i][term_lookup[gen_rule]] = [gen_rule, line[i-1],i-1,i]
    for l in range(2, sen_length+1):
        for i in range(0 , sen_length - l+1):
            j = i + l
            for k in range(i+1, j ):
                #print("Sentence length = " + str(sen_length) + " ( i = " + str(i) + " , j = " + str(j) + " , k = " + str(k))
                # iterate through every rule we know
                for gen_rule, child_rules in grammar.items():
                    for child_rule, prob in child_rules.items():
                        # X -> Y Z  - YZ stored as string "Y Z", need to split
                        t_child_rule = child_rule.split()
                        if len(t_child_rule) == 2:
                           
                            prob_p = prob + best[i][k][term_lookup[t_child_rule[0]]] + best[k][j][term_lookup[t_child_rule[1]]]
                           
                            if prob_p > best[i][j][term_lookup[gen_rule]]:
                                best[i][j][term_lookup[gen_rule]] = prob_p
                                back[i][j][term_lookup[gen_rule]] = [gen_rule,t_child_rule[0],t_child_rule[1],i,k,j]
    #print(line)
    #print(back[0][ sen_length ])
    end_rule =back[0][sen_length][term_lookup['TOP']]
    # failed parse
    if end_rule == 0:
        return "",""
    else:
        parse = print_tree(end_rule, 0,sen_length  , back)
       # print(parse)
        return parse, best[0][sen_length][term_lookup['TOP']]

def print_tree( X, i ,j,back):

    global term_lookup
    ret_string = ""
    ret_string += "("
    ret_string += X[0] + " "
    #print("(", end="")
    #print(X[0] + " ", end = "")
    if len(X) == 4:
        ret_string = "(" + X[0] + " "   + X[1] + ")"
        return ret_string
       # print(X[1], end="")
        
    else:
        y_index = term_lookup[X[1]] 
        k = X[4]
 
        ret_string += print_tree(back[i][k][y_index],i,X[4], back)
        ret_string += " "
       # print( " ", end="")
        z_index = term_lookup[X[2]] 
        ret_string += print_tree(back[k][j][z_index],X[4],j,back)
       # print(")", end="")
        ret_string += ")"
        return ret_string

def convert_probs():
    global grammar
    global sorted_rules
    unique = 0
    for parent_rule, child_rules in grammar.items():
        non_terms.append(parent_rule)
        unique += len(child_rules.keys())       
        child_sum = sum(child_rules.values())
        for child_rule, count in child_rules.items():
            full_rule = parent_rule + ' -> ' + child_rule
            prob = count / child_sum
            prob = np.log(prob) 
            grammar[parent_rule][child_rule] = prob
            sorted_rules.append((full_rule, count, prob))
            for term in child_rule.split():
                non_terms.append(term)
    return unique

def read_training():
    train_file = open(os.getcwd() + '/train.trees.pre.unk') 
    for line in train_file:
        t = Tree.from_str(line)
        traverse_tree(t.root)
def traverse_tree(cur_node):
    global grammar
    global vocabulary
    cur_rule = cur_node.label
    if len(cur_node.children) == 2:
        child_rule = cur_node.children[0].label + " " +  cur_node.children[1].label  

    elif len(cur_node.children) == 1:
        child_rule = cur_node.children[0].label
        vocabulary.append(cur_node.children[0].label)
    else:
        return "ERR : too many children"
        
    if cur_rule in grammar.keys():
        if child_rule in grammar[cur_rule].keys():
            grammar[cur_rule][child_rule] += 1
        else:
            grammar[cur_rule][child_rule] = 1
    else:
        grammar[cur_rule] = {}
        grammar[cur_rule][child_rule] = 1.
    for node in cur_node.children:
        traverse_tree(node)









if __name__ == "__main__":
    main()
