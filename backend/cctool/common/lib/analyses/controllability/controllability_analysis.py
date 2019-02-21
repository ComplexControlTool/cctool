import itertools
import operator
from collections import Counter
from cctool.graphs.models.models import NodePlus

MIN_NODES_FOR_APPROXIMATION = 100;

def bipartiteMatch(graph):
    """
    Find maximum cardinality matching of a bipartite graph (U,V,E).
    The input format is a dictionary mapping members of U to a set
    of their neighbors in V. The output is a triple (M,A,B) where M is a
    dictionary mapping members of V to their matches in U, A is the part
    of the maximum independent set in U, and B is the part of the MIS in V.
    The same object may occur in both U and V, and is treated as two
    distinct vertices if this happens.
    """
    # Initialize greedy matching (redundant, but faster than full search).
    matching = {}
    matchingKeys = set()

    for u in graph:
        temp = graph[u] - matchingKeys
        if temp:
            t = temp.pop()
            matching[t] = u
            matchingKeys.add(t)

    while 1:
        # structure residual graph into layers
        # pred[u] gives the neighbor in the previous layer for u in U
        # preds[v] gives a list of neighbors in the previous layer for v in V
        # unmatched gives a list of unmatched vertices in final layer of V,
        # and is also used as a flag value for pred[u] when u is in the first
        # layer
        preds = {}
        unmatched = []
        pred = dict([(u, unmatched) for u in graph])
        for v in matching:
            if matching[v] in pred:
                del pred[matching[v]]
        layer = list(pred)

        # Repeatedly extend layering structure by another pair of layers.
        while layer and not unmatched:
            newLayer = {}
            for u in layer:
                for v in graph[u]:
                    if v not in preds:
                        newLayer.setdefault(v, []).append(u)
            layer = []
            for v in newLayer:
                preds[v] = newLayer[v]
                if v in matching:
                    layer.append(matching[v])
                    pred[matching[v]] = v
                else:
                    unmatched.append(v)

        # Did we finish layering without finding any alternating paths?
        if not unmatched:
            return (len(matching), matching)

        # Recursively search backward through layers to find alternating paths.
        # Recursion returns true if found path, false otherwise.
        def recurse(v):
            if v in preds:
                L = preds[v]
                del preds[v]
                for u in L:
                    if u in pred:
                        pu = pred[u]
                        del pred[u]
                        if pu is unmatched or recurse(pu):
                            matching[v] = u
                            return 1
            return (0, {})

        for v in unmatched:
            recurse(v)


def createSubGraph(graphSet, possibleSet, nodesInConf):
    """
    Return subgraph of possible nodes and
    super control nodes.
    """
    subGraph = {}
    workingSet = set(possibleSet) | nodesInConf

    for i in graphSet:
        subGraph[i] = graphSet[i] - workingSet

    return subGraph


def createNotInConfSubGraph(graphSet, possibleSet):
    """
    Return a subgraph by removing all incoming
    edges to nodes in the possible set.
    """
    subGraph = {}

    for i in graphSet:
        subGraph[i] = graphSet[i] - possibleSet

    return subGraph


def createInConfSubGraph(graphSet, noOutEdgeSet, noInEdge):
    """
    Return a subgraph by removing all outgoing edges
    from outSet and all incoming edges to inSet
    """
    subGraph = {}
    noInEdgeSet = set()
    noInEdgeSet.add(noInEdge)

    for i in graphSet:
        if i != noOutEdgeSet:
            subGraph[i] = graphSet[i] - noInEdgeSet

    subGraph[noOutEdgeSet] = set()

    return subGraph


def createNotInConfSet(graphSet, nodesNo, controlSize):
    """
    Return a set of nodes that are never
    in the control configuration.
    """

    notInConfigSet = set()

    for i in range(nodesNo):
        possibleSet = set()
        possibleSet.add(i)

        subGraph = createNotInConfSubGraph(graphSet, possibleSet)
        (tControlSize, tMatching) = bipartiteMatch(subGraph)
        # If size is not the same, there is no configuration
        # of minimum size without an edge pointing to node i.
        if tControlSize != controlSize:
            notInConfigSet = notInConfigSet | possibleSet

    return notInConfigSet


def createInConfSet(graphSet, nodesNo, controlSize, nodesNotInConf):
    """
    Return a set of nodes that are always
    in the control configuration.
    """

    inConfigSet = set()

    fail = False
    for i in set(range(nodesNo)) - nodesNotInConf:
        for ii in graphSet:
            if i in graphSet[ii]:
                subGraph = createInConfSubGraph(graphSet, ii, i)
                (tControlSize, tMatching) = bipartiteMatch(subGraph)
                tControlSize += 1
                # If the size is the same, an edge between a and b can be added,
                # thus, b is not in this minimal control configuration.
                if tControlSize == controlSize:
                    fail = True
                    break
        if not fail:
            inConfigSet.add(i)
        fail = False

    return inConfigSet


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
        return (output, matching)

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
    (controlSize, controlMatching) = bipartiteMatch(graphSet)
    matchingSize = nodesNo - controlSize

    if matchingSize == 0:
        return output

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


def find_controllability(graphSet, nodesNo):
    if nodesNo < MIN_NODES_FOR_APPROXIMATION:
        return computeControlConf(graphSet, nodesNo)

    return computeAproxControlConf(graphSet, nodesNo)

def rank_by_node_controllability(control_configurations, stems, node_controllabilities):
    """
    Find the best (easiest) control configuration based
    on the stakeholder's input - controllability of the nodes.
    """
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

    sorted_by_value = sorted(weighted_control_configurations.items(), key=operator.itemgetter(1), reverse=True)
    ranked_control_configurations = dict()
    ranked_stems = dict()
    for i, (id,_) in enumerate(sorted_by_value):
        ranked_control_configurations[i] = control_configurations[id]
        ranked_stems[i] = stems[id]

    return (ranked_control_configurations, ranked_stems)
