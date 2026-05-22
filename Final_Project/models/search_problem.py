from models.search import Problem


class SearchProblem(Problem):

    def __init__(self, graph, start, goal, game):
        super().__init__(start, goal)

        self.graph = graph
        self.game = game

    def actions(self, state):
        neighbors = self.graph.get_neighbors(state)

        actions = []

        for neighbor, distance in neighbors:
            actions.append(neighbor)

        return actions

    def result(self, state, action):
        return action

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, cost_so_far, state1, action, state2):

        neighbors = self.graph.get_neighbors(state1)

        for neighbor, distance in neighbors:

            if neighbor == action:
                return cost_so_far + (distance * self.game.DISTANCE_MULTIPLIER)

        return float("inf")

    def h(self, node):

        current = node.state

        return self.distance_matrix.loc[current,self.goal] * self.game.DISTANCE_MULTIPLIER
    