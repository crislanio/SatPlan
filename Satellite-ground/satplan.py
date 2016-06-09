# -*- coding: utf-8 -*-
import sys
import copy
import random
import time
from parser import *
import pycosat
import math

neg = lambda x: ((x/abs(x))+1)/2


def main(args = "blocks-4-0.strips"):
    pra_valer = True
    print args
    if pra_valer:
        i = 2
        solution = []
        while len(solution) <= 5:
            cnf, names, tn, actions = parser([args, i])
            print i
            solution = pycosat.solve(cnf)
            print solution
            i += 1
        for i in solution:
            if i > 0 and (abs(i) % 100) in actions:
                print names[abs(i) % 100], '>', str(i) 
    else:
        cnf, names, tn, actions = parser([args, 6])
        for i in cnf:
            print [ '~ '[neg(j)] + names[abs(j) % tn] +'--' + str(abs(j)/tn) for j in i]

if __name__ == '__main__':
    main(sys.argv[1])