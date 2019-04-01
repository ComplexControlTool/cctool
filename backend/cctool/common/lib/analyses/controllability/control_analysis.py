import itertools
import operator
from collections import Counter
from cctool.graphs.models.models import NodePlus
from .lib.configs import computeControlConf, computeAproxControlConf
from .lib.hk import bipartiteMatch
from .lib.subgraphs import createSubGraph, createNotInConfSubGraph, createInConfSubGraph
from .lib.sets import createNotInConfSet, createInConfSet

MIN_NODES_FOR_APPROXIMATION = 100;

def find_controllability(graphSet, nodesNo):
    if nodesNo < MIN_NODES_FOR_APPROXIMATION:
        return computeControlConf(graphSet, nodesNo)

    return computeAproxControlConf(graphSet, nodesNo)

def rank_by_node_controllability(control_configurations, stems, node_controllabilities):
    """
    Find the best (easiest) control configuration based
    on the stakeholder's input - controllability of the nodes.
    """
    ranked_control_configurations = dict()
    ranked_stems = dict()
    if not control_configurations and not stems:
        return (ranked_control_configurations, ranked_stems)

    weight_values = {
        NodePlus.NEUTRAL_CONTROLLABILITY: 0,
        NodePlus.EASY_CONTROLLABILITY: 1,
        NodePlus.MEDIUM_CONTROLLABILITY: 2,
        NodePlus.HARD_CONTROLLABILITY: 3
    }

    weighted_nodes = {nodeId:weight_values[controllability] for (nodeId, controllability) in node_controllabilities.items()}
    weighted_control_configurations = dict()
    for (id, configuration) in control_configurations.items():
        weighted_configuration = sum([weighted_nodes[nodeId] for nodeId in configuration])
        weighted_control_configurations[id] = weighted_configuration

    sorted_by_value = sorted(weighted_control_configurations.items(), key=operator.itemgetter(1))
    for i, (id,_) in enumerate(sorted_by_value):
        ranked_control_configurations[i] = control_configurations[id]
        ranked_stems[i] = stems[id]

    return (ranked_control_configurations, ranked_stems)