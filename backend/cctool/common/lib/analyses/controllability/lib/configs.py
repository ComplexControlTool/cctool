import itertools
import operator
from collections import Counter
from .hk import bipartiteMatch
from .subgraphs import createSubGraph, createNotInConfSubGraph, createInConfSubGraph
from .sets import createNotInConfSet, createInConfSet


def computeControlConf(graphSet, nodesNo):
    """
    Computation of the Control Configuration.
    """
    output = {}
    matching = {}
    frequencies = {}
    (controlSize, controlMatching) = bipartiteMatch(graphSet)
    matchingSize = nodesNo - controlSize

    if matchingSize == 0:
        return (output, matching, frequencies)

    # Start methodology.

    # Find the nodes that are never in the control configuration.
    nodesNotInConf = createNotInConfSet(graphSet, nodesNo, controlSize)
    # Find the nodes that are always in the control configuration.
    nodesInConf = createInConfSet(
        graphSet, nodesNo, controlSize, nodesNotInConf)
    # Find the nodes that are sometimes included in the control configuration.
    freeNodes = set(range(nodesNo)) - nodesNotInConf - nodesInConf
    freeControl = matchingSize - len(nodesInConf)

    counter = 0
    # Find all possible sets of control nodes.
    for possibleSet in itertools.combinations(freeNodes, freeControl):
            # Subgraph with no ingoing edges to possible control nodes.
        subGraph = createSubGraph(graphSet, possibleSet, nodesInConf)
        (subMatchingSize, subMatching) = bipartiteMatch(subGraph)
        # Check whether the size of maximum matching remains
        # the same in this subnetwork.
        if subMatchingSize == controlSize:
                # If true, nodes with no incoming edges form control
                # configuration.
            output[counter] = list(set(possibleSet) | nodesInConf)
            matching[counter] = subMatching
            counter += 1

    # Compute node frequencies
    number_of_configurations = len(output)
    if number_of_configurations == 0:
        return (output, matching, frequencies)

    counter = dict(Counter(list(itertools.chain.from_iterable(output.values()))))
    frequencies = {key:(value/number_of_configurations*100) for (key,value) in counter.items()}

    # End of methodology.
    return (output, matching, frequencies)


def computeAproxControlConf(graphSet, nodesNo):
    """
    Computation of the approximated Control Configuration.
    """
    output = {}
    matching = {}
    frequencies = {}
    (controlSize, controlMatching) = bipartiteMatch(graphSet)
    matchingSize = nodesNo - controlSize

    if matchingSize == 0:
        return (output, matching, frequencies)

    # Start methodology.

    # Find the nodes that are never in the control configuration.
    nodesNotInConf = createNotInConfSet(graphSet, nodesNo, controlSize)
    # Find the nodes that are always in the control configuration.
    nodesInConf = createInConfSet(
        graphSet, nodesNo, controlSize, nodesNotInConf)
    # Find the nodes that are sometimes included in the control configuration.
    freeNodes = set(range(nodesNo)) - nodesNotInConf - nodesInConf

    output[0] = freeNodes
    output[1] = nodesInConf
    output[2] = nodesInConf

    # Compute node frequencies
    number_of_configurations = len(output)
    if number_of_configurations == 0:
        return (output, matching, frequencies)

    counter = dict(Counter(list(itertools.chain.from_iterable(output.values()))))
    frequencies = {key:(value/number_of_configurations*100) for (key,value) in counter.items()}

    # End of methodology.
    return (output, matching, frequencies)