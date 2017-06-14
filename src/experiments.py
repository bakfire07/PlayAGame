

from graph_simulation import GameSimulate
from collections import defaultdict

def run_vary_theta_nodes_centrality():
    num_nodes_list = [10,20,30,40]
    edge_probabilities = [0.4,0.6,0.8]
    theta_list = [0.1,1,10]
    strategy=[False,True]
    defender_budget = 100
    #attacker_budget = num_nodes
    #max_time = num_nodes
    deployment_cost = 1
    result = defaultdict(int)
    result1 = defaultdict(int)

    Game = GameSimulate()
    for num_nodes in num_nodes_list:
        attacker_budget = num_nodes
        max_time = num_nodes
        for edge_probability in edge_probabilities:
            Game.create_graph(num_nodes, edge_probability)
            for theta in theta_list:
                result = defaultdict(int)
                result1 = defaultdict(int)
                Game.init_deceptions(theta,False)
                for i in range(100):
                    result[Game.run_simulation(defender_budget, deployment_cost, attacker_budget, max_time)] += 1
                Game.init_deceptions(theta,True)
                for i in range(100):
                    result1[Game.run_simulation(defender_budget, deployment_cost, attacker_budget, max_time)] += 1
                print 'Num of nodes:%d , Edge Probability:%f, Theta:%f with strategy:%s '%(num_nodes,edge_probability,theta,str(result.items()))
                print 'Num of nodes:%d , Edge Probability:%f, Theta:%f  random strategy:%s '%(num_nodes,edge_probability,theta,str(result1.items()))


def run_different_budget():
    num_nodes_list = [10,20,30,40]
    edge_probability = 0.6
    theta = 1
    defender_budget_list = [10,10000,100, 150]
    attacker_budget_list = [10000,10,100,130]
    deployment_cost = 1
    result = defaultdict(int)
    for num_nodes in num_nodes_list:
        Game = GameSimulate()
        Game.create_graph(num_nodes, edge_probability)
        Game.init_deceptions(theta, False)
        max_time = num_nodes

        for defender_budget,attacker_budget in zip(defender_budget_list,attacker_budget_list):
            result = defaultdict(int)
            for i in range(100):
                result[Game.run_simulation(defender_budget, deployment_cost, attacker_budget, max_time)] += 1

            print "Num of Nodes: %d, Defender Budget: %d, Attacker Budget %d :%s"%(num_nodes,defender_budget,attacker_budget,result.items())


def run_different_time():
    num_nodes_list = [10,20,30,40]
    edge_probability = 0.6
    theta = 1
    deployment_cost = 1
    result = defaultdict(int)
    for num_nodes in num_nodes_list:
        defender_budget = 100
        attacker_budget = num_nodes*10000
        Game = GameSimulate()
        Game.create_graph(num_nodes, edge_probability)
        Game.init_deceptions(theta, False)
        max_time_list = [5,8,10,num_nodes]

        for max_time in max_time_list:
            result = defaultdict(int)
            for i in range(100):
                result[Game.run_simulation(defender_budget, deployment_cost, attacker_budget, max_time)] += 1

            print "Num of Nodes: %d, Max time:%d :%s"%(num_nodes,max_time,result.items())



def run_random_deployement():
    num_nodes_list = [10, 20, 30, 40]
    edge_probability = 0.6
    theta = 1
    deployment_cost = 1
    result = defaultdict(int)
    for num_nodes in num_nodes_list:
        defender_budget = 100
        attacker_budget = 100
        Game = GameSimulate()
        Game.create_graph(num_nodes, edge_probability)
        percentage_list = [0.3,0.5,0.8]
        max_time = num_nodes
        for percentage in percentage_list:
            Game.init_deceptions(theta, is_random_deception_req=True, is_deployment_random=True,
                                 percentage_deception=percentage)

            result = defaultdict(int)
            for i in range(100):
                result[Game.run_simulation(defender_budget, deployment_cost, attacker_budget, max_time)] += 1

            print "Num of Nodes: %d, percentage:%f, defender payoff:%f :%s" % (num_nodes, percentage, sum(Game.payoff_defender),result.items())

if __name__ == '__main__':
    #run_vary_theta_nodes_centrality()
    #run_different_budget()
    #run_different_time()
    run_random_deployement()