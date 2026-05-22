import pandas as pd


class CampusGraph:
    def __init__(self):
        #adjacency list
        self.graph = {}

    def load_edges(self, file_path):
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            source = row["Source"]
            target = row["Target"]
            distance = row["Distance"]

            # ensure nodes exist
            if source not in self.graph:
                self.graph[source] = []

            if target not in self.graph:
                self.graph[target] = []

            #undirected graph
            self.graph[source].append((target, distance))
            self.graph[target].append((source, distance))

    def get_neighbors(self, building):
        return self.graph.get(building, [])

    def print_graph(self):
        for building, neighbors in self.graph.items():
            print(f"\n{building}")

            for neighbor, distance in neighbors:
                print(f"  -> {neighbor} ({distance})")