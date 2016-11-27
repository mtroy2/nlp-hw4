from tree import *
import os
grammar = {}

def main(t_file):    
    for line in t_file:
        t = Tree.from_str(line)
        traverse_tree(t.root)
    #  count unique rules
    unique =0  
    most_freq = 0
    sorted_rules = []
    
    for parent_rule, child_rules in grammar.items():
        unique += len(child_rules.keys())
        for child_rule, count in child_rules.items():
            full_rule = parent_rule + ' -> ' + child_rule
            prob = count / sum(child_rules.values())
            grammar[parent_rule][child_rule] = prob
            sorted_rules.append((full_rule, count, prob))
    sorted_rules = sorted( sorted_rules, key= lambda x: x[1])
    
    print("There are " + str(unique) + " unique rules in the grammar" )
    print("The top five rules are: ")
    sorted_rules.reverse()
    top_five = sorted_rules[0:5]
    for rule in top_five:
        print( rule[0] + " # " + str(rule[1] ))
    sorted_rules = sorted( sorted_rules, key = lambda x: x[2])
    sorted_rules.reverse()
    top_five = sorted_rules[0:5]
    print("Top five probable rules are: " )
    for rule in top_five:
        print( rule[0] + " # " + str(rule[2]))
def traverse_tree(cur_node):
    cur_rule = cur_node.label
    if len(cur_node.children) == 2:
        child_rule = cur_node.children[0].label + " " + cur_node.children[1].label
    elif len(cur_node.children) == 1:
        child_rule = cur_node.children[0].label
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
    train_file = open(os.getcwd() + '/train.trees.pre.unk')
    main(train_file)
