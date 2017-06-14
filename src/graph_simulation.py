"""
Author: Deepak Gujraniya
email: deepakgujraniya@gmail.com
"""

import math, random, copy
from random_graph_generator import GenerateGraph

intial_risk = 0.01
damping_factor = 1
mask_const = 0.5


class GameSimulate(object):


    def create_graph(self, n, p):
        self.network = GenerateGraph(n, p, [])
        self.nodes = {node.index: node for node in self.network.graph.nodes()}  # will save some time
        # centrality =  self.network.centrality()
        self.degree_centrailty = {node.index: key for (node, key) in self.network.centrality().iteritems()}

    def init_deceptions(self,theta,is_random_deception_req = False, is_deployment_random = False,percentage_deception =1):
        self.node_masks = {node.index: math.exp(
            - (self.degree_centrailty[node.index] + theta * node.TrueValue)) if node.TrueValue > 0.5 else math.exp(
            self.degree_centrailty[node.index] + theta * node.TrueValue) for node in self.network.graph.nodes()}
        self.cost_signal = {node.index: node.TrueValue * self.node_masks[node.index] for node in
                            self.network.graph.nodes()}
        self.cc_shading = {node: mask_const * math.fabs(1 - mask) for node, mask in self.node_masks.iteritems()}

        deception_temp = {node: c * self.cost_signal[node] for node, c in self.degree_centrailty.iteritems()}
        avg_dvalue = sum(deception_temp.values()) * 1.0 / len(deception_temp)
        self.deceptions = {node: 1 if value > avg_dvalue else 0 for node, value in deception_temp.iteritems()}

        # based on the number of deception nodes. Assign them randomly
        if is_random_deception_req:
            if is_deployment_random == False:
                self.deceptions = self.random_deception_assignment()
            else:
                self.deceptions = self.random_deception_deployment(percentage_deception)

        self.visited_nodes = dict.fromkeys(self.deceptions.keys())
        for node in self.visited_nodes.keys():
            self.visited_nodes[node] = set()
        self.treasure_node = self.find_treasure_node()
        #print "number of deceptions ", sum(self.deceptions.values())

    def run_simulation(self, defender_budget, cost_D, attacker_budget, max_time):

        self.deceptions[self.treasure_node.index] = 0
        self.payoff_defender = list()
        self.payoff_attacker = list()
        deception_recognized = list()  # to stop revisiting the nodes
        # current_node = self.nodes[0]
        current_node = self.find_lowest_valuenode()
        t = 0
        seen_deception = 0
        winner = "attacker"
        for node in self.visited_nodes.keys():
            self.visited_nodes[node] = set()
        if self.deceptions[0] == 1:
            seen_deception = 1
        self.update_payoff(0, cost_D, self.deceptions[0], seen_deception, t)
        neighbors = self.network.graph.neighbors(self.nodes[0])
        while sum(self.payoff_defender) + defender_budget > 0:
            t += 1
            if t >= max_time:
                #print "attacker stayed too long"
                winner = "defender"
                break
            if sum([ x if x<0 else 0 for x in self.payoff_attacker]) + attacker_budget < 0:
                #print "attacker exhausted budget"
                winner = "defender"
                break

            utilities = self.expected_attacker_payoff(current_node, neighbors, seen_deception, t)
            max_utility = max(utilities)
            # print utilities, max_utility
            if max_utility != 0:
                location_util = utilities.index(max_utility)
                # print location_util, "all padosi of ", current_node.index, [n.index for n in neighbors]
                next_node = neighbors[location_util]
                # print "isitd noes for urr node", current_node.index, self.visited_nodes
                u = 0
                while True:
                    if next_node.index in self.visited_nodes[current_node.index]:
                        # print "location util", location_util , [n.index for n in neighbors]
                        neighbors.pop(location_util)
                        utilities.pop(location_util)
                        if len(utilities) > 0:
                            location_util = utilities.index(max(utilities))
                            next_node = neighbors[location_util]
                        else:
                            next_node = None
                            break
                        # print "next node", next_node.index
                        u += 1
                    else:
                        break
                if next_node is None:
                    #print "attacker lost, didn't find a node to move"
                    winner = "defender"
                    break
                if self.treasure_node.index == next_node.index:
                    #print "attacker found the treasure"
                    winner = "attacker"
                    break
                #print "next node selected by attacker is: ", next_node.index
                self.visited_nodes[current_node.index].add(next_node.index)
                self.update_payoff(next_node.index, cost_D, self.deceptions[next_node.index], seen_deception, t)
                seen_deception += self.deceptions[next_node.index]
                neighbors = self.network.graph.neighbors(next_node)
                if current_node in neighbors:
                    if len(neighbors) > 1:
                        neighbors.remove(current_node)

                current_node = next_node
            else:
                #print "attacker lost, didn't find a node to move onto"
                winner = "defender"
                break

        #print "attacker's payoff: ", sum(self.payoff_attacker)
        #print "defender's payoff: ", sum(self.payoff_defender)
        #print "game ended after {0} moves".format(t)
        #print "winner is ", winner
        # self.network.draw_graph()
        return winner
    def random_deception_deployment(self,percentage):

        num_dec = int(len(self.deceptions) * percentage)
        nodes = self.deceptions.keys()
        random.shuffle(nodes)
        deception_dict = dict.fromkeys(nodes[:num_dec], 1)
        no_deception_dict = dict.fromkeys(nodes[num_dec:], 0)
        return dict(deception_dict.items() + no_deception_dict.items())

    def update_payoff(self, node, cost_d, is_deception, seen_deceptions, t):
        risk = intial_risk + math.exp(damping_factor * t)
        operability = self.get_operability(t)
        if is_deception == 1:
            if self.is_deception_recognized(seen_deceptions):
                if operability == 1:
                    self.payoff_attacker.append(self.nodes[node].TrueValue - risk)
                    self.payoff_defender.append(0 - self.nodes[node].TrueValue - cost_d - self.cc_shading[node])
                else:
                    self.payoff_attacker.append(0 - risk)
                    self.payoff_defender.append(0 - cost_d - self.cc_shading[node])
            else:
                if operability == 1:
                    self.payoff_attacker.append(0 - risk)
                    self.payoff_defender.append(0 - cost_d - self.cc_shading[node])
                else:
                    self.payoff_attacker.append(0 - risk)
                    self.payoff_defender.append(0 - cost_d - self.cc_shading[node])
        else:
            if operability == 1:
                self.payoff_attacker.append(self.nodes[node].TrueValue - risk)
                self.payoff_defender.append(0 - self.nodes[node].TrueValue - self.cc_shading[node])
            else:
                self.payoff_attacker.append(0 - risk)
                self.payoff_defender.append(0 - self.cc_shading[node])

    def expected_attacker_payoff(self, current_node, nodes, seen_deception, t):
        payoffs = list()
        risk = intial_risk + math.exp(damping_factor * t)
        for node in nodes:
            oper = self.get_operability(t)
            payoff_d0 = (1-oper)*(self.cost_signal[node.index] + node.TrueValue - current_node.TrueValue - risk) + \
                oper * (0 - risk)
            p_d = 1 - math.exp(-(seen_deception*1.0/2))
            payoff_d1 = p_d * payoff_d0 + (1-p_d) * (0 - risk)
            expected_payoff = (payoff_d0 + payoff_d1)*1.0/2
            payoffs.append(expected_payoff)
        return payoffs

    def find_treasure_node(self):
        max_val = 0
        node = None
        node1 = None
        # return self.network.graph.nodes()[random.randint(1, len(self.network.graph.nodes())-1)]
        for n in self.network.graph.nodes():
            if n.TrueValue > max_val:
                node1 = node
                max_val = n.TrueValue
                node = n
        # if node.index == 0:
        #     return node1
        return node

    def random_deception_assignment(self):
        num_dec = sum(self.deceptions.values())
        nodes = self.deceptions.keys()
        random.shuffle(nodes)
        deception_dict = dict.fromkeys(nodes[:num_dec], 1)
        no_deception_dict = dict.fromkeys(nodes[num_dec:], 0)
        return dict(deception_dict.items() + no_deception_dict.items())

    def find_lowest_valuenode(self):
        min_val = 0
        node = None
        # return self.network.graph.nodes()[random.randint(1, len(self.network.graph.nodes())-1)]
        for n in self.network.graph.nodes():
            if n.TrueValue > min_val:
                min_val = n.TrueValue
                node = n
        return node

    @staticmethod
    def find_next_node(utils, max_val):
        temputil = copy.deepcopy(utils)
        temputil.remove(max_val)
        return max(temputil)

    @staticmethod
    def get_operability(t):
        val =  (1-math.exp(-t))
        return val

        #p = random.random()
        #if p > val:
        #    return 1
        #else:
        #    return 0

    @staticmethod
    def is_deception_recognized(seen_deceptions):
        p = 1 - math.exp(-(seen_deceptions*1.0/2))
        p_d = random.random()
        return p_d > p


if __name__ == '__main__':
    num_nodes = 10
    edge_probability = 0.6
    theta = 1
    defender_budget = 100
    attacker_budget = 140 #num_nodes*1000000
    max_time = num_nodes
    deployment_cost = 1
    Game = GameSimulate()
    Game.create_graph(num_nodes, edge_probability)
    Game.init_deceptions(theta, is_random_deception_req=True,is_deployment_random=True,percentage_deception=0.3)
    ###
    from collections import defaultdict

    result = defaultdict(int)
    for i in range(100):
        result[Game.run_simulation(defender_budget, deployment_cost, attacker_budget, max_time)]+=1
    print result.items()
