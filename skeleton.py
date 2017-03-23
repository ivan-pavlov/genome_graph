#!/usr/bin/env python3

import argparse
from tqdm import tqdm


class Edge:
    show_sequences = False

    def __init__(self, v1, v2):

        # Edge instance should contain
        # starting and finishing vertices,
        # coverage and edge sequence

        # isinstance(v1, Vertex) == True
        # isinstance(v2, Vertex) == True

        raise NotImplementedError

    def inc_coverage(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def merge(self, following_edge):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class Vertex:
    show_sequences = False

    def __init__(self, seq):

        # Vertex instanace should contain
        # sequence, output and input edges

        raise NotImplementedError

    def add_edge(self, other):
        # Increases coverage if the edge already exists

        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
    
    def compress(self):
        # Returns False, if cannot be compressed
        # Otherwise compresses this vertex and returns true

        raise NotImplementedError


class Graph:
    k = None

    def __init__(self):
        # Contains all vertices

        raise NotImplementedError

    def add_edge(self, seq1, seq2):
        # Increases coverage if the edge already exists

        raise NotImplementedError

    def add_seq(self, seq):
        # Adds edges between all k-mers in the sequence

        raise NotImplementedError

    def compress(self):

        to_delete = [] # List of redundant vertices

        for kmer, vertex in ¯\_(ツ)_/¯:
            if vertex.compress():
                to_delete.append(kmer)
        for kmer in to_delete:
            # Delete redundant vertex

    def save_dot(self, outp):
        raise NotImplementedError


complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}


def reverse_complement(seq):
    return ''.join(complement[nt] for nt in seq[::-1])


def read_fastq(f):
    for line in f:
        name = line.strip()
        seq = next(f).strip()
        next(f)
        next(f)
        yield name, seq


def read_fasta(f):
    name = None
    seq = None
    for line in f:
        if line.startswith('>'):
            if name:
                yield name, seq
            name = line.lstrip('>').strip()
            seq = ''
        else:
            seq += line.strip()
    yield name, seq


def read(f):
    if f.name.endswith('a'):
        return read_fasta(f)
    else:
        return read_fastq(f)


def main():
    parser = argparse.ArgumentParser(description='De Bruijn graph')
    parser.add_argument('-i', '--input', help='Input fastq', metavar='File',
                        type=argparse.FileType(), required=True)
    parser.add_argument('-k', help='k-mer size (default: 55)', metavar='Int',
                        type=int, default=55)
    parser.add_argument('-o', '--output', help='Output dot', metavar='File',
                        type=argparse.FileType('w'), required=True)
    parser.add_argument('-c', '--compress', help='Shrink graph', action='store_true')
    parser.add_argument('--vertex', help='Show vertex sequences', action='store_true')
    parser.add_argument('--edge', help='Show edge sequences', action='store_true')
    args = parser.parse_args()

    Graph.k = args.k
    Vertex.show_sequences = args.vertex_seq
    Edge.show_sequences = args.edge_seq

    graph = Graph()
    for name, seq in tqdm(read(args.input)):
        graph.add_seq(seq)
        graph.add_seq(reverse_complement(seq))
    
    if args.compress:
        graph.compress()
    graph.save(args.output)


if __name__ == '__main__':
    main()

