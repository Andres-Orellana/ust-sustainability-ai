from models.campus_graph import CampusGraph
from models.sustainability_game import SustainabilityGame
from models.search_problem import SearchProblem
from models.AStar import AStar

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

    navigator = AStar(game)

    while True:
        navigator = AStar(game)
        # A* stuff
        suggestion = navigator.get_best_move()
        route = navigator.get_best_path()
        target = navigator.get_target()

        game.display_status()

        print(
            f"\nTarget Building: "
            f"{target}"
        )

        print(
            f"A* Suggested Move: "
            f"{suggestion}"
        )

        print(
            f"A* Route: "
            f"{route}"
        )
        if game.game_complete():

            print(
                "\nAll sustainability "
                "sites collected!"
            )
            break

        move = input(
            "\nMove to building (or quit): "
        ).strip()

        if move.lower() == "quit":
            break

        game.move(move)

if __name__ == "__main__":
    main()