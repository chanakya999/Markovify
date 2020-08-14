class Node(object):
    def __init__(self, val):
        self.val = val
        self.edges = []

    def add_edge(self, val, node):
        for edge in self.edges:
            if val == edge.val:
                edge.weight += 1
                return
        self.edges.append(Edge(val, node))

    def total_weight(self):
        # weight = 0
        # for edge in self.edges:
        #     weight += edge.weight
        # return weight
        return sum(edge.weight for edge in self.edges)


class Edge(object):
    def __init__(self, val, node):
        self.destination = node
        self.val = val
        self.weight = 1