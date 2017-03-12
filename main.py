# -*- coding: utf-8 -*-

import pygraphviz as pgv
import subprocess
import argparse
import time
from tqdm import tqdm


def parse_fq(file_path):
    node_l = []
    with open(file_path) as fq_in:
        while True:
            try:
                next(fq_in)
            except StopIteration:
                break
            seq = next(fq_in).strip()
            i = 0
            while i <= len(seq) - k:
                if seq[i:i + k] not in node_l:
                    node_l.append(seq[i:i + k])
                if rev_compl(seq[i:i + k]) not in node_l:
                    node_l.append(rev_compl(seq[i:i + k]))
                i += 1
            next(fq_in)
            next(fq_in)
    return node_l


def parse_fa(file_path):
    node_l = []
    with open(file_path) as fa_in:
        seq = ''
        c = 1
        while True:
            c += 1
            try:
                line = next(fa_in)
            except StopIteration:
                break
            if line[0] == '>':
                do_seq(seq, node_l)
                seq = ''
                continue
            else:
                seq += line.strip()
        do_seq(seq, node_l)
    return node_l


def rev_compl(seq):
    nt_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join([nt_dict.get(nt) for nt in seq[-1::-1].upper()])


def do_seq(seq, node_l):
    i = 0
    while i <= len(seq) - k:
        if seq[i:i + k] not in node_l:
            node_l.append(seq[i:i + k])
        if rev_compl(seq[i:i + k]) not in node_l:
            node_l.append(rev_compl(seq[i:i + k]))
        i += 1

parser = argparse.ArgumentParser(
        description='Homemade genome assembler v0.1')
parser.add_argument('-i', '--in_file', default=None, type=str, help='Input fasta/fastq file path')
parser.add_argument('-o', '--out_file', default=None, type=str, help='Output pdf file path')
parser.add_argument('-k', '--k_mer', default=20, type=int, help='k-mer length')

args = parser.parse_args()

k = args.k_mer

print('step 1\nget the data')
t = time.perf_counter()
if args.in_file[-1] == 'a':
    node_l = parse_fa(args.in_file)
elif args.in_file[-1] == 'q':
    node_l = parse_fq(args.in_file)
else:
    print('Wrong file type\nOnly fasta or fastq supported')
print(time.perf_counter() - t, 'sec')

print('step 2\nadd nodes and edges')
t = time.perf_counter()
G = pgv.AGraph(strict=False, directed=True)
G.add_nodes_from(node_l)
for node in node_l:
    matches = [x for x in node_l if x[1:] == node[:-1]]
    for seq in matches:
        G.add_edge(seq, node)
print(time.perf_counter() - t, 'sec')
# print(node_l)

print('step 3\nshrink graph')
t = time.perf_counter()
node_iter = iter(node_l)
for node in node_l:
    if G.out_degree(node) == G.in_degree(node) == 1:
        G.add_edge(G.in_neighbors(node)[0], G.out_neighbors(node)[0])
        G.remove_edge(node, G.out_neighbors(node)[0])
        G.remove_edge(G.in_neighbors(node)[0], node)
        G.remove_node(node)
print(time.perf_counter() - t, 'sec')

print('step 4\nrender graph')
t = time.perf_counter()
G.draw(args.out_file, prog='dot')
print(time.perf_counter() - t, 'sec')

subprocess.call('open -a Preview %s' % args.out_file, shell=True)



