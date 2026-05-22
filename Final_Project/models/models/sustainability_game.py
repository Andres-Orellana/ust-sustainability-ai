class SustainabilityGame:

    HIGH_PRIORITY_SITES = {
        "GraceHall": 5,
        "CretinHall": 5,
        "LorasHall": 5,
        "FlynnHall": 5,
        "Terrace": 5,
        "KochCommons": 4,
        "Anderson": 4,
        "StudentCenterAnnex": 4
    }

    MEDIUM_PRIORITY_SITES = {
        "Library": 3,
        "Brady": 3,
        "JohnRoach": 3,
        "Schoenecker": 3,
        "McNeely": 3
    }

    # scoring system
    LOW_PRIORITY_POINTS = 10
    MEDIUM_PRIORITY_POINTS = 20
    HIGH_PRIORITY_POINTS = 35
    REVISIT_PENALTY = 5
    DISTANCE_MULTIPLIER = 10000
    COMPLETION_BONUS = 100

    def __init__(self, graph):

        self.graph = graph

        # state
        self.current_location = None
        self.collected_locations = set()

        # collection sites
        self.collection_sites = self.build_collection_sites()

        # scoring
        self.score = 0
        self.total_distance = 0
        self.visited_locations = set()

    def build_collection_sites(self):

        sites = {}

        for building in self.graph.graph.keys():

            if building in self.HIGH_PRIORITY_SITES:
                sites[building] = {
                    "priority": self.HIGH_PRIORITY_SITES[building]
                }

            elif building in self.MEDIUM_PRIORITY_SITES:
                sites[building] = {
                    "priority": self.MEDIUM_PRIORITY_SITES[building]
                }

        return sites

    def start_game(self, start_building):
            
        self.current_location = start_building

        self.visited_locations.add(
            start_building
        )

        if start_building in self.collection_sites:

            self.collect_resource(start_building)

            reward = self.get_collection_reward(
                start_building
            )

            self.score += reward

    def collect_resource(self, building):

        self.collected_locations.add(building)

    def move(self, destination):

        neighbors = self.graph.get_neighbors(
            self.current_location
        )

        valid_moves = {}

        for neighbor, distance in neighbors:
            valid_moves[neighbor] = distance

        if destination not in valid_moves:
            print("\nInvalid move.")
            return

        distance = valid_moves[destination]

        # distance penalty
        travel_penalty = (
            distance * self.DISTANCE_MULTIPLIER
        )

        self.score -= travel_penalty
        self.total_distance += distance

        # revisit penalty
        if destination in self.visited_locations:

            self.score -= self.REVISIT_PENALTY

            print(
                f"\nRevisited building "
                f"(-{self.REVISIT_PENALTY} points)"
            )

        self.current_location = destination
        self.visited_locations.add(destination)

        # collect reward
        if destination in self.collection_sites:

            if destination not in self.collected_locations:

                self.collect_resource(destination)

                reward = self.get_collection_reward(
                    destination
                )

                self.score += reward

                print(
                    f"\nCollected sustainability "
                    f"materials!"
                )

                print(
                    f"+{reward} points"
                )

        # completion bonus
        if self.game_complete():

            self.score += self.COMPLETION_BONUS

            print(
                f"\nCompletion bonus: "
                f"+{self.COMPLETION_BONUS}"
            )

    def get_state(self):

        return (
            self.current_location,
            frozenset(self.collected_locations)
        )

    def get_remaining_sites(self):

        return (
            set(self.collection_sites.keys())
            - self.collected_locations
        )

    def heuristic_remaining_locations(self):
        """
        Simple heuristic:
        number of locations left
        """

        return len(self.get_remaining_sites())

    def display_status(self):

        print("\n======================")

        print(
            f"Current location: "
            f"{self.current_location}"
        )

        print(
            f"\nScore: "
            f"{self.score:.6f}"
        )

        print(
            f"Distance traveled: "
            f"{self.total_distance:.6f}"
        )

        print(
            f"\nCollected Sites: "
            f"{len(self.collected_locations)}"
            f"/{len(self.collection_sites)}"
        )

        print(
            f"Remaining Sites: "
            f"{len(self.get_remaining_sites())}"
        )

        print("\nSustainability Buildings:")

        for building in sorted(self.collection_sites.keys()):

            reward = self.get_collection_reward(
                building
            )

            if building in self.collected_locations:
                status = "COLLECTED"
            else:
                status = "remaining"

            print(
                f"- {building}: "
                f"{reward} points "
                f"({status})"
            )

        print("\nNeighboring Buildings:")

        neighbors = self.graph.get_neighbors(
            self.current_location
        )

        for neighbor, distance in neighbors:

            print(
                f"- {neighbor} "
                f"(distance={distance:.6f})"
            )

        print("======================")
        
    def get_collection_reward(self, building):

        priority = self.collection_sites[building][
            "priority"
        ]

        if priority >= 5:
            return self.HIGH_PRIORITY_POINTS

        elif priority >= 3:
            return self.MEDIUM_PRIORITY_POINTS

        return self.LOW_PRIORITY_POINTS

    def game_complete(self):

        return (
            len(self.get_remaining_sites()) == 0
        )

    