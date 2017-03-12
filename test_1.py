import pygraphviz as pgv
import subprocess

G = pgv.AGraph(strict=False, directed=True)

G.add_nodes_from([1, 2, 3, 4])
G.add_edge(1, 2, label='ACGTT\ncoverage: 10')
G.add_edge(1, 3)
# G.edge_attr.update(label='ACGTT\ncoverage: 10')


G.draw('./data/out/1.pdf', prog='dot')
subprocess.call('open -a Preview ./data/out/1.pdf', shell=True)
