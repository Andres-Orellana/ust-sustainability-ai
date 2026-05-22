import random


class SustainabilityGame:

    HIGH_PRIORITY_SITES = {
        "GraceHall": 5,
        "CretinHall": 5,
        "LorasHall": 5,
        "FlynnHall": 5,
        "Dowling": 5,
        "Ireland": 5,
        "FreyHall": 5,
        "Anderson": 5,
    }

    MEDIUM_PRIORITY_SITES = {
        "Library": 3,
        "Brady": 3,
        "Murray": 3,
        "Schoenecker": 3,
        "McNeely": 3
    }

    TRIVIA_QUESTIONS = [
        # --- SSLP ---
        {
            "topic": "Student Sustainability Leadership Program",
            "type": "mc",
            "question": "Which of the following is true about the Student Sustainability Leadership Program (SSLP)?",
            "choices": {
                "A": "It is a student employment opportunity designed to prepare the next generation of environmental leaders.",
                "B": "It provides hands-on experience with sustainability on campus.",
                "C": "It increases student sustainability knowledge and action through peer-education.",
                "D": "All of the above.",
            },
            "answer": "D",
            "explanation": "All three statements are true about SSLP!",
        },
        {
            "topic": "Student Sustainability Leadership Program",
            "type": "tf",
            "question": "The Student Sustainability Leadership Program (SSLP) is only for students with environmental majors.",
            "answer": "false",
            "explanation": "SSLP is open for students from any major to apply!",
        },
        # --- Energy ---
        {
            "topic": "Energy",
            "type": "mc",
            "question": "Which of the following is NOT a way to conserve energy?",
            "choices": {
                "A": "Unplugging any devices when not in use.",
                "B": "Turning off lights when leaving the room.",
                "C": "Keeping windows closed to retain heat indoors in the winter.",
                "D": "Washing laundry in small loads instead of full loads.",
            },
            "answer": "D",
            "explanation": "Washing full loads of laundry saves energy since each load takes energy to wash.",
        },
        {
            "topic": "Energy",
            "type": "tf",
            "question": "Keeping blinds closed during the hottest parts of the day to limit excess heat in the summer is a way to conserve energy.",
            "answer": "true",
            "explanation": "Blocking sunlight reduces cooling load and saves energy.",
        },
        # --- Pollinator Path ---
        {
            "topic": "Pollinator Path",
            "type": "mc",
            "question": "What is the name of the series of gardens around campus that attract pollinators and supports the study of pollinator activity on campus?",
            "choices": {
                "A": "Bee Garden",
                "B": "Pollinator Path",
                "C": "Butterfly Garden",
                "D": "Bee Path",
            },
            "answer": "B",
            "explanation": "It's called the Pollinator Path!",
        },
        {
            "topic": "Pollinator Path",
            "type": "tf",
            "question": "The Pollinator Path is a series of gardens around campus which attract pollinators and support the study of pollinator activity on campus.",
            "answer": "true",
            "explanation": "That's exactly what the Pollinator Path is!",
        },
        # --- Bike ---
        {
            "topic": "Bike",
            "type": "mc",
            "question": "Where is there a bike repair station located on campus?",
            "choices": {
                "A": "On the south side of O'Shaughnessy Stadium.",
                "B": "Inside the secure bike storage in Frey Residence Hall.",
                "C": "Inside the secure bike storage in Schoenecker Hall North.",
                "D": "All of the above.",
            },
            "answer": "D",
            "explanation": "Bike repair stations exist at all three locations!",
        },
        {
            "topic": "Bike",
            "type": "tf",
            "question": "A bike repair station is located between ASC and O'Shaughnessy Stadium.",
            "answer": "true",
            "explanation": "There is indeed a bike repair station on the south side of O'Shaughnessy Stadium.",
        },
        # --- Food ---
        {
            "topic": "Food",
            "type": "mc",
            "question": "Which of the following is NOT a helpful tip for reducing food waste?",
            "choices": {
                "A": "Storing produce properly.",
                "B": "Planning meals at the beginning of the week.",
                "C": "Only purchasing what you need.",
                "D": "Storing all items from the store in the refrigerator.",
            },
            "answer": "D",
            "explanation": "Not all food belongs in the fridge — storing items incorrectly can actually cause them to spoil faster.",
        },
        {
            "topic": "Food",
            "type": "tf",
            "question": "You get 25 cents off for bringing a reusable cup at campus coffee shops.",
            "answer": "true",
            "explanation": "Campus coffee shops offer a 25-cent discount for reusable cups!",
        },
        # --- Water ---
        {
            "topic": "Water",
            "type": "mc",
            "question": "Which of the following is NOT a way to conserve water?",
            "choices": {
                "A": "Eating more plant-based meals.",
                "B": "Taking shorter showers.",
                "C": "Leaving the sink on while brushing your teeth.",
                "D": "Only washing full loads of laundry.",
            },
            "answer": "C",
            "explanation": "Leaving the sink running wastes water — always turn it off while brushing!",
        },
        {
            "topic": "Water",
            "type": "tf",
            "question": "The water that collects in the storm drains located on campus and the surrounding streets ends up in the Mississippi River.",
            "answer": "true",
            "explanation": "Storm drain runoff flows into the Mississippi River, so keeping campus clean matters!",
        },
        # --- Academics / Research ---
        {
            "topic": "Academics/Research",
            "type": "mc",
            "question": (
                "The Sustainable Communities Partnership (SCP) collaborates with local and regional "
                "government, nonprofit, and campus partners to integrate sustainability projects into "
                "St. Thomas courses. Which of the following disciplines have courses that have included an SCP project?"
            ),
            "choices": {
                "A": "Marketing",
                "B": "Engineering",
                "C": "Theology",
                "D": "All of the above and more!",
            },
            "answer": "D",
            "explanation": "SCP projects span many disciplines across campus!",
        },
        {
            "topic": "Academics/Research",
            "type": "tf",
            "question": "St. Thomas does not offer a sustainability minor.",
            "answer": "false",
            "explanation": "The Department of Earth, Environment, and Society offers a sustainability minor open to students of all majors!",
        },
        # --- Reuse ---
        {
            "topic": "Reuse",
            "type": "mc",
            "question": "Dining Services reduces waste by...",
            "choices": {
                "A": "Safely recovering leftover food to be donated.",
                "B": "Offering reusable to-go containers in T's.",
                "C": "Offering a discount for bringing your own reusable cup to campus coffee shops.",
                "D": "All of the above.",
            },
            "answer": "D",
            "explanation": "Dining Services does all three to reduce waste!",
        },
        {
            "topic": "Reuse",
            "type": "tf",
            "question": "Tommies Closet is a monthly pop-up that allows students to shop for secondhand clothes donated by fellow Tommies.",
            "answer": "true",
            "explanation": "Tommies Closet is a great way to reuse clothing on campus!",
        },
        # --- Recycling ---
        {
            "topic": "Recycling",
            "type": "mc",
            "question": "At St. Thomas, plastics with which number in the recycling triangle are NOT accepted for recycling?",
            "choices": {
                "A": "1",
                "B": "2",
                "C": "4",
                "D": "5",
            },
            "answer": "C",
            "explanation": "Only plastics #1, #2, and #5 in the recycling triangle can be recycled on campus.",
        },
        {
            "topic": "Recycling",
            "type": "tf",
            "question": "Plastic bags can be recycled in the blue recycling bins around campus.",
            "answer": "false",
            "explanation": "Plastic bags should not go in blue bins — bring them to the specialized recycling stations instead.",
        },
        # --- Organics Recycling ---
        {
            "topic": "Organics Recycling",
            "type": "mc",
            "question": "All of the following items are accepted for organics recycling (compost), EXCEPT:",
            "choices": {
                "A": "All food scraps",
                "B": "Napkins",
                "C": "All paper cups",
                "D": "Flower trimmings",
            },
            "answer": "C",
            "explanation": "Paper cups must have a BPI logo to be accepted for organics recycling.",
        },
        {
            "topic": "Organics Recycling",
            "type": "tf",
            "question": "At St. Thomas, items placed in the green organics recycling bins are turned into compost that can be used in gardens and lawns.",
            "answer": "true",
            "explanation": "Green bin organics become compost that benefits gardens and lawns!",
        },
        # --- Specialized Recycling ---
        {
            "topic": "Specialized Recycling",
            "type": "mc",
            "question": "Where is there a specialized recycling bin located on campus?",
            "choices": {
                "A": "Outside the Campus Store in Murray-Herrick",
                "B": "In the entrance to the Facilities & Design Center",
                "C": "In the create[space]",
                "D": "All of the above",
            },
            "answer": "D",
            "explanation": "Specialized recycling bins can be found at all of those locations!",
        },
        {
            "topic": "Specialized Recycling",
            "type": "tf",
            "question": "Plastic bags are accepted for recycling at the specialized recycling stations on campus.",
            "answer": "true",
            "explanation": "Unlike the blue bins, specialized stations do accept plastic bags!",
        },
    ]

    # scoring system
    TRIVIA_BONUS = 15
    TRIVIA_PENALTY = 5
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

                print(
                    f"\nYou arrived at a sustainability "
                    f"collection site! Answer a trivia "
                    f"question to earn a bonus."
                )

                self.ask_trivia_question()

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

    def ask_trivia_question(self):
        """
        Randomly pick a trivia question, prompt the player,
        and award/deduct points based on correctness.
        Returns True if the player answered correctly.
        """
        q = random.choice(self.TRIVIA_QUESTIONS)

        print("\n--- SUSTAINABILITY TRIVIA ---")
        print(f"Topic: {q['topic']}")
        print(f"\n{q['question']}")

        if q["type"] == "mc":
            for letter, text in q["choices"].items():
                print(f"  {letter}. {text}")
            valid = set(q["choices"].keys())
            prompt = f"Your answer ({'/'.join(sorted(valid))}): "
        else:
            print("  (True / False)")
            valid = {"true", "false", "t", "f"}
            prompt = "Your answer (True/False): "

        raw = input(prompt).strip().lower()

        # normalise single-letter T/F shorthand
        if q["type"] == "tf":
            if raw == "t":
                raw = "true"
            elif raw == "f":
                raw = "false"

        correct_answer = q["answer"].lower()
        correct = raw == correct_answer

        if correct:
            self.score += self.TRIVIA_BONUS
            print(f"\nCorrect! +{self.TRIVIA_BONUS} points")
        else:
            self.score -= self.TRIVIA_PENALTY
            print(f"\nIncorrect. -{self.TRIVIA_PENALTY} points")
            display_answer = (
                f"{q['answer']}. {q['choices'][q['answer']]}"
                if q["type"] == "mc"
                else q["answer"].capitalize()
            )
            print(f"Correct answer: {display_answer}")

        print(f"  {q['explanation']}")
        print("----------------------------")

        return correct

    def game_complete(self):

        return (
            len(self.get_remaining_sites()) == 0
        )

    