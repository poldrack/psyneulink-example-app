#!/usr/bin/env python3
"""
read description of PNL model from json and reconstruct
"""

import json
from psyneulink import *

show_graph = False

jsonfile = 'example.json'
with open(jsonfile) as f:
        model_desc = json.load(f)


# read in the nodes and parse into functions

nodes = {} # dictionary containing all of the defined nodes

# for now, just set these to desired value pending word from JDC

# optimal_color_control = 1
model_desc['nodes']['Color']['function']['parameters']['slope']=1

# optimal_motion_control = .5
model_desc['nodes']['Motion']['function']['parameters']['slope']=.5


good_proc_params = ['slope','intercept']
good_ddm_params =['starting_point','noise','t0','threshold',]
for n in model_desc['nodes']:
        node = model_desc['nodes'][n]
        if node['type']=='ProcessingMechanism':
                print('found Processing Mechanism:',node['name'])
                param_string=','.join(['{}={}'.format(i,node['function']['parameters'][i]) for i in node['function']['parameters'] if i in good_proc_params])
                fxn='%s(%s)'%(node['function']['type'],param_string)
                nodes[n]=ProcessingMechanism(name=node['name'],function=eval(fxn))
                                
        elif node['type']=='DDM':
                print('found DDM:',node['name'])
                param_string=','.join(['{}={}'.format(i,node['function']['parameters'][i]) for i in node['function']['parameters'] if i in good_ddm_params])
                fxn='%s(%s)'%(node['function']['type'],param_string)
                nodes[n]=DDM(name=node['name'],function=eval(fxn),
                        output_states=[DDM_OUTPUT.PROBABILITY_UPPER_THRESHOLD, DDM_OUTPUT.RESPONSE_TIME])

c = Composition(name=model_desc['name'])

# this next bit is a kludge, relies upon assumptions about naming of projections
# to find appropriate nodes

for k in model_desc['projections']:
        if k.find('_CIM') == -1: # drop Input/Output_CIM projections
                keys = k.split(' to ')
                c.add_linear_processing_pathway([nodes[keys[0]],nodes[keys[1]]])


if show_graph:
        c.show_graph()
# c.show_graph(show_node_structure=ALL)

stimuli = {nodes['Color']: [0,1,0],
           nodes['Motion']: [1,0,1]}

c.run(inputs=stimuli)
print (c.results)


