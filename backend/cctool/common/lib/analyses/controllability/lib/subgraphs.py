import itertools
import operator
from collections import Counter
from cctool.graphs.models.models import NodePlus


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