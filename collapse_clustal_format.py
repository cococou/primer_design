#!/usr/bin/env python3
import os
import re
import sys
import pandas as pd

confusion ={
        'R': ['A','G'],
        'Y': ['C','T'],
        'M': ['A','C'],
        'K': ['G','T'],
        'S': ['C','G'],
        'W': ['A','T'],
        'H': ['A','C','T'],
        'B': ['C','G','T'],
        'V': ['A','C','G'],
        'D': ['A','G','T'],
        'N': ['A','C','G','T'],
        'I': ['A','C','G','T']
        }

def GetConfusion(basel):
    basel = [i.upper() for i in basel]
    basel = set(basel)   
    for key,value in confusion.items():
        if len(basel) == len(set(value) & basel):
            return key
    return "N" 

def Collapse(bases):
    seq = ''
    for i in range(len(bases)):
        if '-' in bases[i]:
            continue
        if len(bases[i]) > 1:
            seq += 'N'
            #seq += GetConfusion(bases[i])
        elif len(bases[i]) == 1:
            seq += bases[i][0].upper()
    return seq           
  
def Consensus(l):
    length = len(l[0])
    bases ={}
    for seq in l:
        for i in range(length):
            bases[i] = bases.get(i,'')
            bases[i] += seq[i]
    bases = {key:list(set(value)) for key,value in bases.items()}
    seq = Collapse(bases)
    return seq
        


def Xopen(f):
    seqs =[]
    final_seqs = []
    with open(f) as handle:
        for line in handle:
            line = line.replace('\n','')
            if not line or line.startswith("CLUSTAL"):continue
            if line.startswith(' '):
                seq = Consensus(seqs)
                final_seqs.append(seq)
                seqs = []
            else:
                seqs.append(line.split(None)[1])
    if  seqs and not seqs.startswith(' '):
        seq = Consensus(seqs)
        final_seqs.append(seq)
    return final_seqs

def GetContinueSeq(final_seqs):
    seq = ''
    seqs = []
    for i in final_seqs:
        if i.startswith(' ') or not i:
            if seq: seqs.append(seq)
            seq = ''
        else:
            seq += i
    if seq:
        seqs.append(seq)
    return seqs
    
if __name__ == "__main__":
    final_seqs = Xopen(sys.argv[1])
    seqs = GetContinueSeq(final_seqs)
    for i in range(len(seqs)):
        print('>',i,sep="")
        print(seqs[i])
        
