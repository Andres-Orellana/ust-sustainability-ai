from models.campus_graph import CampusGraph
from models.sustainability_game import SustainabilityGame

def main():
    print("Loading campus graph...\n")

    graph = CampusGraph()
    graph.load_edges("data/ust_building_edges-1.csv")

    # graph.print_graph() # For checking accuracy; can be removed later.

    game = SustainabilityGame(graph)
    
    print("Available Buildings:")

    for building in graph.graph.keys():
        print("-", building)

    choosing = True
    while choosing:
        start = input("\nChoose starting building: ").strip()

        if start not in graph.graph.keys():
            print("Invalid entry.")
            continue
        
        choosing = False

    game.start_game(start)

    while True:

        game.display_status()

        if game.game_complete():

            print(
                "\nAll sustainability "
                "sites collected!"
            )
            break

        move = input(
            "\nMove to building (or quit): ").strip()

        if move.lower() == "quit":
            break

        game.move(move)

if __name__ == "__main__":
    main()