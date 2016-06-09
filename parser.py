# -*- coding: utf-8 -*-
import sys
import copy
import random
import time

def no_neg(s):
    if '~' in s:
        return s[1:]
    return s

def shift_list(l, offset = 1):
    i = 0
    while i < len(l):
        l[i] = l[i] + offset
        i += 1
    return l

def cnf_str(cnf):
    s = ''
    for i in cnf:
        for j in i:
            s = s + str(j) + ' '
        s = s + '0' + '\n'
    return s

def parser(args):
    if len(args) == 0:
        filename = "blocks-4-0.strips"
        tamanho_plano = 4
    else:
        filename = args[0]
    #    tamanho_plano = int(args[1])
    tamanho_plano = args[1]
    f = open(filename, 'r')
    l = f.readlines()
    l = map(lambda x:x[0:-1],l)
    l = l[0:-3] + l[-2:]
    ll = map(lambda x: x.split(';'), l)
    names = []
    for i in ll:
        for j in i:
            if not no_neg(j) in names:
                names.append(no_neg(j))
    actions = []
    i = 0
    while i < len(ll) - 2:
        actions.append(names.index(ll[i][0]))
        i += 3
    atoms = []
    i = 0
    while i < len(names):
        if not i in actions:
            atoms.append(i)
        i += 1
    actions = shift_list(actions)
    atoms = shift_list(atoms)
    names = ['...'] + names
     #quantidade de turnos possívelmente
    tamanho_de_turno = len(names)
    i = 10
    while i <= tamanho_de_turno:
        i = i*10
    tamanho_de_turno = i
    turno_atual = 0
    cnf = []
    lista_p = [{f:[(f + j*tamanho_de_turno), -(f + (j+1)*tamanho_de_turno)] for f in atoms} for j in range(tamanho_plano)]
    lista_n = [{f:[-(f + j*tamanho_de_turno), (f + (j+1)*tamanho_de_turno)] for f in atoms} for j in range(tamanho_plano)]
    
    #adicionando estado inicial
    i = 0
    while i < len(ll[-2]):
        cnf.append([names.index(ll[-2][i])])
        i += 1
    
    #adicionando aqueles que não estão no estado inicial
    # de forma negativa
    i = 1
    while i < len(names):
        if not i in actions and not [i] in cnf:
            cnf.append([-i])
        i += 1

    while turno_atual < tamanho_plano:
        i = 0
        while i < len(ll) - 2:

            #
            clause = []
            clause.append(-(names.index(ll[i][0]) + (turno_atual)*tamanho_de_turno))

            k = 0
            while k < len(ll[i+2]):
                if '~' in ll[i+2][k]:
                    cnf.append(clause+[-(names.index(ll[i+2][k][1:]) + (turno_atual+1)*tamanho_de_turno)])
                else:
                    cnf.append(clause+[(names.index(ll[i+2][k]) + (turno_atual+1)*tamanho_de_turno)])
                k += 1

            k = 0
            while k < len(ll[i+2]):
                if '~' in ll[i+2][k]:
                    lista_n[turno_atual][names.index(ll[i+2][k][1:])].append(names.index(ll[i][0]) + (turno_atual)*tamanho_de_turno)
                else:
                    lista_p[turno_atual][names.index(ll[i+2][k])].append(names.index(ll[i][0]) + (turno_atual)*tamanho_de_turno)
                k += 1

            k = 0
            while k < len(ll[i+1]):
                if '~' in ll[i+1][k]:
                    cnf.append([clause[0], -(names.index(ll[i+1][k][1:]) + (turno_atual)*tamanho_de_turno) ])
                else:
                    cnf.append([clause[0], names.index(ll[i+1][k]) + (turno_atual)*tamanho_de_turno])
                k += 1
            i += 3
            
        #já tenho a parte da cnf que transforma
        #as ações em CNFs
        #falta as restrições de turnos

        #restrição de duas ações no mesmo turno
        i = 0
        while i < len(actions):
            j = i + 1
            while j < len(actions):
                if i != j:
                    cnf.append([-(actions[i] + (turno_atual)*tamanho_de_turno), -(actions[j] + (turno_atual)*tamanho_de_turno)])
                j += 1
            i += 1

        #pelo menos uma ação por turno:
        i = 0
        clause = []
        while i < len(actions):
            clause.append(actions[i] + (turno_atual)*tamanho_de_turno)
            i += 1
        cnf.append(clause)

        #estado final
        if turno_atual == tamanho_plano - 1:
            i = 0
            while i < len(ll[-1]):
                cnf.append([names.index(ll[-1][i]) + (turno_atual+1)*tamanho_de_turno])
                i += 1
        turno_atual += 1

    for t in lista_p:
        for f in t:
            cnf.append(t[f])
    for t in lista_n:
        for f in t:
            cnf.append(t[f])

    return cnf, names, tamanho_de_turno, actions

if __name__ == '__main__':
    parser(sys.argv[1:3])