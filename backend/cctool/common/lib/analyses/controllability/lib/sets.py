import itertools
import operator
from collections import Counter
from .hk import bipartiteMatch
from .subgraphs import createSubGraph, createNotInConfSubGraph, createInConfSubGraph


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