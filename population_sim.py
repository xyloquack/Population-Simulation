import random
import math
import os

absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
os.chdir(directory_name)

EXPORT_DATA = True
OUTPUT_FILE = "data.txt"

A_ID = 1
A_ON_B_PERF = 0.5
A_ON_A_PERF = 1.75
A_ON_NONE_PERF = 2
A_FOOD_REQ = 1

B_ID = 2
B_ON_A_PERF = 1.5
B_ON_B_PERF = 0.75
B_ON_NONE_PERF = 2
B_FOOD_REQ = 1

STOP_ON_EXTINCTION = True

current_generation = []
next_generation = []
food_sources = []

current_a_count = 0
current_b_count = 0

frequency_over_time = []

class Creature():
    __slots__ = ['id', 'opp_perf', 'self_perf', 'none_perf', 'food_req']
    def __init__(self, creature_id, opposing_performance, self_performance, none_performance, food_requirement):
        self.id = creature_id
        self.opp_perf = opposing_performance
        self.self_perf = self_performance
        self.none_perf = none_performance
        self.food_req = food_requirement

    def reproduce(self, opp_id):
        global next_generation
        global current_a_count
        global current_b_count
        children = 0
        if opp_id != self.id and opp_id != 0:
            children += int(self.opp_perf)
            if not self.opp_perf % self.food_req == 0:
                if self.opp_perf - (self.food_req * children) >= random.random() * self.food_req:
                    children += 1

        elif opp_id == self.id:
            children += int(self.self_perf)
            if not self.self_perf % self.food_req == 0:
                if self.self_perf - (self.food_req * children) >= random.random() * self.food_req:
                    children += 1

        else:
            children += int(self.none_perf)
            if not self.none_perf % self.food_req == 0:
                if self.none_perf - (self.food_req * children) >= random.random() * self.food_req:
                    children += 1

        children = int(children)

        for child in range(children):
            new_child = Creature(self.id, self.opp_perf, self.self_perf, self.none_perf, self.food_req)
            next_generation.append(new_child)

        if self.id == 1:
            current_a_count += children
        else:
            current_b_count += children

class FoodSource():
    __slots__ = ['visitors', 'occupancy']
    def __init__(self):
        self.visitors = []
        self.occupancy = 0

def main():
    global current_generation
    global next_generation
    global food_sources
    global current_a_count
    global current_b_count
    global frequency_over_time

    if EXPORT_DATA:
        file = open(OUTPUT_FILE, "w")
        file.write("")
        file.close()

    total_number_of_creatures = int(input("How many creatures should we start with? "))
    pop_a_proportion = float(input("What proportion do you want to be Creature A (in a decimal ratio)? "))

    pop_a_start = math.ceil(total_number_of_creatures * pop_a_proportion)
    pop_b_start = total_number_of_creatures - pop_a_start

    for i in range(pop_a_start):
        new_creature = Creature(A_ID, A_ON_B_PERF, A_ON_A_PERF, A_ON_NONE_PERF, A_FOOD_REQ)
        current_generation.append(new_creature)

    for i in range(pop_b_start):
        new_creature = Creature(B_ID, B_ON_A_PERF, B_ON_B_PERF, B_ON_NONE_PERF, B_FOOD_REQ)
        current_generation.append(new_creature)

    number_of_food_sources = int(input("How many food sources do you want? "))

    for i in range(number_of_food_sources):
        new_source = FoodSource()
        food_sources.append(new_source)

    num_generations = int(input("How many generations do you want? "))
    generation = 0

    print(f"Gen 0: A = {pop_a_start} B = {pop_b_start}")

    current_a_count = pop_a_start
    current_b_count = pop_b_start

    if EXPORT_DATA:
        file = open("data.txt", 'a')
        frequency = pop_a_proportion
        file.write(f"{frequency}\n")

    while generation < num_generations:
        if STOP_ON_EXTINCTION and (current_a_count == 0 or current_b_count == 0):
            break
        available_sources = list(food_sources)
        current_a_count = 0
        current_b_count = 0
        random.shuffle(current_generation)
        placed_creatures = 0

        if len(current_generation) > len(food_sources) * 2:
            for i in range(0, len(food_sources) * 2, 2):
                source = food_sources[i // 2]
                source.visitors.append(current_generation[i])
                source.visitors.append(current_generation[i + 1])
                source.occupancy = 2

        for i in range(len(current_generation)):
            if placed_creatures == (2 * number_of_food_sources):
                break
            random_index = random.randint(0, len(available_sources) - 1)
            selected_food_source = available_sources[random_index]
            selected_food_source.visitors.append(current_generation[i])
            selected_food_source.occupancy += 1
            if selected_food_source.occupancy == 2:
                available_sources.pop(random_index)
            placed_creatures += 1
        
        for food_source in food_sources:
            if food_source.occupancy == 0:
                continue
            elif food_source.occupancy == 1:
                food_source.visitors[0].reproduce(0)
            else:
                food_source.visitors[0].reproduce(food_source.visitors[1].id)
                food_source.visitors[1].reproduce(food_source.visitors[0].id)

        current_generation.clear()
        current_generation.extend(next_generation)
        next_generation.clear()

        generation += 1
        print(f"Gen {generation}: A = {current_a_count}, B = {current_b_count}")

        for i in range(number_of_food_sources):
            food_sources[i].occupancy = 0
            food_sources[i].visitors = list()


        if EXPORT_DATA:
            frequency = current_a_count / (current_a_count + current_b_count)
            file.write(f"{frequency}\n")

    if EXPORT_DATA:
        file.close()

if __name__ == "__main__":
    main()