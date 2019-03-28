#!/usr/bin/env python3
"""
read description of PNL model from json and reconstruct
"""

import argparse
import json
import pandas
from psyneulink import *

# some needed settings
good_params = ['slope','intercept','starting_point',
                'noise','t0','threshold',]

type_specific_additions = {'DDM':'output_states=[DDM_OUTPUT.PROBABILITY_UPPER_THRESHOLD, DDM_OUTPUT.RESPONSE_TIME]'}

# get command line arguments
parser = argparse.ArgumentParser(description='Example Psyneulink entrypoint script.')
parser.add_argument('-j','--json_file', help='json file containing model specification')
parser.add_argument('-s','--stimulus_file', 
        help="tsv file containing stimulus features (with label in first column")


args = parser.parse_args()

print('using model spec from:',args.json_file)
with open(args.json_file) as f:
        model_desc = json.load(f)

# open stimulus file
stimulus = pandas.read_csv(args.stimulus_file,sep='\t',)

# read in the nodes and parse into functions

nodes = {} # dictionary containing all of the defined nodes

for n in model_desc['nodes']:
        node = model_desc['nodes'][n]
        print('found node:',node['name'])
        param_string=','.join(['{}={}'.format(i,node['function']['parameters'][i]) for i in node['function']['parameters'] if i in good_params])
        fxn='%s(name="%s",function=%s(%s)'%(node['type'],node['name'],
                                        node['function']['type'],param_string)
        # add type-specific arguments
        if node['type'] in type_specific_additions:
                fxn = fxn + ', %s'%type_specific_additions[node['type']]
        # finish off the command
        fxn = fxn + ')'
        nodes[n]=eval(fxn)

# compose the model
c = Composition(name=model_desc['name'])

# this next bit is a kludge, relies upon assumptions about naming of projections
# to find appropriate nodes
# would be better if each projection contained the names of its origin and destination
for k in model_desc['projections']:
        if k.find('_CIM') == -1: # drop Input/Output_CIM projections
                keys = k.split(' to ')
                c.add_linear_processing_pathway([nodes[keys[0]],nodes[keys[1]]])

# create stimulus dict from info in stimuli file
stimuli = {}
for i in range(stimulus.shape[0]):
        stimuli[nodes[stimulus.iloc[i,0]]]=stimulus.iloc[i,1:].tolist()

# execute the model
c.run(inputs=stimuli)
print (c.results)


