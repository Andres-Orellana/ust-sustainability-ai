from models.campus_graph import CampusGraph


def main():
    print("Loading campus graph...\n")

    graph = CampusGraph()

    graph.load_edges("data/ust_building_edges-1.csv")

    graph.print_graph() # For checking accuracy; can be removed later.



if __name__ == "__main__":
    main()