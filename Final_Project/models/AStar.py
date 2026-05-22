from models.search import astar_search
from models.search_problem import SearchProblem
import pandas as pd


class AStar:

    def __init__(self, game):

        self.game = game

        # NEW
        self.distance_matrix = pd.read_csv(
            "data/ust_distance_matrix-1.csv",
            index_col=0
        )

    def choose_best_target(self):

        remaining = self.game.get_remaining_sites()

        if len(remaining) == 0:
            return None

        current = self.game.current_location

        best_target = None
        best_value = float("-inf")

        for site in remaining:

            reward = self.game.get_collection_reward(site)

            estimated_distance = (
                self.estimate_distance(
                    current,
                    site
                )
            )

            value = (
                reward
                -
                (
                    estimated_distance
                    *
                    self.game.DISTANCE_MULTIPLIER
                )
            )

            if value > best_value:
                best_value = value
                best_target = site

        return best_target

    # CHANGED
    def estimate_distance(
        self,
        start,
        goal
    ):

        return self.distance_matrix.loc[
            start,
            goal
        ]

    def get_goal_node(self):

        target = self.choose_best_target()

        if target is None:
            return None

        problem = SearchProblem(
            self.game.graph,
            self.game.current_location,
            target,
            self.game
        )

        # NEW
        problem.distance_matrix = (
            self.distance_matrix
        )

        return astar_search(problem)

    def get_best_path(self):

        goal = self.get_goal_node()

        if goal is None:
            return []

        return goal.solution()

    def get_best_move(self):

        path = self.get_best_path()

        if len(path) == 0:
            return None

        return path[0]

    def get_target(self):
        return self.choose_best_target()